# Architecture — 끊기 (Kkeugi)

> `/plan-eng-review` Section 1 결과 · 2026-05-24 · v1 DRAFT
> Stack: Flutter + FastAPI + Postgres on Supabase Free + Fly.io seoul
> PRD §7 + design doc + DESIGN.md 기반

## 1. Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│  Flutter (Android, Material 3, Pretendard + IBM Plex Mono)          │
│  ─────────────────────────────────────────────────────────────────  │
│  · UsageStatsManager (Kotlin platform channel)                       │
│  · Drift SQLite — offline-first cache                                │
│  · Riverpod state                                                    │
│  · Kakao OAuth (kakao_flutter_sdk_user)                              │
│  · firebase_messaging (FCM 토큰만)                                    │
│  · flutter_local_notifications (threshold 즉시 알람)                  │
│  · Sentry Flutter                                                    │
└───────────────────────┬─────────────────────────────────────────────┘
                        │ JWT Bearer + REST/JSON
                        │ (https://api.kkeugi.kr)
                        ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FastAPI on Fly.io seoul region (shared-1x VM)                       │
│  ─────────────────────────────────────────────────────────────────  │
│  /v1/auth/* · /v1/me · /v1/usage/* · /v1/reports/*                   │
│  /v1/thresholds/* · /v1/fcm/* · /v1/payments/*                       │
│  /webhooks/toss · /health · /ready                                   │
│                                                                       │
│  APScheduler (Asia/Seoul timezone):                                  │
│    · Sun 22:00  → weekly_reflection (active filter SQL → LLM → 카톡) │
│    · */30 min   → threshold_check (daily limit 도달 사용자 카톡)      │
│    · Daily 03:00 → cleanup (expired subscriptions, old refresh tokens)│
│                                                                       │
│  외부 호출:                                                           │
│    · SOLAPI/Aligo REST   (카톡 알림톡)                                │
│    · Anthropic SDK       (Claude Haiku 3.5)                          │
│    · Firebase Admin SDK  (FCM HTTP v1 발송)                          │
│    · Toss Payments REST  (결제 확인 + webhook)                        │
│    · Kakao OAuth /v2/user/me                                          │
│                                                                       │
│  관측: Sentry Python · Mixpanel server events · Fly.io metrics       │
└───────────────────────┬─────────────────────────────────────────────┘
                        │ asyncpg + SQLAlchemy 2.0 async
                        ↓
┌─────────────────────────────────────────────────────────────────────┐
│  PostgreSQL 16 on Supabase (Free → Pro → Hetzner)                    │
│  ─────────────────────────────────────────────────────────────────  │
│  users · usage_events (monthly partitioned) · weekly_reports         │
│  subscriptions · kakao_consents · fcm_tokens · thresholds            │
│  refresh_tokens · usage_event_archive (90+일)                        │
│                                                                       │
│  Alembic migrations · 일 backup 자동 · PgBouncer connection pool      │
└─────────────────────────────────────────────────────────────────────┘
```

## 2. Stack Summary

| 레이어 | 기술 | 비고 |
|---|---|---|
| Frontend | Flutter 3.x + Material 3 + Riverpod + Drift (SQLite) | Pretendard + IBM Plex Mono |
| Platform channel | Kotlin → `UsageStatsManager` | PACKAGE_USAGE_STATS 권한 |
| API | FastAPI (Python 3.12) on Fly.io seoul shared-1x | uv + pyproject.toml |
| DB | PostgreSQL 16 on Supabase Free → Pro → Hetzner | asyncpg + SQLAlchemy 2.0 async |
| Migrations | Alembic | autogenerate + manual review |
| Auth | JWT 15min access + 30d refresh + rotation | Kakao OAuth backend verification |
| Cron | APScheduler (async, Asia/Seoul tz) | weekly + threshold + cleanup |
| LLM | Anthropic SDK (Claude Haiku 3.5) | fallback GPT-5 mini |
| Push (앱) | Firebase FCM HTTP v1 API | Firebase Admin SDK from Python |
| Push (로컬) | flutter_local_notifications | threshold 즉시 알람 |
| 카톡 | SOLAPI / Aligo / DirectSend REST | 1택 (TODOS 결정 대기) |
| 결제 | Toss Payments REST + webhook | 외부 결제 (Google Play 30% 우회) |
| 모니터링 | Sentry (Python + Flutter) + Mixpanel | free tier |

## 3. Postgres Schema

### users (2026-05-24 Google Sign-In primary)
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  google_sub VARCHAR(255) UNIQUE NOT NULL,  -- Google ID token 'sub' claim
  kakao_id VARCHAR(255) UNIQUE,             -- V2 카톡 연동 시 채워짐 (V1 NULL)
  email VARCHAR(255) NOT NULL,              -- Google 계정 이메일 (verified)
  display_name VARCHAR(100),
  tier VARCHAR(20) NOT NULL DEFAULT 'free'
    CHECK (tier IN ('free', 'one_time', 'subscription')),
  hourly_value INTEGER,
  work_start_hour SMALLINT,  -- 0-23, V1.5 heuristic
  work_end_hour SMALLINT,
  timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Seoul',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_users_google_sub ON users(google_sub);
CREATE INDEX idx_users_kakao_id ON users(kakao_id) WHERE kakao_id IS NOT NULL;  -- V2
CREATE INDEX idx_users_tier_active ON users(tier) WHERE deleted_at IS NULL;
```

### usage_events (monthly partitioned)
```sql
CREATE TABLE usage_events (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  package_name VARCHAR(255) NOT NULL,
  category VARCHAR(20) NOT NULL
    CHECK (category IN ('sns', 'shorts', 'game', 'webtoon', 'other')),
  duration_seconds INTEGER NOT NULL CHECK (duration_seconds > 0),
  occurred_at TIMESTAMPTZ NOT NULL,
  in_work_hours BOOLEAN NOT NULL DEFAULT FALSE,
  source VARCHAR(20) NOT NULL DEFAULT 'usagestats'
    CHECK (source IN ('usagestats', 'manual')),
  client_event_id UUID NOT NULL,
  synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id, occurred_at),
  UNIQUE (user_id, client_event_id, occurred_at)  -- idempotency
) PARTITION BY RANGE (occurred_at);

-- Partition naming: usage_events_y2026m06, usage_events_y2026m07, ...
-- 매월 1일 03:00 cron으로 다음 달 partition 자동 생성 (pg_partman 또는 manual)

CREATE INDEX idx_usage_events_user_occurred
  ON usage_events (user_id, occurred_at DESC);
CREATE INDEX idx_usage_events_user_category_occurred
  ON usage_events (user_id, category, occurred_at DESC);
```

### weekly_reports
```sql
CREATE TABLE weekly_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  week_start_date DATE NOT NULL,  -- 월요일
  total_minutes INTEGER NOT NULL,
  recovered_minutes INTEGER NOT NULL,  -- prev_week - this_week (음수면 증가)
  recovered_won INTEGER,  -- recovered_minutes × hourly_value / 60 (nullable)
  llm_card_text TEXT NOT NULL,  -- one paragraph reflection
  llm_card_insight TEXT,  -- "화요일 오후가 가장 흩어졌어요"
  kakao_sent BOOLEAN NOT NULL DEFAULT FALSE,
  kakao_sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, week_start_date)
);
CREATE INDEX idx_weekly_reports_user_week
  ON weekly_reports (user_id, week_start_date DESC);
```

### subscriptions
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  kind VARCHAR(20) NOT NULL
    CHECK (kind IN ('one_time', 'monthly', 'yearly')),
  toss_payment_key VARCHAR(255) NOT NULL UNIQUE,
  toss_order_id VARCHAR(100) NOT NULL,
  amount INTEGER NOT NULL,
  status VARCHAR(20) NOT NULL
    CHECK (status IN ('active', 'cancelled', 'expired', 'refunded')),
  starts_at TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  cancelled_at TIMESTAMPTZ,
  refunded_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_subscriptions_user_active
  ON subscriptions (user_id) WHERE status = 'active';
CREATE INDEX idx_subscriptions_expires_active
  ON subscriptions (expires_at) WHERE status = 'active';
```

### kakao_consents
```sql
CREATE TABLE kakao_consents (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  subscribed BOOLEAN NOT NULL DEFAULT FALSE,
  kakao_phone VARCHAR(20),  -- E.164 format
  subscribed_at TIMESTAMPTZ,
  unsubscribed_at TIMESTAMPTZ,
  preferred_send_hour SMALLINT NOT NULL DEFAULT 22 CHECK (preferred_send_hour BETWEEN 0 AND 23),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### fcm_tokens
```sql
CREATE TABLE fcm_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) NOT NULL UNIQUE,
  device_id VARCHAR(100),
  last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_fcm_tokens_user ON fcm_tokens (user_id);
```

### thresholds
```sql
CREATE TABLE thresholds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category VARCHAR(20) NOT NULL,
  daily_limit_minutes INTEGER NOT NULL CHECK (daily_limit_minutes > 0),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  last_triggered_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, category)
);
CREATE INDEX idx_thresholds_active ON thresholds (user_id) WHERE enabled = TRUE;
```

### refresh_tokens (JWT rotation)
```sql
CREATE TABLE refresh_tokens (
  jti UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL,
  revoked_at TIMESTAMPTZ,
  rotated_to UUID REFERENCES refresh_tokens(jti),  -- chain of rotations
  user_agent VARCHAR(255),
  ip_address INET
);
CREATE INDEX idx_refresh_tokens_user_active
  ON refresh_tokens (user_id) WHERE revoked_at IS NULL;
CREATE INDEX idx_refresh_tokens_expires
  ON refresh_tokens (expires_at) WHERE revoked_at IS NULL;
```

## 4. REST API Specification

### Versioning
- 모든 API는 `/v1/` prefix
- V2 도입 시 `/v2/` 별도 namespace, V1 backward compat 12개월 유지
- Webhook은 unversioned (`/webhooks/toss`)

### Auth (`/v1/auth`)
| Method | Path | Description | Auth |
|---|---|---|---|
| POST | `/v1/auth/google` | Google ID token → JWT pair (V1, 2026-05-24 primary) | None |
| POST | `/v1/auth/kakao_link` | Link Kakao to existing user (V2 카톡 연동) | Access token |
| POST | `/v1/auth/refresh` | Refresh access token (rotation) | Refresh token |
| POST | `/v1/auth/logout` | Revoke refresh token | Refresh token |
| DELETE | `/v1/auth/account` | Soft delete user account (GDPR/PIPA) | Access token |

### User (`/v1/me`)
| Method | Path | Description |
|---|---|---|
| GET | `/v1/me` | Current user + tier + settings |
| PATCH | `/v1/me` | Update settings (hourly_value, work_hours, timezone) |
| PATCH | `/v1/me/kakao_consent` | Subscribe/unsubscribe + preferred_send_hour |

### Usage Events (`/v1/usage`)
| Method | Path | Description |
|---|---|---|
| POST | `/v1/usage/batch` | Bulk insert (idempotent via client_event_id) |
| GET | `/v1/usage/stats/today` | Today summary by category |
| GET | `/v1/usage/stats/week` | Last 7 days summary |

### Reports (`/v1/reports`)
| Method | Path | Description |
|---|---|---|
| GET | `/v1/reports/weekly` | Latest weekly report |
| GET | `/v1/reports/weekly/:date` | Specific week (week_start_date) |
| POST | `/v1/reports/regenerate` | Force regenerate (paid only, rate-limited) |

### Thresholds (`/v1/thresholds`)
| Method | Path | Description |
|---|---|---|
| GET | `/v1/thresholds` | List |
| POST | `/v1/thresholds` | Create (paid only) |
| PATCH | `/v1/thresholds/:id` | Update |
| DELETE | `/v1/thresholds/:id` | Delete |

### FCM (`/v1/fcm`)
| Method | Path | Description |
|---|---|---|
| POST | `/v1/fcm/register` | Register device token |
| DELETE | `/v1/fcm/tokens/:id` | Deregister |

### Payments (`/v1/payments`)
| Method | Path | Description |
|---|---|---|
| POST | `/v1/payments/confirm` | Toss payment 확인 (server verification) |
| GET | `/v1/payments/subscription` | Current subscription status |
| POST | `/v1/payments/cancel` | Cancel subscription |

### Webhooks
| Method | Path | Description |
|---|---|---|
| POST | `/webhooks/toss` | Toss payment events (refund, expire) |

### Health
| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness (return 200) |
| GET | `/ready` | Readiness (DB + LLM + Kakao reachable) |

## 5. Auth Flow (Google Sign-In → JWT 15min + 30d rotation, 2026-05-24 변경)

```
[Flutter login flow]
1. User → "Google로 시작" 버튼
2. google_sign_in pub package: GoogleSignIn().signIn()
3. Receive Google ID token (JWT signed by Google)
4. POST /v1/auth/google { id_token }
5. Receive { access_token, refresh_token, user }
6. Store in flutter_secure_storage

[FastAPI /v1/auth/google]
1. Verify ID token signature + audience via google-auth library:
   from google.oauth2 import id_token
   from google.auth.transport import requests
   idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
2. Extract google_sub (idinfo['sub']), email (verified), name
3. UPSERT users WHERE google_sub = ?
4. Issue:
   access_token  = JWT(sub=user_id, exp=NOW+15min)
   refresh_token = JWT(sub=user_id, jti=uuid, exp=NOW+30d)
5. INSERT refresh_tokens (jti, user_id, expires_at, user_agent, ip)
6. Return { access_token, refresh_token, user }

[V2 Kakao 연동 (사업자 등록 후, 카톡 알림톡 추가 시점)]
POST /v1/auth/kakao_link { kakao_access_token } (인증 필요)
1. 기존 Google Sign-In 사용자 (인증된 user_id 보유)
2. Kakao access_token verify via GET https://kapi.kakao.com/v2/user/me
3. UPDATE users SET kakao_id = ? WHERE id = current_user.id
4. INSERT channel_subscriptions (channel='kakao', identifier=phone)

[Refresh rotation]
POST /v1/auth/refresh { refresh_token }
1. Decode refresh_token, verify signature + expiry
2. SELECT FROM refresh_tokens WHERE jti = ? AND revoked_at IS NULL
3. If not found OR revoked → reject (token reuse detection)
4. UPDATE refresh_tokens SET revoked_at = NOW(), rotated_to = new_jti
5. Issue new access_token + new refresh_token
6. Return pair

[Auto-attach interceptor (Flutter)]
- dio Interceptor: attach Authorization: Bearer {access_token}
- On 401: queue request, call /v1/auth/refresh, retry original request
- On refresh fail (revoked or expired): clear secure_storage, → login screen

[Logout]
POST /v1/auth/logout { refresh_token }
→ UPDATE refresh_tokens SET revoked_at = NOW() WHERE jti = ?
→ Flutter clears secure_storage
```

**보안 메모**:
- Access token JWT signed with HS256 (HMAC) — single backend instance면 HS256 충분. Multi-instance면 RS256.
- Refresh rotation = 토큰 reuse 감지 → 의심 시 user 전체 refresh 무효화 (`UPDATE WHERE user_id = ?`).
- Secret stored in Fly.io secrets (`fly secrets set JWT_SECRET=...`).

## 6. Sync Pattern (8h interval + 로컬 threshold)

### Usage events 동기화

```
[Local capture]
1. UsageStatsManager polling (Kotlin platform channel)
   → Flutter Drift INSERT INTO local_usage_events
   → client_event_id = uuid_v4() locally generated
   → synced = false

[Sync triggers]
Trigger A: 앱 foreground 진입 (Flutter App lifecycle observer)
Trigger B: WorkManager periodic 8시간

[Sync flow]
1. SELECT FROM local_usage_events WHERE synced = false LIMIT 1000
2. POST /v1/usage/batch { events: [...] }
3. FastAPI:
   INSERT INTO usage_events (...) 
   ON CONFLICT (user_id, client_event_id, occurred_at) DO NOTHING
   RETURNING id, client_event_id
4. Flutter UPDATE local_usage_events SET synced = true 
   WHERE client_event_id IN (returned list)
5. Network fail → 다음 trigger에 재시도 (idempotent라 안전)
```

### Threshold trigger 즉시성 (로컬 detection)

```
[Local check — 매 30분 Flutter background timer]
1. SELECT today usage by category FROM local Drift
2. SELECT thresholds FROM local cache (last sync from server)
3. For each category: if today_usage >= limit AND not_triggered_today:
   → flutter_local_notifications 즉시 알람
   → INSERT INTO local_triggered_log (category, date)

[Server check — APScheduler 매 30분]
1. SELECT users WHERE today_usage (from synced events) >= threshold
   AND threshold.last_triggered_date < TODAY
   AND kakao_consents.subscribed = TRUE
2. For each: SOLAPI/Aligo POST → 카톡 알림톡
3. UPDATE thresholds SET last_triggered_date = TODAY
```

→ **로컬 즉시 알람 + 서버 카톡 발송 (daily 1회 한도)**. 8h sync로도 즉시성 확보.

### Settings sync (last-write-wins)

```
1. Flutter PATCH /v1/me { hourly_value: 30000 }
2. Server: UPDATE users SET ..., updated_at = NOW()
3. On app open: GET /v1/me → compare server.updated_at vs local.updated_at
4. Newer wins (보통 server)
```

## 7. APScheduler Jobs

```python
# backend/app/scheduler/scheduler.py
scheduler = AsyncIOScheduler(timezone='Asia/Seoul')

# Sunday 22:00 KST — weekly reflection
@scheduler.scheduled_job(CronTrigger(day_of_week='sun', hour=22, minute=0))
async def weekly_reflection():
    # Active filter SQL
    active_users = await db.fetch_all("""
        SELECT u.id, u.kakao_phone, u.hourly_value, u.tier,
               kc.preferred_send_hour
        FROM users u
        INNER JOIN kakao_consents kc ON kc.user_id = u.id
        WHERE kc.subscribed = true
          AND u.deleted_at IS NULL
          AND EXISTS (
            SELECT 1 FROM usage_events ue
            WHERE ue.user_id = u.id
              AND ue.occurred_at > NOW() - INTERVAL '7 days'
          );
    """)
    for user in active_users:
        report = await generate_weekly_report(user)  # Anthropic Haiku
        await save_weekly_report(report)
        await kakao_sender.send_reflection(user, report)

# Every 30 min — threshold check
@scheduler.scheduled_job(CronTrigger(minute='*/30'))
async def threshold_check():
    candidates = await db.fetch_threshold_breaches_today()
    for c in candidates:
        await kakao_sender.send_threshold_alert(c)
        await db.mark_triggered(c.id, today)

# Daily 03:00 — cleanup
@scheduler.scheduled_job(CronTrigger(hour=3, minute=0))
async def daily_cleanup():
    # Expire subscriptions
    await db.execute("""
        UPDATE subscriptions SET status = 'expired'
        WHERE status = 'active' AND expires_at < NOW();
    """)
    # Revoke expired refresh tokens
    await db.execute("""
        UPDATE refresh_tokens SET revoked_at = NOW()
        WHERE expires_at < NOW() AND revoked_at IS NULL;
    """)

# Monthly 1st 03:00 — create next month's partition
@scheduler.scheduled_job(CronTrigger(day=1, hour=3, minute=0))
async def create_next_partition():
    next_month = (datetime.now() + relativedelta(months=1))
    await db.execute(f"""
        CREATE TABLE IF NOT EXISTS usage_events_y{next_month.year}m{next_month.month:02d}
        PARTITION OF usage_events
        FOR VALUES FROM ('{next_month.replace(day=1)}')
                    TO ('{(next_month + relativedelta(months=1)).replace(day=1)}');
    """)
```

## 8. Project Layout

### Backend (FastAPI)

```
backend/
├── app/
│   ├── main.py                       # FastAPI app + lifespan
│   ├── config.py                     # pydantic-settings (env vars)
│   ├── deps.py                       # get_db, get_current_user
│   ├── auth/
│   │   ├── kakao.py                  # Kakao OAuth verification
│   │   ├── jwt.py                    # JWT issue + verify + rotation
│   │   └── routes.py
│   ├── users/
│   │   ├── models.py                 # SQLAlchemy ORM
│   │   ├── schemas.py                # Pydantic
│   │   ├── service.py
│   │   └── routes.py
│   ├── usage/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py                # idempotent batch insert
│   │   └── routes.py
│   ├── reports/
│   │   ├── generator.py              # LLM 1-shot (Anthropic Haiku)
│   │   ├── service.py
│   │   └── routes.py
│   ├── thresholds/
│   │   ├── models.py
│   │   ├── service.py
│   │   └── routes.py
│   ├── payments/
│   │   ├── toss.py                   # Toss client + webhook verifier
│   │   ├── service.py
│   │   └── routes.py
│   ├── kakao/
│   │   ├── client.py                 # SOLAPI/Aligo wrapper
│   │   └── templates.py              # 알림톡 템플릿 3종
│   ├── fcm/
│   │   ├── client.py                 # Firebase Admin SDK wrapper
│   │   └── routes.py
│   ├── scheduler/
│   │   ├── scheduler.py
│   │   ├── weekly_reflection.py
│   │   ├── threshold_check.py
│   │   ├── daily_cleanup.py
│   │   └── partition_manager.py
│   ├── webhooks/
│   │   ├── toss.py
│   │   └── routes.py
│   └── db/
│       ├── session.py                # async_engine + async_session
│       └── base.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py                   # test DB fixtures
│   ├── test_auth.py
│   ├── test_usage_idempotency.py     # critical
│   ├── test_reports_generation.py
│   ├── test_threshold_check.py
│   ├── test_kakao_active_filter.py   # critical
│   └── test_partition_manager.py
├── pyproject.toml                    # uv + dependencies
├── Dockerfile
├── fly.toml
├── alembic.ini
└── .env.example
```

### Frontend (Flutter)

```
frontend/
├── lib/
│   ├── main.dart
│   ├── app.dart                      # MaterialApp + theme
│   ├── theme/
│   │   ├── colors.dart               # DESIGN.md tokens
│   │   ├── typography.dart           # Pretendard + IBM Plex Mono
│   │   └── spacing.dart
│   ├── features/
│   │   ├── auth/
│   │   ├── onboarding/               # P5 60sec flow
│   │   ├── home/                     # 타이머 + hero numeral
│   │   ├── usage/                    # 4 카테고리 breakdown
│   │   ├── report/                   # weekly reflection card
│   │   ├── threshold/
│   │   ├── settings/
│   │   └── payment/
│   ├── core/
│   │   ├── api/                      # http client + interceptors (JWT)
│   │   ├── local_db/                 # Drift schema + queries
│   │   ├── platform_channel/         # UsageStatsManager bridge
│   │   ├── sync/                     # 8h sync engine
│   │   ├── fcm/                      # firebase_messaging
│   │   ├── local_notifications/      # threshold 즉시 알람
│   │   ├── kakao/                    # kakao_flutter_sdk_user
│   │   └── error/                    # Sentry integration
│   └── shared/
│       ├── widgets/
│       └── utils/
├── android/
│   └── app/src/main/kotlin/.../
│       └── UsageStatsBridge.kt       # Kotlin native bridge
├── test/
├── integration_test/
├── pubspec.yaml
└── analysis_options.yaml
```

## 9. CI/CD

### GitHub Actions

**`.github/workflows/backend.yml`**:
```yaml
name: Backend CI/CD
on:
  push:
    branches: [main]
    paths: ['backend/**']
  pull_request:
    paths: ['backend/**']

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test }
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install uv && uv sync
      - run: uv run alembic upgrade head
      - run: uv run pytest --cov --cov-fail-under=80

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

**`.github/workflows/frontend.yml`**:
```yaml
name: Flutter CI/CD
on:
  push:
    branches: [main]
    paths: ['frontend/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with: { flutter-version: '3.x' }
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test --coverage

  build_android:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - uses: actions/setup-java@v4
        with: { java-version: '17' }
      - run: flutter build appbundle --release
      - uses: actions/upload-artifact@v4
        with:
          name: app-release.aab
          path: build/app/outputs/bundle/release/app-release.aab
      # Play Store upload: V1 manual, V1.5 fastlane 자동화 검토
```

## 10. Monitoring + Observability

### Sentry (Python + Flutter, free tier)
- Python: `sentry-sdk[fastapi]` — 모든 unhandled exception + custom events
- Flutter: `sentry_flutter` — 모든 unhandled error + breadcrumbs
- Release tracking: 자동 (CI/CD 시 SENTRY_RELEASE env)
- Performance monitoring: 5% sampling (free tier 한도)

### Mixpanel (server-side events)
- 핵심 event:
  - `signup` (kakao_id, source)
  - `usage_synced` (count, in_work_hours)
  - `report_generated` (week, recovered_minutes)
  - `kakao_sent` (type='weekly'|'threshold')
  - `payment_confirmed` (kind, amount)
  - `subscription_cancelled` (reason)
- KPI dashboard: D7/D30 retention, conversion funnel

### Fly.io built-in metrics
- CPU/memory/network — Fly dashboard
- Health check: `/health` 30s 간격, `/ready` 60s

### Logging
- structlog (Python JSON logging)
- Fly.io tail: `fly logs`
- 검색: `fly logs | grep ERROR`

## 11. 환경 변수 (Fly.io secrets)

```
DATABASE_URL              postgres://...                  (Supabase connection string)
JWT_SECRET                <random 32 bytes>               (HS256)
KAKAO_REST_API_KEY        <Kakao Developers>
KAKAO_CHANNEL_ID          <비즈니스 채널>
SOLAPI_API_KEY            <vendor 선택 후>
SOLAPI_API_SECRET         
ANTHROPIC_API_KEY         <Claude>
OPENAI_API_KEY            <GPT-5 mini fallback>
TOSS_SECRET_KEY           <Toss>
TOSS_WEBHOOK_SECRET       
FIREBASE_SERVICE_ACCOUNT  <JSON, base64 encoded>
SENTRY_DSN                
MIXPANEL_PROJECT_TOKEN    
ENVIRONMENT               production | staging
```

## 12. Implementation Order (W2-W8)

```
W2  Backend setup
    ├── FastAPI 프로젝트 생성 + uv setup
    ├── Fly.io seoul 배포 (hello world)
    ├── Supabase Free 프로젝트 + DATABASE_URL
    ├── Alembic + 첫 migration (users, refresh_tokens)
    ├── /v1/auth/kakao + /v1/auth/refresh (Kakao OAuth + JWT)
    ├── Flutter 프로젝트 생성 + theme 설정 (DESIGN.md)
    ├── Drift schema (local users, settings)
    ├── http client + JWT interceptor
    ├── 온보딩 5화면 (Figma 동기 진행)
    └── /v1/me PATCH (hourly_value 입력)

W3  Timer + 4 카테고리 + FCM
    ├── usage_events partition (y2026m06 ~ y2026m12)
    ├── Drift local_usage_events
    ├── 타이머 화면 (Material 3 + hero numeral)
    ├── 4 카테고리 프리셋 + Firebase Remote Config (웹툰 list)
    ├── FCM 토큰 등록 + /v1/fcm/register
    └── 일일 목표 설정 화면

W4  UsageStatsManager + 카톡 심사 시작 + P7
    ├── Kotlin platform channel UsageStatsBridge
    ├── 동의 화면 UX (P5: 이유 → 권한 → shock)
    ├── Drift batch insert + 8h WorkManager
    ├── /v1/usage/batch (idempotent)
    ├── 카카오 비즈니스 채널 등록 + vendor 가입
    ├── 알림톡 템플릿 3종 초안 심사 제출
    ├── 개인정보처리방침 + 이용약관 Vercel URL 공개
    └── Play Console Digital Wellbeing 정책 self-check

W5  Toss 결제 + KFTC 재검증
    ├── /v1/payments/confirm (server-side verification)
    ├── /webhooks/toss
    ├── 결제 화면 (₩9,900 일회 / ₩4,900 월구독)
    ├── 환불 정책 화면
    └── Toss 외부 결제 2024+ KFTC enforcement 재검증

W6  AI Reports + V1.5 spike
    ├── /v1/reports/weekly (generator with Anthropic SDK)
    ├── 주간 리포트 카드 Flutter Canvas
    ├── 카톡 + 인스타 1-tap 공유
    ├── APScheduler weekly_reflection (active filter SQL)
    ├── V1.5 spike: work_hours heuristic (in_work_hours flag)
    └── 카드 디자인 review

W7  Threshold + 카톡 통합 + 베타
    ├── /v1/thresholds CRUD
    ├── Threshold local detection (Flutter 30min polling)
    ├── flutter_local_notifications 즉시 알람
    ├── APScheduler threshold_check (카톡)
    ├── 카톡 심사 결과 확인 + SOLAPI/Aligo 통합
    ├── Daily cleanup cron
    ├── 클로즈드 베타 50명 + feedback 수집
    └── KPI: 동의율 / retention / 결제 전환

W8  Play Store 출시 + 모니터링
    ├── Sentry Python + Flutter 통합
    ├── Mixpanel events 6종 instrumentation
    ├── Play Store 출시 ($25 등록)
    ├── 가격 페이지 + 결제 funnel
    ├── KPI dashboard
    ├── 공개 launch (긱뉴스 + okky + X)
    └── /canary monitoring
```

## 13. Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-05-22 | Backend = FastAPI + Postgres on Supabase Free + Fly.io seoul | 본인 주력 stack + 사업 확장 호환성 + 데이터 주권 |
| 2026-05-24 | usage_events V1부터 monthly partition | 1년 후 7,300만 row 예상, native PARTITION BY RANGE |
| 2026-05-24 | Sync = 앱 foreground + 8h WorkManager | 배터리 우선, 로컬 threshold detection으로 즉시성 보완 |
| 2026-05-24 | JWT = 15min access + 30d refresh + rotation | 업계 표준, refresh_tokens 테이블로 revocation 가능 |
| 2026-05-24 | API versioning = `/v1/` prefix from day 1 | V2 도입 시 cleanly migrate, backward compat 가능 |
| 2026-05-24 | Auth = Kakao OAuth single provider (V1) | 한국 ICP에 가장 friction 낮음. Email/Google V2 검토 |
| 2026-05-24 | **Auth = Google Sign-In primary (V1 변경)**. Kakao OAuth V2 격하 (카톡 연동 시점 link only) | Android 표준 + Google Play Billing 자연 통합 + Kakao 비즈니스 앱 심사 회피 (W2 일정 단축) + 발각 risk 회피 (Kakao 본명 강결합). V2 카톡 link 시 phone 1회 입력 step 추가. |
| 2026-05-24 | **V1 = 무료 도구 pivot**. 사업자 미보유 (회사 겸업 금지). 카톡·Toss V2 격하. | wedge #3 재정의: multi-channel retention (FCM + 이메일 + Telegram). 회사 발각 risk 회피 + portfolio + V2 monetization base. |
| 2026-05-24 | channel_subscriptions 통합 테이블 (kakao_consents 대체) | FCM/이메일/Telegram/Discord/Slack 일관 schema. 확장성 ↑. |
| 2026-05-24 | **V1 인앱결제 paid re-pivot**: subscriptions·payments 테이블 부활 (Google Play Billing). /v1/payments/google_play/* + /webhooks/google_play_rtdn endpoint 부활. Toss는 V2 격하. | Google Play Console Individual 계정 = 사업자 X로 매출 발생 가능. 가격 ₩11K/₩5.9K/₩39K + 7일 free trial + 베타 50명 50% + 출시 7일 30%. |

## 14. Subagent Cold Read 반영 (2026-05-24)

Architecture 작성 직후 독립 subagent challenge 14개 반영.

### P0 — W2 시작 전 즉시 (today)

**14.1. 카카오 비즈니스 채널 + 사업자 등록 + 알림톡 템플릿 심사 즉시 착수**
- 사업자 등록 (홈택스): 1-3일
- 카카오 비즈니스 채널 가입 + 인증: 1-2주
- 알림톡 템플릿 심사: 3-7일 × 반려 가능 (worst case 2-3주)
- → W2 시작 시 사업자 등록 + 채널 신청 + 템플릿 초안 **동시 진행**
- W4 "초안 제출"이 아니라 **W2 첫째 날부터 병행**

**14.2. .kr 도메인 + 본인인증 + Fly.io custom domain + Let's Encrypt**
- .kr 등록은 한국 통신사 본인인증 필요 (반나절)
- W2 backend 배포 전 준비

### P1 — Architecture 수정 필요

**14.3. usage_events idempotency 재설계**
- 기존: `UNIQUE (user_id, client_event_id, occurred_at)` → `occurred_at` millisecond drift로 중복 row 생성 가능
- 변경: **별도 non-partitioned `usage_event_dedupe` 테이블 + 24h TTL** 또는 Redis SET 활용

```sql
CREATE TABLE usage_event_dedupe (
  user_id UUID NOT NULL,
  client_event_id UUID NOT NULL,
  inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, client_event_id)
);
-- 24h TTL cleanup cron (daily 03:00)
```

Batch insert flow:
```python
async def batch_insert_usage_events(user_id, events):
    # 1. Check dedupe table
    seen = await db.fetch_all("""
        SELECT client_event_id FROM usage_event_dedupe
        WHERE user_id = $1 AND client_event_id = ANY($2)
    """, user_id, [e.client_event_id for e in events])
    new_events = [e for e in events if e.client_event_id not in seen]
    
    # 2. Insert dedupe markers (atomic with usage_events insert)
    async with db.transaction():
        await db.executemany("""
            INSERT INTO usage_event_dedupe (user_id, client_event_id) VALUES ($1, $2)
        """, ...)
        await db.executemany("""
            INSERT INTO usage_events (...) VALUES (...)
        """, ...)
```

**14.4. FK ON DELETE CASCADE 제거 → soft delete + batch archive**
- 변경: `usage_events.user_id REFERENCES users(id)` (CASCADE 없이)
- 사용자 hard delete는 30일 grace + batch archive cron으로 분리
- `users.deleted_at IS NOT NULL` 사용자의 usage_events는 archive_usage_events로 batch move 후 hard delete

**14.5. PIPA 준수 — 처리방침 보완**
- **국외 이전 동의** (Fly.io US 모회사) — 별도 체크박스
- 위탁 처리 list 명시: Anthropic, OpenAI, Toss, SOLAPI/Aligo, Firebase, Fly.io, Supabase, Sentry, Mixpanel
- **만 14세 미만 age gate**: 가입 시 생년월일 확인 또는 14세+ 동의 체크
- **회원 탈퇴 30일 grace → hard delete cron**

**14.6. 카톡 알림톡 정책 — 광고성 회피 + 수신거부 footer**
- "₩X 회복" wording 위험 → "이번 주 SNS·쇼츠·웹툰에서 N분 줄였어요" 톤 유지 (혜택성 X)
- 22:00 발송도 정보성 분류로 사전 카카오 확인 필요
- **모든 알림톡 메시지 footer에 수신거부 안내 + 1-tap 링크 필수**

**14.7. Toss + Google Play 정책 충돌 — Plan B 명시**
- Toss 외부 결제 (KFTC 허용) ≠ Google Play 정책 통과
- Plan B: Play in-app billing fallback (수수료 30%, 가격 ₩11,000/₩5,900 인상)
- W5 KFTC 재검증 시점에 Play 정책 변동 확인 + Plan B 활성화 가능 상태 유지

**14.8. W2 timeline split (cognitive load 관리)**
```
W2 (수정): Backend only
  ━ FastAPI + Fly.io + .kr 도메인 + Supabase + Alembic + Kakao OAuth + JWT

W3 (수정): Flutter scaffolding
  ━ 프로젝트 + theme (DESIGN.md) + Drift + http interceptor + 온보딩 5화면

W4 (변동 없음): UsageStatsManager + 카톡 진행
W5-W8: 기존 PRD §12 유지
```

→ PRD §12 W2-W3 분리 update 필요 (별도 commit).

**14.9. APScheduler single-process risk → 외부 cron trigger fallback**
- Fly.io machine auto-stop 시 cron miss
- 변경:
  - `fly.toml`에 `min_machines_running = 1` 명시
  - **cron-job.org 외부 webhook trigger fallback** — 일요일 22:00에 cron-job.org → POST /v1/internal/trigger-weekly (secret-protected)
  - 동일하게 daily 03:00 cleanup도 외부 trigger

### P2 — 구현 시 반영 (W2-W8)

**14.10. Anthropic Tier 1 prepay** — Free RPM 50 → 일요일 5,000 동시 처리 시 초과. Tier 1 $5 prepay 또는 batch API 활용.

**14.11. Supabase Free → Pro trigger 명시** — DB > 400MB OR 6개월 도달 OR Sunday cron 부담 ↑ 시 자동 Pro 전환. M3-M4 시점 예상.

**14.12. Sentry quota 관리** — Free 5K errors/월. Aggressive filtering (4xx 제외) + alert rule on 80% quota.

**14.13. LLM fallback prompt 추상화** — `reports/templates.py`에 model-agnostic prompt template. Claude / GPT-5 mini 양쪽에 동치 prompt 사용.

**14.14. Backup 전략** — Supabase Free 7일 backup 보관, restore는 Pro only. **M3 GO 시점에 무조건 Pro 전환** (사고 시 데이터 손실 회피).

### 추가 미시 사항
- `fcm_tokens.token VARCHAR(500)` → `VARCHAR(1024)` (FCM v1 토큰 길이 안전 buffer)
- `thresholds.last_triggered_date DATE` → `last_triggered_at TIMESTAMPTZ` (timezone 처리)
- `recovered_won` 곱셈 중간값 BIGINT 변환 (overflow 회피)
- HS256 single-instance 명시 (`min_machines_running = 1, max_machines_running = 1`)
- `/health` `/ready` fly.toml `[[http_service.checks]]` 명시
- LLM call의 결과를 weekly_reports에 저장 시 service_used 컬럼 추가 (claude/gpt-mini 추적)

## 14a. V1 무료 도구 Pivot 반영 (2026-05-24, post §14 cold read)

본인 회사 겸업 명시적 금지 → 사업자 등록 V1에서 X → 카톡·Toss V2 격하. multi-channel retention으로 wedge #3 재정의.

### Schema 변경

**kakao_consents 제거 → channel_subscriptions로 generalize**:

```sql
CREATE TABLE channel_subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  channel VARCHAR(20) NOT NULL
    CHECK (channel IN ('fcm', 'email', 'telegram', 'discord', 'slack')),
  channel_identifier VARCHAR(500) NOT NULL,  -- email address / chat_id / FCM token / webhook URL
  subscribed BOOLEAN NOT NULL DEFAULT TRUE,
  preferred_send_hour SMALLINT NOT NULL DEFAULT 22,
  subscribed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  unsubscribed_at TIMESTAMPTZ,
  metadata JSONB,  -- channel별 추가 정보 (Telegram username, Discord server 등)
  UNIQUE (user_id, channel)
);
CREATE INDEX idx_channel_subscriptions_active
  ON channel_subscriptions (user_id) WHERE subscribed = TRUE;
```

**subscriptions 테이블 V1 부활 (2026-05-24 인앱결제 re-pivot)**:

```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),  -- soft delete only, no CASCADE
  source VARCHAR(20) NOT NULL DEFAULT 'google_play'
    CHECK (source IN ('google_play', 'toss')),  -- toss는 V2
  kind VARCHAR(20) NOT NULL
    CHECK (kind IN ('one_time', 'monthly', 'yearly')),
  
  -- Google Play Billing 정보
  gp_purchase_token VARCHAR(500) UNIQUE,  -- Google Play purchase token
  gp_order_id VARCHAR(100),
  gp_product_id VARCHAR(100),  -- 'kkeugi.cert', 'kkeugi.monthly', 'kkeugi.yearly'
  
  -- V2 Toss 정보 (사업자 등록 후)
  toss_payment_key VARCHAR(255),
  toss_order_id VARCHAR(100),
  
  amount_krw INTEGER NOT NULL,  -- gross 사용자 결제 금액
  net_krw INTEGER NOT NULL,     -- 본인 net 수령 (Google 70%, Toss 96.7%)
  
  status VARCHAR(20) NOT NULL
    CHECK (status IN ('active', 'in_trial', 'cancelled', 'expired', 'refunded')),
  
  trial_starts_at TIMESTAMPTZ,  -- 7일 free trial 시작
  starts_at TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  cancelled_at TIMESTAMPTZ,
  refunded_at TIMESTAMPTZ,
  
  promo_code VARCHAR(50),  -- 베타 50명 'BETA50', 출시 7일 'LAUNCH30'
  discount_percent SMALLINT DEFAULT 0,
  
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_subscriptions_user_active 
  ON subscriptions (user_id) WHERE status IN ('active', 'in_trial');
CREATE INDEX idx_subscriptions_expires 
  ON subscriptions (expires_at) WHERE status = 'active';
CREATE INDEX idx_subscriptions_gp_token ON subscriptions (gp_purchase_token);
```

**API endpoints 부활 (V1)**:
- POST `/v1/payments/google_play/verify` — purchase token 서버 검증 (Google Play Developer API)
- GET `/v1/payments/subscription` — current subscription status
- POST `/v1/payments/cancel` — cancel subscription (Google Play 자동 처리, 서버에서는 mark cancelled)
- POST `/v1/payments/refund` — 환불 처리 (자체 7일 청약철회)
- POST `/webhooks/google_play_rtdn` — Google Play Real-time Developer Notifications (refund, expire, renewal)

### API 변경

**V1 부활 (2026-05-24 인앱결제 re-pivot)**:
- POST /v1/payments/google_play/verify (위 schema 참조)
- GET /v1/payments/subscription
- POST /v1/payments/cancel
- POST /v1/payments/refund
- POST /webhooks/google_play_rtdn

**V2 격하 (사업자 등록 후 추가)**:
- POST /v1/payments/toss/confirm
- POST /webhooks/toss

**추가 (V1)**:
- POST /v1/me/email_consent { email } — 이메일 채널 구독
- POST /v1/me/telegram_link { telegram_username } — Telegram Bot start 후 chat_id 저장
- DELETE /v1/me/channels/:channel_id — 구독 해제
- GET /v1/me/channels — 구독 목록

### Multi-channel dispatch 흐름

```python
# backend/app/scheduler/weekly_reflection.py

async def weekly_reflection_job():
    active_subs = await db.fetch_all("""
        SELECT u.id, u.display_name, u.hourly_value,
               array_agg(json_build_object(
                 'channel', cs.channel,
                 'identifier', cs.channel_identifier,
                 'metadata', cs.metadata
               )) AS channels
        FROM users u
        INNER JOIN channel_subscriptions cs ON cs.user_id = u.id
        WHERE u.deleted_at IS NULL
          AND cs.subscribed = TRUE
          AND EXISTS (
            SELECT 1 FROM usage_events ue
            WHERE ue.user_id = u.id
              AND ue.occurred_at > NOW() - INTERVAL '7 days'
          )
        GROUP BY u.id;
    """)
    
    for user in active_subs:
        report = await generate_weekly_report(user)  # Anthropic Haiku
        await save_report(report)
        
        for channel in user.channels:
            try:
                if channel.channel == 'fcm':
                    await fcm_client.send_card(channel.identifier, report)
                elif channel.channel == 'email':
                    await mailgun_client.send_card(channel.identifier, report)
                elif channel.channel == 'telegram':
                    await telegram_bot.send_card(channel.identifier, report)
            except ChannelDeliveryError as e:
                sentry.capture_exception(e)
                # 다른 채널은 계속 시도
```

### Stack 변경

| 제거 | 추가 |
|---|---|
| Toss Payments SDK | 없음 |
| SOLAPI/Aligo/DirectSend | Mailgun SDK (Python) |
| Kakao 비즈메시지 vendor | python-telegram-bot SDK |

### 14.7. Toss + Google Play Plan B 제거
V1 무료 도구라 결제 자체가 없음. V2 진입 시점에 재검토.

## 15. Open Questions / Future Work

- **Vendor 선택**: SOLAPI / Aligo / DirectSend 중 1택 (W4 시작 전 결정 — TODOS P2)
- **Play Store category**: "Digital Wellbeing" vs "Productivity" — review risk 따라 결정
- **FCM Pro 전환 시점**: 한도 free 충분. paid 전환 trigger 없음 (FCM free unlimited)
- **Hetzner migration**: 5,000명 도달 + Supabase Pro 비용 > Hetzner 인프라 + ops 시간 비용 시
- **iOS Companion**: Phase 1 매출 ₩200만/월 도달 후 외주 ₩200-500만
- **챗봇 (사용자 카톡으로 명령)**: V2 후보, 자체 서버라 가능
- **Multi-product (Phase 2 B-3 카페인·수면)**: 같은 user_id로 별도 테이블 추가

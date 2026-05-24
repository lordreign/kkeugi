# Kkeugi Backend

FastAPI + PostgreSQL + Google Sign-In + JWT.

## Stack
- Python 3.12 + uv
- FastAPI + uvicorn + SQLAlchemy 2.0 async + asyncpg
- Alembic migrations
- google-auth (Google ID token verify)
- python-jose (JWT 15min access + 30d refresh + rotation)
- Sentry (optional)
- Fly.io (deploy)

## Quickstart (Local)

### 사전 요구
- **uv** (`brew install uv` 또는 `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Docker Desktop** (Postgres 컨테이너용)
- **Python 3.12+** (uv가 자동 설치)

### 첫 setup — 한 줄

```bash
cd backend
make setup
```

이 명령이 다음을 자동 실행합니다:
1. `.env.example` → `.env` 복사 (없으면)
2. Postgres Docker 컨테이너 시작 (port 5432, db: `kkeugi` + `kkeugi_test`)
3. `uv sync` 의존성 설치
4. `alembic upgrade head` migration 적용

### 서버 실행

```bash
make run
```

- API docs: http://localhost:8080/docs
- Health: http://localhost:8080/health
- Ready (DB ping): http://localhost:8080/ready

### Dev login (Google OAuth setup 없이 바로 시작)

local dev/test 환경에서만 활성되는 `/v1/auth/dev/login` 사용:

```bash
curl -X POST http://localhost:8080/v1/auth/dev/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"me@test.com","name":"Test User"}'
```

응답:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "...",
    "email": "me@test.com",
    "tier": "free",
    ...
  }
}
```

access_token으로 인증된 endpoint 호출:
```bash
curl http://localhost:8080/v1/me \
  -H "Authorization: Bearer eyJ..."
```

**프로덕션에서는 `/v1/auth/dev/login` 비활성** (`ENVIRONMENT=production` 시 404).

## Make commands

```
make setup     — first-time setup (env + db + install + migrate)
make db-up     — start postgres container
make db-down   — stop postgres container
make db-reset  — drop volumes + restart (DESTROYS LOCAL DATA)
make install   — uv sync dependencies
make migrate   — alembic upgrade head
make run       — uvicorn with reload (port 8080)
make test      — pytest with coverage
make lint      — ruff check
make fmt       — ruff format
make clean     — remove caches
```

## Tests

```bash
make test
# 또는
uv run pytest -v
uv run pytest --cov=app --cov-report=html  # HTML coverage report
```

`kkeugi_test` DB는 `make db-up` 시 자동 생성됨 (`scripts/init-test-db.sql`).

## Production endpoints (W2 완료)

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health` | None | Liveness probe |
| GET | `/ready` | None | DB readiness |
| POST | `/v1/auth/google` | None | Google ID token → JWT pair |
| POST | `/v1/auth/refresh` | Refresh | Rotate token pair |
| POST | `/v1/auth/logout` | Refresh | Revoke refresh token |
| GET | `/v1/me` | Access | Current user |
| PATCH | `/v1/me` | Access | Update settings |
| DELETE | `/v1/me` | Access | Soft delete account |

## Dev-only endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/v1/auth/dev/login` | Bypass Google verify, create/fetch user by email |

## Deploy (Fly.io)

P0 checklist (`docs/W2-prestart-P0.md`) 완료 후:

```bash
# 1. Fly.io 앱 생성
fly launch --no-deploy --config fly.toml

# 2. Secrets 등록
fly secrets set \
  DATABASE_URL="postgresql+asyncpg://postgres.xxx:password@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres" \
  JWT_SECRET="$(openssl rand -hex 32)" \
  GOOGLE_CLIENT_ID="xxx.apps.googleusercontent.com" \
  ANTHROPIC_API_KEY="sk-ant-xxx" \
  SENTRY_DSN_BACKEND="https://xxx@sentry.io/yyy"

# 3. Deploy
fly deploy

# 4. Custom domain (api.kkeugi.kr 등록 후)
fly certs add api.kkeugi.kr

# 5. Logs
fly logs
```

## Troubleshooting

### `make setup` 실패 — Docker 미설치
```bash
brew install --cask docker
open -a Docker
```

### `uv sync` 실패 — Python 3.12 없음
uv가 자동으로 Python 3.12 download해야 함. 안 되면:
```bash
uv python install 3.12
```

### Postgres 연결 실패
```bash
make db-down
make db-up  # 다시 시작
docker logs kkeugi-pg  # 에러 확인
```

### `alembic upgrade head` 실패 — DB 비어있지 않음
```bash
make db-reset  # ⚠️ 로컬 데이터 삭제됨
```

### JWT_SECRET 보안
프로덕션 deploy 전 강력한 secret 생성:
```bash
openssl rand -hex 32
```

## Next (W3+)

- W3: Flutter scaffolding + Drift local DB + http JWT interceptor + 온보딩 5화면
- W4: Kotlin UsageStatsManager + Mailgun + privacy URL publish
- W5: Google Play Billing + Telegram Bot + 회원 탈퇴 UX
- W6: AI weekly report + Anthropic SDK + APScheduler + paywall UX
- W7: Threshold local detection + 베타 50명
- W8: Play Store 출시

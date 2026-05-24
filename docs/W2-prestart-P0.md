# W2 시작 전 P0 Checklist

> 본인 계정·payment·도메인 작업. W2 코드 시작 전 모두 완료 권장.
> 일부 (예: Mailgun·Telegram)는 W4-W5 시작 전까지로 늦출 수 있음.

## 🔴 W2 시작 전 즉시 (이번 주 안에)

### 1. .kr 도메인 등록
- [ ] `api.kkeugi.kr` 또는 `kkeugi.kr` 등록 신청
- [ ] 한국 통신사 본인인증 (KT/SKT/LGU+ 명의)
- [ ] 등록 대행사 권장: **가비아** ([gabia.com](https://www.gabia.com)) 또는 **후이즈** ([whois.co.kr](https://whois.co.kr))
- [ ] 비용: 연 ₩20,000-30,000
- [ ] 처리 시간: 반나절

### 2. Fly.io 가입 + payment
- [ ] [fly.io/dashboard](https://fly.io/app/sign-up) 가입 (GitHub 연동 권장)
- [ ] 신용카드 등록 (free tier 가능, payment method는 필수)
- [ ] CLI 설치: `brew install flyctl`
- [ ] `fly auth login`

### 3. Supabase Free 프로젝트
- [ ] [supabase.com/dashboard](https://supabase.com/dashboard) 가입
- [ ] New project 생성:
  - Region: **Northeast Asia (Seoul)** (ap-northeast-2)
  - DB password 강력하게 설정 + 안전한 곳 저장
  - Tier: Free
- [ ] DATABASE_URL 복사 (Settings → Database → Connection string → URI)
  - PgBouncer transaction mode 권장 (`?pgbouncer=true&connection_limit=1`)
- [ ] DB > 400MB 도달 시 Pro 전환 alert 설정 (Dashboard)

### 4. Google Cloud Console — OAuth 2.0 Client ID
- [ ] [console.cloud.google.com](https://console.cloud.google.com) 가입
- [ ] 새 프로젝트 생성 (이름: kkeugi)
- [ ] **OAuth consent screen** 설정:
  - User type: External
  - App name: 끊기 (Kkeugi)
  - User support email: 본인 이메일
  - Developer contact: 본인 이메일
  - Authorized domain: `kkeugi.kr` (도메인 등록 후)
- [ ] **Credentials → OAuth Client ID** 생성:
  - Application type: **Android**
  - Package name: `kr.kkeugi` (Flutter 프로젝트에서 사용)
  - SHA-1 certificate fingerprint: Android keystore에서 추출 (W3에 필요, W2에서 미리 dev/release 양쪽 생성 권장)
  - Web Client ID도 별도 생성 (backend에서 ID token verify용)
- [ ] GOOGLE_CLIENT_ID (Web Client ID) 복사 → 백엔드 secret으로 저장
- [ ] 비용: 무료

### 5. Anthropic API + Tier 1 prepay
- [ ] [console.anthropic.com](https://console.anthropic.com) 가입
- [ ] **Tier 1 prepay $5** (Workspace → Billing → Add credits)
  - Free tier RPM 50 → Tier 1 RPM 1,000+
  - 일요일 22:00 동시 LLM 호출 대비
- [ ] API key 발급 → 백엔드 secret으로 저장
- [ ] ANTHROPIC_API_KEY 환경 변수

### 6. Sentry Free 가입
- [ ] [sentry.io](https://sentry.io) 가입
- [ ] 새 프로젝트 2개 생성:
  - 백엔드: Python (FastAPI)
  - 프론트엔드: Flutter (Mobile)
- [ ] DSN 2개 복사 → secrets 저장 (SENTRY_DSN_BACKEND, SENTRY_DSN_FLUTTER)
- [ ] Free tier alert: 5K errors/월 80% 도달 시 알람 (Settings → Alerts)

### 7. GitHub repo + Actions
- [ ] 현재 `pjs/kkeugi` repo가 GitHub origin 있는지 확인
  - 없으면 새 repo 생성 (private 권장)
- [ ] GitHub Settings → Secrets and variables → Actions
- [ ] 다음 secrets 등록 (W2 deploy workflow에서 사용):
  - FLY_API_TOKEN (Fly.io → User → Access tokens)
  - DATABASE_URL_TEST (테스트용 Postgres)

## 🟡 W4 시작 전 (2-3주 후)

### 8. Mailgun 가입 (이메일 retention)
- [ ] [mailgun.com](https://mailgun.com) 가입
- [ ] Free tier (5K emails/월) 활성
- [ ] 발신 도메인 추가 (예: `mail.kkeugi.kr` 서브도메인)
- [ ] DNS 레코드 추가 (SPF, DKIM, MX)
- [ ] MAILGUN_API_KEY + MAILGUN_DOMAIN secret 등록
- [ ] AWS SES도 대안 ($0.10/1K) — 비용 더 싸지만 setup 복잡

## 🟡 W5 시작 전 (3-4주 후)

### 9. Telegram BotFather에서 Bot 생성
- [ ] Telegram 앱에서 `@BotFather` 검색
- [ ] `/newbot` → 이름: "Kkeugi" / username: `kkeugi_bot`
- [ ] API token 발급 → TELEGRAM_BOT_TOKEN secret 등록
- [ ] Bot description 한국어 설정
- [ ] `/setcommands` 등록:
  - `start` — 회고 알림 받기 시작
  - `stop` — 알림 끄기
  - `help` — 도움말

### 10. Google Play Console Individual 가입
- [ ] [play.google.com/console](https://play.google.com/console) 가입
- [ ] Account type: **Individual** (사업자등록증 X)
- [ ] 등록비 $25 (일회)
- [ ] 결제 정보:
  - 본인 명의 한국 통장
  - 주민번호 (tax info)
- [ ] Merchant Center 별도 setup (Google Play Billing 활성 시 자동)
- [ ] 3 product 등록 (W5 작업):
  - `kkeugi.cert` — 일회 ₩11,000
  - `kkeugi.monthly` — 월 ₩5,900
  - `kkeugi.yearly` — 연 ₩39,000
- [ ] 7일 free trial Google Play 표준 설정

## 🟢 W7 시작 전 (5-6주 후)

### 11. 베타 50명 promo code 발급
- [ ] Google Play Console → Promotions → Create promo code
- [ ] 평생 50% 할인 코드 50개 생성
- [ ] 베타 사용자에게 배포 (이메일 또는 Slack/Discord)

### 12. 출시 7일 30% 할인 sale
- [ ] Google Play Console → Pricing → Sale
- [ ] 30% off, 출시일부터 7일

## 📋 Secrets 종합 list (Fly.io secrets 등록)

W2 시작 시 다음 secrets `fly secrets set` 명령으로 등록:

```bash
fly secrets set \
  DATABASE_URL="postgresql+asyncpg://..." \
  JWT_SECRET="$(openssl rand -hex 32)" \
  GOOGLE_CLIENT_ID="...apps.googleusercontent.com" \
  ANTHROPIC_API_KEY="sk-ant-..." \
  SENTRY_DSN_BACKEND="https://...@sentry.io/..." \
  ENVIRONMENT="production"

# W4 추가
fly secrets set MAILGUN_API_KEY="..." MAILGUN_DOMAIN="mail.kkeugi.kr"

# W5 추가
fly secrets set TELEGRAM_BOT_TOKEN="..."

# V2 추가 (사업자 등록 후)
fly secrets set TOSS_SECRET_KEY="..." TOSS_WEBHOOK_SECRET="..."
```

## 📋 Status tracker

| 항목 | 시작 | 완료 | 비고 |
|---|---|---|---|
| 1. .kr 도메인 | | | |
| 2. Fly.io | | | |
| 3. Supabase | | | |
| 4. Google Cloud OAuth | | | |
| 5. Anthropic Tier 1 | | | |
| 6. Sentry | | | |
| 7. GitHub Actions | | | |
| 8. Mailgun (W4) | | | |
| 9. Telegram Bot (W5) | | | |
| 10. Google Play Console (W5) | | | |

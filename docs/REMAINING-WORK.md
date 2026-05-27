# 끊기 — 남은 작업 & 본인 할 일 정리

> **2026-05-27 갱신.** W5~W7 코드 + 회고 카드 공유까지 완료(커밋 `2917976`).
> **코드로 끝낼 수 있는 작업은 사실상 모두 완료** — 남은 건 ① 키스토어 의존 코드 1건 ② 프론트 CI(보류) ③ W8 출시 코드 ④ **본인 외부 작업(계정·심사·배포·실기기·마케팅)**.
> 상세: [PRD §12](PRD.md) · [W5-prestart-P0](W5-prestart-P0.md) · [W5~W7 build-plan](W7-build-plan.md)

---

## 0. 현황 한눈에

```
W0 기획 ✅   W1 설계 ✅   W2 백엔드 ✅   W3 프론트 ✅   W4 데이터 ✅
W5 결제·탈퇴·Telegram(코드 Step1~5) ✅ / Step6 실기기=본인
W6 리포트·cron·multi-channel·gating·archive·회고카드공유 ✅
W7 thresholds 백엔드·UI·로컬알람·KPI ✅
W8 ⬜ 출시 (마케팅·data safety) + 본인 store listing·launch
```
- **출시 전 "지금 가능한 코드"는 완료.** 모든 외부 연동은 Fake 추상화로 검증됨(실 키 연결만 남음).
- 검증 현황: 백엔드 pytest 65 green / 프론트 analyze 0·테스트 25 green / debug APK + AVD end-to-end.

---

## A. 남은 코드 작업 (Claude가 진행 가능)

### A-1. ⏸ 릴리스 서명 코드화 (키스토어 본인 생성 후 — 보류)
- [ ] `android/key.properties` 연결 + `build.gradle.kts` release `signingConfig` (현재 debug 키)
  - **보류 사유**: 키스토어 생성(B-2)이 선행돼야 함. 생성 후 코드 1줄 연결.
- [ ] (선택) 구매 acknowledge를 **서버 검증 후**로 정교화 (현재 V1은 즉시 complete)

### A-2. ⬜ 프론트엔드 CI 워크플로우 (보류 — 순차 도입)
- [ ] `.github/workflows/frontend.yml`: `paths: frontend/**` → `flutter pub get`·`analyze`·`test`·(선택) `build apk --debug`
  - 현재 `backend.yml`만 존재(`paths: backend/**`) → **프론트 커밋은 CI 미작동**. 로컬 수동 검증 중.
  - **도입 타이밍**: 본인 B-6 GitHub Actions secrets 등록 단계에서 함께.

### A-3. ⬜ W8 출시 대응 코드
- [ ] 마케팅/소개 페이지 (정적 또는 앱 내 + 법무 URL 링크)
- [ ] Play Store **Data safety** 항목에 맞춘 코드/권한 점검
- [ ] (실 키 연결 후) Mixpanel 이벤트가 실제 수집되는지 dashboard 확인

### A-4. ⬜ V1.5 spike (출시 후)
- [ ] P4 작업 시간대 heuristic (탐색) — 설정 "작업 시간 (V1.5)" 플레이스홀더 실동작
- [ ] 베타 피드백 반영 버그 수정 (W7 베타 중)

### ✅ 완료된 코드 작업 (참고)
- W5: Telegram link · 회원탈퇴/PIPA 삭제 · 결제 백엔드(Fake/Real verifier) · paywall+billing(Fake/Real) · RealBilling 코드
- W6: 주간 리포트(LLM Fake/Haiku) · APScheduler cron(주간·hard-delete·파티션) · multi-channel dispatch(Mailgun/FCM/Telegram) · archive 화면 · **매출환산 paywall gating** · **회고 카드 1-tap 공유(1080×1920)**
- W7: thresholds 백엔드(require_paid) · 한도 설정 UI · **로컬 알람**(flutter_local_notifications) · **KPI 계측**(Fake/Mixpanel 6 이벤트)

---

## B. 본인이 해야 할 작업 (외부·계정·결제 — 코드로 못 함)

> ⏰ 표시는 **리드타임이 길어 일찍 시작해야 W8 출시 일정에 맞는 것**. **이제 메인 병목은 전부 여기.**

### B-1. ⏰⏰ Google Play 클로즈드 테스트 (출시 최대 blocker)
- [ ] 개인 계정은 프로덕션 전 **테스터 12명 × 14일 연속** opt-in 필요
- [ ] 테스터 12명 확보: 품앗이 + 지인·가족 (회사 동료 X) — [W5-prestart A-1](W5-prestart-P0.md)
- [ ] **W7 베타 = 14일 시계 시작**으로 설계 → Play Console 셋업은 즉시

### B-2. ⏰ Google Play Console
- [ ] 가입 + 등록비 $25 + **신원 확인**(수일, 개발자 표시명 본명 회피)
- [ ] 앱 생성: 패키지명 **`kr.kkeugi.kkeugi`**
- [ ] 릴리스 **키스토어 생성** + Play App Signing 등록 → 이후 A-1 코드 연결
- [ ] **SHA-1 두 종류(업로드키 + Play 서명키)를 Google Cloud OAuth에 등록** (안 하면 Google 로그인 실패)
- [ ] 내부 테스트 트랙에 서명 AAB 업로드 → **그 후** 인앱상품 3종(`kkeugi.cert`/`monthly`/`yearly`) + 7일 trial offer 생성
- [ ] 라이선스 테스터(Gmail) 추가
- [ ] Store listing: 스크린샷·설명·아이콘·**Data safety** 작성

### B-3. ⏰ 영수증 검증용 서비스 계정 (Google Play Developer API)
- [ ] Google Cloud 서비스 계정 생성 + Play Console 권한 연결
- [ ] JSON 키 발급 → 배포 secret `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON`

### B-4. Telegram (리드타임 낮음)
- [ ] BotFather `/newbot` → `kkeugi_bot` 토큰 → `TELEGRAM_BOT_TOKEN`
- [ ] 배포 후 웹훅 등록 (`setWebhook` → `https://api.kkeugi.kr/webhooks/telegram` + secret)

### B-5. 이메일 (Mailgun)
- [ ] Mailgun 가입 + free tier + 발신 도메인(`mail.kkeugi.kr`) DNS(SPF/DKIM/MX)
- [ ] `MAILGUN_API_KEY` + `MAILGUN_DOMAIN`

### B-6. 인프라·배포·CI
- [ ] `.kr` 도메인(`api.kkeugi.kr`) 등록
- [ ] Fly.io 가입 + 카드 + `FLY_API_TOKEN`(GitHub Actions secret) → 첫 배포
- [ ] Supabase 프로젝트(Seoul) → prod `DATABASE_URL`
- [ ] Google Cloud OAuth Client(Android + Web) → `GOOGLE_CLIENT_ID`
- [ ] Anthropic API key + Tier 1 prepay → `ANTHROPIC_API_KEY`
- [ ] Sentry DSN(백엔드/프론트), **Mixpanel 프로젝트 토큰**(KPI 실 수집)
- [ ] 이 단계에서 **A-2 `frontend.yml` CI 함께 도입**

### B-7. 실기기 통합 검증 (W5 Step 6)
- [ ] 실기기 `--dart-define=USE_FAKE_BILLING=false` 빌드 → 라이선스 테스터 실구매
- [ ] 구매 → 서버 `/verify`(RealGooglePlayVerifier) → entitlement → paywall 해제
- [ ] 텔레그램 실제 연결(딥링크→/start) + 회고 카드 수신 + 회고 카드 공유 실기기 확인

### B-8. 출시·운영 결정
- [ ] 클로즈드 베타 50명 모집 + 회고 카드 공유 요청(바이럴)
- [ ] 공개 launch (긱뉴스·OKKY·X 빌드인퍼블릭)
- [ ] **사업자 등록 결정**: 월 net 매출 ₩35~50만 도달 시 (M3 hard checkpoint) → V2(Toss·카톡)
- [ ] 개인정보처리방침·이용약관 **URL 호스팅** (`docs/legal/*.md` 작성됨, 위치만 결정)

---

## C. 의존 순서 (지금 → 출시)

```
[지금]  본인 B-2 Play Console 가입·신원확인 시작 (리드타임 최우선)
[그다음] 본인 B-6 인프라 secrets + 첫 배포 (Fly/Supabase/OAuth/Anthropic/Mixpanel)
        → 이때 Claude A-2 frontend CI + A-1 릴리스 서명(키스토어 생성 후) 연결
        → Telegram 웹훅(B-4) / Mailgun(B-5) 실연동
[W7~]   본인 B-1 클로즈드 테스트 14일 시작 + B-7 실기기 billing 검증(B-2·B-3 후)
[W8]    Claude A-3 마케팅·data safety  +  본인 B-2 store listing + B-8 출시·launch
```

**핵심**: 코드는 준비 완료. 이제 **Play Console 신원확인·클로즈드 테스트(리드타임)** 가 출시 일정을 결정한다. 인프라 secrets가 준비되면 실 billing·telegram·email·Mixpanel·릴리스 서명·프론트 CI를 한 번에 통합.

---

## D. 배포 시 등록할 Secrets (종합)

```bash
# Fly.io (백엔드)
fly secrets set \
  DATABASE_URL="postgresql+asyncpg://...supabase..." \
  JWT_SECRET="$(openssl rand -hex 32)" \
  GOOGLE_CLIENT_ID="...apps.googleusercontent.com" \
  ANTHROPIC_API_KEY="sk-ant-..." \
  SENTRY_DSN_BACKEND="https://...@sentry.io/..." \
  TELEGRAM_BOT_TOKEN="..." \
  TELEGRAM_WEBHOOK_SECRET="$(openssl rand -hex 16)" \
  MAILGUN_API_KEY="..." MAILGUN_DOMAIN="mail.kkeugi.kr" \
  GOOGLE_PLAY_PACKAGE_NAME="kr.kkeugi.kkeugi" \
  GOOGLE_PLAY_SERVICE_ACCOUNT_JSON="$(cat play-sa.json)" \
  ENVIRONMENT="production"

# GitHub Actions
#   FLY_API_TOKEN  (백엔드 배포 게이트 — 미설정 시 deploy job skip)
```
- 릴리스 빌드 dart-define: `USE_FAKE_BILLING=false` · `API_BASE_URL=https://api.kkeugi.kr` · `IS_PRODUCTION=true` · `MIXPANEL_TOKEN=...` · `SENTRY_DSN=...`
- 키스토어/SHA-1은 secret 아님 — **안전 보관**(분실 시 앱 업데이트 영구 불가)

---

## 한 눈 체크리스트

| 구분 | 항목 | 담당 | 상태 |
|---|---|---|---|
| W5 | Step 1~5 코드(결제·탈퇴·Telegram) | Claude | ✅ |
| W5 | Step 6 실 billing 검증 | 본인 | ⬜ (B-2·B-3·B-7) |
| W6 | 리포트·cron·multi-channel·gating·archive·**회고카드공유** | Claude | ✅ |
| W7 | thresholds·로컬알람·KPI 코드 | Claude | ✅ |
| A-1 | 릴리스 서명 코드화 | Claude | ⏸ (키스토어 후) |
| A-2 | 프론트엔드 CI(`frontend.yml`) | Claude | ⬜ (B-6과 함께) |
| W8 | 마케팅·data safety 코드 | Claude | ⬜ |
| W7 | 클로즈드 테스트 12명/14일 | 본인 | ⬜ ⏰⏰ |
| W8 | store listing·출시·launch | 본인 | ⬜ |
| 상시 | Play Console·신원확인·키스토어 | 본인 | ⬜ ⏰⏰ |
| 상시 | 인프라 계정·secrets·배포·CI | 본인 | ⬜ |
| 상시 | Mailgun·Telegram·Mixpanel·도메인 | 본인 | ⬜ |
| 상시 | 개인정보/약관 URL 호스팅 | 본인 | ⬜ |
| M3 | 사업자 등록 결정 | 본인 | ⬜ |

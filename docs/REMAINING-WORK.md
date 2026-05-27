# 끊기 — 남은 작업 & 본인 할 일 정리

> 2026-05-25 기준. **코드 작업(Claude가 가능)**과 **본인이 직접 해야 할 작업(외부 계정·심사·결제·실기기)**을 분리.
> 상세: [PRD §12](PRD.md) · [W5-prestart-P0](W5-prestart-P0.md) · [W5-build-plan](W5-build-plan.md)

---

## 0. 현황 한눈에

```
W0 기획   ✅   W1 설계   ✅   W2 백엔드 ✅   W3 프론트 ✅
W4 데이터 파이프라인 ✅   W5 코드(Step1~5) ✅ / Step6=본인
W6 ⬜ 리포트·결제연동·multi-channel   W7 ⬜ threshold·베타   W8 ⬜ 출시
```
- **코드로 끝낼 수 있는 것의 절반 이상 완료** (W2~W5 코드). 앱 기능 빌드는 W6에서 사실상 마무리.
- 남은 건 크게 ① W6~W7 코드 ② **본인의 외부 작업(Play Console·계정·배포·실기기·마케팅)**.

---

## A. 남은 코드 작업 (Claude가 진행 가능)

### A-1. W5 마무리 (코드 거의 없음)
- [ ] 릴리스 빌드 설정 코드화: `android/key.properties` 연결 + `build.gradle.kts` release signingConfig (키스토어는 본인 생성 → B-2)
- [ ] (선택) 구매 acknowledge를 **서버 검증 후**로 정교화 (현재 V1은 즉시 complete)

### A-2. W6 — AI 주간 리포트 + 운영 (코드 중심, 가장 큰 덩어리)
- [ ] **APScheduler** FastAPI 내장 (일요일 22:00 Asia/Seoul cron) + 외부 trigger fallback
- [ ] **AI 리포트 1-shot 파이프라인**: Anthropic SDK(Haiku) 직접 호출 → `weekly_reports` 저장 (GPT-5 mini fallback)
- [ ] **Active user filter SQL** (지난 7일 usage_events ≥1건 사용자만 — 비용·정책)
- [ ] **Multi-channel dispatch**: FCM 발송(firebase-admin) + **Mailgun 이메일**(코드) + Telegram(✅ Step1 send 완료) — 사용자 채널 선택대로
- [ ] **회고 카드 Flutter Canvas 렌더링** + 인스타 1-tap 공유
- [ ] **weekly_reports archive 화면** (회고 탭 실데이터 연결)
- [ ] **paywall gating 적용**: 리포트 매출환산·카테고리 한도 등 유료 기능에 `require_paid` 연결 (paywall UI는 ✅ W5 Step4)
- [ ] **hard-delete cron 등록** (W5 Step2 함수 완성됨 → APScheduler 일 1회 연결)
- [ ] **다음 달 파티션 자동 생성 cron** (매월 1일, usage_events)
- [ ] P4 V1.5 spike: 작업 시간대 heuristic (탐색)

### A-3. W7 — threshold + 베타 대응 (코드)
- [ ] **Threshold local detection**: Flutter 30분 polling + `flutter_local_notifications` 즉시 알람
- [ ] 카테고리별 일일 한도 설정 UI (설정 → 목표) + `/v1/thresholds` 연결
- [ ] **KPI metrics 수집 코드**: 권한 동의율·채널별 retention·D7/D30·NPS 이벤트(Mixpanel)
- [ ] 베타 피드백 반영 버그 수정 (베타 중)

### A-4. W8 — 출시 대응 (코드 일부)
- [ ] 마케팅/소개 페이지 (정적 또는 앱 내)
- [ ] KPI dashboard 연동 (Mixpanel 이벤트 정의)
- [ ] Play Store data safety 항목에 맞춘 코드 점검

---

## B. 본인이 해야 할 작업 (외부·계정·결제 — 코드로 못 함)

> ⏰ 표시는 **리드타임이 길어 일찍 시작해야 W8 출시 일정에 맞는 것**.

### B-1. ⏰⏰ Google Play 클로즈드 테스트 (출시 최대 blocker)
- [ ] 개인 계정은 프로덕션 전 **테스터 12명 × 14일 연속** opt-in 필요 (정책 재확인)
- [ ] 테스터 12명 확보: 품앗이 + 지인·가족 (회사 동료 X) — [W5-prestart A-1](W5-prestart-P0.md) 전략 참고
- [ ] **W7 베타 = 14일 시계 시작**으로 설계 → 그래서 Play Console 셋업은 지금(W5)

### B-2. ⏰ Google Play Console
- [ ] 가입 + 등록비 $25 + **신원 확인**(수일, 발각 risk 통제 — 개발자 표시명 본명 회피)
- [ ] 앱 생성: 패키지명 **`kr.kkeugi.kkeugi`**
- [ ] 릴리스 **키스토어 생성** + Play App Signing 등록
- [ ] **SHA-1 두 종류(업로드키 + Play 서명키)를 Google Cloud OAuth에 등록** (안 하면 내부테스트 빌드 Google 로그인 실패)
- [ ] 내부 테스트 트랙에 서명 AAB 업로드 → **그 후** 인앱상품 3종(`kkeugi.cert`/`monthly`/`yearly`) + 7일 trial offer 생성
- [ ] 라이선스 테스터(Gmail) 추가
- [ ] Store listing: 스크린샷·설명·아이콘·**Data safety** 작성

### B-3. ⏰ 영수증 검증용 서비스 계정 (Google Play Developer API)
- [ ] Google Cloud 서비스 계정 생성 + Play Console에 권한 연결
- [ ] JSON 키 발급 → 배포 secret `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON`

### B-4. Telegram (리드타임 낮음, 언제든)
- [ ] BotFather `/newbot` → `kkeugi_bot` 토큰 → `TELEGRAM_BOT_TOKEN` (실제 메시지 수신 검증 가능)
- [ ] 배포 후 Telegram 웹훅 등록 (`setWebhook` to `https://api.kkeugi.kr/webhooks/telegram` + secret)

### B-5. 이메일 (Mailgun) — W6 코드와 짝
- [ ] Mailgun 가입 + free tier + 발신 도메인(`mail.kkeugi.kr`) DNS(SPF/DKIM/MX)
- [ ] `MAILGUN_API_KEY` + `MAILGUN_DOMAIN`

### B-6. 인프라·배포 (W2-prestart에서 일부 시작했을 수 있음 — 확인)
- [ ] `.kr` 도메인(`api.kkeugi.kr`) 등록 (가비아/후이즈)
- [ ] Fly.io 가입 + 카드 + `FLY_API_TOKEN`(GitHub Actions secret) → 첫 배포
- [ ] Supabase 프로젝트(Seoul) → prod `DATABASE_URL`
- [ ] Google Cloud OAuth Client(Android + Web) → `GOOGLE_CLIENT_ID`
- [ ] Anthropic API key + Tier 1 prepay → `ANTHROPIC_API_KEY`
- [ ] Sentry(백엔드/프론트) DSN, Mixpanel 토큰

### B-7. 실기기 통합 검증 (W5 Step 6)
- [ ] 실기기에서 `--dart-define=USE_FAKE_BILLING=false` 빌드 → 라이선스 테스터 계정으로 실구매
- [ ] 구매 → 서버 `/verify`(RealGooglePlayVerifier) → entitlement → paywall 해제 확인
- [ ] 텔레그램 실제 연결(딥링크 → /start) + 회고 카드 수신

### B-8. 출시·운영 결정
- [ ] 클로즈드 베타 50명 모집 + 1-tap 공유 요청
- [ ] 공개 launch (긱뉴스·OKKY·X 빌드인퍼블릭)
- [ ] **사업자 등록 결정**: 월 net 매출 ₩35~50만 도달 시 (M3 hard checkpoint) → V2(Toss·카톡) 진입 path
- [ ] (출시 전) 개인정보처리방침·이용약관 **URL 호스팅** (`docs/legal/*.md` 작성됨, 위치만 결정)

---

## C. 의존 순서 (지금 → 출시)

```
[지금]  본인 B-2 Play Console 가입·신원확인 시작 (리드타임)  ┐
        Claude A-2 W6 코드 (리포트·multi-channel·gating)     ┤ 병행 가능
[그다음] 본인 B-6 인프라 secrets + 첫 배포 (Fly/Supabase)     ┘
        → Telegram 웹훅(B-4) / Mailgun(B-5) 실연동
[W7]    Claude A-3 threshold 코드  +  본인 B-1 클로즈드 테스트 14일 시작(베타)
        본인 B-7 실기기 billing 검증 (B-2 인앱상품·B-3 서비스계정 완료 후)
[W8]    본인 B-2 store listing + B-8 출시·launch
```

**핵심**: ① Play Console 신원확인·클로즈드 테스트는 리드타임이 기니 **지금 착수**. ② 그동안 Claude는 W6 코드를 배포 전 단계별 검증(W5 방식)으로 진행. ③ 실 billing·실 telegram·실 email은 계정/배포가 준비된 뒤 한 번에 통합 검증.

---

## D. 배포 시 등록할 Secrets (종합)

```bash
# Fly.io
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
#   FLY_API_TOKEN  (배포 게이트 — 미설정 시 배포 job skip)
```
- 릴리스 빌드: `--dart-define=USE_FAKE_BILLING=false --dart-define=API_BASE_URL=https://api.kkeugi.kr --dart-define=IS_PRODUCTION=true`
- 키스토어/SHA-1은 secret 아님 — **안전 보관**(분실 시 앱 업데이트 영구 불가)

---

## 한 눈 체크리스트

| 구분 | 항목 | 담당 | 상태 |
|---|---|---|---|
| W5 | Step 1~5 코드 | Claude | ✅ |
| W5 | Step 6 실 billing 검증 | 본인 | ⬜ (B-2·B-3·B-7) |
| W6 | 리포트·cron·multi-channel·gating | Claude | ⬜ |
| W7 | threshold·KPI 코드 | Claude | ⬜ |
| W7 | 클로즈드 테스트 12명/14일 | 본인 | ⬜ ⏰ |
| W8 | 마케팅·dashboard 코드 | Claude | ⬜ |
| W8 | store listing·출시·launch | 본인 | ⬜ |
| 상시 | Play Console·신원확인 | 본인 | ⬜ ⏰⏰ |
| 상시 | 인프라 계정·secrets·배포 | 본인 | ⬜ |
| 상시 | Mailgun·Telegram·도메인 | 본인 | ⬜ |
| 상시 | 개인정보/약관 URL 호스팅 | 본인 | ⬜ |
| M3 | 사업자 등록 결정 | 본인 | ⬜ |

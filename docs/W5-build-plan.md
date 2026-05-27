# W5 빌드 플랜 — "배포 전 단계별 검증"

> 목표: W5 코드(Billing·Telegram·회원탈퇴)를 **배포 전에 거의 전부 작성·검증**하고,
> 실제 Google Play Console 연결은 **마지막 단일 게이트(Step 6)**에서만 확인한다.
> 사전 계정 작업은 [W5-prestart-P0.md](W5-prestart-P0.md) 참조.

## 원칙: 외부 의존을 인터페이스 + Fake로 추상화

dev login이 Google Sign-In을 대체하듯, **`FakeBillingService`가 Google Play Billing을 대체**한다.
결제 "행위"만 Fake로 갈아끼우면 나머지 전 플로우(구매→서버검증→구독상태→paywall 해제→매출환산)는
지금 AVD에서 100% 검증 가능. dev 전용 경로는 `ENVIRONMENT=development/test` 가드(기존 dev login과 동일).

전환 스위치: `--dart-define=USE_FAKE_BILLING=true`(debug 기본) ↔ `false`(release).

## 빌드 순서 (각 단계 = 빌드 → 검증 게이트 → 다음)

| Step | 내용 | 배포 전 검증 | Play Console |
|---|---|---|---|
| **1. Telegram link** | 백엔드 link_token + `/webhooks/telegram` chat_id 바인딩 + send_message + Flutter 설정 연결 | pytest + 실제 봇(BotFather 무료)으로 메시지 수신 / webhook payload 시뮬레이트 curl | ❌ |
| **2. 회원 탈퇴/삭제** | `DELETE /v1/auth/account`(존재) 연결 + hard-delete cron + 설정 UX + 재로그인 차단 | pytest + AVD: 탈퇴→로그인 차단 | ❌ |
| **3. 결제 백엔드** | subscriptions + `/v1/payments/verify`(dev fake verifier) + `/subscription` + tier gating + dev-only `dev/grant` | pytest + 라이브 curl(dev grant→tier paid) | ❌ |
| **4. paywall + 결제 UI** | `BillingService` 인터페이스 + `FakeBillingService` + paywall 화면 + 구매 플로우 + 매출환산 unlock | AVD: Fake 구매→tier paid→paywall 해제 | ❌ |
| **5. RealBilling 구현** | `in_app_purchase` 어댑터 작성(코드 완성) + 서버 영수증 검증(Google Play Developer API) 코드 | analyze·compile. 동작은 Fake로 대체 검증 | ❌ (코드만) |
| **6. 실 Billing 게이트** | RealBilling 활성 + 서명 AAB + 내부테스트 업로드 + 라이선스 테스터 | 실기기에서 실제 구매→서버검증→tier | ✅ **유일** |

## 검증 방법 (W4와 동일 루틴)
- 백엔드: `make lint` + `make test`(pytest) + 라이브 `curl`
- 프론트: `flutter analyze` + AVD `flutter run` + 스크린샷
- 각 Step 종료 시 CLAUDE.md 변경 이력 1줄

## product ID (변경 불가 — 코드 상수와 Play Console 일치)
- `kkeugi.cert` (일회 ₩11,000) · `kkeugi.monthly` (월 ₩5,900) · `kkeugi.yearly` (연 ₩39,000) · 7일 free trial offer

## 진행 상태
- [x] **Step 1 — Telegram link** ✅ (2026-05-25)
  - 백엔드: `ChannelSubscription` 모델 + `/v1/me/telegram`(status·link_token·unsubscribe) + `/webhooks/telegram`(/start 바인딩·/stop) + `telegram/client.send_message`. pytest 9건.
  - 프론트: `telegram_api`·`telegram_provider` + 설정 카드 실상태 반영 + 토글→link_token→딥링크 실행.
  - 검증: pytest 30 green + 라이브(link_token→웹훅 /start→chat_id 바인딩→status linked) + AVD(토글→link_token 401→refresh→200→딥링크 launch→스낵바).
  - **배포 게이트만 남음**: 실 BotFather 토큰 + Telegram→공개 `/webhooks/telegram` 웹훅 등록(public URL 필요).
- [x] **Step 2 — 회원 탈퇴/데이터 삭제** ✅ (2026-05-25)
  - 백엔드: `DELETE /v1/me` 소프트 삭제(존재) + get_current_user·google·refresh·dev-login 모두 삭제계정 차단 + `users/cleanup.hard_delete_expired_accounts`(PIPA 30일 grace, usage_events 수동 삭제 + FK CASCADE). pytest 4건(soft delete·재로그인 차단·grace 보존·만료 cascade).
  - 프론트: 설정 회원 탈퇴 → 확인 다이얼로그(30일 grace 안내) → `deleteAccount`(soft delete + 토큰 clear + /login 리다이렉트).
  - 검증: 백엔드 pytest 34 green + **위젯 테스트 2건**(다이얼로그→탈퇴→deleteAccount 호출 / 취소→미호출). AVD는 다이얼로그 버튼 hit-test 미등록(Impeller 한계)으로 위젯 테스트로 확정 검증.
  - **배포 게이트**: hard-delete cron은 W6 APScheduler에서 일 1회 등록 예정(함수는 완성·테스트됨).
- [x] **Step 3 — 결제 백엔드** ✅ (2026-05-25)
  - `Subscription` 모델(subscriptions, GP Billing) + `products.py`(server-authoritative 카탈로그) + `verifier.py`(FakeVerifier dev/test, GooglePlayVerifier stub) + `entitlement.py`(get_active_subscription·require_paid 402) + `/v1/payments/verify`(gp_purchase_token 멱등)·`/v1/payments/subscription`.
  - 검증: pytest 8건(42 green) + 라이브(free→verify ₩11K→paid·tier one_time→멱등 1 row). 마이그레이션 불필요(001에 GP 컬럼 완비).
  - **배포 게이트**: prod GooglePlayVerifier 실구현은 Step 5(서버 영수증 검증).
- [x] **Step 4 — paywall + 결제 UI (Fake)** ✅ (2026-05-25)
  - `Env.useFakeBilling`(debug 기본 true) + `payment_api`(verify·subscription) + `billing_service`(BillingService 추상 + FakeBillingService 합성 토큰 + kCatalog) + `payments_providers`(entitlement·purchase) + `paywall_screen`(3플랜·기본 월구독·7일 trial·하단 CTA) + 설정 매출환산 행 entitlement 연결.
  - 검증: 위젯 테스트 2건(월구독→verify trial / 일회→verify cert) + AVD end-to-end(매출환산 잠김 → paywall → "7일 무료로 시작" → /verify 200 → entitlement paid → 매출환산 ON + 스낵바, DB monthly/in_trial).
- [x] **Step 5 — RealBilling 코드 완성** ✅ (2026-05-25)
  - 백엔드: `GooglePlayVerifier` 실구현(androidpublisher REST + 서비스계정 OAuth2, one_time=products.get·구독=subscriptionsv2.get) + config(GOOGLE_PLAY_PACKAGE_NAME·SERVICE_ACCOUNT_JSON). import·lint·42 test green.
  - 프론트: `in_app_purchase ^3.2.0` + `RealBillingService`(purchaseStream→Future 브리지) + billingServiceProvider를 `Env.useFakeBilling` 스위치로 연결.
  - 검증: analyze 0 + paywall 위젯테스트 green + **debug APK 빌드 성공**(in_app_purchase_android 통합 컴파일 확인). 실동작은 Step 6.
- [ ] Step 6 — 실 Billing 게이트 (배포 시 · Play Console 필요)

# W5 시작 전 P0 Checklist

> W5 = **Google Play Billing 인앱결제** + **Telegram Bot** + **회원 탈퇴/데이터 삭제 UX**.
> 이 중 **Google Play Console**은 프로젝트 전체에서 리드타임이 가장 길고 **W8 출시 일정을 좌우**한다.
> 코드보다 먼저 시작해야 하는 외부 계정·심사·키 작업을 여기 모은다.
> (W2-prestart-P0.md의 9·10·11·12 항목을 W5 관점에서 상세화 + 정정)

---

## ⏰ 가장 먼저 — 리드타임 경고 (오늘 시작해야 W8 출시 가능)

### A. Google Play 개인 계정 "클로즈드 테스트 의무" (W8 출시 최대 blocker) 🔴🔴
2023-11-13 이후 생성된 **개인(Individual) 개발자 계정**은 프로덕션 출시 신청 전:
- [ ] **테스터 12명 이상**이 **14일 연속** 클로즈드 테스트에 opt-in 한 기록 필요
  - (정책 수치는 변동 가능 — Play Console 최신 안내 재확인 필수)
- [ ] 즉, **W7 베타(50명) 시작 = 이 14일 시계 시작**으로 설계해야 W8 프로덕션 가능
- [ ] 테스터 12명 Gmail 주소를 W7 전에 미리 확보 (본인 follower·지인)
- **함의**: W5에 Play Console 셋업 + 내부 테스트 트랙 업로드까지 끝내야, W7에 클로즈드 테스트 14일을 돌릴 수 있다. 늦으면 W8 출시가 2주 밀린다.

#### A-1. 테스터 12명 확보 전략 (1인 개발자)
> 12명 = 서로 다른 Google 계정 12개가 opt-in + 14일 연속 유지. 활발한 사용 강제는 아니나, 프로덕션 승인이 재량적이라 실제 설치·약간 사용이 반려 risk를 낮춤.

- [ ] **① 테스터 품앗이 (표준 해법)** — 인디 개발자끼리 서로 테스터 되어주기
  - 카카오 오픈채팅 "구글 테스터 품앗이", OKKY, 디시 앱개발 갤, Reddit r/androiddev closed-testing 교환 스레드, Discord 교환 서버
- [ ] **② build-in-public 팔로워** — PRD §6 Phase 0a 베타 50명의 **부분집합**. 별도 노력 아님. 12명만 W5~W6로 당겨 14일 시계 조기 시작
- [ ] **③ 지인·가족** 5~6명 (기기 없어도 계정 opt-in 가능). ⚠️ **회사 동료·직무 네트워크 제외** (겸업 발각 risk, §11)
- [ ] **④ 본인 보조 계정 다수 = 비권장** (Google 탐지 강화 + 취지 위반 → 반려 risk). 보조로만
- [ ] **관리**: Google Groups 1개 생성 → 그룹을 테스터 목록으로 지정 (이메일 일괄 add/remove)
- **추천 조합**: 지인·가족 5~6 + 품앗이 6~7 = 12명 즉시 가능 → W5~W6 opt-in → W7 베타와 연결

### B. 개인 신원 확인 (identity verification)
- [ ] 개인 계정도 **신분증 기반 신원 확인** 요구 (D-U-N-S는 법인만 해당, 개인은 불필요)
- [ ] 처리: 보통 수 시간~수일. 반려 시 재제출 → 며칠 더
- [ ] **회사 겸업 발각 risk** (PRD §11 HIGH): Play Store 개발자 표시명·연락처가 공개됨
  - [ ] 개발자 표시명을 본명 강결합 회피 (예: 브랜드명 "끊기" 위주, 본인 식별 정보 최소)
  - [ ] 지원 이메일은 별도 주소 권장

---

## 🔴 W5 시작 전 즉시

### 1. Google Play Console Individual 가입
- [ ] [play.google.com/console](https://play.google.com/console) 가입
- [ ] Account type: **Individual** (사업자등록증 X — V1 전략 그대로)
- [ ] 등록비 **$25** (일회)
- [ ] 신원 확인 제출 (위 B)
- [ ] 결제 프로필(payments profile): 본인 명의 한국 통장 + tax 정보(주민번호)
  - Google Play Billing 활성 시 Merchant 연결 자동

### 2. 앱 생성 + applicationId 확정
- [ ] Play Console → 앱 만들기
- [ ] **패키지명 = `kr.kkeugi.kkeugi`** ⚠️ (W2 문서의 `kr.kkeugi`는 오기 — 실제 build.gradle.kts applicationId는 `kr.kkeugi.kkeugi`)
- [ ] 앱 이름: 끊기 (Kkeugi), 기본 언어: 한국어
- [ ] 무료/유료: **무료**(인앱결제로 수익화하므로 앱 자체는 무료)

### 3. 릴리스 키스토어 + Play App Signing
- [ ] 업로드 키스토어 생성:
  ```bash
  keytool -genkey -v -keystore ~/kkeugi-upload.jks \
    -keyalg RSA -keysize 2048 -validity 10000 -alias upload
  ```
  - 비밀번호·alias 안전한 곳 저장 (분실 시 업데이트 불가)
- [ ] `android/key.properties` + build.gradle.kts release signingConfig 연결 (W5 코드 작업)
- [ ] Play App Signing 등록 (Play Console가 앱 서명 키 관리)
- [ ] **SHA-1 / SHA-256 두 종류 모두** Google Cloud OAuth(W2 #4)에 등록:
  - 업로드 키 SHA-1 (`keytool -list -v -keystore ~/kkeugi-upload.jks`)
  - **Play 앱 서명 키 SHA-1** (Play Console → 앱 무결성 → 앱 서명에서 복사)
  - ⚠️ 둘 다 등록 안 하면 **내부테스트/프로덕션 빌드에서 Google Sign-In 실패** (dev debug keystore SHA-1만으론 부족)

### 4. 내부 테스트 트랙에 첫 AAB 업로드 (인앱상품 생성 선결조건)
- [ ] release AAB 빌드: `flutter build appbundle --dart-define=...`
  - `com.android.vending.BILLING` 권한 포함 (in_app_purchase 플러그인이 자동 추가)
- [ ] Play Console → 내부 테스트 → AAB 업로드
- [ ] ⚠️ **인앱상품은 BILLING 권한이 있는 AAB가 한 번 업로드된 뒤에만 생성 가능** (순서 의존)
- [ ] 내부 테스트 트랙에 테스터(본인 + 라이선스 테스터) 추가

### 5. 인앱상품 3종 생성 (W5 코드와 병행)
- [ ] **`kkeugi.cert`** — 관리형 상품(one-time, non-consumable) **₩11,000** (일회 인증서)
- [ ] **`kkeugi.monthly`** — 구독, base plan 월 **₩5,900**
- [ ] **`kkeugi.yearly`** — 구독, base plan 연 **₩39,000**
- [ ] **7일 무료 체험** = 구독 상품의 **offer(free trial)**로 설정 (월·연 각각)
- [ ] product ID는 코드 상수와 일치 확인 (변경 불가하므로 신중)

### 6. 라이선스 테스트 계정 (무료 테스트 결제)
- [ ] Play Console → 설정 → 라이선스 테스트 → 테스터 Gmail 추가
- [ ] 이 계정으로 로그인한 기기/에뮬레이터에서 **실제 청구 없이** 결제 플로우 테스트
- [ ] ⚠️ **현재 AVD(pixel7)는 Google 계정 미설정** → Billing 테스트하려면:
  - (a) AVD에 라이선스 테스터 Google 계정 로그인, 또는
  - (b) **실기기**(권장 — 가장 확실)

### 7. Telegram Bot 생성 (리드타임 낮음, 언제든)
- [ ] Telegram에서 `@BotFather` → `/newbot`
  - 이름: "끊기" / username: `kkeugi_bot` (사용 가능 여부 확인)
- [ ] API token 발급 → `TELEGRAM_BOT_TOKEN` secret
- [ ] `/setdescription` 한국어 설정
- [ ] `/setcommands`:
  - `start` — 주간 회고 알림 받기 시작
  - `stop` — 알림 끄기
  - `help` — 도움말
- [ ] 연동 방식 확정: 봇이 deep-link(`https://t.me/kkeugi_bot?start=<link_token>`)로 chat_id 회수 → `/v1/me/telegram_link`

---

## 🟢 W5 중 결정 사항 (코드 시작 시)

### 8. Flutter Billing 패키지 결정
- [ ] **`in_app_purchase`** (Flutter 공식, Google 직접) ← V1 권장. 추가 수수료 0
- [ ] 대안 `purchases_flutter`(RevenueCat): 구독 상태관리 편하지만 매출 1% 추가 수수료 → V1 마진 고려 시 보류
- [ ] 서버 검증: 구매 영수증(purchase token)을 백엔드로 보내 **Google Play Developer API**로 검증 후 `subscriptions` 테이블 기록 (ARCHITECTURE subscriptions 스키마 활용)
- [ ] Google Play Developer API 접근용 **서비스 계정** 생성 + Play Console 권한 연결 (서버 영수증 검증에 필요)

### 9. 회원 탈퇴 / 데이터 삭제 UX (PIPA)
- [ ] 백엔드 `DELETE /v1/auth/account` 이미 스펙 존재 (soft delete) → UX 연결
- [ ] PIPA 30일 grace 후 hard delete cron
- [ ] Play Store 데이터 안전 섹션(Data safety) 작성 — 출시 전 필수

---

## 📋 발급받을 IDs / Secrets (이번 단계 추가분)

```bash
# 백엔드 (Fly.io secrets)
fly secrets set \
  TELEGRAM_BOT_TOKEN="..." \
  GOOGLE_PLAY_SERVICE_ACCOUNT_JSON="$(cat play-service-account.json)"

# Flutter 코드 상수 (변경 불가 — 신중)
#   PRODUCT_CERT    = kkeugi.cert
#   PRODUCT_MONTHLY = kkeugi.monthly
#   PRODUCT_YEARLY  = kkeugi.yearly
```

키스토어/SHA-1은 secret이 아닌 **안전 보관**(분실 시 앱 업데이트 영구 불가):
- `~/kkeugi-upload.jks` + 비밀번호 + alias
- Play 앱 서명 키 SHA-1 (Play Console에서 조회 가능)

---

## 📋 Status tracker

| 항목 | 시작 | 완료 | 비고 |
|---|---|---|---|
| A. 클로즈드 테스트 12명/14일 계획 | | | W7 베타 = 시계 시작 |
| B. 신원 확인 제출 | | | 수일 소요, 발각 risk 통제 |
| 1. Play Console Individual 가입 ($25) | | | |
| 2. 앱 생성 (`kr.kkeugi.kkeugi`) | | | 패키지명 정정 |
| 3. 릴리스 키스토어 + App Signing + SHA-1 OAuth 등록 | | | Google Sign-In 연동 |
| 4. 내부 테스트 AAB 업로드 | | | 인앱상품 선결 |
| 5. 인앱상품 3종 + 7일 trial | | | |
| 6. 라이선스 테스터 + 테스트 기기 | | | 실기기 권장 |
| 7. Telegram Bot | | | 리드타임 낮음 |
| 8. in_app_purchase + 서버 검증 서비스계정 | | | |
| 9. 회원 탈퇴 UX + Data safety | | | PIPA |

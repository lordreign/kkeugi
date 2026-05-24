# W3 Frontend Spec

> Flutter scaffolding + 핵심 widget + auth flow + 온보딩 5단계 skeleton.
> 본인 Flutter 설치 후 즉시 시작 가능한 구조.

## 사전 요구
- Flutter SDK 3.24+ (`brew install --cask flutter`)
- Android Studio (AVD) 또는 실디바이스
- `flutter doctor` 통과

## 시작

```bash
cd frontend

# Flutter project 초기화 (기존 lib/·pubspec.yaml 보존)
flutter create . \
  --org kr.kkeugi \
  --project-name kkeugi \
  --platforms=android \
  --android-language=kotlin

# 의존성 설치
flutter pub get

# Backend 실행 (별도 터미널)
cd ../backend && make run

# AVD 실행 (Android Studio Device Manager)
# Flutter run
cd ../frontend
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8080
```

## 작성된 파일 (현재 상태)

```
frontend/
├── pubspec.yaml                              ✓ 의존성 목록
├── README.md                                 ✓ setup 가이드
├── analysis_options.yaml                     ✓ Dart lints
├── .gitignore                                ✓ Flutter standard
├── lib/
│   ├── main.dart                             ✓ App entry + Sentry init
│   ├── app.dart                              ✓ MaterialApp + bottom nav 3개
│   ├── theme/
│   │   ├── colors.dart                       ✓ DESIGN.md tokens
│   │   ├── typography.dart                   ✓ Pretendard + IBM Plex Mono
│   │   ├── spacing.dart                      ✓ 4px scale
│   │   └── theme.dart                        ✓ ThemeData Material 3
│   ├── core/
│   │   ├── api/
│   │   │   ├── env.dart                      ✓ API_BASE_URL dart-define
│   │   │   ├── api_client.dart               ✓ Dio + interceptor
│   │   │   └── auth_interceptor.dart         ✓ JWT attach + 401 refresh
│   │   └── storage/
│   │       └── secure_storage.dart           ✓ JWT secure storage
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/auth_api.dart            ✓ /v1/auth/google·dev/login·logout
│   │   │   └── presentation/login_screen.dart ✓ "Google로 시작" CTA + dev login (debug only)
│   │   └── home/
│   │       └── home_screen.dart              ✓ Hero numeral + 4 카테고리 skeleton
│   └── shared/widgets/
│       └── hero_numeral.dart                 ✓ DESIGN.md signature widget
└── test/widget_test.dart                     ✓ LoginScreen + HeroNumeral basic test
```

## 미작성 (W3.5 또는 W4)

### W3.5 (Flutter 설치 후 빠르게 추가):
- `lib/core/local_db/` — Drift schema + DAO
- `lib/features/auth/presentation/auth_provider.dart` — Riverpod StateNotifier
- `lib/features/onboarding/` — 5단계 (step1-5)
- `lib/features/archive/` — 무한 스크롤 카드 list
- `lib/features/settings/` — 6 섹션 (가치·시간대·채널·목표·개인정보·앱)
- `lib/features/channel/` — ChannelToggleCard + link flow
- `lib/core/fcm/` — firebase_messaging 통합 + /v1/fcm/register
- go_router 도입 (현재 StatefulWidget 임시)
- Sentry test event

### W4 (UsageStatsManager):
- `lib/core/platform_channel/usage_stats.dart` — MethodChannel
- `android/app/src/main/kotlin/kr/kkeugi/UsageStatsBridge.kt`
- 권한 요청 UX (PACKAGE_USAGE_STATS Settings 이동)
- 8h WorkManager background sync

### W5:
- Google Play Billing 통합 (in_app_purchase package)
- 가격 plan 3종 product 등록 (Console에서)
- Telegram Bot link flow
- 회원 탈퇴 UX

### W6:
- AI weekly report 카드 widget (편지 톤)
- Paywall modal (D7 trigger + 매출 환산 toggle 진입 시)

### W7:
- Threshold local detection (Flutter 30분 polling)
- flutter_local_notifications 즉시 알람
- 베타 50명 promo code 입력 UX

## Backend 연결 흐름 (현재 작동 가능)

```
LoginScreen → onDevLogin() tap
  → POST http://10.0.2.2:8080/v1/auth/dev/login {email, name}
  → TokenPairResponse 받음
  → SecureStorage.saveTokens(access, refresh)
  → HomeShell로 전환 (bottom nav 3개)
```

현재 LoginScreen은 mock state (auth 실제 호출 없음). W3.5에서 Riverpod AuthProvider 추가 시 실제 backend 호출 연결.

## DESIGN.md 일관성 check

```
✓ Pretendard + IBM Plex Mono (typography.dart)
✓ Clay #8B5A3C accent (colors.dart)
✓ 4px spacing scale (spacing.dart)
✓ Material 3 + light only V1 (theme.dart)
✓ Hero numeral signature widget (hero_numeral.dart)
✓ Bottom tab 3개 (app.dart)
✓ "Google로 시작" 단일 CTA (login_screen.dart)
✓ Quiet motion (page transition fade only, no spring)
✓ Card shadow 0, divider 1px
✓ Bubble radius 금지 (4·8·12 limit)
```

## 가장 critical missing — W3.5 priority

1. **Auth Riverpod provider + 실제 backend 호출 연결** (1일)
2. **온보딩 5단계 PageView** (2일)
3. **Drift local DB** (1일)
4. **go_router** (0.5일)
5. **Settings 6 섹션** (1일)

Total W3.5: ~5.5일 part-time.

## 검증 방법

```bash
flutter analyze  # lint 통과 확인
flutter test     # widget_test.dart 통과
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8080
# AVD에서:
#   1. "Google로 시작" 보임
#   2. (debug build) "Dev Login" 버튼 보임
#   3. tap → HomeShell로 전환
#   4. bottom tab 3개 (홈·회고·설정) 전환 동작
#   5. 홈 화면: +47분 hero numeral + 4 카테고리 breakdown
```

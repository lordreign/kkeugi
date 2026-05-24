# Kkeugi Frontend (Flutter Android)

Material 3 + Pretendard + IBM Plex Mono + Drift + Riverpod + Google Sign-In.

## Pre-requisites (Flutter 미설치 시)

```bash
# macOS
brew install --cask flutter
brew install --cask android-studio

# Flutter doctor 통과 확인
flutter doctor
# Android toolchain - Java 17+ + Android SDK 34+
# Android Studio
# Connected device (USB 또는 AVD)
```

## First-time setup

```bash
cd frontend

# Flutter project 초기화 (기존 lib/·android/ 보존)
flutter create . \
  --org kr.kkeugi \
  --project-name kkeugi \
  --platforms=android \
  --android-language=kotlin \
  --description="끊기 - 한국 1인 워커 디지털 디톡스"

# 의존성 설치
flutter pub get

# DRift code generation (W3 단계)
dart run build_runner build --delete-conflicting-outputs

# 로컬 backend 실행 (별도 터미널)
cd ../backend && make run

# Flutter 실행 (AVD 또는 실디바이스)
cd ../frontend
flutter run
```

## Project structure (W3 spec)

```
frontend/
├── pubspec.yaml                    # dependencies (이미 작성됨)
├── README.md                       # 이 파일
├── analysis_options.yaml           # Dart lints
├── .gitignore                      # Flutter standard
├── android/                        # flutter create로 생성됨
│   └── app/src/main/kotlin/kr/kkeugi/   # UsageStatsBridge.kt (W4)
├── lib/
│   ├── main.dart                   # App entry + Riverpod ProviderScope
│   ├── app.dart                    # MaterialApp + theme + routing
│   ├── theme/
│   │   ├── colors.dart             # DESIGN.md tokens (clay #8B5A3C, ivory #FAFAF7 등)
│   │   ├── typography.dart         # Pretendard + IBM Plex Mono TextTheme
│   │   ├── spacing.dart            # 4px base scale (xs·sm·md·lg·xl·2xl)
│   │   └── theme.dart              # ThemeData 통합 (Material 3 + Pretendard 적용)
│   ├── core/
│   │   ├── api/
│   │   │   ├── api_client.dart     # dio + base URL + interceptors
│   │   │   ├── auth_interceptor.dart  # JWT attach + 401 refresh
│   │   │   ├── api_exception.dart  # 통일 에러 매핑
│   │   │   └── env.dart            # API_BASE_URL (dev/prod)
│   │   ├── local_db/
│   │   │   ├── app_database.dart   # Drift @DriftDatabase
│   │   │   ├── tables/
│   │   │   │   ├── local_settings.dart    # JWT secure storage 보완
│   │   │   │   ├── local_usage_events.dart  # client_event_id 기반
│   │   │   │   ├── local_thresholds.dart
│   │   │   │   └── local_weekly_reports.dart  # archive cache
│   │   │   └── dao/                # CRUD layer
│   │   ├── fcm/
│   │   │   ├── fcm_service.dart    # firebase_messaging wrap
│   │   │   └── fcm_register.dart   # /v1/fcm/register 호출
│   │   ├── platform_channel/
│   │   │   └── usage_stats.dart    # MethodChannel (W4 실제 구현)
│   │   ├── error/
│   │   │   └── sentry_init.dart    # sentry_flutter
│   │   └── storage/
│   │       └── secure_storage.dart  # flutter_secure_storage (JWT 보관)
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   │   ├── auth_api.dart   # /v1/auth/google · /refresh · /logout
│   │   │   │   └── auth_dev_api.dart  # /v1/auth/dev/login (dev only)
│   │   │   ├── domain/
│   │   │   │   ├── user.dart       # User model (freezed)
│   │   │   │   └── token_pair.dart
│   │   │   └── presentation/
│   │   │       ├── login_screen.dart    # "Google로 시작" 단일 CTA
│   │   │       ├── auth_provider.dart   # Riverpod StateNotifier
│   │   │       └── auth_state.dart
│   │   ├── onboarding/
│   │   │   ├── onboarding_flow.dart       # 5단계 PageView
│   │   │   ├── step1_reason.dart          # "이유" — 관찰 중립 톤
│   │   │   ├── step2_permission.dart      # PACKAGE_USAGE_STATS Settings 이동
│   │   │   ├── step3_shock.dart           # 어제 사용 시간 reveal
│   │   │   ├── step4_hourly_value.dart    # 시간당 가치 입력 (skip 가능)
│   │   │   └── step5_channel_select.dart  # FCM 강제 + 이메일·Telegram 옵션
│   │   ├── home/
│   │   │   ├── home_screen.dart           # hero numeral +N분 + 4 카테고리
│   │   │   ├── today_usage_card.dart      # 4종 프리셋 breakdown
│   │   │   └── home_provider.dart
│   │   ├── archive/
│   │   │   ├── archive_screen.dart        # 무한 스크롤 카드 list
│   │   │   ├── weekly_card.dart           # 회고 카드 widget
│   │   │   └── archive_provider.dart
│   │   ├── settings/
│   │   │   ├── settings_screen.dart       # 6 섹션 (가치·시간대·채널·목표·개인정보·앱)
│   │   │   ├── hourly_value_section.dart
│   │   │   ├── work_hours_section.dart
│   │   │   ├── channel_management.dart    # FCM·Email·Telegram toggle
│   │   │   ├── threshold_setup.dart       # 4 카테고리별 슬라이더
│   │   │   ├── privacy_section.dart       # PIPA + 회원 탈퇴
│   │   │   └── app_info.dart
│   │   └── channel/
│   │       ├── channel_toggle_card.dart   # DESIGN.md ChannelToggleCard widget
│   │       └── channel_link_flow.dart     # 이메일·Telegram link UX
│   └── shared/
│       ├── widgets/
│       │   ├── hero_numeral.dart   # IBM Plex Mono 64-80sp, tabular nums
│       │   ├── primary_button.dart
│       │   ├── text_only_cta.dart  # clay accent text-only
│       │   ├── card_container.dart # DESIGN.md surface + divider
│       │   └── reflection_card.dart # 주간 리포트 카드 (편지 톤)
│       └── utils/
│           ├── time_formatter.dart  # "+47분", "₩68,250" 표시
│           └── debt_calculator.dart # 시간 빚 / 매출 환산 계산
├── test/                           # unit tests
│   ├── theme/
│   ├── core/
│   └── features/
└── integration_test/               # end-to-end
    └── onboarding_test.dart
```

## W3 작업 list (Flutter 설치 후)

```
[1] Flutter 프로젝트 초기화
    □ flutter create . --org kr.kkeugi (현 dir에)
    □ pubspec.yaml dependencies 적용 (이미 작성됨)
    □ flutter pub get

[2] Theme (DESIGN.md tokens)
    □ lib/theme/colors.dart — clay #8B5A3C 등
    □ lib/theme/typography.dart — Pretendard + IBM Plex Mono
    □ lib/theme/spacing.dart — 4px base
    □ lib/theme/theme.dart — ThemeData(useMaterial3: true)
    □ Pretendard ttf bundle (assets/fonts/) 또는 pretendard pub package
    □ IBM Plex Mono: google_fonts package

[3] Routing (go_router)
    □ /                → splash → 인증 확인 → login or home
    □ /login           → LoginScreen
    □ /onboarding      → OnboardingFlow (5단계 PageView)
    □ /home            → HomeScreen (bottom tab 0)
    □ /archive         → ArchiveScreen (bottom tab 1)
    □ /settings        → SettingsScreen (bottom tab 2)
    □ /paywall (modal) → W6 paywall (D7 trigger)

[4] API client (dio + JWT interceptor)
    □ ApiClient.dart with base URL env
    □ AuthInterceptor — JWT attach + 401 → /v1/auth/refresh → retry
    □ Refresh fail → secure_storage clear → /login redirect

[5] Drift local DB
    □ AppDatabase + 4 tables
    □ build_runner code gen
    □ DAO layer

[6] Auth feature
    □ Google Sign-In flow (google_sign_in package, V1.5 활성)
    □ V1 dev fallback: /v1/auth/dev/login 호출 옵션 (개발 빌드)
    □ JWT secure_storage 저장 (access + refresh)
    □ Riverpod AuthProvider (StateNotifier)

[7] 온보딩 5단계 (P5)
    □ step1: "사용 패턴을 분석해 집중력이 흩어지는 시간대를 찾아드려요" 카피
    □ step2: PACKAGE_USAGE_STATS 권한 안내 (실제 권한 요청은 W4)
    □ step3: 어제 사용 시간 shock (데이터 없으면 fallback 카피)
    □ step4: 시간당 가치 ₩30K default + skip
    □ step5: 채널 multi-select (FCM 강제 + 이메일·Telegram opt-in)

[8] 4종 프리셋 + FCM
    □ home_screen.dart skeleton (hero numeral + 4 카테고리)
    □ Firebase Remote Config (웹툰 패키지 list 동적)
    □ firebase_messaging 토큰 등록 + /v1/fcm/register

[9] Shared widgets
    □ HeroNumeral (IBM Plex Mono 64-80sp, tabular nums)
    □ PrimaryButton, TextOnlyCTA, CardContainer
    □ ReflectionCard (편지 톤)

[10] Tests
    □ widget test (theme tokens 적용 확인)
    □ integration_test (login → onboarding → home flow)
```

## W4-W8 미리 알 것 (W3에는 미구현)

- W4: lib/core/platform_channel/usage_stats.dart 실구현 + Kotlin UsageStatsBridge
- W5: Google Play Billing 통합 (in_app_purchase package)
- W6: AI 리포트 카드 + paywall UI
- W7: Threshold local detection + flutter_local_notifications

## DESIGN.md tokens → Flutter ThemeData

```dart
// lib/theme/colors.dart
const colorBg = Color(0xFFFAFAF7);
const colorSurface = Color(0xFFFFFFFF);
const colorTextPrimary = Color(0xFF1A1A1A);
const colorTextSecondary = Color(0xFF8A8A85);
const colorAccent = Color(0xFF8B5A3C);  // clay
const colorDivider = Color(0xFFE8E5DE);

// lib/theme/typography.dart
final textTheme = TextTheme(
  displayLarge: TextStyle(
    fontFamily: 'Pretendard',
    fontWeight: FontWeight.w700,
    fontSize: 56,
    letterSpacing: -1.68,
    height: 1.0,
  ),
  headlineMedium: TextStyle(
    fontFamily: 'Pretendard',
    fontWeight: FontWeight.w600,
    fontSize: 28,
    letterSpacing: -0.56,
  ),
  bodyLarge: TextStyle(
    fontFamily: 'Pretendard',
    fontWeight: FontWeight.w400,
    fontSize: 16,
    height: 1.6,
  ),
);

// HeroNumeral widget — IBM Plex Mono
Text(
  '+47',
  style: GoogleFonts.ibmPlexMono(
    fontWeight: FontWeight.w600,
    fontSize: 72,
    letterSpacing: -2.88,
    fontFeatures: const [FontFeature.tabularFigures()],
  ),
)
```

## Local dev — backend 연결

```bash
# 1. backend 실행 (다른 터미널)
cd ../backend && make run

# 2. frontend의 .env 또는 dart-define으로 API_BASE_URL 설정
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8080  # Android AVD에서 localhost
# 실디바이스: --dart-define=API_BASE_URL=http://192.168.x.x:8080 (PC IP)

# 3. Dev login (Google OAuth setup 없이)
# LoginScreen에서 "Dev Login" 버튼 (development build에만 노출) tap
```

## Status (W3 완료 — 2026-05-24, Flutter 3.44 검증)

```
✅ flutter create 완료 (android/ 생성, package kr.kkeugi.kkeugi)
✅ flutter pub get 성공 (70 packages)
✅ flutter analyze — 에러 0 (info-level lint 8개만)
✅ flutter test — 2/2 통과 (LoginScreen·HeroNumeral)
✅ flutter build apk --debug — app-debug.apk (169MB) 빌드 성공
✅ Pretendard otf bundle (assets/fonts/) — pub package 대신
✅ Theme·Auth·Home·HeroNumeral·bottom nav 동작
```

### W3 setup 중 해결된 build issue 4개

```
1. pretendard pub package 없음
   → assets/fonts/Pretendard-{Regular,Medium,SemiBold,Bold}.otf bundle
   → pubspec.yaml fonts: 섹션 + theme.dart fontFamily: 'Pretendard'

2. intl ^0.19.0 충돌 (flutter_localizations가 0.20.2 pin)
   → intl ^0.20.2로 변경

3. sentry_flutter 8.x Kotlin 1.6 incompatibility (Flutter 3.44 toolchain)
   → sentry_flutter ^9.0.0로 upgrade

4. flutter_local_notifications core library desugaring 필요
   → android/app/build.gradle.kts:
     isCoreLibraryDesugaringEnabled = true
     minSdk = maxOf(flutter.minSdkVersion, 23)
     coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")
```

### 실행

```bash
# Android emulator 생성 (없으면)
flutter emulators --create --name pixel
flutter emulators --launch pixel

# 또는 실디바이스 USB 연결

# Backend 실행 (별도 터미널)
cd ../backend && make run

# Frontend 실행
cd frontend
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8080
```

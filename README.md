# 끊기 (Kkeugi)

> 한국 1인 워커(개발자·디자이너·작가·연구자·프리·1인 사업자)를 위한 디지털 디톡스 Android 앱 (Flutter).
> SNS·쇼츠·게임·웹툰 끊기 타이머 + UsageStatsManager 자동 import + AI 주간 "시간 빚 환산" 리포트 + **multi-channel retention** (FCM + 이메일 + Telegram).
> **V1 = Google Play 인앱결제** (사업자 X 가능): Hybrid 일회 ₩11K + 월 ₩5.9K + 연 ₩39K + 7일 free trial + 베타 50% + 출시 7일 30%.
> 사업자 등록 trigger = **월 net 매출 ₩35-50만 도달**. V2 (사업자 후) = Toss·카톡 추가.

**PRD**: [`docs/PRD.md`](docs/PRD.md) (원본: `find_business/docs/candidates/b2c_mobile_app/deepdive/2026-05-18-kkeugi-habit-stop-timer.md`)

## 한눈에

| | |
|---|---|
| **점수** | 82.5 / verdict pass / **GO (V1 무료 도구)** |
| **V1 자본** | 약 ₩10만 (Google Play $25 + .kr 도메인 + 예비) |
| **V1 MVP** | 8주 full-time 또는 12-16주 part-time (본업 유지) |
| **V1 수익** | Google Play 인앱결제: 일회 ₩11K + 월 ₩5.9K + 연 ₩39K + 7일 free trial |
| **사업자 trigger** | 월 net 매출 ₩35-50만 도달 시 |
| **V2 수익 (사업자 후)** | Toss 외부결제 (수수료 30%→3.3%) + 카톡 알림톡 |
| **Phase 1 채널** | X 한국 인디 메이커 + 긱뉴스 + okky + 노션 한국 커뮤니티 (V1 무료라 viral easier) |
| **iOS** | V2 격하 |

## 기술 스택

- **앱**: Flutter 3.x (Dart) + Material 3 + Riverpod + Drift (SQLite offline) — Android 단일 시드
- **OS 데이터**: Flutter platform channel → Kotlin → `UsageStatsManager` (PACKAGE_USAGE_STATS)
- **백엔드**: **FastAPI (Python) on Fly.io seoul** + **PostgreSQL on Supabase Free** + JWT + Kakao OAuth + APScheduler cron (2026-05-23 pivot from Firebase)
- **푸시**: Firebase project FCM only (Firestore·Auth 미사용)
- **LLM**: Claude Haiku 3.5 (primary) + GPT-5 mini (fallback) — Anthropic SDK from FastAPI
- **결제**: Toss Payments 앱 SDK (외부 결제, 인앱결제 우회) — 일회 + 구독 빌링키
- **카톡**: 카카오 비즈메시지 알림톡 정보성 — Aligo / SOLAPI / DirectSend (FastAPI 직접 호출)
- **모니터링**: Sentry free tier + Mixpanel free

## 8주 빌드 + gstack 매핑

| 주차 | 빌드 | gstack |
|---|---|---|
| W0 | 레포 init (이 단계) + Flutter SDK 설치 + Android Studio + Firebase project | `/setup-gbrain` · `/setup-deploy` · **`/office-hours`** (PRD 디테일 발산) |
| W1 | Flutter 학습 + Figma wireframe 5화면 + Firestore 스키마 | **`/design-consultation`** → DESIGN.md · **`/plan-design-review`** · **`/plan-eng-review`** |
| W2 | Firebase 연동 + 카카오 OAuth + 온보딩 + 시간당 가치 입력 | `/investigate` · `/review` |
| W3 | 타이머 화면 + 행동 3종 + FCM schedule | `/investigate` |
| W4 | Platform channel → Kotlin → UsageStatsManager + 동의 UX | **`/codex` consult** · **`/cso`** (권한 보안) |
| W5 | Toss Payments + 환불 정책 | **`/cso`** (결제 위협 모델) · `/review` |
| W6 | AI 주간 리포트 (Cloud Functions + Claude Haiku) + 카드 렌더링 + 1-tap 공유 | **`/codex`** (프롬프트 검증) · `/review` |
| W7 | 카카오 채널 + 알림톡 + cron + 클로즈드 베타 50명 | **`/qa`** · **`/design-review`** + 법무 자문 ₩30~50만 |
| W8 | Play Store 출시 ($25) + 결제 funnel + KPI dashboard | **`/ship`** · **`/land-and-deploy`** · **`/canary`** |
| W9+ | 운영·반복 | `/retro` 주간 · `/document-release` · `/devex-review` (랜딩·결제 funnel) |

## 다음 단계 (현재 W0)

1. Flutter SDK 설치 — `brew install --cask flutter` 또는 [공식 가이드](https://docs.flutter.dev/get-started/install/macos)
2. Android Studio 설치 + Flutter plugin
3. `flutter doctor` 통과 확인
4. `flutter create kkeugi --org kr.kkeugi --platforms=android` (이 디렉토리 안에서)
5. Firebase project 생성 + `flutterfire configure`
6. `/office-hours` 호출 → PRD에 빠진 UX·매출 환산 계산식 디테일 발산
7. `/design-consultation` 호출 → DESIGN.md 생성
8. `/plan-eng-review` 호출 → 아키텍처 확정

## 핵심 결정 사항 (변경 시 PRD에 기록)

- **Flutter 채택 (Android 단일 시드)**: 2026-05-21. iOS v2 격하. persona.md 갱신 (RN+Expo 제거, Flutter "중" 본격 전환).
- **UsageStatsManager 직접 접근**: PWA 단독 불가, Flutter platform channel → Kotlin native.
- **Toss 외부 결제**: Google Play Billing 30% 우회 (한국 인앱결제법 2022 시행). 가격 ₩9,900 / ₩4,900 유지.
- **카톡 알림톡 정보성만**: 2026.1.1 정책 준수. 마일리지·쿠폰·할인 메시지 0. 친구톡 2025.12.31 종료 — 사용 X.
- **본인이 ICP**: 1인 워커. 콘텐츠·UX 추측 0.

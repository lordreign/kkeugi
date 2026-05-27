# 끊기 (Kkeugi) — 프로젝트 컨텍스트

> Claude Code / gstack 의 모든 에이전트가 이 파일을 읽고 컨텍스트를 잡는다.

## 한 줄 정의 (2026-05-24 V1 인앱결제 paid product)

한국 1인 워커를 위한 디지털 디톡스 Android 앱 (Flutter). SNS·쇼츠·게임·웹툰 끊기 타이머 + UsageStatsManager 자동 import + AI 주간 "시간 빚 환산" 리포트 + **multi-channel retention** (FCM + 이메일 + Telegram). **V1 = Google Play Billing 인앱결제** (Hybrid 일회 ₩11K + 월 ₩5.9K + 연 ₩39K + 7일 free trial, 사업자 X 가능). **사업자 등록 trigger = 월 net 매출 ₩35-50만 도달**. **V2 (사업자 등록 후) = Toss + 카톡 추가**.

## 핵심 정보

| | |
|---|---|
| **ICP** | 한국 1인 워커 (개발자·디자이너·작가·연구자·프리·1인 사업자) — 본인이 곧 ICP |
| **wedge 3개 (V1)** | (1) 시간 빚 환산 AI 리포트, (2) UsageStatsManager 자동 import, (3) **multi-channel retention** (FCM + 이메일 + Telegram, 사용자 선택) |
| **플랫폼** | Android 네이티브 (Flutter) 단일 시드. iOS는 V2 |
| **V1 수익** | **Google Play 인앱결제** (사업자 X): 일회 ₩11K + 월 ₩5.9K + 연 ₩39K + 7일 free trial + 베타 50% + 출시 7일 30% |
| **사업자 trigger** | 월 net 매출 ₩35-50만 고정 도달 시 사업자 등록 결정 |
| **V2 수익 (사업자 후)** | Toss 외부결제 (수수료 30%→3.3%) + 카톡 알림톡 추가 |
| **V1 자본** | 약 ₩10만 (Google Play Console $25 + .kr 도메인 + 예비) |
| **MVP** | 8주 full-time 또는 12-16주 part-time (본업 유지) |
| **GO/NO-GO** | **GO** (2026-05-24 V1 인앱결제 paid re-pivot 확정) |

## 빌드 단계 (W0 = 지금)

상세 매핑은 [README.md](README.md) 참조.

- **W0 (지금)**: 레포 init + Flutter SDK 설치 + Firebase project + `/office-hours` (PRD 발산)
- **W1**: Flutter 학습 + Figma + `/design-consultation` + `/plan-eng-review`
- **W2~W6**: 빌드
- **W7**: 베타 50명 + `/qa` + `/design-review`
- **W8**: Play Store 출시 + `/ship` + `/land-and-deploy` + `/canary`

## 기술 스택 (확정 — 2026-05-23 백엔드 pivot)

### Frontend
- **앱**: Flutter 3.x (Dart) + Material 3 + Riverpod (state)
- **로컬 캐시**: Drift (SQLite) — offline-first
- **OS API**: Flutter platform channel → Kotlin → `UsageStatsManager` (PACKAGE_USAGE_STATS)
- **푸시 수신**: firebase_messaging (FCM 토큰만)
- **Auth 클라이언트 (V1)**: google_sign_in pub package (Google Sign-In primary)
- **Auth 클라이언트 (V2)**: kakao_flutter_sdk_user (Kakao 카톡 연동 link)

### Backend
- **API 서버**: **FastAPI (Python)** on Fly.io seoul region (~$10-15/월)
- **DB**: **PostgreSQL on Supabase** (Free tier 5,000명까지, 이후 Pro $25 또는 Hetzner self-managed migration)
- **Auth (V1)**: **JWT + Google Sign-In** (google-auth library ID token verify, Firebase Auth 미사용)
- **Auth (V2)**: Kakao OAuth link (카톡 연동 시점, phone 입력 step)
- **Cron**: APScheduler (FastAPI 내장) — 일요일 22:00 reflection + threshold trigger
- **Migrations**: Alembic
- **Sync 패턴**: REST endpoints, last-write-wins for settings, append-only for usage_events

### 외부 서비스 (V1)
- **LLM**: Claude Haiku 3.5 primary (Anthropic SDK from FastAPI), GPT-5 mini fallback
- **푸시 발송**: Firebase project FCM only (Firebase Admin SDK from Python) — Firestore·Auth 미사용
- **이메일**: Mailgun free tier (5K/월) — transactional email
- **Telegram**: Bot API (python-telegram-bot SDK) — 무료, 사업자 X
- **분석**: Mixpanel free
- **모니터링**: Sentry free tier (Python + Flutter)

### 외부 서비스 (V2, 사업자 등록 후 도입)
- **결제**: Toss Payments 앱 SDK (외부 결제) — V2
- **카톡**: 카카오 비즈메시지 알림톡 정보성 (Aligo / SOLAPI / DirectSend) — V2

### Phase 1 → Phase 2 사업 확장 호환성
- **데이터 ownership**: Postgres pg_dump 자유, 어디든 migration 가능
- **Schema 자유**: B-2 ICP 확장 (user_segment 컬럼), B-3 행동 확장 (caffeine_events, sleep_events 새 테이블)
- **데이터 분석**: raw SQL + pandas + scikit-learn 자유
- **매각 due diligence**: Postgres dump = 표준 자산, vendor 의존 0
- **한국 데이터 주권**: Fly.io seoul region — 본인 ICP "기기 안에만" 메시지와 일관

## 핵심 원칙

1. **본인이 ICP** — 콘텐츠·UX·우선순위 결정 시 본인 일상 체험 우선. 외부 추측 X.
2. **단일 vertical 깊이** — 디지털 디톡스 1개 카테고리만. multi-action 통합 회피 (B-4 회귀 risk).
3. **자본 ₩50만 안에서 W8 출시** — iOS Companion 외주는 Phase 1 매출 후.
4. **카톡 알림톡 정보성만** — 마일리지·쿠폰·할인 메시지 0 (2026.1.1 정책 위반 risk).
5. **개인정보 최소** — UsageStats 데이터는 사용자 동의 + Firestore 저장 시 anonymize 우선.

## Skill routing (gstack)

자연어 요청이 다음과 매칭되면 해당 gstack skill 호출:

| 의도 | skill |
|---|---|
| 제품 아이디어 / 브레인스토밍 | `/office-hours` |
| 스코프 / 전략 검토 | `/plan-ceo-review` |
| 아키텍처 / 데이터 모델 | `/plan-eng-review` |
| 디자인 시스템 (1회) | `/design-consultation` |
| 디자인 플랜 리뷰 | `/plan-design-review` |
| 전체 리뷰 파이프라인 | `/autoplan` |
| 버그 / 에러 디버깅 | `/investigate` |
| QA / 사이트 테스트 | `/qa` (또는 보고만 `/qa-only`) |
| 코드 리뷰 / 변경분 검토 | `/review` |
| 시각 폴리시 | `/design-review` |
| 배포 / PR | `/ship` 또는 `/land-and-deploy` |
| 출시 후 모니터링 | `/canary` |
| 2차 의견 / 어드버서리얼 | `/codex` |
| 보안 감사 | `/cso` |
| 진척 저장 / 복원 | `/context-save` / `/context-restore` |

When in doubt, invoke the skill.

## 참고 자료

- **본 PRD**: [`docs/PRD.md`](docs/PRD.md)
- **원본 PRD (sync 시)**: `/Users/jungsunpark/Projects/pjs/find_business/docs/candidates/b2c_mobile_app/deepdive/2026-05-18-kkeugi-habit-stop-timer.md`
- **사업 발굴 하네스**: `/Users/jungsunpark/Projects/pjs/find_business/`
- **persona**: `/Users/jungsunpark/Projects/pjs/find_business/config/persona.md` (Flutter "중" 본격 전환 2026-05-21)

## Design System

`DESIGN.md`를 항상 모든 UI·시각 결정 전에 읽는다. 모든 폰트·색·spacing·미학 방향이 거기 정의되어 있다.
사용자 명시 허가 없이 deviate 금지. QA 모드에서 DESIGN.md와 불일치하는 코드 발견 시 flag.
Memorable thing: **거울 같은 친구 — 압박 X · 비난 X · 객관 O · 지속 동기.** 새 컴포넌트·카피·색 추가 시 이 4축으로 self-check.

## 변경 이력

| 날짜 | 변경 | 사유 |
|---|---|---|
| 2026-05-21 | 레포 init. PRD 복사. CLAUDE.md + README.md 작성. Flutter SDK·Android Studio 설치 대기 (W0) | find_business deepdive GO 판정 + gstack 활용 결정. 다음: Flutter 설치 → `/office-hours` |
| 2026-05-22 | `/office-hours` 완료 → design doc APPROVED (`~/.gstack/projects/kkeugi/jungsunpark-main-design-20260522-001310.md`). Approach B "Focus Accountant Reframing" 채택. P1-P7 premise 확정. | 본인 ICP episode 발산 + premise 6개 + Google Play policy P7. PRD 9항목 변경 후보. |
| 2026-05-22 | `/design-consultation` 완료 → `DESIGN.md` 작성. Pretendard + IBM Plex Mono + clay `#8B5A3C` accent + light default 확정. | Memorable thing "거울 같은 친구" 발견. P2 시점별 톤 분리 design tokens 반영. |
| 2026-05-23 | `/plan-eng-review` 진행 중 → PRD §4·§8·§11·§12·§14 update. 카톡 알림 reframed (무료 주1회 reflection / 유료 주1회+threshold+시간custom). W4에 카톡 채널 등록·심사·privacy policy URL 공개·UsageStatsManager 통합. W7 법무 budget ₩50~70만 (P7). | 사용자 challenge "gandan은 단식 active session, 끊기는 회고 — cadence 다름". memorable thing "압박 X" 일치. 비용 ₩37만 → ₩6.7만/월 (1,000명). |
| 2026-05-23 | **백엔드 stack pivot**: Firebase → FastAPI + Postgres on Supabase Free + Fly.io seoul. PRD §7 전면 rewrite, §8 운영비 재산정, §12 W2·W3·W6 update. Assumption Audit #6 신규. CLAUDE.md 기술 스택 섹션 전면 재구성. | 사용자 결정: (1) FastAPI 본인 주력 stack, Firebase 학습 비용 회피, (2) 사업 확장 (Phase 2·매각·multi-product) 시 Postgres ownership·schema 자유·analytics 필수. Firebase는 FCM only로 축소. |
| 2026-05-24 | **Cash 비용 재산정 + active filter 채택**. 1,000명 ₩7.4만 / 5,000명 ₩28만 / 20,000명 ₩117만 (gross margin 81-86%). 카톡 active filter: 지난 7일 usage_events ≥1건 + 카톡 친구 추가 사용자만 발송. PRD §8 카톡 ₩6.7만 → ₩3.4만 (-50%). §12 W6 active filter SQL 구현 추가. | 사용자 challenge "비활성 사용자에게 카톡 무의미". 정보성 정책 준수 강화 + 비용 driver 완화. |
| 2026-05-24 | **🔄 V1 = 인앱결제 paid product re-pivot**. 무료 도구 pivot reverse. Google Play Billing Individual = 사업자 X로 매출 발생. 가격 ₩11K/₩5.9K/₩39K Hybrid + 7일 free trial + 베타 50% + 출시 7일 30%. 사업자 trigger = 월 net 매출 ₩35-50만. autoplan CEO subagent challenge 반영 — 발각 risk·maintenance trap·ICP paradox·exit criteria PRD §11·§13 정량화. PRD §1·§4·§5·§7·§11·§12·§13·§14 + ARCHITECTURE subscriptions 부활 + DESIGN paywall + TODOS + CLAUDE + README update. | autoplan CEO review subagent challenge. 사업자 X 매출 가능 path 발견 (Google Play Individual). 위험 정량화 후 사용자 결정. |
| 2026-05-24 | **Auth Google Sign-In primary 변경** (Kakao OAuth → V2 격하). 사용자 catch "카카오 OAuth를 사용해야하는 이유는?". google_sign_in pub package + google-auth library backend verify. Kakao Developers 비즈 심사 W2에서 제거. V2 카톡 연동 시점에 /v1/auth/kakao_link (phone 입력 step). PRD §7 §12 + ARCHITECTURE §5 + DESIGN 온보딩 + users.google_sub 추가. | Android 표준 + Google Play Billing 자연 통합 + W2 일정 단축 + 본명 강결합 발각 risk 회피. V2 카톡 link 시 phone 5초 friction. |
| 2026-05-24 | **PRD §8 3-시나리오 매트릭스 재구성** (보수 4% / 기본 7% / 공격 12% paid). 이전 "20% paid" 비현실적 가정 정정. 9-셀 매트릭스 (scenario × scale). Gross margin 90-96% 달성. | 사용자 challenge "유료 비율 현실은?". §9 매출 시뮬레이션과 framing 일관. |
| 2026-05-24 | **PRD §6 GTM Phase별 Acquisition 전략 통합**. 0a/0b/1/2 4단계 매트릭스. 단계별 채널 × yield × CAC + LTV/CAC 21.5x→5.7x. Shorts/Reels는 V1.5+ 홀딩 (TODOS 등록, 시리즈 5종 후보 명시). | 사용자 catch "PRD §9 수치만 있고 어떻게 달성하는지 미명시". §6 단계별 전략 부재 보완. |
| 2026-05-24 | **PRD §9 매출 detail 3종 추가**: Sensitivity (acquisition #1 민감), Cash flow + Capital ROI 48.3x BEP M3, Best/Worst case + NO-GO trigger (M3 hard checkpoint). Detail 1-4 (Cohort/MRR/ARPU/Churn)는 M3+ 데이터 모인 후 추가 (TODOS 등록). | 본인 자본 ₩50만 회수 시점·NO-GO timing 정밀화. |
| 2026-05-24 | **`/plan-eng-review` Architecture 완료** → `docs/ARCHITECTURE.md` 작성. usage_events monthly partition / Sync 8h + 로컬 threshold / JWT 15min + 30d rotation 결정 잠금. Subagent cold read 14개 issue 반영 (idempotency 재설계, FK CASCADE 제거, PIPA, 카톡 광고성 회피, Toss-Play Plan B, W2-W3 split, APScheduler 외부 trigger fallback, Anthropic Tier 1, Supabase Pro trigger, Sentry 등). **P0 critical: 사업자 등록 + 카카오 비즈니스 채널 + 알림톡 심사 W2 전 즉시 착수**. | Solo founder + 8주 + 카톡 wedge #3 검증 가능성 살리기 위해 사업자 등록 timeline 압축. ARCHITECTURE.md = 모든 후속 빌드 single source of truth. |
| 2026-05-24 | **🔄 V1 = 무료 도구 pivot (CRITICAL)**: 본인 회사 겸업 명시적 금지 확인 → 사업자등록증 V1에서 X → 카톡·Toss V2 격하. wedge #3 재정의: **multi-channel retention** (FCM + 이메일 + Telegram, 사용자 선택). PRD §1·§4·§5·§7·§8·§10·§11·§12·§13·§14 + ARCHITECTURE §14a + DESIGN 시점별 톤 + TODOS + CLAUDE.md 전면 update. V1 자본 ₩50만 → ₩10만. V2 진입 = M3 hard checkpoint 시점 사업자 path 결정. | 회사 겸업 제약 + V1 출시 + portfolio 가치 + V2 monetization base. multi-channel 다양성 = 새 wedge로 전환 (카톡 약화 → 1인 워커 친화 메신저 선택). |
| 2026-05-25 | **W2 백엔드 + W3/W3.5 프론트 + AVD 검증 완료**. 백엔드: FastAPI usage/auth/users + alembic 9테이블(usage_events monthly partition) + 21 pytest green. 프론트: 온보딩 5단계 + 로그인 + 홈/회고/설정 탭 + 테마. AVD(pixel7, android-35)에서 dev login·온보딩·홈 end-to-end 검증. | gstack 파이프라인(office-hours→design-consultation→plan-eng-review→autoplan) 후 실제 빌드 단계. 실행 절차는 메모리 `project_run_on_avd` 참조. |
| 2026-05-27 | **W6 잔여(회고 카드 1-tap 공유) 완료 = wedge #1 바이럴**. `share_card`(`ShareCard` 360×640 논리 → pixelRatio 3 = **1080×1920 인스타 스토리**, DESIGN "주간 리포트=편지" 한 단락+hero numeral·차트 없음·"끊기·Focus Accountant" 워터마크 + `ReportSharePreviewScreen` RepaintBoundary 온스크린 캡처→`toImage`→PNG→`share_plus`) + 회고 카드 공유 아이콘 + `report_shared` KPI. 유료=hero `₩` 매출환산 / 무료=`+분`. `share_plus ^10.1.1`. 위젯 4건(25 green) + debug APK + **AVD end-to-end**(공유 미리보기 렌더→이미지로 공유하기→ChooserActivity 오픈, cache PNG **1080×1920** 확인). | wedge #1 시간빚 카드의 바이럴 루프. 오프스크린 대신 미리보기 온스크린 캡처로 폰트·신뢰성 확보. |
| 2026-05-27 | **W7 Step 4(KPI 계측) 완료 = W7 코드 완료**. `Analytics` 추상화(`FakeAnalytics` 토큰X dev·기록만 / `MixpanelAnalytics` HTTP `/track` — 네이티브 SDK 없이 dio, 백엔드 FCM·Mailgun과 동일 "HTTP API only" 패턴) + `analyticsProvider`(`Env.mixpanelToken` 스위치) + 6개 이벤트(`permission_granted` 1회 prefs·`channel_toggled`·`purchase_completed`·`report_viewed` 1회·`threshold_created`·`threshold_fired`) + 로그인 시 `identify(user.id)`. `fireThresholdAlarms` 반환을 `List<ThresholdHit>`로 변경(발동 카테고리 계측). 유닛 4건(21 green) + debug APK + **AVD**(dev login→logcat `[analytics] permission_granted`·`threshold_fired{sns}`). 실 전송은 `MIXPANEL_TOKEN` secret(본인). | wedge KPI: 권한 동의율·채널 retention·구매·열람·한도 발동. FakeAnalytics로 키 없이 전 계측 검증. |
| 2026-05-26 | **W7 Step 3(threshold 로컬 알람) 완료 = W7 핵심 완료**. `LocalNotifications`(flutter_local_notifications 래퍼·`threshold_alarms` 채널·Android 13+ 권한) + `threshold_alarm`(순수 `computeThresholdHits` + `fireThresholdAlarms` 1일 1회 prefs dedup·이전날 키 정리 + `checkAndNotifyThresholds`) + `thresholdAlarmProvider`(홈에서 todayStats·thresholds provider 재사용 → 추가 네트워크 호출 0) + worker 백그라운드 sync 직후 체크(앱 닫혀도 알람) + main init + POST_NOTIFICATIONS + 한도 저장 직후 권한 요청. 유닛 9건(17 green) + debug APK + **AVD end-to-end**(SNS 40분/한도 30분 → 알림 셰이드 "SNS 한도를 넘었어요 · 비난은 아니에요" 렌더). | wedge: 한도 초과 알람은 **로컬**(사업자 X 가능). DESIGN "압박 X·비난 X" 톤 카피. Mixpanel KPI(Step 4)는 키 필요로 deferred. |
| 2026-05-26 | **W7 Step 2(한도 설정 UI) 완료**. `thresholds_api`·`provider` + `ThresholdsScreen`(목록·enabled 토글·삭제·빈상태 "압박은 없어요", 무료는 paywall 유도) + `AddThresholdScreen`(카테고리/분 ChoiceChip + 하단 저장) + 설정 목표 행 연결(설정 개수 표시). 위젯 테스트 2건(8 green) + AVD(paid 유저 한도추가→"SNS 하루 30분" 카드 렌더). | 한도 생성 유료 게이팅 + DESIGN 톤. 로컬 알람은 Step 3. |
| 2026-05-26 | **점검 통과 + W7 Step 1(thresholds 백엔드) 완료**. 점검: 백엔드 58 green·lint clean, 프론트 analyze 0(const lint 4건 정리)·위젯 6 green·debug APK 빌드 OK. W7 Step1: `Threshold` 모델 + `GET/POST(require_paid)/PATCH/DELETE /v1/thresholds` + 카테고리 유니크(409)·소유권(404). pytest 7건(65 green) + 라이브(무료 402/유료 201). `docs/W7-build-plan.md`. | 한도 생성 유료(PRD). 로컬 알람은 Step3. |
| 2026-05-26 | **W6 Step 5(paywall gating) 완료 = W6 전체 완료**. `WeeklyReportOut.from_model(show_revenue)` + GET 리포트 3종에서 entitlement로 **recovered_won 무료=null / 유료=노출** (PRD: 카드 본문 무료, 매출환산 유료). regenerate require_paid(기존). pytest 3건(58 green) + 라이브(무료 None→구매 후 10000). thresholds 게이팅은 W7. **W6 완료**: 리포트·cron·dispatch·archive·gating. 실 LLM/FCM/Mailgun은 키+배포 후. | wedge #1 매출환산이 유료 핵심 가치 — 서버 게이팅으로 보장. |
| 2026-05-26 | **W6 Step 4(프론트 회고 archive) 완료**. 백엔드 `GET /v1/reports`(최신순 목록) + 프론트 `archive/reports_api`·`reports_provider` + `ArchiveScreen`(카드 목록: 주 라벨·card_text·insight·회복분/매출환산·빈상태·pull-to-refresh) + shell 회고 탭을 placeholder→ArchiveScreen 교체. AVD 검증(리포트 seed→회고 탭 "5월 25일 주·30분·회복 15,000원·화요일 오전" 카드 렌더). | wedge #1 회고 카드 UI 완성. |
| 2026-05-26 | **W6 Step 3(Multi-channel dispatch) 완료**. `channels/senders`(Mailgun REST httpx + FCM HTTP v1 API+Firebase 서비스계정 — firebase-admin 미사용, verifier와 동일 패턴) + `channels/dispatch.dispatch_report`(구독 채널 라우팅 telegram/email/fcm, 미설정·pending graceful skip, any_channel_sent 기록) + `FcmToken` 모델 + `POST /v1/fcm/register`. run_weekly_reflection에 dispatch 연결(generate+발송). config에 mailgun·fcm 추가. pytest 5건(56 green) + 라이브(fcm register 204, run_weekly graceful skip). | wedge #3 multi-channel. 키 미설정 dev에서 graceful skip으로 검증. 실발송은 키+배포 후. |
| 2026-05-26 | **W6 Step 2(APScheduler cron) 완료**. `scheduler.py`(AsyncIOScheduler Asia/Seoul: 일요일 22:00 주간 리플렉션 / 매일 03:00 hard-delete / 매월 1일 파티션) + FastAPI lifespan 연결(test 환경 제외) + `run_weekly_reflection`(active filter 지난 7일 usage≥1 + 미삭제) + `usage/partitions.ensure_next_month_partition` + dev `POST /v1/reports/dev/run_weekly`. pytest 3건(51 green) + 라이브(파티션 idempotent, run_weekly→generated:1→카드+insight). | 주간 자동 발송 토대. dispatch는 Step 3. cron 검증은 dev 트리거로. |
| 2026-05-26 | **W6 Step 1(주간 리포트 백엔드) 완료**. `WeeklyReport` 모델 + `reports/service`(주간 집계 total·category·peak[요일/오전오후] + recovered_minutes·recovered_won upsert) + `reports/llm`(FakeLLM 결정론 / AnthropicLLM Haiku claude-haiku-4-5, env·키 분기, 거울친구 톤) + `GET /v1/reports/weekly`·`/weekly/{date}`(월요일 정규화) + `POST /v1/reports/regenerate`(require_paid). pytest 6건(48 green) + 라이브 검증. `docs/W6-build-plan.md` 작성. | wedge #1 시간빚 환산 리포트. LLM 추상화로 키 없이 dev 검증. |
| 2026-05-25 | **W5 Step 5(RealBilling 코드 완성) 완료**. 백엔드 `GooglePlayVerifier` 실구현(androidpublisher REST + 서비스계정 OAuth2, one_time/구독 분기) + config(package_name·service_account_json). 프론트 `in_app_purchase ^3.2.0` + `RealBillingService`(purchaseStream→Future) + billingServiceProvider를 Env.useFakeBilling 스위치 연결. analyze 0 + 42 backend test + paywall 위젯테스트 + **debug APK 빌드 성공**(플러그인 통합 확인). 실동작은 Step 6(실기기). | 코드 완성/컴파일까지. Real 검증은 Play Console + 라이선스 테스터 필요. |
| 2026-05-25 | **W5 Step 4(paywall + 결제 UI, Fake) 완료**. `Env.useFakeBilling`(debug true) + payment_api·billing_service(BillingService 추상 + FakeBillingService) + payments_providers(entitlement·purchase) + paywall_screen(3플랜·월구독 기본·7일 trial·하단 CTA, DESIGN 톤) + 설정 매출환산 행 entitlement 연결. 위젯 테스트 2건 + AVD end-to-end(잠김→paywall→7일 무료로 시작→verify 200→매출환산 ON, DB monthly/in_trial). | Play Console 없이 Fake billing으로 구매→검증→paywall 해제 전 플로우 검증. Real billing은 Step 5. | 
| 2026-05-25 | **W5 Step 3(결제 백엔드) 완료**. `Subscription` 모델 + `payments/products`(server-authoritative 카탈로그 cert/monthly/yearly + Google 30% net) + `verifier`(FakeVerifier dev / GooglePlayVerifier stub, get_verifier by env) + `entitlement`(get_active_subscription·require_paid 402) + `/v1/payments/verify`(gp_purchase_token 멱등·tier 갱신·7일 trial)·`/v1/payments/subscription`. pytest 8건(42 green) + 라이브 검증(verify→paid·tier one_time→멱등). subscriptions는 001에 GP 컬럼 완비라 마이그레이션 불필요. | dev login 패턴을 결제에 적용 — FakeVerifier로 Play Console 없이 전 플로우 검증. prod 실검증은 Step 5. |
| 2026-05-25 | **W5 Step 2(회원 탈퇴/데이터 삭제) 완료**. 백엔드: `DELETE /v1/me` soft delete + 전 인증경로(get_current_user·google·refresh·dev-login) 삭제계정 차단 + `users/cleanup.hard_delete_expired_accounts`(PIPA 30일 grace, usage_events 수동 삭제). pytest 4건(34 green). 프론트: 설정 회원탈퇴 → 확인 다이얼로그(grace 안내) → deleteAccount. **위젯 테스트 2건**으로 다이얼로그 경로 확정 검증(AVD는 다이얼로그 버튼 hit-test 미등록 — Impeller 한계). hard-delete cron은 W6 APScheduler 등록 예정. | 배포 전 단계별 검증 절차(W5-build-plan) Step 2. AVD 탭 한계는 위젯 테스트로 우회. |
| 2026-05-25 | **W5 사전계획 + Step 1(Telegram link) 완료**. `docs/W5-prestart-P0.md`(Play Console 리드타임·테스터 12명 확보 전략·applicationId `kr.kkeugi.kkeugi` 정정) + `docs/W5-build-plan.md`(Fake 추상화로 배포 전 단계별 검증, Step 1~6). Step 1: ChannelSubscription 모델 + `/v1/me/telegram`(status·link_token·unsubscribe) + `/webhooks/telegram`(/start 바인딩) + send_message. 프론트 설정 카드 실상태 연결. pytest 30 green + AVD 검증. | 사용자: "코드 먼저 전부 완성하고 배포 전 하나씩 검증". dev login 패턴을 결제에도 적용 → Play Console 없이 95% 검증. |
| 2026-05-25 | **W4 데이터 파이프라인 (wedge #2 자동 import) 완료**. 백엔드 `/v1/usage/batch`(usage_event_dedupe 멱등) + `stats/today`·`stats/week` + 9 pytest. alembic 002: usage_events 2026-01~05 파티션 backfill (001이 06부터 시작해 현월 INSERT 실패 버그 수정). Android `MainActivity.kt` MethodChannel `kr.kkeugi/usage` (hasPermission·openSettings·queryUsageSessions, queryEvents 세션 재구성). Flutter: category_map·usage_channel·usage_api·usage_sync(결정론적 UUIDv5 멱등, last_sync 커서)·WorkManager 8h(0.9.0)·홈 실데이터 연결·권한 게이트. AVD에서 실세션→SNS분류→batch→DB→홈 "+1분" end-to-end 검증. **W4 잔여 deferred**: Mailgun 이메일 발송(외부 키 필요), privacy URL 호스팅, Drift 오프라인 캐시(>7일 미사용 대비), WorkManager 8h 라이브 검증. | "데이터 파이프라인 먼저" 선택. workmanager 0.5.x는 Flutter 3.44 비호환→0.9.0. AVD YouTube/Chrome는 Google 계정 미설정으로 foreground 미기록→Settings 임시 매핑으로 검증 후 원복. |

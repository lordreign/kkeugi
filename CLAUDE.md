# 끊기 (Kkeugi) — 프로젝트 컨텍스트

> Claude Code / gstack 의 모든 에이전트가 이 파일을 읽고 컨텍스트를 잡는다.

## 한 줄 정의

한국 1인 워커를 위한 디지털 디톡스 Android 앱 (Flutter). SNS·쇼츠·게임 끊기 타이머 + UsageStatsManager 자동 import + AI 주간 "회복된 집중 시간 → 매출 환산" 리포트 + 카톡 채널 알림.

## 핵심 정보

| | |
|---|---|
| **ICP** | 한국 1인 워커 (개발자·디자이너·작가·연구자·프리·1인 사업자) — 본인이 곧 ICP |
| **wedge 3개** | (1) 매출 환산 AI 리포트, (2) UsageStatsManager 자동 import, (3) 카톡 알림톡 retention |
| **플랫폼** | Android 네이티브 (Flutter) 단일 시드. iOS는 Phase 1 매출 ₩200만/월 후 v2 |
| **수익** | 일회 ₩9,900 인증서 + 구독 ₩4,900/월 hybrid (Toss 외부 결제) |
| **자본** | 약 ₩50만 (Google Play $25 + 법무 ₩30~50만 + 인플 시드 ₩30~50만 + 예비) |
| **MVP** | 8주 (W1 Flutter 학습 포함) |
| **GO/NO-GO** | **GO** (2026-05-21 확정) |

## 빌드 단계 (W0 = 지금)

상세 매핑은 [README.md](README.md) 참조.

- **W0 (지금)**: 레포 init + Flutter SDK 설치 + Firebase project + `/office-hours` (PRD 발산)
- **W1**: Flutter 학습 + Figma + `/design-consultation` + `/plan-eng-review`
- **W2~W6**: 빌드
- **W7**: 베타 50명 + `/qa` + `/design-review`
- **W8**: Play Store 출시 + `/ship` + `/land-and-deploy` + `/canary`

## 기술 스택 (확정)

- **앱**: Flutter 3.x (Dart) + Material 3 + Riverpod (state)
- **OS API**: Flutter platform channel → Kotlin → `UsageStatsManager` (PACKAGE_USAGE_STATS)
- **BaaS**: Firebase (Firestore + Auth + Cloud Functions + FCM)
- **LLM**: Claude Haiku 3.5 primary, GPT-5 mini fallback
- **결제**: Toss Payments 앱 SDK (외부 결제)
- **카톡**: 카카오 비즈메시지 알림톡 정보성 (Aligo / SOLAPI / DirectSend 중 1택)
- **분석**: Firebase Analytics + Mixpanel free

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

## 변경 이력

| 날짜 | 변경 | 사유 |
|---|---|---|
| 2026-05-21 | 레포 init. PRD 복사. CLAUDE.md + README.md 작성. Flutter SDK·Android Studio 설치 대기 (W0) | find_business deepdive GO 판정 + gstack 활용 결정. 다음: Flutter 설치 → `/office-hours` |

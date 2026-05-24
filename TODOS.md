# TODOS

## Open

## P0 — W2 시작 전 즉시 (2026-05-24 V1 무료 도구 pivot 반영)

### [P0] .kr 도메인 등록 + Fly.io custom domain + Let's Encrypt
- **What**: api.kkeugi.kr 등록 (한국 통신사 본인인증 필요, 반나절). Fly.io custom domain 설정 + Let's Encrypt TLS.
- **Why**: W2 backend 배포 전 준비.
- **Deadline**: W2 시작 전
- **Status**: 🔴 OPEN

### [P0] Mailgun 또는 AWS SES 1택 + Telegram Bot 생성
- **What**:
  1. 이메일 vendor 1택 (Mailgun free 5K/월 권장 vs AWS SES $0.10/1K)
  2. BotFather에서 Telegram Bot 생성 + API token 발급
  3. Telegram Bot 한국어 description + 시작 명령어 set
- **Why**: V1 multi-channel retention의 3개 채널 중 2개 (FCM은 W3 자동 진행).
- **Deadline**: W4 시작 전
- **Status**: 🔴 OPEN

### [P0] Google Play Console Individual 계정 가입 + Billing 통합
- **What**:
  1. Google Play Console Individual 계정 가입 ($25 일회, 본인 명의)
  2. 결제 정보 등록 (한국 통장 + 본인 주민번호)
  3. 3 product 등록 (kkeugi.cert ₩11,000 · kkeugi.monthly ₩5,900 · kkeugi.yearly ₩39,000)
  4. 7일 free trial Google Play 표준 설정 (구독만)
  5. 베타 50명 promo code 발급 시스템
  6. 출시 7일 30% sale 설정
- **Why**: V1 인앱결제 paid product의 핵심 인프라.
- **Deadline**: W5
- **Status**: 🔴 OPEN

### [P1] 사업자 등록 trigger 도달 시 path 결정 (월 net 매출 ₩35-50만 도달)
- **What**: trigger 도달 시 다음 중 1개:
  - (A) 본인 명의 개인사업자 등록 — 회사 발각 risk 정량 평가 + 회피 대책
  - (B) 가족 명의 사업자 등록 — 가족 동의 필요
  - (C) 회사 정리 후 본인 명의 — runway 확보 후
  - (D) Maintenance mode (사업자 X 유지, sustained)
- **Why**: V2 monetization (Toss + 카톡) 진입 의 hard prerequisite.
- **Deadline**: 월 net 매출 ₩35-50만 도달 시 30일 내
- **Status**: 결정 대기 (trigger 도달 후)

## P1 — Architecture 수정 (W2 구현 시 반영)

### [P1] usage_events idempotency 재설계 — 별도 dedupe 테이블
- **What**: ARCHITECTURE.md §14.3. `usage_event_dedupe` non-partitioned 테이블 추가 (user_id, client_event_id PK, 24h TTL cleanup).
- **Why**: 기존 `UNIQUE (user_id, client_event_id, occurred_at)` 은 millisecond drift로 중복 row 생성 가능.
- **Status**: W2 Alembic migration에 포함

### [P1] FK ON DELETE CASCADE 제거 + soft delete + batch archive
- **What**: usage_events.user_id → REFERENCES users(id) (CASCADE 없이). 사용자 hard delete는 30일 grace + batch archive cron.
- **Why**: 7,000만 row CASCADE = user 1명 삭제 시 30분 lock.
- **Status**: W2 Alembic migration

### [P1] PIPA 처리방침 보완
- **What**:
  1. 국외 이전 동의 별도 체크박스 (Fly.io US 모회사)
  2. 위탁사 list 명시 (Anthropic, OpenAI, Toss, SOLAPI, Firebase, Fly.io, Supabase, Sentry, Mixpanel)
  3. 만 14세 미만 age gate (가입 시 생년월일 또는 14세+ 동의)
  4. 회원 탈퇴 30일 grace + hard delete cron
- **Why**: PIPA 위반 시 과징금.
- **Status**: W2 처리방침 작성 시 반영

### [P1] 카톡 알림톡 정책 — 광고성 회피 + 수신거부 footer
- **What**:
  1. "₩X 회복" wording 위험 → "이번 주 N분 줄였어요" 톤
  2. 22:00 발송 정보성 분류 사전 카카오 확인
  3. 모든 메시지 footer에 수신거부 1-tap 링크 의무
- **Why**: 광고성 분류 시 템플릿 반려 + 발송 차단.
- **Status**: 템플릿 초안 작성 시 반영 (W2)

### [V2 격하] Toss + Google Play 정책 충돌 Plan B (V1 무료라 V1에서는 비해당)
- **What**: KFTC 허용 ≠ Play 통과. Plan B = Play in-app billing fallback (수수료 30%, ₩11,000/₩5,900 가격 인상). W5 KFTC 재검증 시 동시에 Play 정책 변동 확인 + Plan B 활성화 가능 상태 유지.
- **Why**: Play deletion 시 매출 0.
- **Status**: W5 작업에 포함

### [P1] APScheduler 외부 cron trigger fallback
- **What**:
  1. `fly.toml`에 `min_machines_running = 1` 명시
  2. cron-job.org 외부 webhook → `POST /v1/internal/trigger-weekly` (secret 헤더 보호)
  3. 일요일 22:00 weekly + daily 03:00 cleanup 둘 다 외부 trigger 등록
- **Why**: Fly machine auto-stop 시 cron miss.
- **Status**: W7 cron 통합 시 반영

## P2 — 구현 시 반영 (W2-W8)

### [P2] Anthropic Tier 1 prepay
- **What**: Free RPM 50 → Tier 1 $5 prepay (RPM 1000+) 또는 batch API 활용.
- **Why**: 일요일 5,000명 동시 LLM 호출 시 free RPM 초과.
- **Status**: W6 LLM pipeline 구현 시

### [P2] Supabase Pro 전환 trigger 명시
- **What**: DB > 400MB OR M4 도달 OR Sunday cron 부담 ↑ 시 자동 알람 + Pro 전환.
- **Why**: Free 500MB 한도, partition 7,300만 row 못 들어감.
- **Status**: W2 monitoring 설정

### [P2] Sentry quota aggressive filtering
- **What**: Free 5K errors/월 한도. 4xx 클라이언트 에러 제외, alert on 80% quota.
- **Why**: Production spike 1회 = dead zone risk.
- **Status**: W8 Sentry 통합 시

### [P2] LLM fallback prompt 추상화
- **What**: `reports/templates.py`에 model-agnostic prompt template. Claude Haiku 3.5 + GPT-5 mini 양쪽 동치.
- **Why**: fallback 시 prompt 차이로 응답 품질 불일치.
- **Status**: W6 LLM pipeline 구현 시

### [P2] 미시 schema fix
- `fcm_tokens.token VARCHAR(500)` → `VARCHAR(1024)`
- `thresholds.last_triggered_date DATE` → `last_triggered_at TIMESTAMPTZ`
- `weekly_reports.recovered_won` 곱셈 중간값 BIGINT
- HS256 single-instance fly.toml 명시
- `/health` `/ready` fly.toml `[[http_service.checks]]` 등록
- LLM 결과 weekly_reports에 service_used 컬럼 추가

---

## 기존 P2-P3 (이전 세션 — Backend stack pivot 등)

### [P2] Vendor 선택: SOLAPI / Aligo / DirectSend
- **What**: 알림톡 발송 vendor 1개 선택. 단가·UX·SDK·Python REST 지원 비교 후 결정.
- **Why**: W4 카톡 등록 작업의 prerequisite.
- **비교 기준**:
  - 단가 (1건 ₩10-15 range)
  - REST API + Python SDK 또는 httpx 통합 용이성
  - 템플릿 심사 처리 속도
  - 한국어 docs 품질
- **Decision deadline**: W4 시작 전 (2026-06-?? 추정)
- **Status**: Open

### [P2] Supabase Free → Pro 또는 Hetzner migration trigger 정의
- **What**: Supabase Free tier 한계 (500MB DB, 50K MAU, 2GB bandwidth) 도달 시 migration 의사결정 룰 명시.
- **Trigger 후보**:
  - DB size > 400MB (80% 한계)
  - MAU > 40K (80% 한계)
  - 또는 5,000명 결제 사용자 + 매출 ₩200만/월 도달
- **Migration 후보**:
  - Supabase Pro $25/월 (managed 유지, 1일 작업)
  - Hetzner VPS €5/월 + self-managed Postgres (cash ↓, ops 2-4h/월, 2-3일 작업)
- **Status**: Phase 1 KPI 모니터링 결과에 따라 결정. M6 시점 재검토.

### [P3] Drift SQLite offline-first sync 패턴 설계
- **What**: Flutter Drift 로컬 cache + FastAPI REST sync. 충돌 해결 룰 정의.
- **방향**: last-write-wins 충돌 (개인 데이터라 acceptable). usage_events는 append-only, settings는 last-write-wins.
- **Status**: W2 FastAPI setup 후 W3에 sync 구현

### [P1 — design doc reviewer flagged] PRD §12 timeline 영향 재산정 — 4종 프리셋 + V1.5 spike
- **What**: design doc reviewer concern. 4종 프리셋 (웹툰 추가) + V1.5 heuristic spike → W2~W6 effort 5~10% 증가. PRD §12 timeline 명시적 재추정 필요.
- **Why**: 현재 PRD §12는 변경 effort 증가 미반영. 실제 W8 launch slip risk 있음.
- **Status**: `/plan-eng-review` 진행 중 (이번 세션). 다음 단계.

### [P2 — design doc open question] Brand naming 한국어 결정
- **What**: "끊기" 유지 vs "끊기 (Focus Accountant)" 병기 vs 다른 한국어 이름. 랜딩·X 게시·카톡 채널명에 필요.
- **Decision deadline**: W8 launch 전 마케팅 콘텐츠 제작 시
- **Status**: Open (마케팅 단계로 위임)

### [P3 — design doc open question] 웹툰 패키지 list 점진적 update 메커니즘
- **What**: 한국 웹툰 앱 list 확장 시 (네이버 웹툰, 카카오 웹툰, 레진코믹스, 탑툰 등). Firebase Remote Config 권장.
- **Status**: W4 platform channel 구현 시 결정

### [P3 — design doc open question] V1.5 작업 시간대 heuristic 구현 우선순위
- **What**: W5~W6 spike 안에 시간 가능? 또는 V1.6으로 미루기?
- **Status**: `/plan-eng-review` 결과에 따라 결정

### [P3 — Data-dependent] PRD §9 Detail 1-4 추가 (M3+ 데이터 모인 후)
- **(1) Cohort chain** — M1 가입자 30일 결제·구독 chain 추적 → 첫 cohort full lifecycle 관찰. **추가 timing: M3 (베타 + 출시 후)**.
- **(2) MRR 정밀 모델** — 구독자 ≥ 30명 도달 후 MRR 누적 효과 분리. **추가 timing: M4-M5**.
- **(3) ARPU 정밀** — 무료/일회/구독별 blended ARPU 계산 → pricing 의사결정 base. **추가 timing: M3-M4**.
- **(4) Churn 모델** — 구독 cancel rate 실측 → LTV 정밀 재계산. **추가 timing: M5-M6 (구독자 1 cycle 완료 후)**.
- **Why now skipped**: 모두 실제 데이터 필요. 가정만으로는 의미 약함.
- **Status**: Open, M3 hard checkpoint 시점 재검토

### [P2 — GTM] YouTube Shorts + Instagram Reels 채택 여부 (홀딩 중)
- **What**: 한국 디톡스 vertical에 short-form 강한 indie 앱 없음. 본인이 ICP라 콘텐츠 자가 생산 자연스러움. CAC ₩0 (cash) + 본인 인건비 제외.
- **Potential acquisition**: Phase 0b 500-1,500명, Phase 1 추가 1,500-4,500명
- **Risk**: "디톡스 앱을 쇼츠에 홍보" 위선 톤 risk. 시간 부담 (주 1-3 posts, 30-60분/영상).
- **콘텐츠 시리즈 5종 후보**:
  - (1) 매출 환산 카드 5-10초 reveal — DESIGN.md hero numeral 그대로 viral
  - (2) 1인 개발자 vs SNS 비교 (founder narrative + 본인 SaaS MRR vs SNS 사용시간)
  - (3) AI 작업 중 함정 — P4 본인 episode 재현
  - (4) "디톡스 앱 만들면서 쇼츠 본다" — self-deprecating meta hook
  - (5) "끊기 사용 N일째" before/after — 본인 데이터 공개
- **플랫폼 우선순위**: YouTube Shorts > Instagram Reels > TikTok (한국 시장)
- **결정 deadline**: W4 또는 V1.5 시점
- **결정 시 확인 필요**:
  - 본인 face 노출 가능 vs voiceover only?
  - 콘텐츠 톤 — 진지 vs 가벼움 vs self-deprecating mix?
  - 첫 영상 어떤 시리즈로 시작?
- **Status**: 사용자 홀딩 결정 (2026-05-24)

## Done

### [P1] PRD §4 카톡 알림 차별화 명시 — 무료 vs 유료 ✅ 2026-05-23
- **Decision**: Reframed 안 채택 — 무료 = 주 1회 일요일 reflection, 유료 = 주 1회 + threshold trigger + 시간 customize
- **Rationale**: 사용자 challenge "gandan은 단식 active session, 끊기는 회고 — 의미론적으로 다른 cadence". memorable thing "압박 X" 일치.
- **Updates applied**: PRD §4 #4·#5, PRD §8 운영비, PRD §14 변경 이력

### [P1] W7 카톡 알림톡 심사 → W4로 당기기 ✅ 2026-05-23
- **Decision**: W4로 당김 — 카카오 비즈니스 채널 등록 + vendor 가입 + 알림톡 템플릿 3종 (주간 reflection / threshold trigger / 동의 안내) 초안 제출
- **Rationale**: 심사 영업일 1-3주 → W7 시작이면 W8 launch에 미준비. wedge #3 첫날부터 작동 필요.
- **Updates applied**: PRD §12 W4·W5·W6·W7, PRD §11 P7 법률·심사 risk, PRD §14 변경 이력

### [P1] 카톡 알림톡 active user filter ✅ 2026-05-24
- **Decision**: 지난 7일 `usage_events` 1건 이상 (UsageStatsManager 자동 sync 또는 앱 open 어느 쪽이든) AND `kakao_consents.subscribed = true` 필터링. SQL INNER JOIN으로 weekly cron 시 적용.
- **Rationale**: 사용자 challenge "비활성 사용자에게 카톡 발송 무의미". 정책 준수 강화 (정보성 = 본인 데이터 존재) + 비용 50% 절감.
- **결과**:
  - 1,000명 카톡 ₩6.7만 → ₩3.4만
  - 5,000명 카톡 ₩33.6만 → ₩16.8만
  - 20,000명 카톡 ₩134만 → ₩67만
  - Gross margin 73-78% → **81-86%**
- **Updates applied**: PRD §8 카톡 cell + 합계 표, §12 W6 active filter SQL 구현, §14 변경 이력

### [P0] 백엔드 stack 결정: FastAPI + Postgres ✅ 2026-05-23
- **Decision**: Firebase (Firestore + Auth + Cloud Functions + FCM) → **FastAPI + Postgres on Supabase Free + Fly.io seoul region**. Firebase는 FCM only로 축소.
- **Rationale**:
  - 본인 FastAPI 주력 stack "상" → 학습 곡선 0, productivity ↑
  - 사업 확장 (Phase 2 B-2/B-3, multi-product, 매각, 데이터 분석) 시 Postgres 표준 ownership·schema 자유·analytics 자유 필수
  - Cash ₩2.5만 → ₩1.4-2.1만/월 (1,000명). 5,000명까지 Supabase Free.
  - 한국 IDC (Fly.io seoul) = 본인 ICP "기기 안에만" 메시지와 일관
- **Updates applied**: PRD §7 전면 rewrite, §8 운영비, §12 W2·W3·W6·W7, §14 변경 이력 + Assumption Audit #6 신규

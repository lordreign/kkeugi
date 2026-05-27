# W6 빌드 플랜 — AI 주간 리포트 + 운영

> W5와 동일: 외부 의존(LLM·FCM·Mailgun)을 추상화 + Fake/graceful-skip → **배포 전 단계별 검증**.
> 실 LLM·FCM·Mailgun은 키/배포 준비 후 통합. 상세 배경: [PRD §12 W6](PRD.md) · [REMAINING-WORK A-2](REMAINING-WORK.md)

## 원칙
- **LLM**: dev/test = `FakeLLM`(stats 기반 템플릿 카드, 결정론적). prod = Anthropic Haiku(키 있으면). wedge #1 "시간 빚 환산" 톤 = 거울 같은 친구(압박X·비난X·객관O).
- **발송**: Telegram(✅ W5) + FCM + Mailgun. **미설정 채널은 graceful skip**(dev에서 키 없이 동작).
- **active filter**: 지난 7일 usage_events ≥1건 사용자만 리포트/발송.

## 빌드 순서 (각 단계 = 빌드 → 검증 게이트 → 다음)
- [x] **Step 1 — 주간 리포트 백엔드** ✅ (2026-05-26): `WeeklyReport` 모델 + `reports/service`(compute_week_stats 주간 total·category·peak요일/오전오후 + generate_report recovered_minutes·recovered_won upsert) + `reports/llm`(FakeLLM 결정론 / AnthropicLLM Haiku, env·키 분기) + `GET /v1/reports/weekly`·`/weekly/{date}`(월요일 정규화) + `POST /v1/reports/regenerate`(require_paid). pytest 6건(48 green) + 라이브(구매→regenerate→GET).
- [x] **Step 2 — APScheduler cron** ✅ (2026-05-26): `scheduler.py`(AsyncIOScheduler Asia/Seoul — 일요일22:00 reflection·매일03:00 hard-delete·매월1일 파티션) + lifespan 연결(test 제외) + `service.run_weekly_reflection`(active filter 지난7일) + `usage/partitions.ensure_next_month_partition` + dev `POST /v1/reports/dev/run_weekly`. pytest 3건(51 green) + 라이브(파티션 idempotent + run_weekly→generated:1→카드+insight "화요일 오전").
- [x] **Step 3 — Multi-channel dispatch** ✅ (2026-05-26): `channels/senders`(Mailgun httpx + FCM HTTP v1 API+서비스계정, firebase-admin 미사용) + `channels/dispatch.dispatch_report`(구독 채널 라우팅, telegram pending/미설정 graceful skip, any_channel_sent 기록) + `FcmToken` 모델 + `POST /v1/fcm/register` + run_weekly_reflection에 dispatch 연결. pytest 5건(56 green) + 라이브(fcm register 204, run_weekly dispatch graceful skip→any_channel_sent f, 무크래시).
- [x] **Step 4 — 프론트 회고 archive** ✅ (2026-05-26): 백엔드 `GET /v1/reports`(목록) + 프론트 `reports_api`·`reports_provider` + `ArchiveScreen`(카드 목록·주라벨·card_text·insight·회복분/매출환산·빈상태·pull-refresh) + shell 회고 탭 연결. AVD 검증(dev 유저 리포트 seed → 회고 탭 카드 "5월 25일 주·30분·15,000원·화요일 오전" 렌더, GET /v1/reports 200).
- [x] **Step 5 — paywall gating 적용** ✅ (2026-05-26): `WeeklyReportOut.from_model(show_revenue)` + GET 리포트 3종(list·weekly·by_date)에서 entitlement(get_active_subscription)로 **recovered_won 무료=null/유료=노출**. regenerate는 require_paid(기존). pytest 3건(58 green) + 라이브(무료 won=None→구매 후 10000). thresholds 게이팅은 W7(미구현)에서.

**W6 완료** — 백엔드 58 test green. 실 LLM/FCM/Mailgun/Telegram 발송은 키+배포 후(graceful skip로 dev 검증 완료).

## 검증
- 백엔드: `make lint` + `make test` + 라이브 curl(dev trigger)
- 프론트: `flutter analyze` + 위젯 테스트 + AVD
- 각 Step 종료 시 CLAUDE.md 변경 이력 1줄

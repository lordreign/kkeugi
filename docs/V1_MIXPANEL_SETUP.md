# Mixpanel 대시보드 셋업 가이드 (V1)

V1_EXECUTION_PLAN §4 KPI 재정의에 따라, Mixpanel 콘솔에서 만들어야 하는 4개 view.
PHASE 2-D 에서 Mixpanel 가입 + Project Token 발급 직후 진행.

---

## 사전 준비

1. https://mixpanel.com 가입 (free tier)
2. 새 프로젝트 생성 — 이름 `kkeugi`
3. Settings → Project Settings → **Project Token** 복사
4. 토큰을 release 빌드 dart-define 에 주입:
   ```
   --dart-define=MIXPANEL_TOKEN=<your-token>
   ```
5. 첫 빌드 후 Live View 에서 이벤트 도착 확인 (대시보드 → Live View)

---

## 현재 보내고 있는 이벤트 (코드 기준)

| 이벤트명 | 발생 시점 | 속성 |
|---|---|---|
| `permission_granted` | 사용 통계 권한 첫 동의 (1회) | — |
| `channel_toggled` | 알림 채널 on/off | `channel`, `on` |
| `paywall_viewed` | paywall 화면 진입 | — |
| `purchase_completed` | 결제 완료 | `product_id`, `trial` |
| `report_viewed` | 회고 카드 첫 렌더 (1회/세션) | — |
| `report_shared` | 회고 카드 공유 버튼 → share sheet | — |
| `threshold_created` | 한도 생성 | `category`, `minutes` |
| `threshold_fired` | 한도 초과 로컬 알람 발동 | `category` |

`identify(user.id)` 는 로그인 시 호출.

---

## View 1 — Activation → Paid Funnel

목적: 핵심 funnel 의 drop-off 구간 확인. V1 가장 중요한 view.

Mixpanel → **Insights → Funnels → New Funnel**

| Step | Event | 조건 |
|---|---|---|
| 1 | `permission_granted` | — |
| 2 | `report_viewed` | — |
| 3 | `paywall_viewed` | — |
| 4 | `purchase_completed` | — |

- Time window: 30 days
- Conversion criteria: `unique` per `distinct_id`
- Group by: 비워두기

저장 이름: `Activation → Paid V1`

---

## View 2 — Cohort Retention (D30)

목적: V1 PMF KPI Tier 1 = D30 12% / stretch 25% 측정.

Mixpanel → **Insights → Retention → New Retention**

- First event: `permission_granted` (또는 `purchase_completed` for paid cohort)
- Return event: 아무 event (default: ANY event) — 권장 활성도 신호 `report_viewed` 또는 `threshold_fired`
- Period: Day
- Show: 30 days (D1, D7, D14, D30 표시)
- Filter: 출시 후 cohort 별

저장 이름: `D30 Retention V1`

---

## View 3 — 공유율 (Ratio Chart)

목적: V1 PMF KPI Tier 2 = 공유율 5% / stretch 15% 측정.

Mixpanel → **Insights → Custom Formula**

```
A / B
where:
  A = count of `report_shared` in last 7 days
  B = count of `report_viewed` in last 7 days
```

또는 두 line chart 를 겹쳐서 비율 시각.

저장 이름: `주간 공유율 V1`
리뷰 cadence: **주간**

---

## View 4 — Daily KPI Dashboard

목적: 매일 보는 핵심 지표 한눈에.

Mixpanel → **Dashboards → New Dashboard** 이름 `V1 Daily KPI`

추가할 chart 4개:

1. **신규 install (일별)**
   - Insights → Trends → `permission_granted` (unique users) per day

2. **paid 전환 (일별)**
   - Insights → Trends → `purchase_completed` per day

3. **DAU**
   - Insights → Trends → ANY event (unique users) per day

4. **paywall_viewed → purchase_completed 일별 비율**
   - Custom formula = `purchase_completed / paywall_viewed` per day

저장 후 모바일 알림 설정 (Mixpanel iOS/Android 앱) → 매일 오전 9시 review.

---

## Pivot Trigger 모니터링 (M1 시점)

V1_EXECUTION_PLAN §Pivot Trigger 정량 임계치 = M1 누적 paid conversion < 2%.

Mixpanel → **Insights → Trends**

- Metric: `purchase_completed` / `permission_granted` (cumulative)
- Period: 30 days from launch
- 알림 설정: 30일째 임계치 < 2% 이면 본인 메일로 알림

---

## 정기 리뷰 cadence

| 빈도 | 무엇을 보나 |
|---|---|
| **매일** | View 4 (Daily KPI Dashboard) |
| **매주 월요일** | View 1 (Funnel drop-off) + View 3 (공유율) |
| **매월 초** | View 2 (D30 Retention) + Pivot Trigger 임계치 |

---

## 광고 / 추적 정책

Mixpanel free tier 는 anonymizing 옵션 있음. 한국 PIPA 준수 위해:
- IP anonymize: ON
- Geo lookup: 시·도 수준만 (구·동 X)
- User properties 에 본명·전화번호 절대 보내지 말 것

코드 측에서 `distinct_id` = user.id (UUID) 사용. 개인 식별 정보 0.

---

## 백업 / Export

Mixpanel free tier 는 데이터 보존 기간 제한 있음 (12개월). 월 1회 export 권장:

- Mixpanel → Data Management → Export
- JSON 형식으로 본인 Google Drive 에 저장

이 데이터가 사업 자산 (1인 워커 시간 사용 패턴) — Phase 2·매각 시점에 가치.

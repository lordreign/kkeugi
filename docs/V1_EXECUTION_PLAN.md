# 끊기(KKEUGI) V1 실행 우선순위 및 개선안 — v2

## 문서 목적

본 문서는 사업성 검토 및 PRD 리뷰를 기반으로 실제 출시 직전 단계에서 수행해야 할 작업을 우선순위 순으로 정리한 실행 계획서이다.

중요한 점은 본 문서가 장기 전략 문서가 아니라는 것이다.

목표는 오직 하나이다.

> 출시 후 사용자가 실제로 매출환산 기능에 돈을 지불하는지 검증한다.

그 외의 모든 기능은 이후 단계에서 검토한다.

**v2 변경점**: PHASE 매핑, 손실 계산식, Streak break 정책, AI 코치 발송 timing, feature flag 인프라, 인터뷰 모집 plan, pivot trigger 정량 criteria, KPI 측정 cadence 8가지 명세 추가.

---

# 핵심 가설

현재 사업의 성패는 아래 질문 하나로 압축된다.

> 사용자는 "시간 손실"보다 "금전 손실"에 더 강하게 반응하는가?

예시

무료 사용자

```
오늘 47분을 흩어졌습니다.
```

유료 사용자

```
오늘 47분을 흩어졌습니다.

예상 손실 금액
₩23,500
```

만약 사용자가 이 차이에 월 ₩5,900을 지불한다면 사업은 성립한다.

그렇지 않다면 향후 AI 행동 코치 등 다른 유료 가치를 찾아야 한다.

---

# Pivot Trigger (정량 + 정성 동시 충족 시)

V1 출시 후 **M1 시점(출시 30일)** 에 아래 두 조건이 모두 충족되면 매출환산 가설 실패로 판단하고 V1.5 에서 AI 행동 코치 paid 로 hook 이전 + 매출환산 무료화.

| 조건 | 임계치 |
|---|---|
| 정량 | 누적 paid conversion < **2%** (≒ 보수 시나리오 4% 절반) |
| 정성 | 인터뷰 5명 중 **4명 이상**이 "₩ 표시 무감각" 응답 |

둘 다 충족하지 않으면 V1 path 유지 + V1.5 보강.

---

# 현재 단계에서 하지 말아야 할 것

## AI 행동 코치

보류

이유

* PMF 미검증
* 결제 검증 미완료
* 유지율 검증 미완료

좋은 아이디어지만 지금 필요한 기능은 아니다. V1.5 편입.

---

## A/B 테스트 (분석만 보류, 인프라는 출시 전 준비)

분석 보류

이유

현재 클로즈드 테스트 규모

* 12명
* 15명 수준

에서는 통계적으로 의미 있는 결과를 얻을 수 없다.

지금 필요한 것은

* 정량 실험

이 아니라

* 정성 인터뷰

이다.

**단, feature flag 인프라는 출시 전 구축한다** — 출시 후 누적 사용자 500명 도달 시점에 즉시 A/B 가능하게 하기 위함. 인프라 없이 시작하면 그때 또 1-2주 빌드 사이클 추가됨.

---

# V1 출시 전 필수 작업 (총 ~4일)

각 작업의 PHASE 매핑은 `docs/REMAINING-WORK-email.md` 의 7 PHASE 기준.

| # | 작업 | 작업량 | PHASE | 종류 |
|---|---|---|---|---|
| 1 | Threshold 무료화(1개) | 0.5-1일 | PHASE 2 (백엔드 배포 전) | 코드 |
| 2 | 손실 누적 Paywall | 0.5-1일 | PHASE 2 (코드+UI) | 코드 |
| 3 | 포지셔닝 카피 변경 | 0.5일 | PHASE 6-A (Store listing) | 문서 |
| 4 | KPI 재정의 + Mixpanel 셋업 | 1일 | PHASE 2-D 직후 (Mixpanel 토큰 받은 시점) | 문서 + 셋업 |
| 5 | Employment Risk PRD 섹션 | 0.5일 | PHASE 0 (지금) | 문서 |
| 6 | V2 우선순위 재정렬 | 0.5일 | PHASE 0 (지금) | 문서 |
| 7 | **feature flag 인프라 (신규)** | 1일 | PHASE 2 (백엔드 배포 전) | 코드 |

---

## 1. Threshold 무료화

우선순위: 최고
예상 작업량: 0.5-1일
PHASE: 2 (백엔드 배포 전 코드 변경)

---

현재

Threshold 생성

↓

유료(전부)

---

문제

행동 변화 기능 자체를 무료 사용자가 사용할 수 없다.

---

추천

무료

* Threshold **1개**

유료

* Threshold 무제한

---

기대 효과

* Retention 증가
* 행동 변화 경험 제공
* 결제 모수 확보

---

구현 명세

* 백엔드 `POST /v1/thresholds`: require_paid 제거 → 사용자 thresholds count 조회 후 **2번째 이상부터** 402 응답
* 프론트 `ThresholdsScreen` "한도 추가" CTA: list 길이 0 → 무료 진입 가능 / 1 이상 + 무료 → paywall 진입
* 카피 변경: "한도 추가" 버튼 옆 무료 안내 ("무료는 1개까지")

---

## 2. 손실 누적 Paywall

우선순위: 최고
예상 작업량: 0.5-1일
PHASE: 2 (코드+UI)

---

현재 Paywall

```
월 ₩5,900
```

---

추천

Paywall 직전

```
이번 달

당신은

230분을 흩었습니다

예상 손실

₩115,000
```

표시 후 plan 옵션 노출

---

기대 효과

* 손실 회피 심리 자극
* 결제 전환율 상승

---

주의

손실 금액은 **홈 화면에 상시 노출하지 않는다**. Paid 가치 보존을 위해 Paywall 진입 시점에만 1회 노출.

---

### 손실 계산식

```
손실(원) = (월초 ~ 현재 분 단위 합계) × (시급 / 60)
```

기간 정의

* 월초 = 매월 1일 00:00 Asia/Seoul
* 현재 = 사용자의 paywall 진입 시점

시급 정의

* 1순위: 사용자가 onboarding 또는 설정에서 입력한 hourly_value
* 2순위 (default): ₩30,000/h — 본인 ICP 1인 워커 추정치
* 권장: **onboarding 시 시급 입력을 필수 step 로 승격** → default 의존 회피

백엔드

* `GET /v1/usage/stats/month-loss` 신규 엔드포인트
* 응답: `{ "minutes": 230, "loss_won": 115000, "hourly_value": 30000 }`
* 무료/유료 모두 호출 가능 (paywall 노출 전 사용)

---

## 3. 포지셔닝 카피 변경

우선순위: 최고
예상 작업량: 0.5일
PHASE: 6-A (Store listing 작성 시점)

---

현재

```
디지털 디톡스 앱
```

---

변경

```
시간빚 추적 앱
```

---

적용 위치

* Store Listing 제목·단문 설명·장문 설명
* Landing Page
* X 소개글
* PRD §1
* README

---

금지 표현 (메인 카피)

* 디지털 디톡스 앱
* AI 생산성 앱
* 집중력 관리 앱

---

추천 표현

* 당신의 시간빚을 보여주는 앱
* 쇼츠 때문에 잃은 시간을 추적하세요
* 집중력 손실을 확인하세요
* 시간을 돈으로 환산하세요

---

ASO (검색 최적화) 절충

Play Store 카테고리 = **자기계발** ("디지털 디톡스" 카테고리 X)

검색 키워드(앱 설명 안에 자연스럽게 포함)

* 디톡스
* 집중력
* SNS 끊기
* 쇼츠 차단
* 시간 관리

→ **메인 카피 = "시간빚 추적", 검색 노출용 보조 키워드 = "디톡스 등"** layered 전략.

---

영어 병기 정책

* 메인 = 한글 "시간빚 추적"
* 보조 = X(트위터) 카피 등에서 "Time Debt" 가벼운 병기 가능
* 한국 시장 메인 노출에는 영어 단독 X

---

## 4. KPI 재정의 + Mixpanel 셋업

우선순위: 높음
예상 작업량: 1일
PHASE: 2-D 직후 (Mixpanel 토큰 받은 시점)

---

기존

* 다운로드
* 결제율

---

변경

### Tier 1 — D30 Retention

목표 (base): **12%**
Stretch Goal: 25%

근거: 디톡스 카테고리 평균 D30 = 8-15% (data.ai 추정). 12% = 카테고리 median 부근, 25% = best-in-class.

측정 timing: 출시 후 **30일 이후만 측정 가능**
리뷰 cadence: **월간**

---

### Tier 2 — 회고 카드 공유율

목표 (base): **5%**
Stretch Goal: 15%

근거: 일반 SaaS 공유율 3-7%. 디톡스 + 회고 카드는 공유 동기 강함 (체면 효과). base 5%, stretch 15%.

측정: weekly `report_shared / report_viewed`
리뷰 cadence: **주간**

---

### Tier 3 — 유료 전환율

목표: **4~7%** (PRD §8 보수~기본 시나리오)

측정: 누적 `purchase_completed / 누적 install` (Mixpanel funnel)
리뷰 cadence: **주간**

---

### Mixpanel 대시보드 셋업 명세 (PHASE 2-D 직후 본인 작업)

Mixpanel 콘솔에서 4개 view 생성:

1. **Funnel "Activation → Paid"**
   - Step 1: `permission_granted`
   - Step 2: `report_viewed`
   - Step 3: paywall 진입 (custom event 신규 필요 — 출시 전 작업 2 에서 함께 추가)
   - Step 4: `purchase_completed`

2. **Cohort Retention chart**
   - 이벤트: `permission_granted` 기준 cohort
   - retention 이벤트: 임의의 session 발생 (custom event `session_started` 추가)
   - 표시: D1, D7, D14, D30

3. **공유율 ratio chart**
   - 분자: `report_shared` (주간)
   - 분모: `report_viewed` (주간)

4. **Daily KPI dashboard**
   - 일별 신규 install
   - 일별 paid 전환
   - 일별 활성 사용자

---

## 5. Employment Risk PRD 섹션 추가

우선순위: 높음
예상 작업량: 0.5일
PHASE: 0 (지금, 코드 X)

---

사업 최대 리스크

경쟁

아님

---

회사 겸업 발각

임

---

PRD 별도 섹션 생성

제목: **Employment Risk**

---

관리 대상

* 개발자명 (Play Console Individual = `pjshi`, 본명 X)
* 결제 구조 (V1 = Google Play Billing Individual / V2 사업자 결정 시점)
* 도메인 (`kkeugi.kr` whois — privacy 보호 등록)
* 개인정보 (개인정보처리방침 contact email = 개인 메일)
* 세금 신고 시점 (M3 매출 trigger ₩35-50만/월 도달 시 사업자 등록 검토)
* 사업자 등록 시점 (V2 진입 = 본인 직장 관계 정리 후)

---

발각 시 비용

* 직장 손실 risk
* 사업 자체 손실보다 큼

따라서 모든 V1 결정(가격·기술·플랫폼·홍보)은 **이 risk 가 base** 임을 명시.

---

## 6. V2 우선순위 재정렬

우선순위: 높음
예상 작업량: 0.5일
PHASE: 0 (지금, 문서)

---

현재

iOS 진입 우선

---

추천

### V1

* PMF 검증 (매출환산 가설)
* D30 12% / 공유율 5% / paid 4-7%

### V1.5 (M1 ~ M3)

* Streak (V1.5 §1 참조)
* 공유 강화 (streak 표시 추가)
* AI 행동 코치 (월간 Deep Report, V1.5 §2 참조)

### V2 (M3 매출 trigger 도달 후 사업자 등록 결정 시)

* 사업자 등록
* Toss 외부 결제 (Google Play 30% → 3.3%)
* 카카오톡 알림톡 추가
* **iOS Companion 은 V2 후반 또는 V3** (사업자 등록 + Apple Developer $99 비용 동반 시점)

---

## 7. Feature Flag 인프라 (신규)

우선순위: 중
예상 작업량: 1일
PHASE: 2 (백엔드 배포 전, 코드)

---

목적

* 출시 후 사용자 500명 도달 시점에 **즉시 A/B 가능**하게 하기 위한 인프라 사전 구축
* 현재 활성 flag 0개 (인프라만 깔고 대기)

---

구현 명세

백엔드

* `app/feature_flags.py` 모듈 신규
* `GET /v1/feature_flags` 엔드포인트 (인증 필요)
* 응답: `{ "flags": ["show_loss_paywall_v2", ...], "bucket": "A" | "B" }`
* 버킷 할당 = `hash(user_id + flag_name) % 100` 기반 결정론적

프론트

* `core/flags/feature_flags_provider.dart` — 로그인 직후 1회 fetch, in-memory 캐시
* 사용 패턴
  ```dart
  final flags = ref.watch(featureFlagsProvider).valueOrNull;
  if (flags?.has('show_loss_paywall_v2') ?? false) { ... }
  ```

첫 A/B 후보 (출시 후 시작)

* 손실 누적 paywall 카피 A/B (₩ 회복 vs ₩ 손실)
* 매출환산 노출 강도 A/B (홈 노출 X / 회고만 / 회고 + 홈 약하게)

---

# 출시 직후 해야 할 일

## 사용자 인터뷰 5명

필수

### 모집 plan

* 출시 후 1주 안에 다운로드한 사용자 중 **paid conversion 완료자 3명 + 미전환 사용자 2명**
* 모집 채널: 앱 안 설정 화면에 "1:1 피드백 인터뷰 (Notion 폼 링크)" 배너 1주만 노출
* 인센티브: 커피쿠폰 ₩5,000 (5명 = ₩25,000)
* 방법: Zoom 또는 카카오톡 음성 15분 (1:1)
* 분석: 녹취 + 4가지 질문별 노트 + 동일 표현 빈도 코딩

---

### 질문

#### 1
가장 충격적인 화면은?

#### 2
₩ 표시를 보고 어떤 생각이 들었나요?

#### 3
(paid 전환자) 왜 결제했나요? / (미전환자) 왜 결제하지 않았나요?

#### 4
(미전환자) 어떤 기능이면 결제할 의향이 있나요?

---

이 4개 질문만으로도 PMF 단서 + Pivot Trigger 정성 측정 가능.

---

## Mixpanel 분석 (KPI 재정의 §4 참조)

관찰 Funnel

```
permission_granted
↓
report_viewed
↓
paywall_viewed (출시 전 작업 2 에서 추가되는 신규 이벤트)
↓
purchase_completed
```

---

이탈 구간 확인 → 가장 큰 drop-off 구간이 V1.5 개선 1순위.

---

# V1.5 우선순위

## 1. Streak

조건

* 활성 Threshold 존재 (최소 1개)
* Threshold 미초과

---

### Break 정책

* **카테고리 별 streak** (예: "SNS streak 14일")
  - 전체 streak 단일화 X → 한 카테고리 실패가 모든 streak 0 으로 가는 가혹함 회피
* **주 1회 면제 (grace day)**
  - Snapchat streak 패턴 차용. 한 주에 1번 초과는 streak 유지.
  - 2번 이상 초과 시 그 카테고리 streak 0 reset.

---

예시

* SNS 7일 연속 성공
* 게임 30일 연속 성공

---

공유 카드에 포함

예시

"SNS 30일 연속 목표 달성"

---

## 2. AI 행동 코치

예시

```
당신은

매주 화요일
14:00~16:00

집중력이 가장 크게 무너집니다.
```

---

### 발송 timing

* **매월 첫 일요일 22:00 KST** (주간 회고와 같은 cadence, 충돌 방지 위해 첫 주 격주 X 검토)
* 채널: 사용자가 주간 회고를 받는 **같은 채널** 자동 선택 (Telegram / 이메일 / FCM)
* 무료 사용자: **첫 1줄 + "더 보기는 Pro" 잠금**
* 유료 사용자: 전체 4-6줄 deep report

---

### 비용 통제

* 로컬 패턴 분석 = Drift SQLite 쿼리로 요일·시간대 통계 추출
* LLM 입력 = 통계 요약만 (raw events X)
* prompt caching 활용 (시스템 프롬프트 캐시)
* 예상 비용: 5,000명 유료 시 ₩30K/월 (Haiku, 캐시 적용)

---

# V2

조건

월 매출 안정화 + M3 매출 trigger 도달

---

진행

* 사업자 등록
* Toss 외부 결제
* 카카오톡 알림톡 추가
* (V2 후반 또는 V3) iOS Companion

---

효과

Google Play 30%

↓

Toss 3.3%

---

마진 대폭 개선 (1,000명 paid 시 +₩1.5M/월 margin gain)

---

# 최종 결론

현재 끊기의 성공 여부는

Flutter

UsageStatsManager

FastAPI

Supabase

같은 기술 요소가 결정하지 않는다.

성공 여부는 아래 질문 하나가 결정한다.

> 사용자가 "47분 손실"보다 "₩23,500 손실"에 실제로 돈을 지불하는가?

이 가설이 검증되면 사업은 성장 가능성이 높다.

이 가설이 실패하면

AI 행동 코치와 행동 패턴 분석이 다음 유료 가치가 되어야 한다.

따라서 지금 단계의 모든 개발 우선순위는

"매출환산 가치 검증"

을 중심으로 정렬되어야 한다.

---

# 변경 이력

| 날짜 | 변경 | 사유 |
|---|---|---|
| 2026-06-05 v1 | 6개 출시 전 작업 + Pivot Trigger + 인터뷰 4질문 + Mixpanel funnel | 사업성 검토 + PRD 리뷰 기반 |
| 2026-06-05 v2 | PHASE 매핑 표 + 손실 계산식 + Streak break 정책 + AI 코치 timing + feature flag 인프라 + 인터뷰 모집 plan + Pivot trigger 정량 임계치 + KPI cadence 8가지 명세 추가 | 실행 plan 측면 보강 |

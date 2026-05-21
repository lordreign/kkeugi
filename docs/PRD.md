---
name: "끊기 — 1인 워커 디지털 디톡스 Android 앱 (Flutter, 집중 시간 회복 + AI 매출 환산 리포트)"
slug: "kkeugi-habit-stop-timer"
domain: "b2c_mobile_app"
status: "deepdive"
created_at: "2026-05-18"
evaluated_at: "2026-05-21"
deepdive_at: "2026-05-21"
total_score: 82.5
verdict: "pass"
go_no_go: "GO"
sources:
  - "korea-app-charts"
  - "plan-ceo-review-2026-05-21"
  - "deepdive-research-2026-05-21"
  - "platform-pivot-android-flutter-2026-05-21"
---

<!--
파일 저장 경로: docs/candidates/b2c_mobile_app/deepdive/2026-05-18-kkeugi-habit-stop-timer.md
2026-05-21 deepdive 작성 후 같은 날 platform pivot.
PWA → Android 네이티브 (Flutter) 단일 시드로 전환 — 핵심 wedge #2 (스크린타임 자동 import) 가 PWA 단독 불가 사실 확정에 따라 audit 가정 2 재재정의.
사용자 선호: Flutter 기반 (persona.md 신규 학습 1~2주 마진 반영).
GO/NO-GO: GO (Android UsageStatsManager 표준 API, PoC 불요. iOS는 v2 격하).
-->

# 끊기 — 1인 워커 디지털 디톡스 Android 앱 (Flutter) · PRD

## 1. 요약

### 한 문장 정의
**한국 1인 워커**(개발자·디자이너·작가·연구자·프리·1인 사업자)에게 SNS·쇼츠·게임 끊기 타이머 + 스크린타임 자동 import + AI 주간 "회복된 집중 시간 → 매출 환산" 리포트를 제공하는 **Android 네이티브 앱 (Flutter)**. 카톡 채널(알림톡 정보성) 알림·인증·공유. 일회 ₩9,900 인증서 + 구독 ₩4,900/월 hybrid. **iOS는 Phase 1 PMF 확인 후 v2**.

### 핵심 후크
1. 한국 디지털 디톡스 vertical 비어있음 (Forest·간단 모두 1인 워커·매출 환산·카톡 wedge 안 함)
2. 본인이 곧 ICP — 콘텐츠·UX·우선순위 추측 0
3. **Android 단일 시드 (Flutter) + Toss 외부 결제 + 카톡 채널** = 김윤후 '간단' 검증 패턴 정확 답습. UsageStatsManager 표준 API로 wedge #2 (자동 import) 즉시 확보. iOS Family Controls 승인 의존 제거. 자본 약 ₩50만 (capital_krw_10k 의 50%) 내 MVP.

### GO/NO-GO 한 줄 결론
**GO** — Android UsageStatsManager 는 표준 API ([Android Developers](https://developer.android.com/reference/android/app/usage/UsageStatsManager)), 사용자 동의 1회로 접근 가능. iOS Family Controls 승인 1~3주 의존성 제거됨. 디지털 디톡스 카테고리는 Play Store 풍부 → 심사 risk 매우 낮음. Phase 1 W1~W8 (Flutter 학습 W1 포함) 안에 MVP 출시 가능. iOS는 Phase 1 매출 ₩200만/월 도달 후 자가 자본으로 v2 진입.

### 1년차 목표 (보수)
- Phase 1 (M0~M6): 월 평균 ₩48만 (시드 ₩100~150만 도달 시 인플루언서 1명 추가)
- Phase 2 (M7~M12): ₩300~500만/월 (B-2 또는 B-3 분기 결과)
- Y1 매각 시나리오: ₩1.2~2.4억 (인디 인수, Phase 2 진입 시 ₩1~2억 헬스/라이프 vertical 매수자)

---

## 2. 시장

### TAM / SAM / SOM

| 단위 | 정의 | 규모 | 출처 |
|---|---|---|---|
| **TAM (한국)** | 한국 전체 1인 사업체·프리랜서·특수고용·자영업자 | 약 400만~500만 명 | 통계청 비임금근로자 2024, [파이낸셜뉴스 2026](https://www.fnnews.com/news/202605011637374675) (특수고용+플랫폼+프리 210만) + 자영업자 약 500만 |
| **SAM (한국 1인 워커 IT/지식)** | 한국 IT/디자인/콘텐츠/작가/연구 직군 — 집중 시간이 직접 매출인 segment | 약 100만~150만 명 (추정) | 통계청 IT 종사자 약 100만 + 디자인·콘텐츠 프리 약 50만 (추정) |
| **SOM (Y1)** | 본인 채널(X 인디·긱뉴스·okky·노션 한국) + 인플루언서 1명 도달 가능 | 무료 5,000명 / 유료 200~300명 | 김윤후 '간단' 초기 성장 패턴 패러디 (추정) |

### 한국 경쟁사 정밀 비교

| 경쟁자 | 가격 | DL/사용자 | 강점 | 약점 (우리 wedge) |
|---|---|---|---|---|
| **Forest** (글로벌, 한국 유저 많음) | 일회 ₩3,300 | 누적 6,000만 DL ([Forest](https://www.forestapp.cc/)) | 게임화·이쁨, 카테고리 1위 | 매출 환산 X, 1인 워커 메시지 X, 카톡 X, 한국화 약함 |
| **Stay Focused / 포레스트 류** | 무료 + 광고 | 100만+ (추정) | 차단 기능 단순 | UX 산만, 구독 모델 약함, 자동 import X |
| **챌린저스** | 보증금 + 쇼핑 | 누적 171만, 5,000억 거래 ([Platum](https://platum.kr/archives/226879)) | 종합 챌린지 1위, 보증금 강제 | 1인 워커 특화 X, 디지털 디톡스 단일 아님 |
| **간단 (Liviet)** | freemium 구독 | 250만 DL, 일 ₩20~40만 ([Play Store](https://play.google.com/store/apps/details?id=kr.co.hoo.gandan), [eopla 2024](https://eopla.net/magazines/31129)) | 단식 단일 vertical 6년 검증, 김윤후 본인이 ICP | 단식 1개만. 디지털 디톡스 안 함. 인접 행동 확장 시 직접 경쟁 (리스크 #1) |
| **루티너리** | 구독 ₩4,400~6,600/월 | 200만+ DL (추정) | 종합 루틴 1위 | UX 복잡. 매출 환산 wedge 없음. 디톡스 단일 vertical 아님 |
| **노션·옵시디언** | $10/월 | — | 집중 워크플로 | 차단·인증·OS 데이터 X |

**우리 wedge 3개**
1. **"회복된 집중 시간 → 매출 환산" AI 주간 리포트** — 한국 누구도 안 함. 1인 워커 결제 motivation 핵심 trigger.
2. **iOS Screen Time + Android Digital Wellbeing 자동 import** — 수동 입력 불필요 (※ T6 PoC 필수)
3. **카톡 채널 봇 알림·인증** — 한국 워커 일상 채널. 정보성 발송이라 2026.1.1 정책([Channel.io 공지](https://docs.channel.io/updates/ko/articles/공지-카카오-알림톡-발송-가능-기준-변경-안내2611-시행-f9f70118)) 위반 0.

### 글로벌 벤치마크

| 제품 | 매출/MRR | 카테고리 | 매각/투자 |
|---|---|---|---|
| **Opal** (US, iOS only) | **ARR $10M** (2025년 5월), 200k+ 유저 ([Speedinvest 2025](https://www.speedinvest.com/knowledge/scaling-smart-how-opal-built-a-10m-arr-business-in-just-2-years)) | 디지털 디톡스 (Screen Time API 1호 launcher) | 시리즈 A $4M, 11명 회사 |
| **Freedom** | ARR $20M+ (추정) | 차단·생산성 | 60만+ 유료, [Freedom.to](https://freedom.to/) |
| **Cold Turkey** | 일회 $39 buy-out | 데스크톱 차단 | 인디 sustained |
| **Forest** | $1.99~3.99 일회 | 게임화 집중 | 누적 6,000만 DL |
| **간단** (한국) | 일 ₩20~40만 (월 ₩600~1,200만) | 단식 단일 vertical | 250만 DL, 김윤후 1인 인디 |

→ Opal $10M ARR 단 2년 / 11명, **iOS 한정** 임에도 디톡스 vertical만으로 도달. 한국에서 동일 카테고리·동일 wedge × 1인 워커 narrow ICP × hybrid 가격 × 카톡 채널은 비어있음.

---

## 3. 타깃 사용자

### 페르소나 1: "민준" (32, 1인 개발자 / SaaS 운영자)
- **일상**: 오전 9시 슬랙·메일 확인 → 코딩 2시간 → 인스타·X 30분 (집중 깨짐) → 점심 → 유튜브 쇼츠 1시간 → 오후 코딩 (집중 끊김 반복) → 저녁 자기 SaaS MRR 확인 → 침대에서 릴스 2시간
- **통점**:
  - 일 SNS·쇼츠 3시간 30분 = 시간당 가치 ₩50,000 기준 일 ₩175,000 기회비용
  - 본인 SaaS MRR ₩2,000,000 인데 "이번 달 신기능 못 만든 이유는 시간 부족" 매일 자각
  - Forest 써봤으나 잠금 풀고 다시 봄. 일주일 만에 삭제
- **현 해결책 한계**: 스크린타임 일일 limit 잠금 → 자기가 해제. 측정만 보고 환산 0. 친구한테 보여주기 부끄러움.
- **지불 의사**: 노션 $10/월, Cursor $20/월 익숙. ₩9,900 일회 인증서 "이번 달 한번 해보자" 마찰 낮음. 효과 있으면 ₩4,900/월 구독 자연 전환.

### 페르소나 2: "지영" (29, 프리 디자이너 / 일러스트레이터)
- **일상**: 외주 마감 일정 압박 + 인스타 피드 (영감 핑계로 2시간 스크롤) + 카톡 친구 단톡 + 유튜브 쇼츠. 매일 "내일은 진짜 집중" 다짐 후 반복.
- **통점**:
  - 외주 시급 환산 ₩40,000~70,000 — 일 ₩100,000 이상 기회비용
  - 의지 의존 솔루션 다 실패. 측정·환산·인증 데이터 없음.
- **현 해결책 한계**: 인스타 일시정지 → 다시 다운로드. 챌린저스 보증금 너무 부담. Forest는 카드 디자인 취향.
- **지불 의사**: 일회 ₩9,900 (외주 1건 시급 1/5) 부담 없음. 매출 환산 카드를 인스타 스토리에 1-tap 공유 가능하면 retention.

### 일상 통점 (공통)
- 평균 SNS·쇼츠 일 2~3시간 — 1인 워커는 본업 시간 직접 침해
- "줄였는지·매출에 영향 줬는지" 측정 데이터 없음
- 기존 차단 앱은 의지 의존, 1주일 후 복귀 사이클

### 지불 의사 단서
- 김윤후 '간단' freemium 전환율 한국 평균 10~20% (인디 메이커 공개 데이터, 추정)
- 1인 워커 평균 결제 의사 일반 소비자보다 높음 (노션·Cursor·Figma·Linear 월 $10~30 익숙)
- ₩9,900 일회 마찰 매우 낮음 (커피 2잔 수준)

---

## 4. 제품 (MVP)

### 핵심 기능 우선순위

1. **타깃 행동 설정 + 타이머 (P0)**
   - SNS(인스타·X·페북·스레드) / 쇼츠(틱톡·유튜브쇼츠·릴스) / 게임(모바일) 3종 프리셋
   - 일일 목표 시간 설정 (예: 30분/일)
   - 큰 타이머 화면 + 잔여 시간 시각화
2. **스크린타임 자동 import (P0, Android 표준 API 직접)**
   - Android: `PACKAGE_USAGE_STATS` 권한 → 사용자 동의 화면 1회 (Settings → 사용 정보 접근 허용) → Flutter platform channel 로 `UsageStatsManager` 직접 호출 → 앱별·시간대별 사용 데이터 fetch
   - 일 1회 백그라운드 동기화 → Firestore 저장
   - **iOS (v2)**: Apple Family Controls Entitlement 신청 + Swift Native Companion. Phase 1 매출 ₩200만/월 이후 자가 자본화 단계에서 검토
3. **AI 주간 회복 리포트 (P0 — 핵심 wedge)**
   - 매주 일요일 자동 생성
   - 1-shot 흐름: 이전 7일 사용 데이터 + 사용자 시간당 가치 → LLM 1회 호출 → 카드 1장
   - 출력 예: "이번 주 SNS 평균 4h 12m → 3h 05m 감소. 회복된 67분 × 시간당 ₩50,000 = **₩55,800 매출 환산**. 화요일 오후 슬럼프 시간이 가장 많이 줄었네요."
4. **카톡 채널 알림 (P1 — 정책 안전 범위)**
   - 카카오 채널 친구 추가 → **알림톡 (정보성)** 매일 22:00 일일 요약
   - 2026.1.1 정책 ([Channel.io](https://docs.channel.io/updates/ko/articles/공지-카카오-알림톡-발송-가능-기준-변경-안내2611-시행-f9f70118)) 준수: 마일리지·쿠폰 마케팅성 메시지 0, 사용자 본인 데이터 요약만
   - 친구톡은 2025.12.31 종료, 브랜드 메시지로 자동 대체 — 본 서비스는 알림톡 정보성만 사용
5. **프리미엄 / 일회 인증서 (P0)**
   - 무료: 행동 1종, 주 1회 AI 리포트, 카톡 알림 일 1회
   - **일회 ₩9,900**: 30일 디톡스 인증서 + AI 리포트 4주 무제한 + 매출 환산
   - **구독 ₩4,900/월 (또는 ₩39,000/년)**: 행동 무제한 + AI 리포트 무제한 + 카톡 봇 전체 + 스크린타임 90일 트렌드

### AI 1-shot 흐름

```
입력
- 사용자 ID, 시간당 가치(₩50,000 default)
- 지난 7일 OS 스크린타임 데이터 (앱별·시간대별)
- 지난 7일 사용자 목표 (예: SNS 30분/일)
- 전 주 baseline (비교용)

처리 (Claude Haiku / GPT-4o-mini 1회 호출, ~1.5k input + ~500 output tokens)
- 시간대별 패턴 인사이트 1개 추출 (예: "화요일 오후 슬럼프")
- 회복 분 × 시간당 가치 = 매출 환산
- 카드 카피 2~3문장 생성

출력
- 카드 1장 (JSON → PWA 렌더링)
- 1-tap 카톡/인스타 공유 (이미지 export)
```

### 비핵심 기능 (V2 이후)
- 그룹 챌린지 (페르소나 2 요청 추정)
- 시간당 가치 자동 추정 (외주 단가·연봉 입력 기반)
- 데스크톱 차단 (macOS extension)
- 다중 행동 동시 추적
- 인플루언서 챌린지 페이지

### UX 차별화
- **카드 디자인**: 김윤후 '간단' 스타일 (한국 정서 미니멀 + 한글 typo 최적화) — Forest의 게임화 ↔ Notion의 미니멀 사이 포지션
- **매출 환산 단위**: ₩ 명시. "67분 회복" 보다 "₩55,800 회복" 이 1인 워커에게 sharp
- **공유 1-tap**: 인스타 스토리 + 카톡 채팅 양쪽 export

---

## 5. 수익 모델

### 가격 구조

| 티어 | 가격 | 내용 |
|---|---|---|
| 무료 | ₩0 | 행동 1종, 주 1회 AI, 카톡 알림 일 1회 |
| 일회 인증서 | **₩9,900** | 30일 디톡스 + AI 4주 무제한 + 매출 환산 |
| 월 구독 | **₩4,900/월** | 전체 기능 + 90일 트렌드 |
| 연 구독 | **₩39,000/년** | 월 환산 ₩3,250 (33% 할인) |

### LTV 계산

- 일회 결제 LTV: ₩9,900
- 일회 → 구독 전환 30% × ₩4,900 × 5개월 평균 = ₩7,350 (추정, 김윤후 패턴 + 1인 워커 결제력 가정)
- **평균 LTV**: ₩9,900 + ₩7,350 = **₩17,250**
- 보수 가정 (전환 20%): ₩9,900 + ₩4,900 × 4 × 0.2 = ₩13,820

### CAC

| 채널 | CAC 추정 | 근거 |
|---|---|---|
| 본인 채널 (X 인디·긱뉴스·okky·노션) | **₩0~500** | 빌드 인 퍼블릭, 직접 게시 |
| 인플루언서 1명 (X 한국 인디 메이커 1만 팔로워급) | **₩500~1,500** | 시드 ₩30~50만 × 전환 200~600명 (추정) |
| Meta 광고 (V2) | ₩3,000~6,000 | 한국 b2c 유틸 평균 (추정) |

### Payback 기간
- 본인 채널: 즉시 (일회 결제 ₩9,900 > CAC ₩500)
- 인플루언서: 첫 결제 시점 (1~2일)
- Meta: 일회 결제만으로는 marginal — 구독 전환 후 3~5개월

### LTV/CAC
- 본인 채널: **₩17,250 / ₩500 = 34.5x**
- 인플루언서: **₩17,250 / ₩1,500 = 11.5x**
- Meta: ₩17,250 / ₩4,500 = 3.8x (V2 검토)

기준선 (LTV/CAC > 3x) 본인 채널·인플루언서 모두 충분히 통과.

---

## 6. GTM (Go-To-Market)

### 마케팅 채널 (한국 first)

| 채널 | 비용 | CPI/CPA 추정 | 도달 |
|---|---|---|---|
| **X (트위터) 한국 인디 메이커** | ₩0 | ₩0~200 | 본인 빌드 인 퍼블릭, 김윤후 모델 답습 |
| **긱뉴스 (news.hada.io)** | ₩0 | ₩100~500 | 1회 노출 500~2,000 view |
| **okky** | ₩0 | ₩300~800 | 개발자 도구·서비스 게시판 |
| **노션 한국 커뮤니티 (오픈톡·페북 그룹)** | ₩0 | ₩200~500 | 1인 워커 직접 도달 |
| **인플루언서 X 1명 (1만+ 팔로워, 인디 메이커)** | ₩30~50만 | ₩500~1,500 | 시드 페이즈 1회 |
| **YouTube 인디 메이커 (Geek News류)** | ₩50만 | ₩1,000~3,000 | V1.5 검토 |
| **Product Hunt (글로벌, V2)** | ₩0 | 변동 | Phase 2 영문화 시 |

### 첫 100 사용자 시나리오 (구체)

| Week | 액션 | 산출 |
|---|---|---|
| W1 | X 본인 계정 "1인 워커 디지털 디톡스 PWA 빌드 시작" 게시 + 노션 진행상황 공개 | 베타 신청 30~50 |
| W2 | 긱뉴스 "끊기 — 1인 개발자가 만든 디지털 디톡스 PWA (MVP 공개)" | 베타 신청 50~150 |
| W3 | okky · 노션 한국 그룹 동시 게시 + 본인 SaaS 운영자 X DM 10명 베타 초대 | 100명 활성 |
| W4 | 인플루언서 1명 시드 (₩30~50만) — "1인 개발자 실험 + AI 매출 환산 카드 share" 콘텐츠 | 200~500 신규 |

### 인플루언서 시드 후보 (X 한국 인디 메이커)
- 본인 일상 채널 1만~3만 팔로워급 인디 메이커 3~5명 콜드 DM
- 김윤후 '간단' 후기 작성한 사람 우선
- 시드 비용 ₩30~50만 × 1명 우선

### 한국 vs 글로벌
- M0~M6: **한국 100%** (위 채널)
- M7~M12: Phase 2 분기 시 글로벌 PH 검토 — 영문화 후 Opal 사용자 acquisition test

---

## 7. 기술 스택

### 아키텍처

| 레이어 | 스택 | 친숙도 (persona.md) |
|---|---|---|
| **모바일 앱 (메인)** | **Flutter 3.x (Dart)** + Material 3 | 중 (persona.md 2026-05-21 갱신 — RN+Expo 제거, Flutter "중" 본격 전환. 실제 첫 도입은 본 후보, 학습 timebox W1 1주) |
| **OS 데이터 접근** | Flutter platform channel → Kotlin → `UsageStatsManager` (PACKAGE_USAGE_STATS 권한) | 중 (Flutter 학습 후 platform channel 표준 패턴) |
| **백엔드 / DB / Auth** | Firebase (Firestore + Authentication + Cloud Functions + FCM) | 중 (persona.md "중") |
| **LLM** | Claude Haiku 3.5 (primary) + GPT-5 mini (fallback) | 상 |
| **결제** | Toss Payments 앱 결제 SDK (한국 인앱결제 외부 결제 허용 정책, 2022 시행) — 일회 + 구독 빌링키. 또는 Google Play Billing (수수료 30%, 가격 ₩11,000/₩5,900 인상 옵션) | 중 — 한국 PG 표준, 1주 학습 |
| **카톡 채널** | 카카오 비즈메시지 알림톡 (정보성 only) — Aligo / SOLAPI / DirectSend SDK | 중 |
| **푸시** | Firebase Cloud Messaging (FCM) — 앱 푸시 메인 + 카톡 알림톡 보조 | 중 |
| **iOS (v2 단계)** | Flutter 동일 코드베이스 + Swift Family Controls Native Companion | **하** (Phase 1 매출 후 외주 또는 학습) |

### 외주 항목

| 항목 | 한국 시세 | 검토 트리거 |
|---|---|---|
| **iOS Family Controls Native Companion (v2)** | ₩200~500만 (외주) | Phase 1 매출 ₩200만/월 도달 + iOS 사용자 수요 베타 신청 100명+ 시 자가 자본화 |
| **로고·일러스트** | ₩0 (Figma 무료 아이콘 + 본인 미니멀) | 매각 직전 V2 폴리시 |
| **카피라이팅** | ₩0 (본인 ICP) | 없음 |
| **법무 자문 (이용약관·개인정보처리방침)** | ₩30~50만 (1회 표준 검토) | W7 클로즈드 베타 직전 |

### Phase 1 자본 impact
- Flutter 신규 학습 — 본인 시간 1~2주 (W1 학습 + W2~ 빌드 병행) → 외주비 ₩0
- Android 단일 시드 → iOS Companion 외주 ₩0 (v2 격하)
- Phase 1 자본 합계: **약 ₩50만** (Google Play $25 = 약 ₩3.5만 + Flutter 학습 시간 비용 0 + 법무 ₩30~50만 + 인플루언서 시드 ₩30~50만 + 예비 ₩10만)
- → criteria `capital_krw_10k = 100` 의 50%, **exclusion 통과**

---

## 8. 운영 비용

### 월 고정비 (1인 운영, 사용자 1,000명 기준)

| 항목 | 금액 (만원/월) | 비고 |
|---|---|---|
| Firebase (Blaze 종량제) | 2.5 | Firestore + Auth + Cloud Functions + FCM, 1,000명 기준 약 $18/월 |
| Google Play 등록 | 0.3 | $25/년 일시 → 월 환산 |
| LLM API (Claude Haiku 3.5) | 1.0 | 1,000명 × 4 리포트/월 × ~$0.005 = $20/월 (아래 정밀 모델 참조) |
| 카카오 알림톡 발송 | 1.5 | 1,000명 × 30회/월 × ₩10~15/건 = ₩30~45만 → 무료 사용자 절반 1일 1회로 한정 시 ₩15만 |
| FCM 푸시 | 0 | 무료 (Firebase 포함) |
| Toss Payments PG 수수료 | 매출의 3.3% (변동비) | 일회 ₩9,900 → 약 ₩327 차감. 외부 결제 사용 시 Google Play 30% 우회 |
| 법인·세무 (간이사업자) | 0 | M0~M6 개인 사업자 유지. 매출 ₩300만/월 이후 법인 검토 |
| 도메인·랜딩 (선택) | 0.5 | Vercel 무료 + 도메인 연 ₩2만 — 마케팅 랜딩 페이지 용도만 |
| **합계 (1,000명)** | **약 5.8만/월** | LTV/CAC 와 무관한 고정 부담. PWA 대비 Vercel·Supabase 통합으로 ₩3만 절감 |

### 변동비 단가

| 단위 | 단가 | 출처/근거 |
|---|---|---|
| LLM 1리포트 (Haiku 3.5) | ~$0.005 (~₩7) | input 1,500t × $0.80/M + output 500t × $4.00/M = $0.0012 + $0.002 = $0.0032 (약 ₩4.5) — 카드 디자인 prompt 합치면 ~$0.005 ([Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| LLM 1리포트 (GPT-5 mini fallback) | ~$0.002 (~₩3) | input 1,500t × $0.25/M + output 500t × $2.00/M = $0.00037 + $0.001 = $0.0014 |
| 카톡 알림톡 1건 | ₩10~15 | 한국 비즈메시지 표준 ([SOLAPI](https://solapi.com/guides/kakao)) |
| Toss PG 수수료 | 매출의 3.3% | 일회 ₩9,900 → ₩327, 구독 ₩4,900 → ₩162 |

### LLM 비용 모델링 (1,000 / 5,000 / 20,000 사용자)

전제: 무료 50% (월 1리포트) + 일회/구독 50% (월 4리포트). Claude Haiku 3.5 단가 (input $0.80/M, output $4.00/M).

| 사용자 | 월 리포트 수 | 월 input tokens | 월 output tokens | 월 LLM 비용 | 월 LLM 비용 (₩) |
|---|---|---|---|---|---|
| 1,000 | 2,500 | 3.75M | 1.25M | $0.003 × 2,500 = **$7.50** | ₩10,500 |
| 5,000 | 12,500 | 18.75M | 6.25M | **$37.50** | ₩52,500 |
| 20,000 | 50,000 | 75M | 25M | **$150** | ₩210,000 |

→ 20,000명 도달해도 LLM 비용 월 ₩21만. ARPU ₩300~500/월(blended) × 20,000 = 매출 ₩600~1,000만/월 대비 2~3% — 매우 sustainable.

GPT-5 mini fallback 채택 시 위 비용 약 40% 감소.

---

## 9. 매출 시뮬레이션

### Phase 1 (M1~M6) — B-1' 단일 vertical 시드

전제:
- 무료 사용자 acquisition: M1=300, M2=600, M3=1,000, M4=1,800, M5=3,000, M6=5,000 (보수 누적)
- 일회 결제율 4% (보수) / 6% (기본) / 10% (공격)
- 일회 → 구독 전환 20% (보수) / 30% (기본) / 40% (공격)
- 구독 평균 유지 기간 4개월 (보수) / 5개월 (기본) / 6개월 (공격)

| 월 | 누적 무료 | 보수 (₩만) | 기본 (₩만) | 공격 (₩만) |
|---|---|---|---|---|
| M1 | 300 | 12 | 18 | 30 |
| M2 | 600 | 24 | 36 | 60 |
| M3 | 1,000 | 40 | 60 | 100 |
| M4 | 1,800 | 72 | 108 | 180 |
| M5 | 3,000 | 120 | 180 | 300 |
| M6 | 5,000 | 200 | 300 | 500 |
| **Phase 1 누적** | — | **468** | **702** | **1,170** |
| **Phase 1 월평균** | — | **78** | **117** | **195** |

(보수 계산 예 M6: 5,000 × 4% × ₩9,900 + 일회 200명 중 누적 구독 ~80명 × ₩4,900 ≈ ₩198만 + ₩39만 ≈ ₩237만 → 신중하게 200만으로 조정)

→ evaluated 단계의 보수 ₩48만/월(M0~M6 평균)은 M1~M3 비중이 높았던 것. M6 단일 월은 보수 시나리오에서도 ₩200만 도달 가능.

### Phase 2 (M7~M12) — B-2 또는 B-3 분기

M7 시점 KPI:
- 무료 5,000명 / 일회 200~300명 / 구독 60~100명 / retention(D30) 25%+ → GO 진입
- 미달 시 Phase 1 재진단

#### 옵션 A: B-2 (ICP 확장)
- 추가 segment: 학습자 (대학원생·고시생·자기개발 직장인)
- 채널 추가: 디시 + 에브리타임 + 자기개발 유튜브
- 시뮬레이션 (기본):

| 월 | 누적 무료 | 매출 (₩만, 기본) |
|---|---|---|
| M7 | 6,500 | 350 |
| M8 | 8,500 | 420 |
| M9 | 11,000 | 480 |
| M10 | 14,000 | 540 |
| M11 | 17,000 | 600 |
| M12 | 20,000 | 700 |

#### 옵션 B: B-3 (행동 확장)
- 추가 행동: 카페인·수면 부족 추적
- ICP 동일 (1인 워커)
- 시뮬레이션 (기본): M7~M12 매출 ₩300 → ₩550만 (행동 확장은 ARPU 상승, 사용자 수는 상대 보수)

### 누적 매출 / BEP

| 시나리오 | Y1 누적 매출 | Y1 누적 수익 (운영비 차감) | BEP 시점 |
|---|---|---|---|
| **보수** | 약 ₩1,800만 | 약 ₩1,000만 | M5 |
| **기본** | 약 ₩3,500만 | 약 ₩2,500만 | M3~M4 |
| **공격** | 약 ₩5,500만 | 약 ₩4,200만 | M2~M3 |

(운영비 = 월 8.8만 × 12 + 알림톡 변동 + 마케팅 ₩50~150만 가정)

---

## 10. 매각 시나리오

### 매각 적합 시점
- ARR ₩500만/월 (= ARR ₩6,000만/년) 도달 시 — Phase 1 보수 시나리오 M6
- ARR ₩2,000만/월 (= ARR ₩2.4억/년) 도달 시 — Phase 2 기본 M12

### 매각 multiple 추정 (한국·글로벌 인디 앱 사례)

| 사례 | multiple | 적용 가능성 |
|---|---|---|
| Cal AI 매각 | 4.5x ARR | 글로벌 AI 카테고리 1위 (높음) |
| 한국 인디 카테고리 1~2위 (Umax류) | 2~3x ARR | 본 후보 직접 적용 |
| Microacquire/Acquire.com 평균 | 2~4x ARR | Phase 1 종료 시 (1.5x~3x 적용) |
| 헬스/라이프 vertical 매수 (모바일닥터·강남언니·닥터다이어리) | 2~3x ARR | Phase 2 행동 확장 시 |

### 잠재 인수자 후보

| 인수자 | 매각 트리거 | 추정 multiple |
|---|---|---|
| **김윤후 (Liviet)** | Phase 1 종료 시점 (단식 vertical → 디톡스 인접 확장) | 2~3x ARR |
| **챌린저스 (브랜드모피어스)** | Phase 2 ICP 확장 (학습자 segment) | 2x ARR |
| **루티너리** | Phase 2 행동 확장 | 1.5~2.5x ARR |
| **모바일닥터·강남언니·닥터다이어리** | 카페인·수면 등 디지털 헬스 인접 | 2~3x ARR |
| **임팩티브·라포랩스** | 라이프스타일 vertical | 2~3x ARR |
| **Microacquire / Acquire.com (글로벌)** | 영문화 후 (Phase 2 후반) | 2~4x ARR |

### 매각가 추정 (Y1 종료 시점)

| 시나리오 | ARR | multiple | 매각가 |
|---|---|---|---|
| **Phase 1 유지 (보수)** | ₩600만/년 (월 ₩50만) | 2~3x | **₩1,200만 ~ ₩1,800만** |
| **Phase 1 유지 (기본)** | ₩1,500만/년 (월 ₩125만) | 2~3x | **₩3,000만 ~ ₩4,500만** |
| **Phase 2 B-2/B-3 진입 (기본)** | ₩6,000만/년 (월 ₩500만) | 2~3x | **₩1.2억 ~ ₩1.8억** |
| **Phase 2 공격** | ₩1.2억/년 (월 ₩1,000만) | 2~3.5x | **₩2.4억 ~ ₩4.2억** |

→ evaluated 단계 시나리오 (₩1.2~2.4억) 는 Phase 2 진입 기본 시나리오에 부합.

---

## 11. 리스크 5종 + 완화책

| 분류 | 리스크 | 영향 | 완화책 |
|---|---|---|---|
| **기술** | (a) Android `PACKAGE_USAGE_STATS` 사용자 동의 거부율 ↑ → 자동 import 무산, (b) Flutter 신규 학습 1~2주가 4주로 늘어남, (c) iOS v2 진입 시 Family Controls entitlement 거부 | **MEDIUM** — Android UsageStatsManager 자체는 표준 API로 거부 risk 0, 사용자 동의 UX 설계로 동의율 80%+ 가능 (Forest·간단·StayFree 사례). Flutter 학습은 W1 학습 + W2~ 빌드 병행으로 흡수. iOS는 v2 격하라 Phase 1 risk 무관 | (a) 동의 화면에 "이 데이터는 기기 안에만, 매출 환산 계산에만 사용" 명확 카피 + 거부 시 수동 입력 fallback 백업, (b) Flutter 학습 timebox W1 1주, 초과 시 빌드 1주 연기 허용, (c) iOS는 Phase 1 매출 ₩200만/월 도달 후 자가 자본화 (외주 ₩200~500만) — 거부 시 베타 신청 list 유지하며 재신청 |
| **시장** | 김윤후('간단') 디지털 디톡스 인접 확장 → 직접 경쟁 | MEDIUM | (a) 1인 워커 + 매출 환산 + 카톡 봇 3개 wedge로 lock-in, (b) 본인이 ICP 라 콘텐츠 가속, (c) Phase 2 분기로 ICP/행동 빠른 확장 |
| **법률** | 카톡 알림톡 2026.1.1 정책 위반 (마케팅성 발송 차단), PWA 결제 환불 분쟁, 스크린타임 데이터 개인정보 | MEDIUM | (a) 정보성(일일 데이터 요약)만 발송, 마일리지·쿠폰·할인 메시지 0 ([정책](https://docs.channel.io/updates/ko/articles/공지-카카오-알림톡-발송-가능-기준-변경-안내2611-시행-f9f70118)), (b) Toss Payments 표준 환불 정책 채택 (7일 청약철회), (c) 개인정보처리방침에 스크린타임 데이터 처리·저장·삭제 권한 명시. 1회 법무 자문 ₩30~50만 |
| **운영** | 주 12시간 한계 — CS 폭증, LLM 비용 폭주, 트렌드 모니터링 부담 | LOW~MEDIUM | (a) 카톡 채널 자동 FAQ, 이메일 비동기 (주 5시간), (b) LLM 비용 alarm + GPT-5 mini fallback, (c) 본인이 ICP 라 트렌드 자체 체험 |
| **윤리** | "매출 환산" 메시지가 일부 사용자에게 압박감/번아웃 유발 가능 | LOW | (a) 시간당 가치 default 보수적 (₩30,000), (b) 카드에 "긍정 응원 톤" guideline, (c) 매출 환산 OFF toggle 제공, (d) 본인이 ICP → 본인 톤 검증 |

---

## 12. 빌드 백로그 (8주 MVP)

| 주차 | 핵심 작업 | 산출물 | 외주 발주 |
|---|---|---|---|
| **W1** | Flutter 학습 (Dart 문법 + Widget tree + state management 1택: Riverpod) + Figma wireframe 5화면 (온보딩·타이머·리포트·결제·설정) + Firestore 스키마 | Flutter hello-world 빌드 + Figma + DB schema | 없음 |
| **W2** | Flutter 프로젝트 + Firebase 연동 (Auth + Firestore) + 카카오 OAuth + 온보딩 흐름 + 시간당 가치 입력 화면 | 인증 + 온보딩 동작 | 없음 |
| **W3** | 타이머 화면 + 행동 3종 프리셋 설정 + 일일 목표 + 푸시 알림 schedule (FCM) | 타이머·푸시 동작 | 없음 |
| **W4** | **Platform channel → Kotlin → UsageStatsManager 연동** + 동의 화면 UX + 일 1회 백그라운드 sync + Firestore 저장 | 자동 import 동작 (wedge #2 확보) | 없음 |
| **W5** | Toss Payments 앱 SDK (한국 외부 결제 정책 활용) — 일회 ₩9,900 + 구독 ₩4,900 빌링키. 환불 정책 화면 | 결제 동작 + 환불 정책 | 없음 |
| **W6** | AI 주간 리포트 1-shot 파이프라인 (Cloud Functions + Claude Haiku) + 카드 Flutter Canvas 렌더링 + 카톡·인스타 1-tap 공유 | 리포트 카드 동작 | 없음 |
| **W7** | 카카오 채널 등록 + 알림톡 템플릿 심사 + Cloud Functions cron (매일 22:00 일일 요약, 매주 일요일 리포트). 클로즈드 베타 50명 + 사용성 피드백 + 버그 수정 | 카톡 알림 동작 + 베타 피드백 노트 | 법무 자문 ₩30~50만 (이용약관·개인정보·환불) |
| **W8** | Play Store 출시 ($25 등록) + 가격 페이지 + 결제 funnel + KPI dashboard (Firebase Analytics + Mixpanel free). 공개 launch (긱뉴스 + okky + X) | **Play Store MVP 출시** | 인플루언서 1명 시드 ₩30~50만 (선택) |

**MVP 기간 결론**: **8주** (Flutter 학습 W1 포함, 마진 1주). Phase 1 자본 약 ₩50만 안에서 가능. iOS Family Controls Companion 은 Phase 1 매출 ₩200만/월 도달 후 자가 자본화 (외주 ₩200~500만, v2).

**대비책**: Flutter 학습이 W1 안에 끝나지 않으면 W2~W3 빌드 1주 연기 허용 (총 9주). persona.md 2026-05-21 갱신으로 Flutter "중" 본격 전환, RN+Expo fallback 제거.

---

## 13. GO/NO-GO 결정 조건

### 현재 판정: **GO**

근거:
- Android `UsageStatsManager`는 표준 API ([Android Developers](https://developer.android.com/reference/android/app/usage/UsageStatsManager)) — 사용자 동의 1회로 접근 가능. PoC 불요.
- 디지털 디톡스 카테고리는 Play Store 풍부 → 심사 risk 매우 낮음
- 자본 약 ₩50만 (capital_krw_10k 100의 50%) 내 W1~W8 빌드 가능
- iOS Family Controls 승인 의존성 v2로 격하 → Phase 1 risk 0

### GO 유지 조건 (모니터링)
- **AND**: M3 시점 KPI — 무료 1,000명+ AND 일회 결제 30명+ AND LTV/CAC > 5x
- **AND**: Android `PACKAGE_USAGE_STATS` 사용자 동의율 70%+ (W7 클로즈드 베타 50명에서 측정)
- **AND**: 카카오 알림톡 정보성 템플릿 심사 통과 (W7)

### NO-GO 전환 조건
- **OR**: M3 시점 무료 < 300 AND 일회 결제 < 5명 (acquisition 채널 무효)
- **OR**: `PACKAGE_USAGE_STATS` 동의율 < 30% AND 수동 입력 fallback 베타 NPS < 0
- **OR**: 카카오 알림톡 정보성 심사 거부 AND FCM·이메일 대체 retention 50% 미만

### v2 (iOS) 진입 조건
- **AND**: Phase 1 매출 ₩200만/월 도달
- **AND**: iOS 사용자 베타 신청 list 100명+ (랜딩 페이지에서 수집)
- **AND**: Apple Developer Program 가입 + Family Controls Entitlement 신청 + 외주 ₩200~500만 자가 자본화 가능

### Pre-launch 검증 (W7 베타에서 수집)
1. Android `PACKAGE_USAGE_STATS` 동의 화면 UX → 동의율 측정 (target 70%+)
2. AI 주간 리포트 카드 → 베타 50명 만족도 NPS (target 30+)
3. 카카오 알림톡 일일 요약 → 7일 retention (target 40%+)
4. 일회 ₩9,900 결제 마찰 → 베타 → 유료 전환율 (target 5%+)

---

## 14. 부록

### 출처 (URL)

- [Opal $10M ARR Scaling Story - Speedinvest 2025](https://www.speedinvest.com/knowledge/scaling-smart-how-opal-built-a-10m-arr-business-in-just-2-years)
- [Opal App Pricing & Reviews - Crunchbase](https://www.crunchbase.com/organization/opal-4768)
- [Apple Family Controls Entitlement 신청 가이드](https://developer.apple.com/documentation/familycontrols/requesting-the-family-controls-entitlement)
- [Apple Screen Time API Documentation](https://developer.apple.com/documentation/screentimeapidocumentation)
- [Android UsageStatsManager API](https://developer.android.com/reference/android/app/usage/UsageStatsManager)
- [카카오 알림톡 2026.1.1 정책 변경 - Channel.io](https://docs.channel.io/updates/ko/articles/공지-카카오-알림톡-발송-가능-기준-변경-안내2611-시행-f9f70118)
- [카카오 친구톡 종료 - Speedy 2025](https://www.speedykorea.com/blog/kakao-friendtalk-end-brand-message)
- [카카오 비즈니스 메시지 - SOLAPI](https://solapi.com/guides/kakao)
- [한국 프리랜서 통계 - 파이낸셜뉴스 2026](https://www.fnnews.com/news/202605011637374675)
- [통계청 사업체조사](https://kosis.kr/statHtml/statHtml.do?orgId=118&tblId=DT_118N_SAUP50)
- [김윤후 '간단' 일 매출 - eopla 2024](https://eopla.net/magazines/31129)
- [간단 Google Play](https://play.google.com/store/apps/details?id=kr.co.hoo.gandan)
- [Forest 앱 공식](https://www.forestapp.cc/)
- [Freedom 앱 공식](https://freedom.to/)
- [Claude API Pricing 공식](https://platform.claude.com/docs/en/about-claude/pricing)
- [LLM Pricing 2026 비교](https://pecollective.com/blog/llm-pricing-comparison-2026/)
- [챌린저스 - Platum](https://platum.kr/archives/226879)
- 자체: `docs/runs/2026-05-18-korea-app-charts.md`
- 자체: plan-ceo-review 세션 2026-05-21

### 분석 변경 이력

| 날짜 | 변경 사항 | 사유 |
|---|---|---|
| 2026-05-18 | 후보 draft 작성 (점수 73.0, borderline 상단) | discover 단계 |
| 2026-05-21 | plan-ceo-review baseline 전면 재구성. ICP narrow → 1인 워커. 의료 segment 제외. PWA 채택 + hybrid 가격 | audit 4축 (수익·플랫폼·ICP·채널) 전부 `재정의` 본문 반영. 점수 73.0 → 82.5 pass |
| 2026-05-21 | deepdive PRD 작성. 14 섹션 전부 채움. T6 PoC 조건부 GO/NO-GO. iOS Family Controls/Android UsageStats/카톡 2026 정책 정밀 리서치. LLM 비용 1K/5K/20K 모델링. 12개월 시뮬레이션 보수/기본/공격 + Phase 2 옵션 A/B. | deepdive-candidate 호출. 매각 multiple 한국 인디 사례 정합. |
| 2026-05-21 (same day) | **Platform pivot**: PWA → Android 네이티브 (Flutter) 단일 시드. iOS는 v2 격하. go_no_go NEEDS_VALIDATION → **GO**. 자본 38만 → 약 50만 (capital 50%, exclusion 통과). Section 1·4·7·8·11·12·13·14 일괄 rewrite. | 사용자 지적 "이 아이템은 앱이 메인 아닌가". deepdive 가 자기 audit으로 plan-ceo-review 의 PWA 결정을 뒤집은 모순 해소. wedge #2 (스크린타임 자동 import) 가 PWA 단독 불가 → 네이티브 메인이 옳음. 디지털 디톡스 카테고리는 의료 키워드 0이라 audit 가정 2 시점의 "심사 risk" 우려 무효. Flutter는 사용자 선호. |

### Assumption Audit 변경 이력 (deepdive 단계 재검증)

| # | 가정 | 이전 결정 (evaluated) | 신규 증거 | 결정 변경 |
|---|---|---|---|---|
| 1 | 구독 단일 적합 | 재정의 (hybrid) | Opal $10M ARR도 일회 $399 + 구독 mix — hybrid 유지 정합 | **유지** |
| 2 | 네이티브 앱 필수 | 재정의 (PWA) | (a) iOS Screen Time API는 Native만, Android UsageStatsManager는 PWA 미접근 → wedge #2 (자동 import) 보장 불가. (b) 디지털 디톡스 카테고리는 의료 키워드 0 → audit 가정 2 시점의 "심사 risk" 우려 무효. (c) 사용자 선호 Flutter. | **재재정의** — **Android 네이티브 (Flutter) 단일 시드 메인, iOS Native Companion v2 격하**. PWA 가설 폐기. |
| 3 | ICP 한국 20~40대 자기관리 직장인 | 재정의 (1인 워커) | 한국 프리랜서 약 400만 + 자영업자 약 500만 (통계청 2024) — TAM 충분 검증 | **유지** |
| 4 | 카톡 친구 그룹 인증 = 바이럴 | 재정의 (X·긱뉴스 acquisition + 카톡 retention) | 카톡 친구톡 2025.12.31 종료 + 알림톡 정보성 only — retention 채널로만 사용 정합 | **유지** + 강화 (친구톡 종료 정책 반영) |
| 5 (신규) | PWA 단독으로 OS 스크린타임 데이터 접근 가능 | — | iOS Family Controls는 Swift only, Android PACKAGE_USAGE_STATS는 PWA 미접근. TWA 또는 Native Companion 필수 | **폐기 → 자동 해소** (가정 2 재재정의로 네이티브 메인 채택, PWA 가정 자체 사라짐) |

### 가정 정리 ("(추정)" 항목)

- 김윤후 '간단' freemium 전환율 10~20% — 인디 메이커 공개 데이터 기반 (추정)
- 1인 워커 평균 결제력 일반 소비자 1.5~2배 — 노션·Cursor·Figma 결제 추정
- 한국 IT 종사자 100만+ / 디자인·콘텐츠 프리 50만+ — 통계청 + 추정
- 인플루언서 1만 팔로워급 시드 단가 ₩30~50만 — 한국 인디 메이커 시세 (추정)
- 일회 → 구독 전환 20~40% — 1인 워커 ICP 가정 (추정, 베타에서 검증 필요)
- 구독 평균 유지 기간 4~6개월 — Forest·간단 기간 추정
- Apple Family Controls 일반 개발자 entitlement 승인률 — 2026년 사례 일부 1~3주, 거부 사례 일부 ([Apple Forums](https://developer.apple.com/forums/tags/family-controls)). 공식 거부률 미공개
- 알림톡 발송 단가 ₩10~15/건 — SOLAPI·Aligo·DirectSend 평균 (정확 단가는 채널 등록 후 변동)
- 매각 multiple 2~3x ARR — Microacquire 한국·글로벌 인디 평균 (추정)

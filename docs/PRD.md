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

### 한 문장 정의 (2026-05-24 V1 = 인앱결제 paid product re-pivot)
**한국 1인 워커**(개발자·디자이너·작가·연구자·프리·1인 사업자)에게 SNS·쇼츠·게임·웹툰 끊기 타이머 + UsageStatsManager 자동 import + AI 주간 "시간 빚 환산" 리포트를 제공하는 **인앱결제 paid Android 네이티브 앱 (Flutter)**. 주간 카드는 **앱 + FCM + 이메일 + Telegram (사용자 선택)** multi-channel 발송. **V1 = Google Play Billing 인앱결제 (사업자 X, 본업 유지)** — 일회 ₩11,000 / 월 ₩5,900 / 연 ₩39,000 hybrid + 7일 free trial. **사업자 등록 trigger = 월 net 매출 ₩35-50만 도달**. **V2 (사업자 등록 후) = Toss 외부결제 + 카톡 알림톡 추가** (Google 30% 수수료 → Toss 3.3% 절감).

### 핵심 후크
1. 한국 디지털 디톡스 vertical 비어있음 (Forest·간단 모두 1인 워커·시간 빚 환산·multi-channel wedge 안 함)
2. 본인이 곧 ICP — 콘텐츠·UX·우선순위 추측 0 (단 본인 = 직장인 vs ICP = freelance segment 일부 paradox 인식, §11 참조)
3. **Android 단일 시드 (Flutter) + multi-channel retention (FCM + 이메일 + Telegram)** = 카톡 사업자 의존 회피 + 1인 워커가 본인이 쓰는 메신저 직접 선택 = 새 wedge
4. **인앱결제만 V1 (Google Play Billing 30% 수수료 흡수)** = 사업자 등록 없이 매출 발생 가능 + 종합소득세 자가 신고 + 회사 인사팀 직접 인지 가능성 낮음

### V1 결정 사유 (회사 겸업 명시적 금지 상황 + 매출 발생 가능 경로)
- 본인 회사 취업규칙 겸업 금지 → 사업자등록증 보유 불가
- 사업자 X = 카톡 알림톡 / Toss 결제 둘 다 불가
- **그러나 Google Play Console 개인 가입 + 인앱결제 = 사업자 X로 매출 가능**
- → V1 = **paid product (인앱결제 only, multi-channel retention)**
- 사업자 등록 trigger = 월 net 매출 ₩35-50만 고정 도달 시
- V2 (사업자 등록 후) = Toss + 카톡 추가

### GO/NO-GO 한 줄 결론
**GO** — Android UsageStatsManager 표준 API + multi-channel retention (사업자 X) + Google Play Billing 인앱결제 (사업자 X 가능, 30% 수수료 흡수). 본업 part-time 빌드 W1~W12 가능. M3 hard checkpoint = 월 net 매출 ₩35-50만 도달 → 사업자 등록. Exit criteria (M3 미달 시) PRD §11·§13 명시.

### 1년차 목표 (V1 인앱결제 paid + V2 Toss·카톡 추가)
- **Phase 1 (M0~M6) V1 paid product**: 사용자 1,000~5,000명 + 결제 4-7% + **월 net 매출 ₩35-50만 도달 (보수 M5-M6)** → 사업자 등록 trigger
- **Phase 2 (M7~M12) 사업자 등록 후**: Toss 외부결제 (수수료 30% → 3.3%) + 카톡 알림톡 추가. 매출 ₩200~500만/월
- **Y1 매각 시나리오**: V1 ARR ₩400-600만 (사업자 미등록이라 매각 약함) → V2 진입 후 ARR ₩2,400-6,000만 (매각 검토 base)

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
4. **Multi-channel retention (P0, 2026-05-24 V1 무료 도구 pivot)**
   - **앱이 source of truth**: 매주 일요일 22:00 새 카드 자동 생성. 과거 모든 주차 archive 앱 내 영원히 회고 가능.
   - **채널 발송 (사용자 선택, 1개 이상)**:
     - ✅ FCM 푸시 (default, 모든 사용자) — tap 시 앱 내 카드로 이동
     - ✅ 이메일 (선택) — Mailgun free tier. 카드 이미지 + 본문 + deeplink
     - ✅ Telegram (선택) — Bot API 무료. 1인 워커 인디 메이커 친화. 30초 setup
     - ▶ Discord (V1.5 후보) — IT 1인 워커 fit
     - ▶ Slack (V1.5 후보) — B2B 익숙 segment
   - **사용자 UX**: 온보딩 마지막 화면 또는 설정에서 채널 multi-select. 언제든 변경 가능.
   - **카톡 알림톡 V2 격하**: 사업자 등록 시점에 카톡 채널 추가 (Phase 2)
   - **threshold trigger**: 로컬 detection (Flutter 30분 polling) → flutter_local_notifications 즉시 알람 (사업자 X로 가능). 채널 발송 없이 device 내부 알람만.
5. **수익 모델 (P0, 2026-05-24 V1 인앱결제 paid re-pivot)**
   - **V1 (Phase 1, M0-M6) Google Play Billing 인앱결제 only**:
     - **Hybrid pricing**: 일회 ₩11,000 (30일 인증서) + 월 ₩5,900 + 연 ₩39,000 (33% 할인, 월 환산 ₩3,250)
     - Google 30% 수수료 흡수 (이전 ₩9,900/₩4,900 본인 net 수령액 동급)
     - **7일 무료 체험** → 자동 구독 전환 (구독만, Google Play Billing 표준)
     - **베타 50명 평생 50% 할인** (월 ₩2,950) — 초기 evangelist
     - **출시 후 7일 30% 할인** (acquisition burst)
     - **환불**: Google 48시간 자동 + 자체 7일 청약철회 (구독)
     - **Paywall 노출 시점**: D7 첫 weekly 리포트 받은 후 + 매출 환산 toggle 진입 시 (옵션 B+C hybrid)
   - **무료 tier (V1, 결제 X 사용자)**:
     - 4종 프리셋·UsageStatsManager·D7까지 weekly 카드·multi-channel 1개 (FCM only)
     - D7 후 paywall 노출 → 결제 시 multi-channel 전체·90일 트렌드·매출 환산·threshold·on-demand 리포트 unlock
   - **V2 (사업자 등록 trigger 도달 후, M3-M6 추정)**:
     - Toss 외부결제 추가 (Google Play와 병행, 수수료 30% → 3.3%)
     - 카톡 알림톡 추가 (multi-channel 4번째 채널)
     - 가격 정책 유지 (₩11,000 / ₩5,900 / ₩39,000) 또는 Toss 결제 시 5% 추가 할인 검토

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
- 카드 1장 (JSON → Flutter Canvas 렌더링)
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

### 가격 구조 (2026-05-24 V1 인앱결제 paid re-pivot)

| 티어 | 가격 | Google 30% 차감 후 본인 net | 내용 |
|---|---|---|---|
| 무료 (D7까지) | ₩0 | ₩0 | 4종 프리셋·UsageStatsManager·FCM weekly 카드 (D7까지만) |
| **일회 인증서** | **₩11,000** | ₩7,700 | 30일 디톡스 + AI 4주 무제한 + 매출 환산 + multi-channel 전체 |
| **월 구독** | **₩5,900/월** | ₩4,130 | 무제한 + 90일 트렌드 + threshold + on-demand |
| **연 구독** | **₩39,000/년** | ₩27,300 | 33% 할인 (월 환산 ₩3,250) |
| **7일 무료 체험** | ₩0 → 자동 구독 | — | 구독만 적용. 8일째 자동 결제 ₩5,900/₩39,000 |
| **베타 50명** | 평생 50% 할인 | — | 월 ₩2,950 영구 |
| **출시 후 7일** | 30% 할인 | — | acquisition burst |

**환불 정책**:
- Google Play 48시간 자동 환불 (Google 표준)
- 자체 7일 청약철회 (구독 — 한국 전자상거래법)
- 30일 보장은 V1.5 검토 (운영 시간 vs 결제 친화 trade-off)

**Paywall 노출 시점** (옵션 B + C hybrid):
- D7 첫 weekly 리포트 받은 직후 → "다음 주부터 매출 환산도 보시려면 ₩11,000 인증서 또는 ₩5,900/월 구독" CTA
- 매출 환산 toggle 진입 시도 → paywall modal
- 결제 X 사용자도 D7까지는 무료 가치 체험 가능 (wedge #3 multi-channel은 FCM only)

### LTV 계산 (2026-05-24 Google 30% 수수료 반영)

```
LTV 본인 net 기준:
  일회 결제 net = ₩7,700 (₩11,000 × 70%)
  구독 net = ₩4,130/월
  일회 → 구독 전환 30% × ₩4,130 × 5개월 평균 = ₩6,195
  
  평균 LTV (본인 net) = ₩7,700 + ₩6,195 = ₩13,895
  보수 LTV (전환 20%): ₩7,700 + ₩4,130 × 4 × 0.2 = ₩11,004
  공격 LTV (전환 40%): ₩7,700 + ₩4,130 × 6 × 0.4 = ₩17,612

LTV gross (사용자 결제 기준, 사업자 등록 후 비교용):
  일회 ₩11,000 + 구독 ₩5,900 × 5 × 0.3 = ₩19,850
```

**V2 사업자 등록 후 Toss 채택 시 LTV 회복**: ₩13,895 → ₩19,217 (Toss 3.3% 수수료)

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

### Phase별 Acquisition 전략 (2026-05-24 추가)

PRD §9 매출 시뮬레이션의 사용자 수치를 어떻게 달성하는지 구체적 전략 매트릭스.

#### Phase 0a — 0 → 100 (W7-W8) · "Closed seed"

| Budget | CAC | Acquisition target |
|---|---|---|
| ₩0 (인플 시드 미사용, 다음 단계 reserve) | ₩0-500 | 100명 (W7 베타 50 → W8 launch 100) |

**전술**:
- W1-W6 본인 X 빌드 in public 매주 post → W7까지 본인 follower 누적
- W7 클로즈드 베타 50명 (본인 SaaS 운영자 X DM 10명 + 본인 follower 모집)
- W8 launch day: 베타 50명에게 1-tap share 요청 (인스타·카톡)

#### Phase 0b — 100 → 1,000 (M0-M3) · "Cold start burst"

| Budget | CAC | Acquisition target |
|---|---|---|
| ₩30-50만 (인플루언서 시드 1명) | ₩300-800 blended | 900명 (3개월) |

**전술 + 예상 yield**:

| 채널 | 작업 | 예상 acquisition | CAC |
|---|---|---|---|
| W8 본인 X launch thread | "1인 워커 Focus Accountant 출시" + 본인 빌드 in public 1달 culmination | 200-300 | ₩0 |
| 긱뉴스 (news.hada.io) launch 글 | "1인 개발자가 만든 한국 디지털 디톡스 앱" | 150-300 | ₩0 |
| okky launch 글 | 개발자 도구·서비스 게시판 | 80-150 | ₩0 |
| 노션 한국 커뮤니티 (페북 그룹·오픈톡) | 직접 게시 + 1인 워커 DM 10명 | 100-200 | ₩0 |
| 인플루언서 1명 시드 (X 1만+ 팔로워) | ₩30-50만, "1인 개발자 실험 + 시간 빚 카드 share" 콘텐츠 | 200-400 | ₩750-2,500 |
| 본인 빌드 in public 매주 X | "이번 주 끊기로 +N분 회복" 카드 자동 share | 100-200 | ₩0 |
| 카톡 채널 검색 자연 유입 | W4 채널 등록 후 자연 발견 | 50-100 | ₩0 |
| 한국 SaaS 미디어 PR | 플래텀·디지털타임즈 outreach | 100-200 | ₩0 (시간만) |
| **Phase 0b 누적 (M0-M3)** | | **980-1,850** | **avg ₩300-800** |

#### Phase 1 — 1,000 → 5,000 (M3-M6) · "Initial traction + paid"

| Budget | CAC | Acquisition target |
|---|---|---|
| ₩200-400만 (매출 ₩50만/월+ 재투자) | ₩1,500-3,000 blended | 4,000명 (3개월) |

**전술 + 예상 yield**:

| 채널 | 작업 | 예상 acquisition | CAC |
|---|---|---|---|
| Meta ads (Instagram·페북) | 한국 1인 워커 targeting (개발자/디자이너/작가/프리), ₩100-200만/월 | 600-1,500 | ₩2,000-3,500 |
| 인플루언서 확장 | 3-5명 인디 메이커, ₩90-200만 | 600-2,000 | ₩500-1,500 |
| YouTube 인디 메이커 게시 | Geek News류 채널 1개, ₩50만 | 200-500 | ₩1,000-2,500 |
| 본인 콘텐츠 마케팅 | 매주 X post + 노션 한국 weekly + 디시 1회/월 | 300-600 | ₩0 |
| 사용자 viral (1-tap share) | 베타→active 사용자 카톡·인스타 share | 400-800 | ₩0 |
| 한국 미디어 PR (2차) | 플래텀 success story (M3+ 매출 발생 후) | 200-400 | ₩0 |
| Play Store ranking + ASO | 디지털 웰빙 카테고리, "Focus Accountant" + Pretendard 키워드 | 300-700 | ₩0 |
| 카톡 채널 친구 자연 증가 | 1K → 5K 자연 follow + WoM | 200-500 | ₩0 |
| **Phase 1 누적 (M3-M6)** | | **2,800-7,000** | **avg ₩800-2,000** |

**LTV/CAC check (PRD §5 기준선 3x)**:
- Blended CAC ₩2,000 vs LTV ₩17,250 = **8.6x ✓**
- 가장 비싼 채널 (Meta ads ₩3,500) = **4.9x ✓**
- 모두 통과

#### Phase 2 — 5,000 → 20,000 (M7-M12) · "Scale + ICP 확장"

| Budget | CAC | Acquisition target |
|---|---|---|
| ₩500-1,000만 (Phase 1 매출 누적) | ₩2,000-5,000 blended | 15,000명 (6개월) |

**전술 변화**:
- Meta ads 본격 (월 ₩300-500만)
- B-2 진입 시: 학습자 segment 추가 (디시·에브리타임·자기개발 유튜브)
- B-3 진입 시: 같은 1인 워커 ICP + 행동 카테고리 확장 (카페인·수면)
- 글로벌 PH (Product Hunt) 영문화 (M12 검토)

#### Phase별 CAC × LTV × Budget 종합

```
Phase           Target          Budget          Blended CAC     LTV/CAC
─────────────────────────────────────────────────────────────────────────
0a (W7-W8)      100명           ₩0              ₩0-500          —
0b (M0-M3)      900명           ₩30-50만         ₩300-800        21.5x
1  (M3-M6)      4,000명         ₩200-400만       ₩1,500-3,000    8.6x
2  (M7-M12)     15,000명        ₩500-1,000만     ₩2,000-5,000    5.7x
─────────────────────────────────────────────────────────────────────────
M12 누적         20,000명        ₩730-1,450만     —              avg 7x
```

### 인플루언서 시드 후보 (X 한국 인디 메이커)
- 본인 일상 채널 1만~3만 팔로워급 인디 메이커 3~5명 콜드 DM
- 김윤후 '간단' 후기 작성한 사람 우선
- 시드 비용 ₩30~50만 × 1명 우선 (Phase 0b), ₩90-200만 × 3-5명 (Phase 1)

### 한국 vs 글로벌
- M0~M6: **한국 100%** (위 채널)
- M7~M12: Phase 2 분기 시 글로벌 PH 검토 — 영문화 후 Opal 사용자 acquisition test

### V1.5+ 검토 채널 (홀딩 중)

#### YouTube Shorts + Instagram Reels (홀딩 — 추후 결정)
- **Potential**: 한국 디톡스 카테고리에 short-form 강한 indie 앱 없음. 본인이 ICP라 콘텐츠 자가 생산 자연스러움. CAC ₩0 (cash) + 본인 인건비 제외.
- **Risk**: "디톡스 앱을 쇼츠에 홍보" 위선 톤 risk. 시간 부담 (주 1-3 posts, 30-60분/영상).
- **콘텐츠 시리즈 후보 (TODOS 참조)**:
  - (1) 매출 환산 카드 5-10초 reveal
  - (2) 1인 개발자 vs SNS 비교 (founder narrative)
  - (3) AI 작업 중 함정 (P4 본인 episode 재현)
  - (4) Meta "디톡스 앱 만들면서 쇼츠 본다" (self-deprecating hook)
  - (5) "끊기 사용 N일째" before/after
- **결정 deadline**: W4 또는 V1.5 검토 시점. TODOS [P2]로 holding.

---

## 7. 기술 스택

### 아키텍처

| 레이어 | 스택 | 친숙도 (persona.md) |
|---|---|---|
| **모바일 앱 (메인)** | **Flutter 3.x (Dart)** + Material 3 | 중 (persona.md 2026-05-21 갱신 — RN+Expo 제거, Flutter "중" 본격 전환. 실제 첫 도입은 본 후보, 학습 timebox W1 1주) |
| **OS 데이터 접근** | Flutter platform channel → Kotlin → `UsageStatsManager` (PACKAGE_USAGE_STATS 권한) | 중 (Flutter 학습 후 platform channel 표준 패턴) |
| **백엔드 (메인)** | **FastAPI (Python)** on Fly.io seoul region — REST API, JWT auth, APScheduler cron, SOLAPI/Aligo SDK 직접, Anthropic SDK 직접, Firebase Admin SDK (FCM 호출만) | **상** (persona.md "상", 본인 주력 stack) |
| **DB** | **PostgreSQL on Supabase** (Free tier 5,000명까지, 이후 Pro $25/월 또는 Hetzner self-managed migration) — Alembic migrations, 일 backup 자동 | 상 (raw SQL · pandas 자유) |
| **Auth (2026-05-24 변경)** | **JWT + Google Sign-In native** (google_sign_in pub package → ID token → FastAPI /v1/auth/google → google-auth library로 verify → JWT). Firebase Auth 미사용. Kakao OAuth는 V2 (카톡 알림톡 link 시점)로 격하. | 상 |
| **Flutter 로컬 캐시** | **Drift (SQLite)** offline-first — REST API sync 패턴, 충돌 시 last-write-wins | 중 |
| **LLM** | Claude Haiku 3.5 (primary, Anthropic SDK from FastAPI) + GPT-5 mini (fallback) | 상 |
| **결제 (V1 인앱결제, 2026-05-24 re-pivot)** | **Google Play Billing** (Individual 계정, 사업자 X 가능, 30% 수수료). 일회 + 구독 + 연구독 product 등록. 7일 free trial Google Play 표준. | 중 — Google Play Console 학습 1주 |
| **결제 (V2 사업자 등록 후 추가)** | Toss Payments 앱 결제 SDK (외부결제, 수수료 3.3%). Google Play와 병행 가능 | V2 |
| **카톡 채널 (V2 격하)** | V1 X (사업자 미보유). V2: 카카오 비즈메시지 알림톡 (정보성 only) — Aligo / SOLAPI / DirectSend | V2 |
| **푸시 (FCM, V1 default)** | Firebase project: FCM 단독 사용 (Firestore·Auth 미사용). Firebase Admin SDK from Python — token storage in Postgres | 중 |
| **이메일 (V1 선택 채널)** | Mailgun free tier (5K emails/월 무료) 또는 AWS SES ($0.10/1K) — FastAPI에서 transactional email 발송 | 중 |
| **Telegram (V1 선택 채널)** | Telegram Bot API (무료, 사업자 X). python-telegram-bot SDK. 사용자가 본인 Bot과 chat 시작 → chat_id 저장 → 메시지 발송 | 중 |
| **로컬 알람 (V1 threshold)** | flutter_local_notifications — 사업자 X로 device 내부 알람 발송 가능 | 중 |
| **모니터링** | Sentry free tier (Python + Flutter) + Fly.io built-in metrics + Supabase Dashboard | 중 |
| **iOS (v2 단계)** | Flutter 동일 코드베이스 + Swift Family Controls Native Companion | **하** (Phase 1 매출 후 외주 또는 학습) |

### 외주 항목

| 항목 | 한국 시세 | 검토 트리거 |
|---|---|---|
| **iOS Family Controls Native Companion (v2)** | ₩200~500만 (외주) | Phase 1 매출 ₩200만/월 도달 + iOS 사용자 수요 베타 신청 100명+ 시 자가 자본화 |
| **로고·일러스트** | ₩0 (Figma 무료 아이콘 + 본인 미니멀) | 매각 직전 V2 폴리시 |
| **카피라이팅** | ₩0 (본인 ICP) | 없음 |
| **법무 자문 (이용약관·개인정보처리방침)** | ₩30~50만 (1회 표준 검토) | W7 클로즈드 베타 직전 |

### Phase 1 자본 impact (2026-05-24 V1 인앱결제 paid re-pivot)
- Flutter 신규 학습 — 본인 시간 1~2주 (W1 학습 + W2~ 빌드 병행) → 외주비 ₩0
- **FastAPI 백엔드 = 본인 주력 stack (persona.md "상")** → 학습 곡선 0, W2-W3 setup 3-5일
- Android 단일 시드 → iOS Companion 외주 ₩0 (v2 격하)
- **V1 = 인앱결제 paid (Google Play Billing 사업자 X 가능)** → 사업자·법무·Toss·카톡 vendor 모두 V2로 격하
- Phase 1 자본 합계: **약 ₩10만** (Google Play Console $25 = ₩3.5만 + .kr 도메인 ₩2만 + 예비 ₩5만)
- 운영비 (본인 cash 부담): 매출 발생 전 ~₩3-4만/월 (Fly·LLM·Mailgun), 매출 발생 후 net revenue로 자동 흡수

### V2 (Phase 2) 진입 시점 추가 자본
사업자 등록 path 결정 후 monetization 도입 시:
- 법무 자문 ₩50~70만 (이용약관·개인정보·환불·Google Play policy)
- 사업자등록 ₩0 (홈택스 무료) — 단 가족 명의 또는 회사 정리 시점 결정
- 카톡 비즈메시지 채널 등록 + 템플릿 심사 ₩0 (시간만)
- Toss Payments 가맹점 가입 ₩0
- 인플루언서 시드 ₩30~50만 (V2 acquisition 가속)

### 사업 확장 (Phase 2 B-2/B-3) 호환성 — Firebase 대신 FastAPI+Postgres 선택 이유
- **데이터 ownership**: Postgres pg_dump 자유, 어디든 migration 가능
- **Schema 자유**: ALTER TABLE로 B-3 행동 확장 시 새 테이블 (caffeine_events, sleep_events) 즉시 추가
- **ICP 확장 (B-2)**: 같은 schema에 user_segment 컬럼만 추가 → 학습자 segment 빠른 도입
- **데이터 분석 + ML**: raw SQL + pandas + scikit-learn 자유, BigQuery export 우회 X
- **외부 API**: FastAPI에 endpoint 추가 자유 — V2 B2B partnership 가능성
- **매각 due diligence**: Postgres dump = 표준 자산, vendor 의존 0
- **한국 데이터 주권**: Fly.io seoul region — 본인 ICP "기기 안에만" 메시지와 일관 (Firebase GCP US 대비)

---

## 8. 운영 비용

### 가정 (2026-05-24 V1 무료 도구 pivot)

- **V1 = 무료 도구**: 매출 0. 모든 비용 본인 부담 cash.
- **Multi-channel cost**: FCM ₩0 + 이메일 (Mailgun free 5K/월) + Telegram Bot ₩0 = 0
- **Active filter**: 지난 7일 `usage_events` 1건 이상 사용자에게만 weekly LLM + push. 비활성 사용자 cost 0.
- **D7 active rate**: 20% (무료 도구라 paid 시 60%보다 낮음, 모두 무료 사용자)
- **본인 인건비 제외 (cash only)**.

### V1 (무료 도구) 운영비 — 본인 cash 부담

| 항목 | 1,000명 | 5,000명 | 20,000명 | 비고 |
|---|---|---|---|---|
| Fly.io seoul (FastAPI) | 1.7만 | 2.8만 | 5.6만 | shared-1x → 1GB → 2GB scale up |
| Supabase Postgres | 0 (Free) | 0-3.5만 (Free→Pro) | 3.5만 (Pro) | Free 5,000명까지 |
| Firebase FCM | 0 | 0 | 0 | HTTP v1 API 무료 |
| Mailgun (이메일) | 0 (Free 5K/월) | 1.4만 (Pro $35) | 2.8만 (Foundation $90) | active filter 시 1K=무료, 5K=Pro |
| Telegram Bot API | 0 | 0 | 0 | 무료 |
| Google Play 등록 | 0.3만 | 0.3만 | 0.3만 | $25/년 ÷ 12 |
| Claude Haiku LLM | 0.4만 | 1.9만 | 7.6만 | active filter 적용 (D7 20%) |
| Sentry | 0 (free) | 0-3.6만 | 3.6만 | 5K errors/월 free |
| Mixpanel | 0 (free) | 0 | 2.8만 | 100K events/월 free |
| .kr 도메인 + Vercel | 0.2만 | 0.2만 | 0.2만 | 연 ₩2만 ÷ 12 |
| **V1 cash 합계 (본인 부담)** | **약 2.6만/월** | **약 10-13만/월** | **약 26-29만/월** | 매출 0 |

→ **V1 핵심: 카톡 ₩6.7만 제거 + 결제 제거 + Mailgun free tier = 비용 ↓**.
→ 본인 본업 소득으로 충분히 흡수 가능한 범위 (월 ₩3만 → ₩30만).

### V2 (Phase 2) 운영비 — 사업자 등록 후 monetization 진입 시

V2 진입 시 카톡 + Toss 추가 → cost matrix는 PRD §8 history 참조 (이전 3-scenario 매트릭스 그대로 valid). Gross margin 90%+ 보장.

### 비용 driver 분석 (V1 무료 도구)

```
1,000명:    Fly.io 65% / 도메인 8% / LLM 15% / 기타 12%
5,000명:    Fly.io 22% / Supabase Pro 27% / LLM 15% / Mailgun 11% / 기타 25%
20,000명:   Fly.io 19% / LLM 26% / Sentry+Mixpanel 22% / Mailgun 10% / 기타 23%
```

**V1에서 cost driver = 인프라 + LLM**. 카톡 X로 driver 분산 → 본인 부담 감내 가능 수준.

### V2 진입 시 cost mitigation
1. 카톡 vendor 단가 협상 (5,000명+ 시)
2. 무료/유료 channel 차별 (V2 paid에 카톡 추가, 무료는 FCM·이메일·Telegram 그대로)
3. Hetzner self-managed migration (20K+ scale)

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

> **2026-05-24 V1 무료 도구 pivot 반영**: V1 (M0-M6) 매출 0. 아래 시뮬레이션은 **V2 (Phase 2) 사업자 등록 + monetization 진입 시 시나리오** (가족 명의 사업자, 회사 정리, 또는 변호사 자문 결과 ack 시점). V1 무료 도구 단계에서는 사용자 수 + retention + NPS KPI만 추적 (§13 참조).

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

### Detail 5 — Sensitivity Analysis (2026-05-24 추가)

핵심 변수 ±20% 변동 시 Y1 누적 매출 영향 (기본 ₩3,500만 기준):

| 변수 | 기본값 | -20% Y1 매출 | +20% Y1 매출 | 민감도 | 영향 우선순위 |
|---|---|---|---|---|---|
| **무료 acquisition** | 5,000명 (M6) | ₩2,300만 (-₩1,200만) | ₩4,700만 (+₩1,200만) | ★★★★★ | **#1** |
| **일회 결제율** | 6% | ₩2,900만 (-₩600만) | ₩4,100만 (+₩600만) | ★★★★ | #2 |
| **구독 전환율** | 30% | ₩3,100만 (-₩400만) | ₩3,900만 (+₩400만) | ★★★ | #3 |
| **구독 retention** | 5개월 | ₩3,200만 (-₩300만) | ₩3,800만 (+₩300만) | ★★★ | #3 |
| **CAC** | ₩2,000 | ₩3,600만 (+₩100만, cost↓) | ₩3,400만 (-₩100만) | ★ | #5 |

**인사이트**:
- **#1: Acquisition이 가장 큰 lever** — Phase 0b·Phase 1 마케팅 효율이 매출 결정. §6 GTM 전략에 집중 정당화.
- **#2-3: Conversion funnel 다음 lever** — 결제율 × 구독 전환 × retention 모두 비슷한 영향.
- **#5: CAC 둔감** — LTV ₩17,250 × LTV/CAC 8.6x 마진 충분. CAC 50% 증가도 견딤.
- → **집중 우선순위: Acquisition channel ROI > Conversion funnel 최적화 > Retention > CAC 최적화**

### Detail 6 — Cash Flow + Capital ROI (2026-05-24 추가)

월별 cash flow 기본 시나리오 (단위 ₩만):

| 월 | 매출 | 운영비 (cash) | 마케팅 budget | 월 net | 누적 cash |
|---|---|---|---|---|---|
| M0 (W0-W8) | 0 | 0 | 0 | -50 (자본 투입) | **-50** |
| M1 | 18 | 4 | 5 (인플 시드 1/3) | +9 | **-41** |
| M2 | 36 | 4 | 5 | +27 | **-14** |
| M3 | 60 | 4 | 5 | +51 | **+37** ← BEP |
| M4 | 108 | 14 (5K 시나리오) | 30 (Phase 1 시작) | +64 | **+101** |
| M5 | 180 | 14 | 80 | +86 | **+187** |
| M6 | 300 | 14 | 100 | +186 | **+373** |
| **Phase 1 누적** | **702** | **54** | **225** | **+423** | **+373** (자본 회수 후) |

**Phase 2 (M7-M12, 기본 옵션 A B-2 ICP 확장)**:

| 월 | 매출 | 운영비 + 마케팅 | 월 net | 누적 cash |
|---|---|---|---|---|
| M7 | 350 | 20 + 150 | +180 | +553 |
| M8 | 420 | 22 + 150 | +248 | +801 |
| M9 | 480 | 24 + 150 | +306 | +1,107 |
| M10 | 540 | 26 + 150 | +364 | +1,471 |
| M11 | 600 | 28 + 150 | +422 | +1,893 |
| M12 | 700 | 30 + 150 | +520 | **+2,413** |

**Capital ROI**:
```
초기 자본 (M0):         ₩50만
Y1 누적 매출 (기본):    ₩3,500만
Y1 누적 net cash:       ₩2,413만
─────────────────────────────────
ROI (배수):              ₩2,413 / ₩50 = 48.3x in 1 year
BEP 시점:                M3 (3개월)
자본 회수 후 잉여:        +₩373만 (Phase 1 종료 시점)
```

**참고**:
- 본인 인건비 미반영. 본인 시간 ₩40K/h × 주 40h × 12개월 = ₩2,400만 기회비용 별도.
- M0 자본 투입 ₩50만 = Google Play $25 + 법무 ₩50-70만 + 인플 시드 ₩30만 + 예비. PRD §7 참조.
- M4-M6 마케팅 budget 누적 ₩210만 = Phase 1 acquisition. PRD §6 참조.
- 매출 ₩300만/월 시점 (M7 추정) 법인 전환 검토 → 추가 cost ₩5만/월 (간이세무).

### Detail 7 — Best / Worst Case + NO-GO Trigger (2026-05-24 추가)

#### WORST case (acquisition 50% 미달)

| 변수 | 기본 | WORST | 결과 |
|---|---|---|---|
| M3 무료 acquisition | 1,000명 | 500명 (-50%) | NO-GO 트리거 직전 |
| M3 일회 결제 | 60명 | 5-10명 | PRD §13 NO-GO 조건 도달 ("M3 < 5명") |
| M6 매출 | ₩300만 | ₩30-50만 | Phase 1 자본 회수 실패 |

**NO-GO 결정 조건 (정밀)**:
```
M3 시점 ALL 도달 시 GO 유지:
  ✓ 무료 사용자 ≥ 500명
  ✓ 일회 결제 ≥ 10명
  ✓ LTV/CAC ≥ 3x

M3 시점 ANY 미달 시 NO-GO 또는 Pivot 검토:
  ✗ 무료 < 300명 (PRD §13 기존)
  ✗ 일회 결제 < 5명 (PRD §13 기존)
  ✗ PACKAGE_USAGE_STATS 동의율 < 30%
  ✗ D7 retention < 10%
  ✗ NPS < 10
```

**NO-GO 시 손실**:
- 자본 ₩50만 직접 손실
- 본인 시간 8주 (W1-W8) ≈ ₩2,400만 기회비용
- Pivot 옵션: B-2 학습자 segment 직접 진입 (₩100만 추가 자본 필요)

#### BEST case (acquisition 150% 초과 + 결제율 12%)

| 변수 | 기본 | BEST | 결과 |
|---|---|---|---|
| M3 무료 acquisition | 1,000명 | 1,500명 (+50%) | Phase 1 가속 |
| 일회 결제율 | 6% | 12% | 결제 180명 (M3) |
| 구독 전환율 | 30% | 50% | 구독 가속 누적 |
| M6 매출 | ₩300만 | ₩600-800만 | 공격 시나리오 초과 |

**BEST case 액션**:
- M4-M6 마케팅 budget 1.5-2x 증액 (₩200-400만 → ₩300-600만)
- Phase 2 M7 진입 가속 — B-2/B-3 동시 검토 시간 확보
- iOS Companion 외주 발주 (₩200-500만) — Phase 1 매출로 자가 자본화
- 인플루언서 시드 확장 (3-5명 동시)

#### 시나리오 비교 매트릭스

| 시나리오 | M3 무료 | M3 결제 | M6 매출 | Y1 매출 | BEP | 결정 |
|---|---|---|---|---|---|---|
| **WORST** | 300-500명 | 5-10명 | ₩30-50만 | ₩400-600만 | M8+ 또는 불가 | NO-GO / Pivot |
| **보수** | 1,000명 | 40명 | ₩200만 | ₩1,800만 | M5 | GO 유지 |
| **기본** | 1,000명 | 60명 | ₩300만 | ₩3,500만 | M3-M4 | GO 유지 |
| **공격** | 1,000명 | 100명 | ₩500만 | ₩5,500만 | M2-M3 | GO + Phase 2 가속 |
| **BEST** | 1,500명+ | 180명+ | ₩600-800만 | ₩7,000-10,000만 | M2 | BEST 액션 발동 |

**NO-GO 의사결정 timing**:
- M2: early warning (acquisition < 600 또는 결제 < 5)
- **M3: hard checkpoint** (NO-GO 또는 GO 결정)
- M4-M6: GO 유지 시 Phase 2 KPI 모니터링
- M6 (Phase 1 종료): Phase 2 B-2 vs B-3 분기 결정

(운영비 = 월 8.8만 × 12 + 알림톡 변동 + 마케팅 ₩50~150만 가정)

---

## 10. 매각 시나리오

> **2026-05-24 V1 무료 도구 pivot 반영**: V1 단계 (M0-M6) 매출 0이므로 매각 ARR multiple 적용 불가. 매각 가치는 user base + brand + portfolio 자산만. **매각 검토는 V2 (Phase 2) 사업자 등록 + monetization 진입 후 ARR 발생 시점.** 아래 시나리오는 V2 진입 가정 하 시나리오.

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
| **법률 (V1 무료 도구, 2026-05-24 단순화)** | 스크린타임 데이터 개인정보 처리, PIPA 준수 | LOW~MEDIUM | (a) 개인정보처리방침에 스크린타임 데이터 처리·저장·삭제 권한 + 위탁사 list (Anthropic, Mailgun, Fly.io, Supabase, Firebase) + 국외 이전 동의 명시, (b) V1 무료 도구라 결제 분쟁 없음, (c) 만 14세+ age gate (Kakao OAuth 후), (d) 회원탈퇴 30일 grace + hard delete cron |
| **법률·심사 (V1 무료 도구)** | (a) Google Play `PACKAGE_USAGE_STATS` review rejection — 디지털 웰빙 앱 거부 사례 다수, (b) 출시 후 takedown risk | MEDIUM | (a) W4까지 privacy policy URL Vercel 공개 + Play Console Digital Wellbeing 카테고리 정책 정독, (b) 필요 시 Google Play Support 사전 문의, (c) 거부 시 수동 입력 fallback 베이스 maintenance |
| **본업·시간 (V1 인앱결제, 2026-05-24 update)** | (a) 회사 겸업 명시적 금지 → 사업자 등록 불가 (V1은 인앱결제로 우회), (b) part-time 빌드 → W1-W8 timeline 8주 → 12-16주 slip 가능, (c) 본업·끊기 동시 cognitive load (95% 3개월 burnout 패턴) | **HIGH** — 본업 risk 시 끊기 자체 보류 또는 본업 손실. 8주 timeline 미준수 시 wedge timing 약화 | (a) V1 = 인앱결제 (사업자 X 가능 경로), (b) 본업 X 게시 빈도 통제 + 본인 식별 정보 노출 회피, (c) M3 hard checkpoint 시점에 V2 진입 path 결정, (d) part-time 시 W1-W12 timeline 허용, (e) 주 야간 작업 limit 20h/주 self-cap |
| **회사 발각 risk (2026-05-24 신규, subagent challenge 반영)** | (a) X 공개 빌드 in public + 블로그 + Google Play 본인 명의 등록 = HR 검색 발각 vector, (b) 종합소득세 5월 신고 시 회사 연말정산 영향 일부 가능, (c) "사업 준비 행위"로 해석 가능 (무료 도구 → 인앱결제 paid 전환은 영리 의도 명확) | **HIGH (정량화)** — 발각 시 즉시 해고 사유 + 손해배상 청구 가능 (한국 IT 대기업 사례 있음). 본업 + 끊기 동시 손실 | (a) 본인 명의 노출 channel 통제: X 익명 계정 vs 본명 계정 분리, 블로그 가명, (b) 출시 후 한국 SaaS 미디어 PR 시 founder 식별 정보 minimum, (c) Google Play Developer 정보 회사 도메인 이메일 사용 X, (d) 매출 발생 후 연말정산 신고 의무 본인 자체 확인 (세무사 자문 ₩5-10만), (e) 본업 영향 X 약속 — 야간 시간 limit, (f) 발각 risk 명시적 인지 + 회사 정리 시점 시나리오 사전 준비 |
| **Maintenance trap (2026-05-24 신규, subagent challenge 반영)** | M3 통과 후 V2 monetization path 미실현 시 1,000+ 사용자 + 매출 미달 + 끊을 수 없는 함정 (사용자 신뢰 깨지는 부담). 운영비 본인 부담 누적. | **MEDIUM (확률 40-50%, subagent 추정)** — 본업 cash 흡수 가능하지만 정신 부담 누적. 셧다운 결정 어려움 | (a) **exit criteria 사전 명시** (§13): M3 NO-GO 조건 도달 시 자동 종료 절차 (사용자 데이터 export·삭제 + 30일 grace), (b) V1.5 결정 = 사업자 등록 trigger 도달 vs 1년 sustained operation 중 선택 (1년 후 sustained면 셧다운 검토 강제), (c) maintenance mode 단계 정의 (기능 추가 X, 버그 fix만, 운영비 ₩5만 cap), (d) 사용자 공지 fairness 보장 |
| **ICP self-paradox (2026-05-24 신규, subagent challenge 반영)** | 본인 = 직장인 (시간당 임금 고정) vs 가정 ICP = 1인 사업자/freelance (시간당 가치 ₩30K-100K 변동). "매출 환산" wedge가 본인에게 직접 안 맞을 수 있음 | **MEDIUM** — 본인 = ICP 가정 자체가 부분 깨짐. 본인 사용 후기·검증 부분 무효 risk | (a) 본인 사용 데이터 6개월 self-tracking (design doc Assignment), (b) 시간당 가치 입력 옵션을 본인 본업 시급 또는 부업·취미 환산 가능하게 (시간당 ₩30K default), (c) V1 베타 50명 중 freelance/1인 사업자 segment 비율 명시 추적, (d) 본인 ≠ ICP 명시 → 페르소나 민준·지영 (PRD §3) 위주 검증 |
| **운영** | 주 12시간 한계 — CS 폭증, LLM 비용 폭주, 트렌드 모니터링 부담 | LOW~MEDIUM | (a) 카톡 채널 자동 FAQ, 이메일 비동기 (주 5시간), (b) LLM 비용 alarm + GPT-5 mini fallback, (c) 본인이 ICP 라 트렌드 자체 체험 |
| **윤리** | "매출 환산" 메시지가 일부 사용자에게 압박감/번아웃 유발 가능 | LOW | (a) 시간당 가치 default 보수적 (₩30,000), (b) 카드에 "긍정 응원 톤" guideline, (c) 매출 환산 OFF toggle 제공, (d) 본인이 ICP → 본인 톤 검증 |

---

## 12. 빌드 백로그 (8주 MVP)

| 주차 | 핵심 작업 | 산출물 | 외주 발주 |
|---|---|---|---|
| **W1** | Flutter 학습 (Dart 문법 + Widget tree + state management 1택: Riverpod) + Figma wireframe 5화면 (온보딩·타이머·리포트·결제·설정) + Firestore 스키마 | Flutter hello-world 빌드 + Figma + DB schema | 없음 |
| **W2** (2026-05-24 Google Sign-In primary 변경) | **Backend only**: FastAPI setup + Fly.io seoul 배포 + .kr 도메인 + Supabase + Alembic migrations (users·usage_events monthly partition·usage_event_dedupe·refresh_tokens·channel_subscriptions·fcm_tokens·thresholds·subscriptions) + JWT 15min + 30d rotation + **Google Sign-In** (google-auth library로 ID token verify, /v1/auth/google endpoint). **개인정보처리방침·이용약관 초안 Vercel URL 공개** (PIPA 준수 필수). Kakao OAuth는 V2 카톡 연동 시점에 추가. Toss V2 격하. | FastAPI deploy + Google Sign-In 동작 + privacy URL live | 없음 |
| **W3** (2026-05-24 V1 무료 pivot) | **Flutter scaffolding**: 프로젝트 + theme (DESIGN.md) + Drift (SQLite) local schema + http client + JWT interceptor + 온보딩 5화면 (P5 60sec flow) + 시간당 가치 입력. 4종 프리셋 (SNS·쇼츠·게임·웹툰) + Firebase Remote Config (웹툰 list 동적 update). FCM 토큰 등록 + /v1/fcm/register. **채널 선택 UX** (온보딩 마지막 또는 설정에서 FCM·이메일·Telegram multi-select). | Flutter 인증·온보딩 동작 + FCM 토큰 등록 + 채널 선택 UX | 없음 |
| **W4** (2026-05-24 V1 무료 pivot) | **Platform channel → Kotlin → UsageStatsManager 연동** + 동의 화면 UX (P5: 이유 → 권한 → shock) + 8h WorkManager background sync + Postgres /v1/usage/batch idempotent. **이메일 vendor (Mailgun free) setup + /v1/me/email_consent + transactional template**. Toss·카톡 작업 제거. Play Console Digital Wellbeing 카테고리 정책 self-check. | 자동 import 동작 (wedge #2) + 이메일 발송 가능 + privacy URL live | 없음 |
| **W5** (2026-05-24 V1 인앱결제 paid re-pivot) | **Google Play Console Individual 가입** ($25) + 결제 정보 등록 + **Google Play Billing 통합** (3 products: 일회 ₩11,000 / 월 ₩5,900 / 연 ₩39,000) + **7일 free trial 설정** + 베타 50명 promo code 발급 + 출시 7일 30% 할인 sale 설정. **Telegram Bot 설정** (BotFather, python-telegram-bot SDK) + /v1/me/telegram_link. **회원 탈퇴 + 데이터 삭제 UX** (PIPA 30일 grace). **본업 시간 배분 점검**: W1-W5 진행률 평가, W6-W8 부족 시 V1.5 격하 항목 결정. Toss V2로 격하. | Google Play Billing 동작 + Telegram 발송 + 회원 탈퇴 UX | 없음 |
| **W6** (2026-05-24 V1 인앱결제 paid re-pivot) | AI 주간 리포트 1-shot 파이프라인 (**FastAPI + APScheduler 일요일 22:00 cron + Anthropic SDK 직접 호출**) + 카드 Flutter Canvas 렌더링 + 인스타 1-tap 공유. **Active user filter SQL**. **Multi-channel dispatch**: FCM + Mailgun + Telegram. **앱 내 weekly_reports archive 화면**. **Paywall UX** (D7 weekly 카드 받은 후 + 매출 환산 toggle 진입 시 modal). **P4 V1.5 spike** (작업 시간대 heuristic). | 리포트 카드 + multi-channel + archive + paywall UX + V1.5 spike | 없음 |
| **W7** (2026-05-24 V1 무료 pivot) | **Threshold local detection** (Flutter 30분 polling + flutter_local_notifications 즉시 알람 — 사업자 X로 가능). 클로즈드 베타 50명 + 사용성 피드백 + 버그 수정. **KPI metrics 수집**: PACKAGE_USAGE_STATS 동의율 + multi-channel retention (FCM·이메일·Telegram 각각) + D7/D30 retention + NPS. Toss·카톡·법무 자문 V2로 격하. | threshold 알람 동작 + 베타 피드백 노트 + V1 무료 도구 metrics | 없음 (법무는 V2 시점) |
| **W8** (2026-05-24 V1 무료 pivot) | Play Store 출시 ($25 등록) + 무료 도구 마케팅 페이지 + KPI dashboard (Mixpanel free). 공개 launch (긱뉴스 + okky + X). **본업 동료 발각 회피**: X 게시 본인 식별 정보 통제. 인플루언서 시드 V2로 격하. | **Play Store MVP 출시 (무료 도구)** | 없음 (인플 시드 V2 시점) |

**MVP 기간 결론**: **8주 (Full-time 가정)** 또는 **12-16주 (part-time, 본업 유지 시)**. V1 자본 약 ₩10만 안에서 가능. iOS Family Controls Companion + 사업자 등록 + monetization 모두 V2 (Phase 2) 시점 자가 자본화.

**대비책**: 본업 part-time 빌드 시 W1-W8 → W1-W12 늘림 허용. cognitive load 통제. M3 hard checkpoint 시점에 V2 진입 path 결정 (가족 명의 사업자 / 회사 정리 / 변호사 자문 결과).

---

## 13. GO/NO-GO 결정 조건

> **2026-05-24 V1 무료 도구 pivot 반영**: V1 매출 0이므로 V1 GO/NO-GO는 user base + retention + NPS 기반. V2 (Phase 2) 진입 시점에 monetization GO/NO-GO 별도 판정.

### V1 현재 판정: **GO (무료 도구)**

근거:
- Android `UsageStatsManager`는 표준 API ([Android Developers](https://developer.android.com/reference/android/app/usage/UsageStatsManager)) — 사용자 동의 1회로 접근 가능
- 디지털 디톡스 카테고리는 Play Store 풍부 → 심사 risk 매우 낮음
- V1 자본 약 ₩10만 (capital_krw_10k 100의 10%) 내 빌드 가능
- 사업자 미보유 환경에서도 multi-channel retention (FCM·이메일·Telegram) 가능
- 본업 유지 + part-time 빌드 가능

### V1 GO 유지 조건 (M3 hard checkpoint, 인앱결제 paid 기준)
- **AND**: 사용자 ≥ 1,000명 (무료 + 결제 합산)
- **AND**: `PACKAGE_USAGE_STATS` 동의율 ≥ 70%
- **AND**: D30 retention ≥ 25%
- **AND**: NPS ≥ 30
- **AND**: 적어도 1개 multi-channel (FCM/이메일/Telegram) retention D7 ≥ 30%
- **AND**: 월 net 매출 ≥ ₩15만 (보수 4% 결제율 × 1,000명 × ₩7,700 net = ₩30.8만 기준 50%)

### V1 NO-GO 전환 조건 (즉시 exit 검토)
- **OR**: M3 사용자 < 300명
- **OR**: `PACKAGE_USAGE_STATS` 동의율 < 30%
- **OR**: D7 retention < 10% (모든 channel 합산)
- **OR**: NPS < 0
- **OR**: M3 월 net 매출 < ₩5만 (paid product 핵심 가설 깨짐)

### V1 → V2 사업자 등록 trigger
- **월 net 매출 ₩35-50만 고정 도달** (보수 가정 M5-M6)
- 도달 시 사업자 등록 path 결정 (개인사업자 본인 명의 또는 가족 명의)
- Toss 외부결제 + 카톡 알림톡 V2 도입

### Exit Criteria (Maintenance Trap 회피, subagent challenge 반영)
M3 NO-GO 도달 시 또는 1년 sustained operation 후:
1. **M3 NO-GO 즉시 종료**:
   - 사용자에게 종료 공지 30일 전 (FCM·이메일)
   - 데이터 export 옵션 (JSON 다운로드)
   - 결제 사용자 환불 (남은 구독 기간 비례)
   - Google Play 앱 unpublish
2. **1년 sustained 후 평가** (M3 통과 + V2 trigger 미달 시):
   - 본업 cash 부담 + 정신 부담 평가
   - 사업자 등록 path 진척 검토
   - 셧다운 vs sustained 결정 강제 분기
3. **Maintenance mode 단계** (sustained 선택 시):
   - 기능 추가 X, 버그 fix만
   - 운영비 ₩5만/월 cap (위반 시 셧다운)
   - 본인 야간 시간 5h/주 cap

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
| 2026-05-22 | `/office-hours` 완료 → design doc APPROVED. Approach B "Focus Accountant Reframing" 채택. P1-P7 premise 확정. PRD §1·§2·§3·§4·§11·§12 9개 변경 항목 도출 (이후 update). | 본인 ICP episode 발산 + premise 6개 + Google Play policy P7. design doc: `~/.gstack/projects/kkeugi/jungsunpark-main-design-20260522-001310.md`. |
| 2026-05-22 | `/design-consultation` 완료 → DESIGN.md 생성. Pretendard + IBM Plex Mono + clay #8B5A3C accent + light default 확정. memorable thing "거울 같은 친구" 도출. | 본인 ICP UX 발산 + 시점별 톤 분리 design tokens 반영. |
| 2026-05-23 | `/plan-eng-review` 진행 중 → **카톡 알림 reframed** (§4 #4·#5 + §8 + §12 W4·W5·W6·W7 update). 무료 = 주 1회 일요일 reflection / 유료 = 주 1회 + threshold trigger + 시간 custom. 매일 22:00 정기 발송 제거. W4 작업에 카톡 채널 등록·심사 + privacy policy URL 공개 추가 (timeline risk 회피). W5 Toss KFTC 재검증, W6 P4 V1.5 spike, W7 법무 budget ₩30-50만 → ₩50-70만 (P7). | 사용자 challenge "gandan은 단식 active session, 끊기는 회고 — 의미론적으로 다른 cadence 필요". memorable thing "압박 X" 위반 risk 회피. 비용 ₩37만 → ₩6.7만/월 (1,000명) 절감. |
| 2026-05-23 | **백엔드 stack pivot**: Firebase (Firestore + Auth + Cloud Functions + FCM) → **FastAPI + Postgres on Supabase Free + Fly.io seoul region**. §7 기술 스택 표 전면 rewrite. §8 운영비 ₩5만 → ₩3.9-4.6만/월 (1,000명, cash). §12 W2 "Firebase 연동" → "FastAPI setup + Postgres schema + JWT + Kakao OAuth", W3 FCM 토큰 endpoint 추가, W6 cron Cloud Functions → APScheduler. 사업 확장 호환성 섹션 신규 추가. | 사용자 결정 사유: (1) FastAPI 본인 주력 stack ("상"), Firebase 학습 비용 회피, (2) 사업 확장 (Phase 2 B-2/B-3, 매각, multi-product) 시 Postgres 표준 데이터 ownership·schema 자유·analytics 자유 필수. Firebase는 V1 속도만 우위, 사업 확장 비용 ↑. Supabase Free tier 5,000명까지 cash ₩1.4만/월, 한계 도달 시 Pro 또는 Hetzner self-managed migration 자유 (Postgres 표준). |
| 2026-05-24 | **§8 cash 비용 재산정 + active filter 채택**. Cash only (본인 인건비 제외) 1,000명 ₩10.7만 → ₩7.4만, 5,000명 ₩45만 → ₩28만, 20,000명 ₩184만 → ₩117만. Gross margin 73-78% → 81-86%로 향상. 카톡 알림톡 active filter (지난 7일 usage_events ≥1건 AND kakao 친구 추가) -50% 비용 절감. §8 카톡 cell typo 수정 (0.7 → 6.7 → 3.4). §12 W6에 active filter SQL 구현 추가. | 사용자 challenge "비활성 사용자에게 카톡 발송 무의미". 정책 준수 강화 (정보성 = 본인 데이터 존재해야 발송) + 비용 driver 60-75% → 46-60%로 완화. Korean 인디 앱 D7 active rate 무료 20% / 유료 70% 가정. |
| 2026-05-24 | **§8 3-시나리오 매트릭스 재구성** (보수 4% / 기본 7% / 공격 12% paid). 이전 "20% paid" 비현실적 가정 정정 (PRD §9 공격 시나리오 14% 상회). 고정 인프라 + 변동 (카톡·LLM) 분리. 모든 9 셀 (3 scenario × 3 scale) 명시. Gross margin 81-86% → **90-96%** 까지 향상 (paid rate 정정 효과). 비용 driver 분석: 카톡 scale에 따라 41% → 60% dominant. | 사용자 challenge "1,000명 중 유료 비율 현실은?". 산업 벤치마크 (모바일 productivity 2-5%, 한국 인디 5-10%) 반영. §9 매출 시뮬레이션과 §8 운영비 framing 일관화. |
| 2026-05-24 | **§6 GTM Phase별 Acquisition 전략 통합**. Phase 0a (W7-W8 100명) / 0b (M0-M3 1K) / 1 (M3-M6 5K) / 2 (M7-M12 20K) 4단계 매트릭스. 각 단계별 채널 × 예상 yield × CAC 명시. Phase 0b ₩30-50만 / Phase 1 ₩200-400만 / Phase 2 ₩500-1,000만 budget. LTV/CAC 21.5x → 8.6x → 5.7x. V1.5+ 검토 채널로 YouTube Shorts + Reels 홀딩 (시리즈 5종 후보 명시, TODOS 등록). | 사용자 catch "PRD §9 사용자 수치 가정만 있고 어떻게 달성하는지 미명시". §6 채널 list 외 단계별 acquisition 전략 부재 보완. Shorts/Reels는 추후 별도 결정 위해 홀딩. |
| 2026-05-24 | **§9 매출 시뮬레이션 Detail 3종 추가**: (5) Sensitivity analysis — 핵심 변수 ±20% 영향 매트릭스 (acquisition 가장 민감), (6) Cash flow + Capital ROI — 월별 cash flow + 자본 ₩50만 회수 시점 M3 + Y1 net cash ₩2,413만 + ROI 48.3x, (7) Best/Worst case + NO-GO trigger — WORST acquisition 50% 미달 시 NO-GO, BEST 150% 초과 시 마케팅 budget 1.5-2x 증액 + iOS Companion 외주. 시나리오 5종 (WORST/보수/기본/공격/BEST) 비교 매트릭스. 1-4번 (Cohort/MRR/ARPU/Churn) 추후 추가 항목으로 TODOS 등록. | 사용자 catch "PRD §9 detail 부재". 본인 자본 결정 + NO-GO timing 정밀화. 1-4번은 실제 데이터 필요해서 M3·M5+ 시점 추가. |
| 2026-05-24 | **/plan-eng-review Architecture 완료** → `docs/ARCHITECTURE.md` 작성 (Postgres schema + REST API + Auth flow + Sync pattern + APScheduler + Project layout + CI/CD + monitoring). 결정 3개 잠금: usage_events monthly partition / Sync 8h + 로컬 threshold / JWT 15min + 30d rotation. Subagent cold read 14개 issue 발견 → ARCHITECTURE.md §14에 P0-P2 반영. **P0 critical: 사업자 등록 + 카카오 비즈니스 채널 + 알림톡 심사 즉시 착수 (오늘부터)**. §12 W2-W3 split (Backend only / Flutter scaffolding). | Solo founder 8주 timeline 살리려면 사업자 등록 W0-W1에 시작 안 하면 W7 베타 카톡 검증 불가. usage_events idempotency 재설계 + PIPA 처리방침 + 카톡 광고성 회피 + Toss-Play Plan B 등 14개 risk 사전 회피. |
| 2026-05-24 | **🔄 V1 = 무료 도구 pivot (CRITICAL)**: 사용자 본업 회사 겸업 명시적 금지 확인 → 사업자등록증 보유 불가 → 카톡 알림톡 + Toss 결제 둘 다 V1에서 X. V1을 무료 도구로 재구성, monetization은 V2 (Phase 2)로 격하. **새 wedge #3**: 카톡 대신 **multi-channel retention** (FCM default + 이메일 Mailgun + Telegram Bot, V1.5 Discord/Slack). 사용자가 본인 선호 메신저 선택 = 1인 워커 친화 새 차별점. PRD §1·§4·§5·§7·§8·§10·§11·§12·§13·§14 전면 재구성. 자본 ₩50만 → ₩10만 (사업자·카톡·Toss·법무 모두 V2 격하). | 회사 겸업 금지 제약 + 사업자 path 미확보 + V1 출시 + portfolio 가치 + Phase 2 monetization 진입 base. 카톡 wedge 약화 → multi-channel 다양성 = 새 wedge로 전환. 본업 유지 + part-time 빌드 W1-W12 timeline. |
| 2026-05-24 | **🔄 V1 = 인앱결제 paid product re-pivot (CRITICAL)**: 무료 도구 pivot reverse. **Google Play Billing Individual 계정 = 사업자 X로 매출 발생 가능** 발견. V1 = paid product (Hybrid 일회 ₩11,000 + 월 ₩5,900 + 연 ₩39,000 + 7일 free trial). Google 30% 수수료 흡수 (₩9,900/₩4,900 → ₩11,000/₩5,900). 가격 정책 패키지: 베타 50명 평생 50% 할인 + 출시 7일 30% 할인 + D7 paywall + Google 48h + 자체 7일 환불. **사업자 등록 trigger = 월 net 매출 ₩35-50만 고정 도달**. autoplan CEO subagent의 추가 critical 우려 반영: 발각 risk 정량화 (§11 HIGH), maintenance trap 명시 (§11 MEDIUM 40-50%), ICP self-paradox (§11 MEDIUM), exit criteria (§13). PRD §1·§4·§5·§7·§11·§12·§13·§14 전면 재구성. Toss·카톡 V2 격하 유지. | autoplan CEO review subagent challenge → 사용자 결정: 인앱결제로 매출 발생 가능 path 확인. 가격 ₩11K 인상으로 Google 30% 흡수. 발각·trap·paradox 등 위험 정량화하여 PRD에 명시. exit criteria로 maintenance trap 회피 메커니즘 보장. |

### Assumption Audit 변경 이력 (deepdive 단계 재검증)

| # | 가정 | 이전 결정 (evaluated) | 신규 증거 | 결정 변경 |
|---|---|---|---|---|
| 1 | 구독 단일 적합 | 재정의 (hybrid) | Opal $10M ARR도 일회 $399 + 구독 mix — hybrid 유지 정합 | **유지** |
| 2 | 네이티브 앱 필수 | 재정의 (PWA) | (a) iOS Screen Time API는 Native만, Android UsageStatsManager는 PWA 미접근 → wedge #2 (자동 import) 보장 불가. (b) 디지털 디톡스 카테고리는 의료 키워드 0 → audit 가정 2 시점의 "심사 risk" 우려 무효. (c) 사용자 선호 Flutter. | **재재정의** — **Android 네이티브 (Flutter) 단일 시드 메인, iOS Native Companion v2 격하**. PWA 가설 폐기. |
| 3 | ICP 한국 20~40대 자기관리 직장인 | 재정의 (1인 워커) | 한국 프리랜서 약 400만 + 자영업자 약 500만 (통계청 2024) — TAM 충분 검증 | **유지** |
| 4 | 카톡 친구 그룹 인증 = 바이럴 | 재정의 (X·긱뉴스 acquisition + 카톡 retention) | 카톡 친구톡 2025.12.31 종료 + 알림톡 정보성 only — retention 채널로만 사용 정합 | **유지** + 강화 (친구톡 종료 정책 반영) |
| 5 (신규) | PWA 단독으로 OS 스크린타임 데이터 접근 가능 | — | iOS Family Controls는 Swift only, Android PACKAGE_USAGE_STATS는 PWA 미접근. TWA 또는 Native Companion 필수 | **폐기 → 자동 해소** (가정 2 재재정의로 네이티브 메인 채택, PWA 가정 자체 사라짐) |
| 6 (2026-05-23 신규) | Firebase BaaS가 1인 인디 indie dev 적합 default | 재정의 (Firebase 채택) | (a) 본인 FastAPI 주력 stack "상", Firebase 학습 곡선 추가 — W1 Flutter 신규 + Firebase 신규 = cognitive load 2배. (b) 사업 확장 (Phase 2 B-2/B-3, multi-product, 매각) 시 Postgres 표준 ownership·schema 자유 필수. Firebase Firestore NoSQL는 schema 자유·analytics·외부 export 모두 우회 필요. (c) Supabase Free tier 5,000명까지 cash ₩1.4만/월 = Firebase Blaze ₩2.5만보다 저렴. | **재재정의** — **FastAPI + Postgres on Supabase Free + Fly.io seoul**. Firebase는 FCM only로 축소. Firestore·Auth·Cloud Functions 미사용. |
| 7 (2026-05-24 신규) | V1에 사업자 등록 + 카톡 알림톡 + Toss 결제 = monetization path | 재정의 (사업자 등록 + 카톡 + Toss = wedge #3 핵심) | (a) 사용자 본업 회사 겸업 명시적 금지 → 사업자등록증 보유 불가 (V1에서 X), (b) 사업자 없으면 카톡 알림톡 + Toss 결제 둘 다 X = wedge #3 + 매출 둘 다 V1 불가, (c) V1 = 무료 도구로 재구성 가능. multi-channel retention (FCM + 이메일 + Telegram) = 사업자 X로 가능 + 새 wedge로 전환. (d) V2 (Phase 2) 사업자 등록 path는 가족 명의 / 회사 정리 / 변호사 자문 결과로 선택. | **재재정의** — V1 = 무료 도구 + multi-channel retention. monetization은 V2 격하. PRD §1·§4·§5·§7·§8·§10·§11·§12·§13 모두 영향. |

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

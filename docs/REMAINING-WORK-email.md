# 끊기 출시까지 — 본인이 해야 할 작업 (이메일 확인용)

2026-06-03 갱신 · 이 문서는 메일로 보내 외부에서도 절차대로 따라가기 위한 정리본입니다.
저장소 원본: `docs/REMAINING-WORK.md` (요약/표 중심), 이 파일은 풀어 쓴 행동 가이드.

---

## 한 줄 요약

코드는 끝났다. 이제 **백엔드 배포 → 지인 1주 soft test → 테스터 12명 모집 → 클로즈드 14일 → 출시** 순서로 간다.

전체 약 **6~8주**. 가장 긴 리드타임 두 개는 **Play Console 신원확인(1~7일)** + **테스터 12명 모집(1~2주)**. 이 둘은 일찍 시작.

**이번 갱신 핵심**: 클로즈드 테스트 14일 시계를 시작하기 전에, 본인 + 가까운 사람 3~5명이 **실 백엔드·실 외부연동 환경에서 1주 써보는 soft test 단계를 추가**했다. 14일 시계 중에 큰 버그가 나면 시계가 망가지므로, 그 전에 한 번 거른다.

---

## 큰 그림 (PHASE 별 순서)

```
PHASE 1  지금 ~ 1주차      Play Console 가입(신원확인) + 도메인 + 키스토어 (리드타임 최우선)
PHASE 2  1주차 ~ 2주차     외부 계정 모두 + 백엔드 배포 + 실외부 연동 검증
PHASE 3  2주차 ~ 3주차     ⭐ 지인 3~5명 sideload 1주 soft test + 본인 실기기 billing 검증
PHASE 4  3주차 ~ 4주차     테스터 12명 모집 (PHASE 3 후반과 병렬 시작 가능)
PHASE 5  4주차 ~ 6주차     클로즈드 테스트 트랙 게시 → 14일 시계
PHASE 6  6주차 ~ 7주차     Store listing + 프로덕션 출시
PHASE 7  출시 후           모니터링 + 사업자 등록 결정(매출 trigger 도달 시)
```

각 PHASE 안의 항목은 **앞 PHASE 결과를 기다리지 않고 시작 가능한 것**부터 묶었다.
리드타임이 있는 외부 심사·DNS·신원확인은 무조건 일찍 시작.

---

## PHASE 1 — 지금 ~ 1주차 (리드타임 3가지 동시 시작)

신원확인·DNS 전파·키스토어는 다른 PHASE 가 시작될 수 없게 막는 prerequisite. 셋 다 지금 동시에 착수.

### 1-A. Google Play Console 가입 (수일 소요, 가장 시급)

**왜**: 신원확인이 1~7일 걸린다. 늦으면 PHASE 2·3 전체가 밀린다.

**무엇을 할 일**

1. https://play.google.com/console 접속 → "개발자 계정 만들기"
2. **계정 유형 = Individual(개인)** 선택 (사업자 등록 없음. V1 path 전제)
3. 등록비 **$25 결제** (1회, 평생)
4. 본인 정보 입력
   - **개발자 표시명**: 본명 회피 권장. 예: `pjshi` 같은 닉/브랜드. 본명 노출은 회사 겸업 발각 risk 증가.
   - 연락 이메일: 개인 메일 (회사 메일 X)
   - 주소·전화: 본인 실 정보 (심사용, 공개 X)
5. **신원확인 자료 제출**: 신분증 사진 + 셀카. 보통 1~7일 안에 결과.
6. (대기 중 1-B·1-C 병행)

**비용**: $25 (1회) · **소요**: 가입 30분 + 신원확인 1~7일
**완료 기준**: Play Console 들어가서 "앱 만들기" 버튼이 활성화됨

---

### 1-B. 도메인 등록 (DNS 전파 = 시간 잡아먹는 외부 작업)

**왜**: 백엔드 배포 URL(`api.kkeugi.kr`) + Mailgun 발송 도메인(`mail.kkeugi.kr`) 둘 다 필요. DNS 전파는 수 시간~수일.

**무엇을 할 일**

1. 가비아·후이즈·Cloudflare 중 하나에서 **`kkeugi.kr`** 등록 (연 ~₩22,000)
2. 등록만 하고 DNS 설정은 PHASE 2 에서.

**비용**: 연 ~₩22,000 · **소요**: 결제 즉시
**완료 기준**: 본인 명의로 `kkeugi.kr` 보유

---

### 1-C. Android 키스토어 생성 (앱 서명 키 — 분실 시 영구 불가)

**왜**: Play Store 업로드용 AAB 에 서명하는 키. **한 번 만들면 절대 분실 금지** (분실 = 앱 업데이트 영구 불가).

**무엇을 할 일**

1. Mac 터미널:
   ```
   keytool -genkey -v \
     -keystore ~/kkeugi-upload-keystore.jks \
     -keyalg RSA -keysize 2048 -validity 10000 \
     -alias kkeugi-upload
   ```
2. 비밀번호 2개 만들고 **1Password / 안전 저장소에 저장**
3. **`.jks` 파일을 백업 2곳 이상** (iCloud · 외장 SSD 등)
4. GitHub 절대 X (gitignore 들어 있어도 추가 보관)
5. 키스토어 준비되면 Claude 에게 "릴리스 서명 코드 1줄 연결" 의뢰 (`android/key.properties`)

**비용**: 0 · **소요**: 10분 + 백업
**완료 기준**: `.jks` 파일 + 비밀번호 안전 보관 + 백업 2곳

---

## PHASE 2 — 1주차 ~ 2주차 (외부 계정 셋업 + 백엔드 배포)

신원확인이 끝나면 시작. 외부 계정·secrets 모은 뒤 백엔드 한 번에 살린다.

### 2-A. Play Console 앱 생성 + SHA-1 추출 (신원확인 통과 후)

**무엇을 할 일**

1. Play Console → "앱 만들기"
2. **패키지명 = `kr.pjshi.kkeugi`** (반드시 정확히 이 값. 업로드 후 영구 변경 불가)
3. 앱 이름: 끊기 (Kkeugi) · 기본 언어: 한국어
4. 무료/유료: **무료** (인앱결제로 수익화)
5. Play App Signing 활성 → 업로드 키스토어(1-C) 등록
6. **SHA-1 두 가지를 모두 추출해 메모**
   - 업로드 키 SHA-1: `keytool -list -v -keystore ~/kkeugi-upload-keystore.jks`
   - Play App Signing 키 SHA-1: Play Console → 앱 → 설정 → 앱 무결성 → 앱 서명
   - **둘 다 등록 안 하면 Google 로그인 실패** — 다음 2-B에서 둘 다 사용

**완료 기준**: 끊기 앱 등록 + SHA-1 2개 메모

---

### 2-B. Google Cloud OAuth + 영수증 검증 서비스 계정

**무엇을 할 일**

1. https://console.cloud.google.com → 새 프로젝트 "kkeugi"
2. **OAuth Client ID 2개 생성**
   - Application type: **Android** → 패키지명 `kr.pjshi.kkeugi` + SHA-1 2개 (2-A) 모두 등록
   - Application type: **Web application** → 결과 **Web Client ID 메모** (백엔드 secret)
3. **Google Play Developer API 활성화** + 서비스 계정 생성
   - 이름 `kkeugi-play-verifier`
   - **JSON 키 다운로드** (백엔드 secret)
4. Play Console → 사용자/권한 → 위 서비스 계정 이메일 초대 + "재무 데이터/주문 보기" 권한

**완료 기준**: Web Client ID + 서비스 계정 JSON 파일

---

### 2-C. Telegram 봇 + Mailgun (외부 채널 계정)

**Telegram 봇**

1. Telegram → `@BotFather` → `/newbot`
2. 봇 이름: 끊기 / username: `kkeugi_bot`(가능한 이름)
3. **봇 토큰 메모** (백엔드 secret)
4. 웹훅 등록은 2-F 에서.

**Mailgun (DNS 작업 → 일찍)**

1. https://www.mailgun.com 가입 (free tier 월 5K)
2. **발신 도메인 `mail.kkeugi.kr` 추가**
3. Mailgun 제시 **SPF / DKIM / MX 레코드를 도메인 등록업체 DNS에 추가** (1-B 도메인)
4. 검증 수 시간~1일. 일찍 시작할수록 좋음.
5. API key 발급 → 메모

**완료 기준**: 봇 토큰 보유 + Mailgun verified + API key 보유

---

### 2-D. 인프라 — Fly.io + Supabase + Anthropic + Sentry + Mixpanel

**무엇을 할 일**

1. **Fly.io** https://fly.io 가입 + 카드. region = **Seoul(`nrt`)** 또는 `hkg`. CLI 설치 후 `flyctl auth login`. **API 토큰 발급 → GitHub Actions secret `FLY_API_TOKEN`**
2. **Supabase** https://supabase.com 가입 + 새 프로젝트 (region = Seoul). DB password 설정 → Settings → Database → **Connection string(transaction pooler, asyncpg 호환)** 복사 → secret `DATABASE_URL`
3. **Anthropic** https://console.anthropic.com 가입 + Tier 1 prepay → API key 발급 → secret `ANTHROPIC_API_KEY`
4. **Sentry** https://sentry.io 가입(free) → 프로젝트 2개(백엔드 Python / 프론트 Flutter) → DSN 각각 메모
5. **Mixpanel** https://mixpanel.com 가입(free) → 프로젝트 생성 → **Project Token** 메모

**완료 기준**: 5개 서비스 모두 토큰/키 메모

---

### 2-E. Secrets 등록 + 백엔드 첫 배포 ⭐ (이 PHASE 의 핵심)

**왜**: 이 단계에서 백엔드 살아나면 PHASE 3 의 지인 sideload 가 실 환경에서 가능해진다.

**무엇을 할 일**

1. `flyctl secrets set` 으로 한꺼번에 주입:
   - `DATABASE_URL` (Supabase 2-D)
   - `JWT_SECRET` = `openssl rand -hex 32` 결과
   - `GOOGLE_CLIENT_ID` = Web Client ID (2-B)
   - `ANTHROPIC_API_KEY` (2-D)
   - `SENTRY_DSN_BACKEND` (2-D)
   - `TELEGRAM_BOT_TOKEN` (2-C)
   - `TELEGRAM_WEBHOOK_SECRET` = `openssl rand -hex 16`
   - `MAILGUN_API_KEY`, `MAILGUN_DOMAIN=mail.kkeugi.kr` (2-C)
   - `GOOGLE_PLAY_PACKAGE_NAME=kr.pjshi.kkeugi`
   - `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON` = JSON 파일 내용 (2-B)
   - `ENVIRONMENT=production`
2. GitHub Settings → Secrets → `FLY_API_TOKEN` 등록 → push 시 자동 배포 활성
3. `kkeugi.kr` DNS 에 Fly.io 가리키는 A/AAAA 레코드 추가 → `api.kkeugi.kr` 연결
4. `https://api.kkeugi.kr/health` 가 `{"status":"ok"}` 응답하는지 확인

**완료 기준**: `api.kkeugi.kr` 백엔드 health OK

---

### 2-F. Telegram 웹훅 + Mailgun 실발송 + 법무 URL 호스팅

**무엇을 할 일**

1. Telegram setWebhook:
   ```
   curl -F "url=https://api.kkeugi.kr/webhooks/telegram" \
        -F "secret_token=<TELEGRAM_WEBHOOK_SECRET>" \
        https://api.telegram.org/bot<TOKEN>/setWebhook
   ```
   봇에게 `/start` 메시지 → 백엔드 로그 확인
2. Mailgun 관리자 → 본인 이메일로 테스트 발송 → 받은편지함(스팸 폴더 포함) 확인
3. **개인정보처리방침 + 이용약관 URL 호스팅**
   - 저장소 `docs/legal/privacy-policy.md` + `terms-of-service.md` 이미 작성 완료
   - **추천**: GitHub Pages 또는 Notion 공개 페이지에 올려 URL 확보
   - 최종 URL 2개를 메모(앱 설정 메뉴 + Play Console data safety 입력용)

**완료 기준**: Telegram 봇 양방향 OK + Mailgun 본인 메일 수신 + 법무 URL 2개

---

## PHASE 3 — 2주차 ~ 3주차 ⭐ 지인 1주 soft test

**이 PHASE 가 추가된 이유**: PHASE 5의 14일 시계 중에 큰 버그가 나면 시계 망가짐 → 출시 2주 추가 지연. 그 전에 본인 + 가까운 사람 3~5명이 실 환경에서 1주 써보면서 한 번 거른다.

**중요**: 이 단계는 Play Console 클로즈드 트랙 게시 X. **Internal App Sharing** 사용 → 12명/14일 카운트와 무관, 즉시 공유 가능.

### 3-A. 릴리스 AAB 빌드 + Internal App Sharing 업로드

**무엇을 할 일**

1. (사전) Claude 에게 **"릴리스 서명 코드 연결"** 의뢰 → `android/key.properties` 와 `build.gradle.kts` 의 release signingConfig 결합 (10분)
2. AAB 빌드:
   ```
   flutter build appbundle --release \
     --dart-define=USE_FAKE_BILLING=false \
     --dart-define=API_BASE_URL=https://api.kkeugi.kr \
     --dart-define=IS_PRODUCTION=true \
     --dart-define=MIXPANEL_TOKEN=<...> \
     --dart-define=SENTRY_DSN=<...>
   ```
3. Play Console → 좌측 메뉴 → **앱 무결성 → 내부 앱 공유**
4. AAB 업로드 → 자동으로 **공유 가능 링크 생성** (`https://play.google.com/apps/test/...`)
5. 이 링크는 카운트와 무관 + 신원확인된 계정만 받을 수 있음 + 즉시 설치 가능

**Internal App Sharing 의 장점**
- **테스터 12명 카운트 X** (클로즈드 트랙과 별개)
- **즉시 공유** (Play 심사 없음)
- 한 링크로 여러 명에게 보낼 수 있음
- 받은 사람은 Play Store 안에서 정상 설치
- 14일 시계 시작 X

**완료 기준**: 공유 링크 생성 + 본인 폰에서 링크 클릭 → 설치 → 실행 확인

---

### 3-B. 인앱상품 3종 + 라이선스 테스터(본인) 등록

**왜**: 본인 실기기 billing 검증을 PHASE 3 안에서 끝낸다. 4-A 가 14일 시계라 그 전에 결제 흐름을 확정.

**무엇을 할 일**

1. Play Console → 수익 창출 → 인앱상품 3개 생성
   - `kkeugi.cert` 일회 ₩11,000
   - `kkeugi.monthly` 월 ₩5,900
   - `kkeugi.yearly` 연 ₩39,000
2. 월/연 상품에 **7일 free trial offer** 추가
3. Play Console → 설정 → 라이선스 테스트 → **본인 Gmail 추가** (실 결제 안 되고 테스트 결제)

**완료 기준**: 인앱상품 3개 활성 + 본인 라이선스 테스터 등록

---

### 3-C. 본인 실기기 billing 검증

**무엇을 할 일**

1. 본인 안드로이드 실기기에서 3-A 링크로 끊기 설치 (라이선스 테스터 Gmail 로그인 상태)
2. 다음 4가지 확인:
   - paywall → 7일 무료로 시작 → 구매 다이얼로그 정확한 ₩ 표시
   - 구매 후 `/v1/payments/verify` 200 응답 + DB `subscriptions.status=active`, `in_trial=true`
   - paywall 잠금 풀리고 "매출환산" 행이 ON
   - 회고 탭 카드에 매출환산 표시
3. 회고 카드 공유 흐름: 회고 카드 → 공유 아이콘 → 1080×1920 이미지 → **인스타 스토리 / 카톡 등으로 실제 공유**

**완료 기준**: 실 구매 → 영수증 검증 → entitlement 해제까지 정상 + 카드 공유 OK

---

### 3-D. 지인 3~5명에게 sideload + 1주 사용

**무엇을 할 일**

1. **가까운 사람 3~5명**(가족·친한 친구) 선정 — 회사 동료 X
2. 각자 Gmail 주소를 받아 → Play Console → 내부 앱 공유 → **이 Gmail들을 "내부 공유 테스터"로 추가** (Internal App Sharing은 신원확인된 receiver 만 가능)
3. 3-A 공유 링크를 카톡/메일로 전송
4. 안내 문구:
   > 끊기 베타 미리 써봐줘. 14일 본격 테스트 전에 며칠 써보고 큰 문제 없는지 확인하려고 해.
   > 1. 링크 클릭 → Play Store 안에서 설치
   > 2. Google 로그인 → 사용 통계 권한 허용
   > 3. **1주 동안 평소처럼 사용**, 너무 어렵게 안 해도 됨
   > 4. 회고 카드 받으면 알려줘 (텔레그램/이메일 채널 선택 가능)
   > 5. 이상하면 그냥 카톡으로 알려주면 됨
5. **1주 동안 모니터링**
   - Sentry 대시보드: 에러 발생 여부
   - Mixpanel: 권한 동의·세션·결제 이벤트 흐름
   - 본인이 Play Console 의 내부 앱 공유 통계로 설치 여부 확인
   - 지인 피드백 카톡 받기

**완료 기준**: 1주 사용 후 큰 버그 0 또는 모두 해결 + 본인이 "이제 12명 테스터에게 보여줘도 되겠다" 판단

---

### 3-E. 발견된 버그·이슈 수정

**무엇을 할 일**

1. 1주 사용 중 발견된 이슈 → Claude 에게 의뢰해 수정
2. 새 AAB 빌드 → 동일 Internal App Sharing 으로 재배포 (지인은 자동 업데이트)
3. 큰 변경 있으면 지인에게 "업데이트 됐어, 한 번만 더 열어봐줘"
4. **이슈 다 잡혔다 판단 → PHASE 4 진입**

**완료 기준**: Sentry 에러 0건 7일 + 핵심 흐름(로그인·권한·결제·회고·공유) 모두 안정

---

## PHASE 4 — 3주차 ~ 4주차 (테스터 12명 모집)

**팁**: PHASE 3 중반(지인 사용 잘 되는 게 확인된 시점)부터 동시 시작하면 PHASE 5 진입을 1주 단축할 수 있다.

### 4-A. 테스터 15~16명 모집 (12명 + 이탈 버퍼 3~4명)

**왜**: 클로즈드 14일 동안 중간 이탈 buffer 가 필요. 12명 정확히는 risk.

**무엇을 할 일**

1. **세 갈래 동시 모집**
   - **지인·가족 추가 5~6명**: PHASE 3 의 3~5명은 그대로 두고, 이 PHASE 에서 추가 모집. "이번엔 14일 정식 베타야"라고 별도 안내.
   - **테스터 품앗이 6~7명**: 인디 개발자끼리 서로 테스터 되어주기. 활동 채널:
     - 카카오 오픈채팅 "구글 테스터 품앗이" 검색
     - OKKY 게시판
     - 디시 앱개발 갤러리
     - Reddit r/androiddev "closed testing exchange" 스레드
     - Discord — Google Play Closed Testing 교환 서버
   - **build-in-public 팔로워 3~4명**: X(트위터) 등 가벼운 공지
2. **Google Groups 1개 생성** → groups.google.com → 새 그룹. 이 그룹 주소를 Play Console "클로즈드 테스트 테스터 목록"으로 등록 예정. 일괄 add/remove 편리.
3. 모인 Gmail 들을 그룹에 차곡차곡 추가.

**테스터에게 보낼 안내 문구 (참고)**

> "끊기"라는 한국 1인 워커용 디지털 디톡스 안드로이드 앱 베타에 도와주세요.
> 1. 첨부 링크에서 "테스터 동의" 클릭
> 2. Play Store 에서 끊기 설치
> 3. 14일 동안 **주 1~2회만 1-2분** 열어주시면 됩니다 (홈 화면 숫자만 보고 닫아도 됨)
> 4. 14일 끝나면 알려드릴게요. 의견 주시면 V1 출시 반영.

**완료 기준**: Google Groups에 12~16명 Gmail + 동의 확보

---

## PHASE 5 — 4주차 ~ 6주차 (클로즈드 14일 시계)

### 5-A. 클로즈드 트랙 게시 → 14일 시계 시작

**무엇을 할 일**

1. Play Console → 클로즈드 테스트 트랙 생성
2. PHASE 3-A 의 AAB 그대로 또는 최신 빌드를 클로즈드 트랙에 업로드
3. 테스터 → 4-A 의 **Google Groups 주소**를 테스터 목록으로 등록
4. **클로즈드 트랙 게시** → 테스터에게 opt-in 링크 전송 → **14일 시계 시작**
5. 1~2일 안에 12명 이상 opt-in 안정화 확인

**완료 기준**: 12명 이상 opt-in 상태로 14일 카운트 진행

---

### 5-B. 14일 모니터링

- 매일 Play Console 통계 — 12명 이하로 내려가지 않는지 확인 (떨어지면 4-A 버퍼에서 보충)
- Sentry — 에러 발생 즉시 대응
- Mixpanel — 사용 패턴 확인 (Google 심사 시 "활성 사용" 신호로 작용)
- 이슈 발견 → 빌드 갱신 → 같은 트랙에 새 버전 → 테스터 자동 업데이트

**완료 기준**: 14일 종료 + 12명 안정 유지 + 큰 버그 0

---

## PHASE 6 — 6주차 ~ 7주차 (출시)

### 6-A. Store listing 작성

**무엇을 할 일**

1. 앱 아이콘 (512×512)
2. **스크린샷 4~8장** (실기기 또는 AVD)
   - 권장: 홈(0분/+47분), 회고 탭, 회고 카드 상세, 한도 설정, 공유 미리보기, paywall
3. **단문 설명**(80자): 한국 1인 워커를 위한 디지털 디톡스. SNS/쇼츠 끊기 + 주간 회고.
4. **장문 설명** (4000자 이내): wedge 3개 강조 — 시간빚 환산 / 자동 import / multi-channel retention
5. **카테고리**: 자기계발 권장
6. **Data safety**: 수집/공유 데이터 작성. 끊기는 사용 통계 + 이메일 정도.
7. **개인정보처리방침 URL** (2-F 결과)

**완료 기준**: Store listing 필수 항목 모두 입력

---

### 6-B. 프로덕션 출시 신청

**무엇을 할 일**

1. 14일 + 12명 요건 충족 확인
2. Play Console → 프로덕션 트랙 → AAB 업로드
3. 출시 검토 요청 → Google 심사 (수일)
4. 승인 → 단계적 출시 (한국 전용, 사용자 비율 100%)

**완료 기준**: Play Store 에서 일반 사용자 설치 가능

---

### 6-C. 런칭 공지

- 긱뉴스 (news.hada.io) build in public 글
- OKKY 게시판
- X(트위터)
- PHASE 3·4 테스터들에게 "정식 출시" 공유 부탁 + 회고 카드 공유 요청

---

## PHASE 7 — 출시 후

### 7-A. KPI 모니터링

- Mixpanel: 권한 동의율 · 채널 toggle 비율 · 구매 완료 · 회고 열람 · 한도 발동
- Sentry: 에러 발생 추적
- Play Console: 일별 설치/제거, 평점, ANR/Crash

### 7-B. 사업자 등록 결정 (M3 hard checkpoint)

**Trigger**: 출시 3개월 누적 **월 net 매출 ₩35~50만** 도달 시
- 도달 → 사업자 등록 → V2 (Toss 외부결제 수수료 절감 + 카카오톡 알림톡 추가)
- 미도달 → V1 path 유지 검토

---

## 비밀번호·키 보관 체크리스트

분실 시 출시·운영 불가. **백업 2곳 이상**.

- [ ] Play Console 비밀번호 + 2FA 복구 코드
- [ ] **업로드 키스토어 `.jks` 파일 + 비밀번호 2개** (분실 = 영구 업데이트 불가)
- [ ] Google Cloud 서비스 계정 JSON
- [ ] Web OAuth Client ID
- [ ] Telegram 봇 토큰
- [ ] Mailgun API key
- [ ] Fly.io API token
- [ ] Supabase DB password + connection string
- [ ] Anthropic API key
- [ ] Sentry DSN 2개
- [ ] Mixpanel project token
- [ ] JWT_SECRET (한 번 만들어 백엔드에 주입한 값)
- [ ] TELEGRAM_WEBHOOK_SECRET

---

## 한 페이지 체크리스트 (이것만 따라가도 됨)

PHASE 1 — 지금 ~ 1주차 (리드타임 동시 시작)
- [ ] 1-A Play Console 가입 + 신원확인 제출
- [ ] 1-B `kkeugi.kr` 도메인 등록
- [ ] 1-C 키스토어 생성 + 백업

PHASE 2 — 1주차 ~ 2주차 (백엔드 살림)
- [ ] 2-A Play Console 앱 생성(`kr.pjshi.kkeugi`) + SHA-1 2개 추출
- [ ] 2-B Google Cloud OAuth(Android + Web) + 서비스 계정 JSON
- [ ] 2-C Telegram 봇 + Mailgun 도메인 + DNS
- [ ] 2-D Fly.io + Supabase + Anthropic + Sentry + Mixpanel
- [ ] 2-E Secrets 등록 + 첫 배포 + `api.kkeugi.kr` 살림
- [ ] 2-F Telegram 웹훅 + Mailgun 실발송 + 법무 URL 호스팅

PHASE 3 — 2주차 ~ 3주차 ⭐ 지인 1주 soft test
- [ ] 3-A 릴리스 AAB 빌드 + Internal App Sharing 업로드
- [ ] 3-B 인앱상품 3종 + 라이선스 테스터(본인) 등록
- [ ] 3-C 본인 실기기 billing 검증 + 회고 카드 공유 검증
- [ ] 3-D 지인 3~5명 sideload + 1주 사용
- [ ] 3-E 발견된 이슈 수정 + 안정화

PHASE 4 — 3주차 ~ 4주차 (테스터 12명 모집)
- [ ] 4-A 테스터 15~16명 Gmail 확보 + Google Groups 생성

PHASE 5 — 4주차 ~ 6주차 (클로즈드 14일)
- [ ] 5-A 클로즈드 트랙 게시 → 14일 시계 시작
- [ ] 5-B 14일 모니터링 + 이슈 즉시 대응

PHASE 6 — 6주차 ~ 7주차 (출시)
- [ ] 6-A Store listing (스크린샷 + 설명 + data safety)
- [ ] 6-B 프로덕션 트랙 출시 신청
- [ ] 6-C 런칭 공지 (긱뉴스 · OKKY · X)

PHASE 7 — 출시 후
- [ ] 7-A KPI 모니터링
- [ ] 7-B 사업자 등록 결정 (월 net 매출 ₩35~50만 도달 시)

---

## 마지막 메모

- **클로즈드 14일 시계의 진짜 시작은 PHASE 5-A** (게시 시점). 그 전 PHASE 3 의 Internal App Sharing 은 시계 X.
- PHASE 3 soft test 가 잘 끝나면 PHASE 5 의 14일이 거의 무사고로 흐를 가능성이 매우 높아진다 — 이 1주가 곧 보험.
- 외부 작업 중 막히면(신원확인 반려·DNS 미전파·인앱상품 활성 지연) 그 PHASE 의 다른 항목을 먼저 진행해 시간을 벌 것.
- 키스토어·서비스 계정 JSON 분실 시 복구 불가. 백업 2곳 이상.
- 회사 겸업 정책상 본명 노출은 최소화. 개발자 표시명 = `pjshi` 같은 브랜드.

끝. 이 문서는 그대로 본인 메일로 보내 외부에서도 절차대로 따라갈 수 있습니다.

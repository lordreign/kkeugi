# 개인정보처리방침 — 끊기 (Kkeugi)

> 시행일: 2026-06-01 (W8 launch 예정일)
> 최종 update: 2026-05-24 (초안, 법무 자문 V2 시점 필요)

## 1. 개인정보 수집·이용 항목

### 필수 수집 항목 (Google Sign-In 시)
- Google 계정 식별자 (`sub`, 변경되지 않는 고유 ID)
- 이메일 주소 (Google 인증)
- 표시 이름 (Google 프로필)

### 사용 데이터 (선택 권한, 별도 동의)
- Android `PACKAGE_USAGE_STATS` 권한을 통한 앱 사용 시간·앱 패키지 이름·사용 시각
- 기기 안에서만 분석 후 본인 사용자 본인 ID와 함께 서버 저장
- 다른 사용자에게 노출 0, 광고 활용 0

### 자동 수집 항목
- IP 주소 (보안 로그 + refresh token 검증)
- User agent
- FCM 토큰 (푸시 알림 발송용)

### 선택 추가 항목 (사용자가 활성화 시)
- 시간당 가치 (매출 환산 기능 사용 시)
- 작업 시간대 (V1.5 heuristic 기능 사용 시)
- 이메일 주소 (Mailgun 발송용, Google과 다를 수 있음)
- Telegram chat ID (Telegram 알림 사용 시)

## 2. 수집·이용 목적
- 회원 인증 및 관리
- AI 주간 회고 카드 생성·발송
- Multi-channel 알림 (FCM·이메일·Telegram) 발송
- 인앱결제 처리 및 결제 영수증 발급
- 서비스 개선 (집계 통계 활용)
- 부정 사용 방지

## 3. 보유·이용 기간
- 회원 정보: 회원 탈퇴 시점부터 **30일 grace period 후 hard delete**
- 사용 데이터 (`usage_events`): 회원 탈퇴 시점부터 30일 grace 후 삭제
- 결제 정보: 전자상거래법에 따라 **5년 보관** (의무 보관)
- 접속 로그: 통신비밀보호법에 따라 **3개월 보관**

## 4. 제3자 제공
원칙적으로 제3자 제공하지 않습니다. 단 다음의 경우 예외:
- 법령상 의무 (수사기관 영장 등)
- 본인 명시적 동의

## 5. 처리 위탁
다음 사업자에게 일부 업무를 위탁합니다. 위탁사 별 처리 데이터 범위 명시:

| 위탁사 | 위탁 목적 | 처리 데이터 | 국외 이전 |
|---|---|---|---|
| **Fly.io, Inc.** (미국) | 백엔드 호스팅 (Tokyo region) | 모든 서버 처리 데이터 | ✅ 미국 모회사 |
| **Supabase, Inc.** (미국) | PostgreSQL DB 호스팅 (Northeast Asia Seoul region) | 사용자·사용 데이터·결제 정보 | ✅ 미국 모회사 |
| **Anthropic PBC** (미국) | AI 주간 회고 LLM 호출 | 사용 통계 요약 (사용자 ID 비식별) | ✅ 미국 |
| **Google LLC** (Google Sign-In + FCM) | 인증·푸시 발송 | 계정 식별자·FCM 토큰 | ✅ 미국 |
| **Google Play Billing** | 결제 처리 | 결제 정보 | ✅ 미국 |
| **Mailgun Technologies** (W4 도입) | 이메일 발송 | 이메일 주소·발송 내용 | ✅ 미국 |
| **Telegram Messenger LLP** (W5 도입) | Telegram Bot 발송 | Telegram chat ID·메시지 내용 | ✅ 영국 |
| **Functional Software, Inc. (Sentry)** | 에러 모니터링 | 에러 stack trace (개인정보 자동 마스킹) | ✅ 미국 |
| **Mixpanel, Inc.** | 사용 분석 | 익명화 이벤트 데이터 | ✅ 미국 |

**국외 이전 동의는 회원 가입 시 별도 체크박스로 받습니다.**

## 6. 만 14세 미만 가입 제한
본 서비스는 **만 14세 이상**만 가입할 수 있습니다. Google Sign-In 인증 후 생년월일 확인 단계를 진행합니다.

## 7. 정보주체의 권리
회원은 언제든 다음 권리를 행사할 수 있습니다:
- 개인정보 열람 요청
- 정정·삭제 요청
- 처리 정지 요청
- 회원 탈퇴 (앱 내 설정 → 회원 탈퇴, 즉시 처리)

## 8. 개인정보 안전성 확보
- 모든 통신 HTTPS (Let's Encrypt TLS)
- 비밀번호 사용하지 않음 (Google Sign-In)
- JWT 15분 access + 30일 refresh + rotation
- Postgres 일별 자동 backup (Supabase)
- 접근 로그 3개월 보관

## 9. 개인정보 보호책임자
- 이름: [개인사업자 등록 후 본인 명의]
- 이메일: privacy@kkeugi.kr (도메인 등록 후)

## 10. 처리방침 변경
변경 시 14일 전 앱 내 공지 + 본 페이지 update.

---

**법무 검토 메모 (2026-05-24)**:
- 본 초안은 PIPA + 정보통신망법 기본 요구사항 반영
- V2 사업자 등록 시점에 법무 자문 ₩50-70만 (PRD §11 P7)
- 카톡 알림톡 추가 시점 (V2)에 처리방침 update
- Toss 외부결제 도입 시 (V2)에 결제 위탁 추가

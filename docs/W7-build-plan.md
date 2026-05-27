# W7 빌드 플랜 — threshold 로컬 알람 + 한도 설정 + KPI

> W5/W6와 동일: 배포 전 단계별 검증. 상세: [PRD §12 W7](PRD.md) · [REMAINING-WORK A-3](REMAINING-WORK.md)
> 본인 작업(클로즈드 베타 12명/14일·실기기)은 [REMAINING-WORK B](REMAINING-WORK.md).

## 원칙
- **threshold 알람은 로컬**: 서버 cron 아닌 Flutter가 today usage(서버 stats 또는 로컬) vs 한도 비교 → `flutter_local_notifications` 즉시 알람. 사업자 X로 가능(로컬 알림).
- **한도 생성은 유료**(PRD: thresholds create = paid). 조회/수정은 기본.
- KPI는 Mixpanel free — 권한 동의율·채널 retention·D7/D30·NPS.

## 빌드 순서
- [x] **Step 1 — thresholds 백엔드** ✅ (2026-05-26): `Threshold` 모델 + `GET/POST(require_paid)/PATCH/DELETE /v1/thresholds` + 카테고리 유니크(409) + 소유권 체크(404). pytest 7건(65 green) + 라이브(무료 402 / 유료 201).
- [x] **Step 2 — 한도 설정 UI** ✅ (2026-05-26): `thresholds_api`·`provider` + `ThresholdsScreen`(목록·토글·삭제·빈상태, 무료는 paywall) + `AddThresholdScreen`(카테고리/분 chips + 저장) + 설정 목표 행 연결(개수 표시). 위젯 2건(8 green) + AVD(paid 추가→"SNS 하루 30분" 카드).
- [x] **Step 3 — threshold 로컬 알람** ✅ (2026-05-26): `LocalNotifications`(flutter_local_notifications 래퍼 + `threshold_alarms` 채널 + Android 13+ 권한 요청) + `threshold_alarm`(순수 `computeThresholdHits` + `fireThresholdAlarms` 1일 1회 prefs dedup + `checkAndNotifyThresholds`) + `thresholdAlarmProvider`(홈에서 todayStats·thresholds 재사용, 추가 호출 X) + worker 백그라운드 체크 + main init + POST_NOTIFICATIONS + 한도 저장 시 권한 요청. 유닛 9건(17 green) + debug APK 빌드 + **AVD end-to-end**(SNS 40분/한도 30분 → "SNS 한도를 넘었어요" 알림 렌더).
- [x] **Step 4 — KPI metrics** ✅ (2026-05-27): `Analytics` 추상화(`FakeAnalytics` 토큰X dev / `MixpanelAnalytics` HTTP `/track` — 네이티브 SDK 없이 dio, 백엔드 FCM/Mailgun과 동일 패턴) + `analyticsProvider`(`Env.mixpanelToken` 스위치) + 6개 이벤트 계측(`permission_granted` 1회 / `channel_toggled` / `purchase_completed` / `report_viewed` / `threshold_created` / `threshold_fired`) + 로그인 시 `identify(user.id)`. 유닛 4건(21 green) + debug APK + **AVD**(dev login → logcat `[analytics] permission_granted`·`threshold_fired{sns}` 확인). 실 전송은 `MIXPANEL_TOKEN`(본인 작업).

## 검증
- 백엔드 `make lint`+`make test`+라이브 curl
- 프론트 `flutter analyze`+위젯 테스트+AVD
- 각 Step 종료 시 CLAUDE.md 변경 이력 1줄

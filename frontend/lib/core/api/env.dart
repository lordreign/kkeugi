import 'package:flutter/foundation.dart';

/// API base URL — set via --dart-define at build time.
///
/// Defaults:
///   Android emulator: http://10.0.2.2:8080
///   Real device:      use PC IP, e.g. http://192.168.0.10:8080
///   Production:       https://api.kkeugi.kr
class Env {
  Env._();

  static const apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8080',
  );

  static const isProduction = bool.fromEnvironment(
    'IS_PRODUCTION',
    defaultValue: false,
  );

  static const sentryDsn = String.fromEnvironment('SENTRY_DSN', defaultValue: '');

  /// KPI: Mixpanel 프로젝트 토큰. 미설정(dev)이면 FakeAnalytics로 대체.
  static const mixpanelToken =
      String.fromEnvironment('MIXPANEL_TOKEN', defaultValue: '');

  /// 결제: Fake billing(서버 fake verifier 경유) 사용 여부.
  /// debug 기본 true → Play Console 없이 전 플로우 검증. release는 false 전달.
  static const useFakeBilling = bool.fromEnvironment(
    'USE_FAKE_BILLING',
    defaultValue: !kReleaseMode,
  );
}

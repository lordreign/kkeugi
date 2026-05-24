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
}

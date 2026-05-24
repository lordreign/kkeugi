import 'package:dio/dio.dart';

import '../storage/secure_storage.dart';
import 'env.dart';

/// Attaches JWT to every request.
/// On 401: tries /v1/auth/refresh once, retries original request.
/// On refresh fail: clears storage + emits logout signal (caller redirects to /login).
class AuthInterceptor extends QueuedInterceptor {
  AuthInterceptor({required this.onAuthExpired});

  final void Function() onAuthExpired;

  bool _refreshing = false;

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Skip auth endpoints
    if (options.path.startsWith('/v1/auth/google') ||
        options.path.startsWith('/v1/auth/dev/login') ||
        options.path.startsWith('/v1/auth/refresh')) {
      return handler.next(options);
    }

    final token = await SecureStorage.readAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  Future<void> onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode != 401 || _refreshing) {
      return handler.next(err);
    }

    _refreshing = true;
    try {
      final refresh = await SecureStorage.readRefreshToken();
      if (refresh == null) {
        await SecureStorage.clear();
        onAuthExpired();
        return handler.next(err);
      }

      final refreshDio = Dio(BaseOptions(baseUrl: Env.apiBaseUrl));
      final resp = await refreshDio.post<Map<String, dynamic>>(
        '/v1/auth/refresh',
        data: {'refresh_token': refresh},
      );

      final newAccess = resp.data!['access_token'] as String;
      final newRefresh = resp.data!['refresh_token'] as String;
      await SecureStorage.saveTokens(
        accessToken: newAccess,
        refreshToken: newRefresh,
      );

      // Retry original request
      final retryOptions = err.requestOptions
        ..headers['Authorization'] = 'Bearer $newAccess';
      final retryDio = Dio(BaseOptions(baseUrl: Env.apiBaseUrl));
      final retryResp = await retryDio.fetch<dynamic>(retryOptions);
      handler.resolve(retryResp);
    } on DioException {
      await SecureStorage.clear();
      onAuthExpired();
      handler.next(err);
    } finally {
      _refreshing = false;
    }
  }
}

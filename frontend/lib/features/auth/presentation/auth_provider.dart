import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/env.dart';
import '../../../core/api/auth_interceptor.dart';
import '../../../core/storage/secure_storage.dart';
import '../data/auth_api.dart';
import '../domain/auth_state.dart';

final authProvider = NotifierProvider<AuthNotifier, AuthState>(AuthNotifier.new);

/// Shared authenticated Dio — features가 이걸 watch해서 API 호출.
final dioProvider = Provider<Dio>((ref) {
  // auth notifier가 dio를 소유하므로 거기서 가져옴
  return ref.watch(authProvider.notifier).dio;
});

class AuthNotifier extends Notifier<AuthState> {
  late final Dio dio;
  late final AuthApi _api;

  @override
  AuthState build() {
    dio = Dio(
      BaseOptions(
        baseUrl: Env.apiBaseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
      ),
    );
    dio.interceptors.add(AuthInterceptor(onAuthExpired: _onExpired));
    _api = AuthApi(dio);
    return const AuthState.unknown();
  }

  /// 앱 시작 시 저장된 토큰으로 자동 로그인 시도.
  Future<void> restore() async {
    final hasToken = await SecureStorage.hasTokens();
    if (!hasToken) {
      state = const AuthState.unauthenticated();
      return;
    }
    try {
      final me = await _api.me();
      state = AuthState.authenticated(me);
    } on DioException {
      await SecureStorage.clear();
      state = const AuthState.unauthenticated();
    }
  }

  Future<void> loginWithGoogle(String idToken) async {
    final pair = await _api.loginWithGoogle(idToken);
    await SecureStorage.saveTokens(
      accessToken: pair.accessToken,
      refreshToken: pair.refreshToken,
    );
    state = AuthState.authenticated(pair.user);
  }

  /// Dev-only — backend ENVIRONMENT development/test.
  Future<void> devLogin({required String email, String? name}) async {
    final pair = await _api.devLogin(email: email, name: name);
    await SecureStorage.saveTokens(
      accessToken: pair.accessToken,
      refreshToken: pair.refreshToken,
    );
    state = AuthState.authenticated(pair.user);
  }

  Future<void> updateHourlyValue(int hourlyValue) async {
    try {
      await dio.patch<Map<String, dynamic>>(
        '/v1/me',
        data: {'hourly_value': hourlyValue},
      );
    } on DioException {
      // non-blocking — 설정에서 재시도 가능
    }
  }

  Future<void> logout() async {
    final refresh = await SecureStorage.readRefreshToken();
    if (refresh != null) {
      try {
        await _api.logout(refresh);
      } on DioException {
        // ignore — clear locally anyway
      }
    }
    await SecureStorage.clear();
    state = const AuthState.unauthenticated();
  }

  void _onExpired() {
    SecureStorage.clear();
    state = const AuthState.unauthenticated();
  }
}

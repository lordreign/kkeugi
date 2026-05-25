import 'package:dio/dio.dart';

class AuthApi {
  AuthApi(this._dio);

  final Dio _dio;

  Future<TokenPairResponse> loginWithGoogle(String idToken) async {
    final resp = await _dio.post<Map<String, dynamic>>(
      '/v1/auth/google',
      data: {'id_token': idToken},
    );
    return TokenPairResponse.fromJson(resp.data!);
  }

  /// Dev-only login — backend ENVIRONMENT must be development/test.
  Future<TokenPairResponse> devLogin({required String email, String? name}) async {
    final resp = await _dio.post<Map<String, dynamic>>(
      '/v1/auth/dev/login',
      data: {'email': email, if (name != null) 'name': name},
    );
    return TokenPairResponse.fromJson(resp.data!);
  }

  Future<void> logout(String refreshToken) async {
    await _dio.post<void>(
      '/v1/auth/logout',
      data: {'refresh_token': refreshToken},
    );
  }

  Future<UserResponse> me() async {
    final resp = await _dio.get<Map<String, dynamic>>('/v1/me');
    return UserResponse.fromJson(resp.data!);
  }
}

class TokenPairResponse {
  TokenPairResponse({
    required this.accessToken,
    required this.refreshToken,
    required this.user,
  });

  factory TokenPairResponse.fromJson(Map<String, dynamic> json) => TokenPairResponse(
        accessToken: json['access_token'] as String,
        refreshToken: json['refresh_token'] as String,
        user: UserResponse.fromJson(json['user'] as Map<String, dynamic>),
      );

  final String accessToken;
  final String refreshToken;
  final UserResponse user;
}

class UserResponse {
  UserResponse({
    required this.id,
    required this.email,
    required this.tier,
    this.displayName,
    this.hourlyValue,
  });

  factory UserResponse.fromJson(Map<String, dynamic> json) => UserResponse(
        id: json['id'] as String,
        email: json['email'] as String,
        tier: json['tier'] as String,
        displayName: json['display_name'] as String?,
        hourlyValue: json['hourly_value'] as int?,
      );

  final String id;
  final String email;
  final String tier;
  final String? displayName;
  final int? hourlyValue;
}

import 'package:dio/dio.dart';

import 'auth_interceptor.dart';
import 'env.dart';

/// Singleton-style ApiClient. Use through Riverpod provider in real code.
class ApiClient {
  ApiClient({required this.onAuthExpired}) {
    dio = Dio(
      BaseOptions(
        baseUrl: Env.apiBaseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 30),
        contentType: 'application/json',
        responseType: ResponseType.json,
      ),
    );
    dio.interceptors.add(AuthInterceptor(onAuthExpired: onAuthExpired));
  }

  late final Dio dio;
  final void Function() onAuthExpired;
}

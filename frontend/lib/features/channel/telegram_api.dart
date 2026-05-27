import 'package:dio/dio.dart';

class TelegramStatus {
  const TelegramStatus({required this.linked, required this.subscribed});

  factory TelegramStatus.fromJson(Map<String, dynamic> j) => TelegramStatus(
        linked: j['linked'] as bool,
        subscribed: j['subscribed'] as bool,
      );

  final bool linked;
  final bool subscribed;

  static const none = TelegramStatus(linked: false, subscribed: false);
}

class TelegramApi {
  TelegramApi(this._dio);

  final Dio _dio;

  Future<TelegramStatus> status() async {
    final resp = await _dio.get<Map<String, dynamic>>('/v1/me/telegram');
    return TelegramStatus.fromJson(resp.data!);
  }

  /// 딥링크 발급 — 사용자가 이 URL을 열어 봇에 /start 보내면 chat_id 바인딩.
  Future<String> linkToken() async {
    final resp = await _dio.post<Map<String, dynamic>>('/v1/me/telegram/link_token');
    return resp.data!['deep_link'] as String;
  }

  Future<void> unsubscribe() async {
    await _dio.delete<void>('/v1/me/telegram');
  }
}

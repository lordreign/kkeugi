import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

/// KPI 이벤트 이름 — PRD §13 (권한 동의율·채널 retention·구매·리포트 열람·한도 발동).
/// 한 곳에 모아 오타·드리프트 방지.
abstract final class AnalyticsEvents {
  static const permissionGranted = 'permission_granted'; // usage stats 권한 동의
  static const channelToggled = 'channel_toggled'; // 알림 채널 on/off
  static const purchaseCompleted = 'purchase_completed'; // 결제 완료
  static const reportViewed = 'report_viewed'; // 주간 회고 열람
  static const reportShared = 'report_shared'; // 회고 카드 공유 (바이럴)
  static const thresholdCreated = 'threshold_created'; // 한도 설정
  static const thresholdFired = 'threshold_fired'; // 한도 초과 알람 발동
}

/// 분석 인터페이스 — UI/로직이 Mixpanel 구현에 직접 의존하지 않도록 분리.
/// 토큰 미설정(dev) 시 FakeAnalytics로 대체 → 키 없이 계측 코드 검증.
abstract class Analytics {
  /// 사용자 식별 — 로그인 시 user id로 distinct_id 고정.
  void identify(String distinctId);

  /// 이벤트 기록. KPI를 막지 않도록 절대 throw하지 않는다(fire-and-forget).
  Future<void> track(String event, [Map<String, Object?> props = const {}]);
}

/// 토큰 없을 때(dev/test) — 전송 없이 기록만. 디버그 로그 + 테스트 검증용.
class FakeAnalytics implements Analytics {
  final List<({String event, Map<String, Object?> props})> events = [];
  String? distinctId;

  @override
  void identify(String distinctId) => this.distinctId = distinctId;

  @override
  Future<void> track(String event, [Map<String, Object?> props = const {}]) async {
    events.add((event: event, props: props));
    if (kDebugMode) {
      debugPrint('[analytics] $event ${props.isEmpty ? '' : props}');
    }
  }
}

/// Mixpanel /track HTTP API — 네이티브 SDK 없이 dio로 직접 전송
/// (백엔드 FCM/Mailgun과 동일한 "HTTP API only" 패턴). 실패는 무시.
class MixpanelAnalytics implements Analytics {
  MixpanelAnalytics(this._token, {Dio? dio})
      : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: 'https://api.mixpanel.com',
                connectTimeout: const Duration(seconds: 5),
                sendTimeout: const Duration(seconds: 5),
                receiveTimeout: const Duration(seconds: 5),
              ),
            );

  final String _token;
  final Dio _dio;
  String _distinctId = 'anonymous';

  @override
  void identify(String distinctId) => _distinctId = distinctId;

  @override
  Future<void> track(String event, [Map<String, Object?> props = const {}]) async {
    try {
      await _dio.post<dynamic>(
        '/track',
        data: [
          {
            'event': event,
            'properties': {
              'token': _token,
              'distinct_id': _distinctId,
              'time': DateTime.now().millisecondsSinceEpoch,
              ...props,
            },
          },
        ],
        options: Options(contentType: 'application/json'),
      );
    } catch (_) {
      // KPI는 best-effort — 네트워크 실패가 UX를 막지 않는다.
    }
  }
}

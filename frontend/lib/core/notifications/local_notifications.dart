import 'package:flutter_local_notifications/flutter_local_notifications.dart';

/// 알람 발송 인터페이스 — 순수 로직(threshold_alarm)이 플러그인에 직접 의존하지
/// 않도록 분리. 테스트에서 fake로 대체해 발송 횟수를 검증한다.
abstract class NotificationSink {
  Future<void> show({
    required int id,
    required String title,
    required String body,
  });
}

/// flutter_local_notifications 래퍼 — 로컬(기기 내) 알람만. 사업자 X로 가능.
/// 즉시 show만 사용(예약 zonedSchedule 미사용 → 추가 receiver 불필요).
class LocalNotifications implements NotificationSink {
  LocalNotifications._();
  static final LocalNotifications instance = LocalNotifications._();

  static const _channelId = 'threshold_alarms';
  static const _channelName = '한도 알림';
  static const _channelDesc = '카테고리별 일일 한도 초과를 조용히 알려드려요.';

  final FlutterLocalNotificationsPlugin _plugin =
      FlutterLocalNotificationsPlugin();
  bool _initialized = false;

  /// main()·백그라운드 isolate 양쪽에서 1회 호출. 멱등.
  Future<void> init() async {
    if (_initialized) return;
    const androidInit = AndroidInitializationSettings('@mipmap/ic_launcher');
    await _plugin.initialize(
      const InitializationSettings(android: androidInit),
    );
    await _android?.createNotificationChannel(
      const AndroidNotificationChannel(
        _channelId,
        _channelName,
        description: _channelDesc,
        importance: Importance.defaultImportance,
      ),
    );
    _initialized = true;
  }

  AndroidFlutterLocalNotificationsPlugin? get _android =>
      _plugin.resolvePlatformSpecificImplementation<
          AndroidFlutterLocalNotificationsPlugin>();

  /// Android 13+ POST_NOTIFICATIONS 런타임 권한 요청. 허용 여부 반환.
  /// 12 이하·iOS는 권한 개념이 달라 true로 간주.
  Future<bool> requestPermission() async {
    await init();
    final android = _android;
    if (android == null) return true;
    return await android.requestNotificationsPermission() ?? false;
  }

  @override
  Future<void> show({
    required int id,
    required String title,
    required String body,
  }) async {
    await init();
    const details = NotificationDetails(
      android: AndroidNotificationDetails(
        _channelId,
        _channelName,
        channelDescription: _channelDesc,
        importance: Importance.defaultImportance,
        priority: Priority.defaultPriority,
      ),
    );
    await _plugin.show(id, title, body, details);
  }
}

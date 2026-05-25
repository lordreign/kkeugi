import 'package:flutter/services.dart';

/// 포그라운드 사용 세션 1건 (네이티브 UsageStatsManager에서).
class UsageSession {
  const UsageSession({
    required this.packageName,
    required this.start,
    required this.duration,
  });

  final String packageName;
  final DateTime start;
  final Duration duration;
}

/// UsageStatsManager 네이티브 브리지 (MainActivity.kt 의 MethodChannel).
class UsageChannel {
  static const _channel = MethodChannel('kr.kkeugi/usage');

  /// PACKAGE_USAGE_STATS 허용 여부.
  static Future<bool> hasPermission() async {
    final v = await _channel.invokeMethod<bool>('hasPermission');
    return v ?? false;
  }

  /// 시스템 "사용 정보 접근" 설정 화면 열기 (사용자가 직접 토글).
  static Future<void> openUsageAccessSettings() =>
      _channel.invokeMethod<void>('openUsageAccessSettings');

  /// [start, end) 구간의 포그라운드 세션 조회.
  static Future<List<UsageSession>> querySessions(
    DateTime start,
    DateTime end,
  ) async {
    final raw = await _channel.invokeMethod<List<dynamic>>(
      'queryUsageSessions',
      {
        'startMs': start.millisecondsSinceEpoch,
        'endMs': end.millisecondsSinceEpoch,
      },
    );
    if (raw == null) return const [];
    return raw.map((e) {
      final m = (e as Map).cast<String, dynamic>();
      return UsageSession(
        packageName: m['packageName'] as String,
        start: DateTime.fromMillisecondsSinceEpoch(
          (m['startMs'] as num).toInt(),
        ),
        duration: Duration(milliseconds: (m['durationMs'] as num).toInt()),
      );
    }).toList();
  }
}

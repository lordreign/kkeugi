import 'dart:convert';

import 'package:flutter/services.dart';

/// 앱별 표시용 메타 (이름·아이콘). 서버는 package_name만 알고,
/// 사람이 읽는 이름·아이콘은 표시 직전 네이티브 PackageManager에서 해석한다.
class AppMeta {
  const AppMeta({
    required this.packageName,
    required this.label,
    required this.icon,
  });

  final String packageName;
  final String label;
  final Uint8List? icon; // PNG bytes, 삭제된 앱은 null

  /// 표시 이름 — 라벨이 비었으면 패키지명 fallback.
  String get displayName => label.isEmpty ? packageName : label;
}

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
  static const _channel = MethodChannel('kr.pjshi/usage');

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

  /// 패키지명 리스트 → 앱 이름·아이콘. 표시할 top N에만 호출 (아이콘은 무거움).
  static Future<List<AppMeta>> getAppMeta(List<String> packages) async {
    if (packages.isEmpty) return const [];
    final raw = await _channel.invokeMethod<List<dynamic>>(
      'getAppMeta',
      {'packages': packages},
    );
    if (raw == null) return const [];
    return raw.map((e) {
      final m = (e as Map).cast<String, dynamic>();
      final b64 = (m['iconBase64'] as String?) ?? '';
      return AppMeta(
        packageName: m['packageName'] as String,
        label: (m['label'] as String?) ?? '',
        icon: b64.isEmpty ? null : base64Decode(b64),
      );
    }).toList();
  }
}

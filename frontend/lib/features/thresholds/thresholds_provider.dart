import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../../core/notifications/local_notifications.dart';
import '../auth/presentation/auth_provider.dart';
import '../usage/usage_providers.dart';
import 'threshold_alarm.dart';
import 'thresholds_api.dart';

final thresholdsApiProvider = Provider<ThresholdsApi>(
  (ref) => ThresholdsApi(ref.watch(dioProvider)),
);

final thresholdsListProvider = FutureProvider<List<ThresholdItem>>(
  (ref) => ref.watch(thresholdsApiProvider).list(),
);

/// 한도 알람 (foreground) — 이미 로드된 todayStats·thresholds provider를
/// 재사용해 추가 네트워크 호출 없이 초과분을 알람. 홈에서 watch로 활성화.
/// 발송 건수 반환(중복은 prefs로 1일 1회 방지).
final thresholdAlarmProvider = FutureProvider.autoDispose<int>((ref) async {
  final stats = await ref.watch(todayStatsProvider.future);
  final thresholds = await ref.watch(thresholdsListProvider.future);
  final hits = computeThresholdHits(stats: stats, thresholds: thresholds);
  final fired = await fireThresholdAlarms(
    hits: hits,
    sink: LocalNotifications.instance,
  );
  final analytics = ref.read(analyticsProvider);
  for (final hit in fired) {
    await analytics.track(
      AnalyticsEvents.thresholdFired,
      {'category': hit.category},
    );
  }
  return fired.length;
});

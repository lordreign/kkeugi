import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../core/notifications/local_notifications.dart';
import '../usage/usage_api.dart';
import 'thresholds_api.dart';

/// 한도 초과 1건 — 알람 대상 카테고리 + 수치.
class ThresholdHit {
  const ThresholdHit({
    required this.category,
    required this.usedMinutes,
    required this.limitMinutes,
  });

  final String category;
  final int usedMinutes;
  final int limitMinutes;

  String get label => thresholdCategoryLabels[category] ?? category;
}

/// 순수 비교 — enabled 한도 중 오늘 사용량이 한도 이상인 카테고리.
/// 부수효과 없음(테스트 대상).
List<ThresholdHit> computeThresholdHits({
  required TodayStats stats,
  required List<ThresholdItem> thresholds,
}) {
  final used = {for (final c in stats.byCategory) c.category: c.minutes};
  final hits = <ThresholdHit>[];
  for (final t in thresholds) {
    if (!t.enabled) continue;
    final u = used[t.category] ?? 0;
    if (u >= t.dailyLimitMinutes) {
      hits.add(
        ThresholdHit(
          category: t.category,
          usedMinutes: u,
          limitMinutes: t.dailyLimitMinutes,
        ),
      );
    }
  }
  return hits;
}

String _dateKey(DateTime d) =>
    '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';

const _firedPrefix = 'threshold_fired_';

/// 초과분 알람 발송 + 1일 1회 중복 방지(prefs). 실제 발송한 hit 리스트 반환
/// (KPI threshold_fired 계측에 사용). 같은 카테고리는 같은 날 한 번만 — DESIGN "압박 X" 톤.
Future<List<ThresholdHit>> fireThresholdAlarms({
  required List<ThresholdHit> hits,
  required NotificationSink sink,
  DateTime? now,
}) async {
  if (hits.isEmpty) return const [];
  final n = now ?? DateTime.now();
  final today = _dateKey(n);
  final prefs = await SharedPreferences.getInstance();

  // 이전 날짜 플래그 정리(누적 방지).
  for (final key in prefs.getKeys().toList()) {
    if (key.startsWith(_firedPrefix) && !key.endsWith(today)) {
      await prefs.remove(key);
    }
  }

  final fired = <ThresholdHit>[];
  for (final hit in hits) {
    final key = '$_firedPrefix${hit.category}_$today';
    if (prefs.getBool(key) ?? false) continue; // 오늘 이미 알림
    await sink.show(
      id: hit.category.hashCode & 0x7fffffff,
      title: '${hit.label} 한도를 넘었어요',
      body: '오늘 ${hit.usedMinutes}분 · 한도 ${hit.limitMinutes}분. '
          '비난은 아니에요 — 그냥 알려드려요.',
    );
    await prefs.setBool(key, true);
    fired.add(hit);
  }
  return fired;
}

/// 한도 체크 + 알람 — 자체적으로 thresholds·today stats 조회.
/// 백그라운드 isolate(usage_worker)에서 사용. 앱이 떠 있는 동안의
/// foreground 체크는 thresholdAlarmProvider가 로드된 provider를 재사용한다.
Future<List<ThresholdHit>> checkAndNotifyThresholds({
  required Dio dio,
  NotificationSink? sink,
  DateTime? now,
}) async {
  final thresholds = await ThresholdsApi(dio).list();
  if (thresholds.every((t) => !t.enabled)) return const [];
  final stats = await UsageApi(dio).today();
  final hits = computeThresholdHits(stats: stats, thresholds: thresholds);
  return fireThresholdAlarms(
    hits: hits,
    sink: sink ?? LocalNotifications.instance,
    now: now,
  );
}

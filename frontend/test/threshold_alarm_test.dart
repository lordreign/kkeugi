import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/core/notifications/local_notifications.dart';
import 'package:kkeugi/features/thresholds/threshold_alarm.dart';
import 'package:kkeugi/features/thresholds/thresholds_api.dart';
import 'package:kkeugi/features/usage/usage_api.dart';
import 'package:shared_preferences/shared_preferences.dart';

TodayStats _stats(Map<String, int> byCategory) => TodayStats(
      date: '2026-05-26',
      totalMinutes: byCategory.values.fold(0, (a, b) => a + b),
      inWorkMinutes: 0,
      byCategory: [
        for (final e in byCategory.entries)
          CategoryStat(category: e.key, minutes: e.value),
      ],
    );

ThresholdItem _t(String cat, int min, {bool enabled = true}) => ThresholdItem(
      id: cat,
      category: cat,
      dailyLimitMinutes: min,
      enabled: enabled,
    );

class _FakeSink implements NotificationSink {
  final List<String> shown = [];

  @override
  Future<void> show({
    required int id,
    required String title,
    required String body,
  }) async {
    shown.add(title);
  }
}

void main() {
  group('computeThresholdHits', () {
    test('한도 이상이면 hit', () {
      final hits = computeThresholdHits(
        stats: _stats({'sns': 35}),
        thresholds: [_t('sns', 30)],
      );
      expect(hits, hasLength(1));
      expect(hits.first.category, 'sns');
      expect(hits.first.usedMinutes, 35);
      expect(hits.first.limitMinutes, 30);
    });

    test('한도 미만이면 hit 없음', () {
      final hits = computeThresholdHits(
        stats: _stats({'sns': 20}),
        thresholds: [_t('sns', 30)],
      );
      expect(hits, isEmpty);
    });

    test('정확히 한도면 hit (>= 경계)', () {
      final hits = computeThresholdHits(
        stats: _stats({'game': 30}),
        thresholds: [_t('game', 30)],
      );
      expect(hits, hasLength(1));
    });

    test('disabled 한도는 무시', () {
      final hits = computeThresholdHits(
        stats: _stats({'sns': 99}),
        thresholds: [_t('sns', 30, enabled: false)],
      );
      expect(hits, isEmpty);
    });

    test('사용량 없는 카테고리는 0으로 취급', () {
      final hits = computeThresholdHits(
        stats: _stats({'sns': 99}),
        thresholds: [_t('game', 30)],
      );
      expect(hits, isEmpty);
    });
  });

  group('fireThresholdAlarms', () {
    setUp(() => SharedPreferences.setMockInitialValues({}));

    test('hit당 1회 발송', () async {
      final sink = _FakeSink();
      final fired = await fireThresholdAlarms(
        hits: const [
          ThresholdHit(category: 'sns', usedMinutes: 35, limitMinutes: 30),
        ],
        sink: sink,
        now: DateTime(2026, 5, 26),
      );
      expect(fired, hasLength(1));
      expect(fired.first.category, 'sns');
      expect(sink.shown, hasLength(1));
      expect(sink.shown.first, contains('SNS'));
    });

    test('같은 날 같은 카테고리는 중복 발송 안 함', () async {
      final sink = _FakeSink();
      const hit = [
        ThresholdHit(category: 'sns', usedMinutes: 35, limitMinutes: 30),
      ];
      final first = await fireThresholdAlarms(
        hits: hit,
        sink: sink,
        now: DateTime(2026, 5, 26),
      );
      final second = await fireThresholdAlarms(
        hits: hit,
        sink: sink,
        now: DateTime(2026, 5, 26),
      );
      expect(first, hasLength(1));
      expect(second, isEmpty); // 중복 방지
      expect(sink.shown, hasLength(1));
    });

    test('다음 날에는 다시 발송', () async {
      final sink = _FakeSink();
      const hit = [
        ThresholdHit(category: 'sns', usedMinutes: 35, limitMinutes: 30),
      ];
      await fireThresholdAlarms(hits: hit, sink: sink, now: DateTime(2026, 5, 26));
      final next = await fireThresholdAlarms(
        hits: hit,
        sink: sink,
        now: DateTime(2026, 5, 27),
      );
      expect(next, hasLength(1));
      expect(sink.shown, hasLength(2));
    });

    test('hit 없으면 미발송', () async {
      final sink = _FakeSink();
      final fired = await fireThresholdAlarms(hits: const [], sink: sink);
      expect(fired, isEmpty);
      expect(sink.shown, isEmpty);
    });
  });
}

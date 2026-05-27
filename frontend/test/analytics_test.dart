import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/core/analytics/analytics.dart';

void main() {
  group('FakeAnalytics', () {
    test('track 이벤트·속성 기록', () async {
      final a = FakeAnalytics();
      await a.track(AnalyticsEvents.thresholdCreated, {
        'category': 'sns',
        'minutes': 30,
      });
      expect(a.events, hasLength(1));
      expect(a.events.first.event, 'threshold_created');
      expect(a.events.first.props['category'], 'sns');
      expect(a.events.first.props['minutes'], 30);
    });

    test('속성 없는 track', () async {
      final a = FakeAnalytics();
      await a.track(AnalyticsEvents.reportViewed);
      expect(a.events.single.event, 'report_viewed');
      expect(a.events.single.props, isEmpty);
    });

    test('identify로 distinct_id 설정', () {
      final a = FakeAnalytics();
      a.identify('user-123');
      expect(a.distinctId, 'user-123');
    });

    test('여러 이벤트 순서 보존', () async {
      final a = FakeAnalytics();
      await a.track(AnalyticsEvents.permissionGranted);
      await a.track(AnalyticsEvents.channelToggled, {'channel': 'telegram', 'on': true});
      await a.track(AnalyticsEvents.purchaseCompleted, {'product_id': 'kkeugi.monthly'});
      expect(
        a.events.map((e) => e.event),
        ['permission_granted', 'channel_toggled', 'purchase_completed'],
      );
    });
  });
}

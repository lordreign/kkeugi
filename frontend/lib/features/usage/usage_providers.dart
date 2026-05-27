import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../auth/presentation/auth_provider.dart';
import 'usage_api.dart';
import 'usage_channel.dart';
import 'usage_sync.dart';

const _kPermissionTrackedKey = 'kpi_permission_granted';

/// 사용 통계 접근 권한 여부. 설정에서 돌아온 뒤 invalidate로 갱신.
final usagePermissionProvider = FutureProvider<bool>((ref) async {
  final granted = await UsageChannel.hasPermission();
  if (granted) {
    // 최초 1회만 KPI 기록 (권한 동의율).
    final prefs = await SharedPreferences.getInstance();
    if (!(prefs.getBool(_kPermissionTrackedKey) ?? false)) {
      await prefs.setBool(_kPermissionTrackedKey, true);
      await ref.read(analyticsProvider).track(AnalyticsEvents.permissionGranted);
    }
  }
  return granted;
});

/// 오늘 통계 — 권한 있으면 sync 후 서버 stats/today 조회.
/// 권한 없거나 데이터 없으면 total 0인 TodayStats 반환 (홈 빈 상태 처리).
final todayStatsProvider = FutureProvider<TodayStats>((ref) async {
  final granted = await ref.watch(usagePermissionProvider.future);
  final dio = ref.watch(dioProvider);

  if (granted) {
    // foreground sync (Trigger A) — 인증 Dio로 즉시 최신화
    await runUsageSync(dio: dio);
  }
  return UsageApi(dio).today();
});

/// 설정 화면 열기 → 사용자가 권한 토글 후 복귀하면 invalidate.
Future<void> openUsagePermissionSettings(WidgetRef ref) async {
  await UsageChannel.openUsageAccessSettings();
}

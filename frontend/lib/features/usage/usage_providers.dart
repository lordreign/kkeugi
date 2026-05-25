import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../auth/presentation/auth_provider.dart';
import 'usage_api.dart';
import 'usage_channel.dart';
import 'usage_sync.dart';

/// 사용 통계 접근 권한 여부. 설정에서 돌아온 뒤 invalidate로 갱신.
final usagePermissionProvider = FutureProvider<bool>((ref) async {
  return UsageChannel.hasPermission();
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

import 'package:dio/dio.dart';
import 'package:workmanager/workmanager.dart';

import '../../core/api/env.dart';
import '../../core/storage/secure_storage.dart';
import 'usage_sync.dart';

const _taskName = 'usageSync';
const _uniqueName = 'kkeugi-usage-sync';

/// WorkManager 백그라운드 isolate 진입점. Riverpod 없이 독립 동작.
/// best-effort: 저장된 access token으로 sync. 401/만료면 다음 foreground sync가 커버.
@pragma('vm:entry-point')
void usageSyncCallbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    try {
      final token = await SecureStorage.readAccessToken();
      if (token == null) return true;
      final dio = Dio(
        BaseOptions(
          baseUrl: Env.apiBaseUrl,
          connectTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 30),
          contentType: 'application/json',
          headers: {'Authorization': 'Bearer $token'},
        ),
      );
      await runUsageSync(dio: dio);
      return true;
    } catch (_) {
      // 실패해도 true 반환 — 재시도 폭주 방지. 8h 다음 주기/foreground가 커버.
      return true;
    }
  });
}

/// 8시간 주기 백그라운드 sync 등록 (Trigger B). main()에서 1회 호출.
Future<void> initUsageBackgroundSync() async {
  await Workmanager().initialize(usageSyncCallbackDispatcher);
  await Workmanager().registerPeriodicTask(
    _uniqueName,
    _taskName,
    frequency: const Duration(hours: 8),
    constraints: Constraints(networkType: NetworkType.connected),
    existingWorkPolicy: ExistingPeriodicWorkPolicy.keep,
  );
}

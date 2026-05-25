import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

import 'category_map.dart';
import 'usage_api.dart';
import 'usage_channel.dart';

/// 결정론적 client_event_id namespace — 같은 (패키지, 시작시각) 세션은
/// 항상 같은 UUID → 서버가 멱등 처리. 로컬 synced 플래그 불필요.
const _kNamespace = '6ba7b812-9dad-11d1-80b4-00c04fd430c8';

const _kLastSyncKey = 'usage_last_sync_ms';
const _minSessionSeconds = 30; // 30초 미만은 노이즈로 무시
const _maxLookback = Duration(days: 3); // 첫 실행/장기 미사용 시 과도 조회 방지
const _overlap = Duration(minutes: 10); // 마지막 sync 직전 세션 누락 방지

class UsageSyncResult {
  const UsageSyncResult({required this.scanned, required this.uploaded});

  final int scanned; // 카테고리 매칭된 세션 수
  final int uploaded; // 서버가 새로 수락한 수

  static const empty = UsageSyncResult(scanned: 0, uploaded: 0);
}

/// 핵심 sync: UsageStatsManager 세션 조회 → 카테고리 매핑 → batch 업로드.
/// foreground(인증 Dio)와 background(토큰 주입 Dio) 양쪽에서 재사용.
Future<UsageSyncResult> runUsageSync({required Dio dio}) async {
  if (!await UsageChannel.hasPermission()) {
    return UsageSyncResult.empty;
  }

  final prefs = await SharedPreferences.getInstance();
  final now = DateTime.now();
  final lastSyncMs = prefs.getInt(_kLastSyncKey);
  var start = lastSyncMs != null
      ? DateTime.fromMillisecondsSinceEpoch(lastSyncMs).subtract(_overlap)
      : now.subtract(_maxLookback);
  final floor = now.subtract(_maxLookback);
  if (start.isBefore(floor)) start = floor;

  final sessions = await UsageChannel.querySessions(start, now);

  final uuid = const Uuid();
  final events = <UsageEventDto>[];
  for (final s in sessions) {
    final seconds = s.duration.inSeconds;
    if (seconds < _minSessionSeconds) continue;
    final category = categoryForPackage(s.packageName);
    if (category == null) continue;
    events.add(
      UsageEventDto(
        clientEventId: uuid.v5(
          _kNamespace,
          '${s.packageName}|${s.start.millisecondsSinceEpoch}',
        ),
        packageName: s.packageName,
        category: category,
        durationSeconds: seconds,
        occurredAt: s.start,
      ),
    );
  }

  if (events.isEmpty) {
    await prefs.setInt(_kLastSyncKey, now.millisecondsSinceEpoch);
    return UsageSyncResult.empty;
  }

  final api = UsageApi(dio);
  var uploaded = 0;
  // 1000건 청크 (서버 batch 상한)
  for (var i = 0; i < events.length; i += 1000) {
    final chunk = events.sublist(i, (i + 1000).clamp(0, events.length));
    final accepted = await api.postBatch(chunk);
    uploaded += accepted.length;
  }

  await prefs.setInt(_kLastSyncKey, now.millisecondsSinceEpoch);
  return UsageSyncResult(scanned: events.length, uploaded: uploaded);
}

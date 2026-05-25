import 'package:dio/dio.dart';

/// 서버로 보낼 usage 이벤트 (POST /v1/usage/batch).
class UsageEventDto {
  const UsageEventDto({
    required this.clientEventId,
    required this.packageName,
    required this.category,
    required this.durationSeconds,
    required this.occurredAt,
    this.source = 'usagestats',
  });

  final String clientEventId;
  final String packageName;
  final String category;
  final int durationSeconds;
  final DateTime occurredAt;
  final String source;

  Map<String, dynamic> toJson() => {
        'client_event_id': clientEventId,
        'package_name': packageName,
        'category': category,
        'duration_seconds': durationSeconds,
        'occurred_at': occurredAt.toUtc().toIso8601String(),
        'source': source,
      };
}

class CategoryStat {
  const CategoryStat({required this.category, required this.minutes});

  factory CategoryStat.fromJson(Map<String, dynamic> j) => CategoryStat(
        category: j['category'] as String,
        minutes: j['minutes'] as int,
      );

  final String category;
  final int minutes;
}

class TodayStats {
  const TodayStats({
    required this.date,
    required this.totalMinutes,
    required this.inWorkMinutes,
    required this.byCategory,
  });

  factory TodayStats.fromJson(Map<String, dynamic> j) => TodayStats(
        date: j['date'] as String,
        totalMinutes: j['total_minutes'] as int,
        inWorkMinutes: j['in_work_minutes'] as int,
        byCategory: (j['by_category'] as List)
            .map((e) => CategoryStat.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
      );

  final String date;
  final int totalMinutes;
  final int inWorkMinutes;
  final List<CategoryStat> byCategory;
}

class UsageApi {
  UsageApi(this._dio);

  final Dio _dio;

  /// 멱등 batch 업로드. accepted client_event_id 리스트 반환.
  Future<List<String>> postBatch(List<UsageEventDto> events) async {
    final resp = await _dio.post<Map<String, dynamic>>(
      '/v1/usage/batch',
      data: {'events': events.map((e) => e.toJson()).toList()},
    );
    return (resp.data!['accepted'] as List).cast<String>();
  }

  Future<TodayStats> today() async {
    final resp = await _dio.get<Map<String, dynamic>>('/v1/usage/stats/today');
    return TodayStats.fromJson(resp.data!);
  }
}

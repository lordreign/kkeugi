import 'package:dio/dio.dart';

const thresholdCategoryLabels = {
  'sns': 'SNS', 'shorts': '쇼츠', 'game': '게임', 'webtoon': '웹툰', 'other': '기타',
};

class ThresholdItem {
  const ThresholdItem({
    required this.id,
    required this.category,
    required this.dailyLimitMinutes,
    required this.enabled,
  });

  factory ThresholdItem.fromJson(Map<String, dynamic> j) => ThresholdItem(
        id: j['id'] as String,
        category: j['category'] as String,
        dailyLimitMinutes: j['daily_limit_minutes'] as int,
        enabled: j['enabled'] as bool,
      );

  final String id;
  final String category;
  final int dailyLimitMinutes;
  final bool enabled;

  String get label => thresholdCategoryLabels[category] ?? category;
}

class ThresholdsApi {
  ThresholdsApi(this._dio);

  final Dio _dio;

  Future<List<ThresholdItem>> list() async {
    final resp = await _dio.get<List<dynamic>>('/v1/thresholds');
    return (resp.data ?? [])
        .map((e) => ThresholdItem.fromJson((e as Map).cast<String, dynamic>()))
        .toList();
  }

  Future<void> create(String category, int minutes) async {
    await _dio.post<Map<String, dynamic>>(
      '/v1/thresholds',
      data: {'category': category, 'daily_limit_minutes': minutes},
    );
  }

  Future<void> update(String id, {int? minutes, bool? enabled}) async {
    await _dio.patch<Map<String, dynamic>>(
      '/v1/thresholds/$id',
      data: {
        if (minutes != null) 'daily_limit_minutes': minutes,
        if (enabled != null) 'enabled': enabled,
      },
    );
  }

  Future<void> delete(String id) async {
    await _dio.delete<void>('/v1/thresholds/$id');
  }
}

import 'package:dio/dio.dart';

class WeeklyReportCard {
  const WeeklyReportCard({
    required this.weekStartDate,
    required this.totalMinutes,
    required this.recoveredMinutes,
    required this.cardText,
    this.recoveredWon,
    this.cardInsight,
  });

  factory WeeklyReportCard.fromJson(Map<String, dynamic> j) => WeeklyReportCard(
        weekStartDate: j['week_start_date'] as String,
        totalMinutes: j['total_minutes'] as int,
        recoveredMinutes: j['recovered_minutes'] as int,
        recoveredWon: j['recovered_won'] as int?,
        cardText: j['card_text'] as String,
        cardInsight: j['card_insight'] as String?,
      );

  final String weekStartDate; // YYYY-MM-DD (월요일)
  final int totalMinutes;
  final int recoveredMinutes; // 음수 = 증가
  final int? recoveredWon;
  final String cardText;
  final String? cardInsight;
}

class ReportsApi {
  ReportsApi(this._dio);

  final Dio _dio;

  Future<List<WeeklyReportCard>> list() async {
    final resp = await _dio.get<List<dynamic>>('/v1/reports');
    return (resp.data ?? [])
        .map((e) => WeeklyReportCard.fromJson((e as Map).cast<String, dynamic>()))
        .toList();
  }
}

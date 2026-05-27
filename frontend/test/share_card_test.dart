import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/features/archive/reports_api.dart';
import 'package:kkeugi/features/archive/share_card.dart';
import 'package:kkeugi/shared/widgets/hero_numeral.dart';

WeeklyReportCard _report({int? won, int minutes = 15}) => WeeklyReportCard(
      weekStartDate: '2026-05-18',
      totalMinutes: 320,
      recoveredMinutes: minutes,
      recoveredWon: won,
      cardText: '이번 주는 지난주보다 차분했어요.',
      cardInsight: '화요일 오전이 가장 단단했어요.',
    );

void main() {
  testWidgets('유료(매출환산) — hero가 ₩ 금액', (tester) async {
    await tester.pumpWidget(
      MaterialApp(home: ShareCard(report: _report(won: 68250))),
    );
    final hero = tester.widget<HeroNumeral>(find.byType(HeroNumeral));
    expect(hero.value, '₩ 68,250');
    expect(find.text('이번 주 되찾은 가치'), findsOneWidget);
    expect(find.text('5월 18일 주'), findsOneWidget);
    expect(find.textContaining('끊기'), findsOneWidget);
  });

  testWidgets('무료 — hero가 +분', (tester) async {
    await tester.pumpWidget(
      MaterialApp(home: ShareCard(report: _report(minutes: 15))),
    );
    final hero = tester.widget<HeroNumeral>(find.byType(HeroNumeral));
    expect(hero.value, '+15');
    expect(hero.unit, '분');
    expect(find.text('이번 주 되찾은 시간'), findsOneWidget);
  });

  testWidgets('시간 증가(음수) — 늘어난 시간 라벨', (tester) async {
    await tester.pumpWidget(
      MaterialApp(home: ShareCard(report: _report(minutes: -20))),
    );
    final hero = tester.widget<HeroNumeral>(find.byType(HeroNumeral));
    expect(hero.value, '-20');
    expect(find.text('이번 주 늘어난 시간'), findsOneWidget);
  });

  testWidgets('미리보기 화면 — 카드 + 공유 CTA', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: ReportSharePreviewScreen(report: _report(won: 10000)),
        ),
      ),
    );
    await tester.pump();
    expect(find.byType(ShareCard), findsOneWidget);
    expect(find.text('이미지로 공유하기'), findsOneWidget);
  });
}

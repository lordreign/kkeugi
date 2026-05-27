import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/features/thresholds/thresholds_api.dart';
import 'package:kkeugi/features/thresholds/thresholds_provider.dart';
import 'package:kkeugi/features/thresholds/thresholds_screen.dart';

class _FakeThresholdsApi extends ThresholdsApi {
  _FakeThresholdsApi() : super(Dio());

  String? createdCategory;
  int? createdMinutes;

  @override
  Future<List<ThresholdItem>> list() async => [];

  @override
  Future<void> create(String category, int minutes) async {
    createdCategory = category;
    createdMinutes = minutes;
  }
}

void main() {
  testWidgets('한도 추가 — 카테고리·분 선택 후 저장 → create 호출', (tester) async {
    final fake = _FakeThresholdsApi();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [thresholdsApiProvider.overrideWithValue(fake)],
        child: MaterialApp(
          home: Builder(
            builder: (ctx) => Scaffold(
              body: Center(
                child: ElevatedButton(
                  onPressed: () => Navigator.push(
                    ctx,
                    MaterialPageRoute<void>(
                      builder: (_) => const AddThresholdScreen(used: {}),
                    ),
                  ),
                  child: const Text('open'),
                ),
              ),
            ),
          ),
        ),
      ),
    );
    await tester.tap(find.text('open'));
    await tester.pumpAndSettle();

    // 기본 카테고리 sns, 분 60으로 변경
    await tester.tap(find.text('60분'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('저장'));
    await tester.pumpAndSettle();

    expect(fake.createdCategory, 'sns');
    expect(fake.createdMinutes, 60);
  });

  testWidgets('한도 추가 — 다른 카테고리 선택 반영', (tester) async {
    final fake = _FakeThresholdsApi();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [thresholdsApiProvider.overrideWithValue(fake)],
        child: const MaterialApp(home: AddThresholdScreen(used: {})),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('게임'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('저장'));
    await tester.pumpAndSettle();

    expect(fake.createdCategory, 'game');
    expect(fake.createdMinutes, 30); // 기본
  });
}

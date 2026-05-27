import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/features/payments/payment_api.dart';
import 'package:kkeugi/features/payments/payments_providers.dart';
import 'package:kkeugi/features/payments/paywall_screen.dart';

/// verify 호출만 기록하는 fake PaymentApi (네트워크 없음).
class _FakePaymentApi extends PaymentApi {
  _FakePaymentApi() : super(Dio());

  String? verifiedProduct;
  bool? verifiedTrial;

  @override
  Future<void> verify({
    required String productId,
    required String purchaseToken,
    bool trial = false,
  }) async {
    verifiedProduct = productId;
    verifiedTrial = trial;
  }

  @override
  Future<Entitlement> subscription() async => Entitlement.free;
}

Future<void> _openPaywall(WidgetTester tester, _FakePaymentApi fake) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [paymentApiProvider.overrideWithValue(fake)],
      child: MaterialApp(
        home: Scaffold(
          body: Builder(
            builder: (ctx) => Center(
              child: ElevatedButton(
                onPressed: () => Navigator.push(
                  ctx,
                  MaterialPageRoute<void>(builder: (_) => const PaywallScreen()),
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
}

void main() {
  testWidgets('기본(월 구독) 구매 → verify(kkeugi.monthly, trial=true) 호출', (tester) async {
    final fake = _FakePaymentApi();
    await _openPaywall(tester, fake);

    // 기본 선택 = 월 구독 → 버튼 '7일 무료로 시작'
    expect(find.text('7일 무료로 시작'), findsOneWidget);
    await tester.tap(find.text('7일 무료로 시작'));
    await tester.pumpAndSettle();

    expect(fake.verifiedProduct, 'kkeugi.monthly');
    expect(fake.verifiedTrial, isTrue);
  });

  testWidgets('일회 인증서 선택 → 버튼 구매하기 → verify(kkeugi.cert, trial=false)', (tester) async {
    final fake = _FakePaymentApi();
    await _openPaywall(tester, fake);

    await tester.tap(find.text('평생 인증서'));
    await tester.pumpAndSettle();
    expect(find.text('구매하기'), findsOneWidget);

    await tester.tap(find.text('구매하기'));
    await tester.pumpAndSettle();

    expect(fake.verifiedProduct, 'kkeugi.cert');
    expect(fake.verifiedTrial, isFalse);
  });
}

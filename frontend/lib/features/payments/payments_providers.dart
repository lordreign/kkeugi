import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../../core/api/env.dart';
import '../auth/presentation/auth_provider.dart';
import 'billing_service.dart';
import 'payment_api.dart';
import 'real_billing_service.dart';

final paymentApiProvider = Provider<PaymentApi>(
  (ref) => PaymentApi(ref.watch(dioProvider)),
);

/// Fake(dev) vs Real(prod) 빌링 — Env.useFakeBilling 스위치.
/// debug 기본 Fake → Play Console 없이 검증. release(USE_FAKE_BILLING=false)는 Real.
final billingServiceProvider = Provider<BillingService>(
  (ref) => Env.useFakeBilling ? FakeBillingService() : RealBillingService(),
);

/// 현재 결제 자격 — GET /v1/payments/subscription.
final entitlementProvider = FutureProvider<Entitlement>(
  (ref) => ref.watch(paymentApiProvider).subscription(),
);

/// 구매 실행: BillingService.buy → 서버 /verify → entitlement 갱신.
/// 성공 시 null, 실패 시 에러 메시지 반환.
Future<String?> purchase(
  WidgetRef ref,
  BillingProduct product, {
  bool trial = false,
}) async {
  final result = await ref.read(billingServiceProvider).buy(product, trial: trial);
  if (!result.success) return result.error ?? '구매를 완료하지 못했어요.';
  try {
    await ref.read(paymentApiProvider).verify(
          productId: result.productId,
          purchaseToken: result.purchaseToken,
          trial: result.trial,
        );
  } on DioException {
    return '결제 확인에 실패했어요. 잠시 후 다시 시도해주세요.';
  }
  await ref.read(analyticsProvider).track(
    AnalyticsEvents.purchaseCompleted,
    {'product_id': result.productId, 'trial': result.trial},
  );
  ref.invalidate(entitlementProvider);
  return null;
}

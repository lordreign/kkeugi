import 'dart:async';

import 'package:in_app_purchase/in_app_purchase.dart';

import 'billing_service.dart';

/// 실제 Google Play Billing 어댑터 (in_app_purchase).
///
/// 코드는 Step 5에서 완성, 실동작 검증은 Step 6(서명 AAB + 라이선스 테스터 + 실기기).
/// purchaseStream(이벤트) → buy()의 Future로 브리지.
class RealBillingService implements BillingService {
  final InAppPurchase _iap = InAppPurchase.instance;

  @override
  List<BillingProduct> catalog() => kCatalog;

  @override
  Future<PurchaseResult> buy(BillingProduct product, {bool trial = false}) async {
    if (!await _iap.isAvailable()) {
      return const PurchaseResult(success: false, error: '스토어를 사용할 수 없어요.');
    }

    final resp = await _iap.queryProductDetails({product.id});
    if (resp.productDetails.isEmpty) {
      return PurchaseResult(success: false, error: '상품을 찾을 수 없어요 (${product.id}).');
    }
    final details = resp.productDetails.first;

    final completer = Completer<PurchaseResult>();
    late final StreamSubscription<List<PurchaseDetails>> sub;
    sub = _iap.purchaseStream.listen((purchases) {
      for (final p in purchases) {
        if (p.productID != product.id) continue;
        switch (p.status) {
          case PurchaseStatus.purchased:
          case PurchaseStatus.restored:
            // 서버 검증 후 ack가 이상적이나 V1은 즉시 complete (Step 6 정교화).
            if (p.pendingCompletePurchase) _iap.completePurchase(p);
            if (!completer.isCompleted) {
              completer.complete(
                PurchaseResult(
                  success: true,
                  productId: product.id,
                  purchaseToken: p.verificationData.serverVerificationData,
                  trial: trial && product.isSubscription,
                ),
              );
            }
          case PurchaseStatus.error:
            if (!completer.isCompleted) {
              completer.complete(
                PurchaseResult(success: false, error: p.error?.message ?? '결제 오류'),
              );
            }
          case PurchaseStatus.canceled:
            if (!completer.isCompleted) {
              completer.complete(const PurchaseResult(success: false, error: '결제가 취소됐어요.'));
            }
          case PurchaseStatus.pending:
            break;
        }
      }
    });

    final param = PurchaseParam(productDetails: details);
    await _iap.buyNonConsumable(purchaseParam: param);

    final result = await completer.future;
    await sub.cancel();
    return result;
  }
}

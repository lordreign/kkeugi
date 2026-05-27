import 'package:uuid/uuid.dart';

/// 상품 (Google Play product_id와 1:1). priceLabel은 표시용.
class BillingProduct {
  const BillingProduct({
    required this.id,
    required this.title,
    required this.priceLabel,
    required this.kind,
    this.hasTrial = false,
  });

  final String id;
  final String title;
  final String priceLabel;
  final String kind; // one_time | monthly | yearly
  final bool hasTrial;

  bool get isSubscription => kind != 'one_time';
}

class PurchaseResult {
  const PurchaseResult({
    required this.success,
    this.productId = '',
    this.purchaseToken = '',
    this.trial = false,
    this.error,
  });

  final bool success;
  final String productId;
  final String purchaseToken;
  final bool trial;
  final String? error;
}

/// V1 상품 카탈로그 (products.py와 동일 — 변경 불가 ID).
const kCatalog = <BillingProduct>[
  BillingProduct(
    id: 'kkeugi.cert',
    title: '평생 인증서',
    priceLabel: '₩11,000',
    kind: 'one_time',
  ),
  BillingProduct(
    id: 'kkeugi.monthly',
    title: '월 구독',
    priceLabel: '₩5,900 / 월',
    kind: 'monthly',
    hasTrial: true,
  ),
  BillingProduct(
    id: 'kkeugi.yearly',
    title: '연 구독',
    priceLabel: '₩39,000 / 년',
    kind: 'yearly',
    hasTrial: true,
  ),
];

abstract class BillingService {
  List<BillingProduct> catalog();
  Future<PurchaseResult> buy(BillingProduct product, {bool trial});
}

/// dev/test — 실제 Billing 없이 합성 purchase_token 발급.
/// 서버 FakeVerifier가 이 토큰을 통과시켜 전 플로우(/verify→entitlement) 검증.
class FakeBillingService implements BillingService {
  @override
  List<BillingProduct> catalog() => kCatalog;

  @override
  Future<PurchaseResult> buy(BillingProduct product, {bool trial = false}) async {
    await Future<void>.delayed(const Duration(milliseconds: 300)); // 결제 UI 흉내
    return PurchaseResult(
      success: true,
      productId: product.id,
      purchaseToken: 'fake-${const Uuid().v4()}',
      trial: trial && product.isSubscription,
    );
  }
}

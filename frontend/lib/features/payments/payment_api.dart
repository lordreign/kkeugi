import 'package:dio/dio.dart';

class Entitlement {
  const Entitlement({
    required this.paid,
    required this.inTrial,
    this.kind,
  });

  factory Entitlement.fromJson(Map<String, dynamic> j) => Entitlement(
        paid: j['paid'] as bool,
        inTrial: j['in_trial'] as bool,
        kind: j['kind'] as String?,
      );

  final bool paid;
  final bool inTrial;
  final String? kind;

  static const free = Entitlement(paid: false, inTrial: false);
}

class PaymentApi {
  PaymentApi(this._dio);

  final Dio _dio;

  /// 영수증 검증 — 성공 시 서버가 구독 생성 + tier 갱신.
  Future<void> verify({
    required String productId,
    required String purchaseToken,
    bool trial = false,
  }) async {
    await _dio.post<Map<String, dynamic>>(
      '/v1/payments/verify',
      data: {
        'product_id': productId,
        'purchase_token': purchaseToken,
        'source': 'google_play',
        'trial': trial,
      },
    );
  }

  Future<Entitlement> subscription() async {
    final resp = await _dio.get<Map<String, dynamic>>('/v1/payments/subscription');
    return Entitlement.fromJson(resp.data!);
  }
}

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/auth/presentation/auth_provider.dart';

/// V1 EXECUTION PLAN §7 — feature flag 인프라.
///
/// 출시 후 누적 사용자 500명 도달 시점부터 A/B 테스트 즉시 가능.
/// 현재 active flag 0개 — 인프라만 깔고 대기.
///
/// 사용 예시:
/// ```dart
/// final flags = ref.watch(featureFlagsProvider).valueOrNull;
/// if (flags?.has('loss_paywall_v2') ?? false) { ... }
/// ```
class FeatureFlags {
  const FeatureFlags(this._flags);

  final Set<String> _flags;

  static const empty = FeatureFlags(<String>{});

  factory FeatureFlags.fromJson(Map<String, dynamic> j) =>
      FeatureFlags(((j['flags'] as List?) ?? []).cast<String>().toSet());

  bool has(String name) => _flags.contains(name);
  bool get isEmpty => _flags.isEmpty;
  Iterable<String> get all => _flags;
}

class FeatureFlagsApi {
  FeatureFlagsApi(this._dio);
  final Dio _dio;

  Future<FeatureFlags> fetch() async {
    try {
      final resp = await _dio.get<Map<String, dynamic>>('/v1/feature_flags');
      return FeatureFlags.fromJson(resp.data ?? const {});
    } catch (_) {
      // 네트워크 실패 시 빈 flag — 기본 경로 (제어군) 으로 처리.
      return FeatureFlags.empty;
    }
  }
}

final featureFlagsApiProvider = Provider<FeatureFlagsApi>(
  (ref) => FeatureFlagsApi(ref.watch(dioProvider)),
);

/// 로그인 직후 1회 fetch + in-memory 캐시.
final featureFlagsProvider = FutureProvider<FeatureFlags>(
  (ref) => ref.watch(featureFlagsApiProvider).fetch(),
);

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../api/env.dart';
import 'analytics.dart';

/// 토큰 있으면 Mixpanel, 없으면 Fake. 앱 수명 동안 단일 인스턴스.
/// 로그인 시 authProvider에서 identify(user.id) 호출.
final analyticsProvider = Provider<Analytics>((ref) {
  return Env.mixpanelToken.isEmpty
      ? FakeAnalytics()
      : MixpanelAnalytics(Env.mixpanelToken);
});

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../auth/presentation/auth_provider.dart';
import 'telegram_api.dart';

final telegramApiProvider = Provider<TelegramApi>(
  (ref) => TelegramApi(ref.watch(dioProvider)),
);

/// 현재 Telegram 연결/구독 상태.
final telegramStatusProvider = FutureProvider<TelegramStatus>((ref) async {
  return ref.watch(telegramApiProvider).status();
});

/// 연결 시작: link_token 발급 → 딥링크 열기 (Telegram 앱/브라우저).
/// 바인딩은 사용자가 Telegram에서 완료 → 복귀 후 status invalidate로 반영.
Future<bool> startTelegramLink(WidgetRef ref) async {
  final deepLink = await ref.read(telegramApiProvider).linkToken();
  final uri = Uri.parse(deepLink);
  return launchUrl(uri, mode: LaunchMode.externalApplication);
}

Future<void> unsubscribeTelegram(WidgetRef ref) async {
  await ref.read(telegramApiProvider).unsubscribe();
  ref.invalidate(telegramStatusProvider);
}

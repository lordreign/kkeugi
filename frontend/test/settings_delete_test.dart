import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/features/auth/presentation/auth_provider.dart';
import 'package:kkeugi/features/channel/telegram_api.dart';
import 'package:kkeugi/features/channel/telegram_provider.dart';
import 'package:kkeugi/features/settings/settings_screen.dart';

/// deleteAccount 호출만 가로채는 fake — 나머지는 실제 AuthNotifier 사용.
class _FakeAuthNotifier extends AuthNotifier {
  bool deleteCalled = false;

  @override
  Future<void> deleteAccount() async {
    deleteCalled = true;
  }
}

Future<void> _pumpSettings(WidgetTester tester, _FakeAuthNotifier fake) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        authProvider.overrideWith(() => fake),
        // 네트워크 차단 — Telegram 카드는 미연결 상태로 고정
        telegramStatusProvider.overrideWith((ref) async => TelegramStatus.none),
      ],
      child: const MaterialApp(home: SettingsScreen()),
    ),
  );
  await tester.pumpAndSettle();
  // ListView 하단의 '회원 탈퇴'까지 스크롤
  await tester.scrollUntilVisible(
    find.text('회원 탈퇴'),
    250,
    scrollable: find.byType(Scrollable).first,
  );
}

void main() {
  testWidgets('회원 탈퇴 → 확인 다이얼로그 → 탈퇴 누르면 deleteAccount 호출', (tester) async {
    final fake = _FakeAuthNotifier();
    await _pumpSettings(tester, fake);

    await tester.tap(find.text('회원 탈퇴'));
    await tester.pumpAndSettle();

    // 확인 다이얼로그 + PIPA grace 안내 노출
    expect(find.textContaining('영구 삭제'), findsOneWidget);
    expect(fake.deleteCalled, isFalse);

    await tester.tap(find.widgetWithText(TextButton, '탈퇴'));
    await tester.pumpAndSettle();

    expect(fake.deleteCalled, isTrue);
  });

  testWidgets('회원 탈퇴 다이얼로그에서 취소하면 deleteAccount 미호출', (tester) async {
    final fake = _FakeAuthNotifier();
    await _pumpSettings(tester, fake);

    await tester.tap(find.text('회원 탈퇴'));
    await tester.pumpAndSettle();
    await tester.tap(find.widgetWithText(TextButton, '취소'));
    await tester.pumpAndSettle();

    expect(fake.deleteCalled, isFalse);
  });
}

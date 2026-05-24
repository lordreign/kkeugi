import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/features/auth/presentation/login_screen.dart';
import 'package:kkeugi/shared/widgets/hero_numeral.dart';
import 'package:kkeugi/theme/theme.dart';

Widget _wrap(Widget child) => ProviderScope(
      child: MaterialApp(
        theme: buildAppTheme(_BuildContextStub()),
        home: child,
      ),
    );

void main() {
  testWidgets('LoginScreen renders Google CTA', (tester) async {
    await tester.pumpWidget(
      _wrap(LoginScreen(onGoogleLogin: () {})),
    );
    expect(find.text('끊기'), findsOneWidget);
    expect(find.text('Google로 시작'), findsOneWidget);
  });

  testWidgets('HeroNumeral renders value + unit', (tester) async {
    await tester.pumpWidget(
      _wrap(const Scaffold(body: HeroNumeral(value: '+47', unit: '분'))),
    );
    expect(find.byType(HeroNumeral), findsOneWidget);
  });
}

/// Stub for theme builder that doesn't need real BuildContext.
class _BuildContextStub extends StatelessElement implements BuildContext {
  _BuildContextStub() : super(Container());
}

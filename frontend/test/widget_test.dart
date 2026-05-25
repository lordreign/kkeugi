import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kkeugi/features/channel/channel_toggle_card.dart';
import 'package:kkeugi/shared/widgets/hero_numeral.dart';
import 'package:kkeugi/theme/theme.dart';

Widget _wrap(Widget child) => MaterialApp(
      theme: buildAppTheme(_Ctx()),
      home: Scaffold(body: child),
    );

void main() {
  testWidgets('HeroNumeral renders (RichText)', (tester) async {
    await tester.pumpWidget(_wrap(const HeroNumeral(value: '+47', unit: '분')));
    expect(find.byType(HeroNumeral), findsOneWidget);
    expect(find.byType(RichText), findsWidgets);
  });

  testWidgets('ChannelToggleCard renders name + switch', (tester) async {
    await tester.pumpWidget(
      _wrap(
        ChannelToggleCard(
          icon: Icons.mail_outline,
          name: '이메일',
          description: '주간 회고',
          value: false,
          onChanged: (_) {},
        ),
      ),
    );
    expect(find.text('이메일'), findsOneWidget);
    expect(find.byType(Switch), findsOneWidget);
  });
}

class _Ctx extends StatelessElement implements BuildContext {
  _Ctx() : super(Container());
}

import 'package:flutter/material.dart';

import '../../channel/channel_toggle_card.dart';
import '../onboarding_flow.dart';

/// Step 5 — 채널 선택 (FCM 강제 ON + 이메일·Telegram 옵션, 1개 이상).
class Step5ChannelSelect extends StatelessWidget {
  const Step5ChannelSelect({
    super.key,
    required this.selected,
    required this.onToggle,
    required this.onComplete,
  });

  final Set<String> selected;
  final void Function(String channel, bool on) onToggle;
  final VoidCallback onComplete;

  @override
  Widget build(BuildContext context) {
    final hasAtLeastOne = selected.isNotEmpty;
    return OnboardingStepScaffold(
      title: '주간 회고를\n어디로 받으시겠어요?',
      subtitle: '일요일 22:00 카드를 받을 채널을 1개 이상 선택해주세요.',
      ctaLabel: '시작하기',
      onCta: hasAtLeastOne ? onComplete : () {},
      child: Column(
        children: [
          ChannelToggleCard(
            icon: Icons.notifications_outlined,
            name: 'FCM 푸시',
            description: '기본 알림 (앱 내 + 푸시)',
            value: true,
            enabled: false, // FCM 강제 ON
            onChanged: null,
          ),
          ChannelToggleCard(
            icon: Icons.mail_outline,
            name: '이메일',
            description: '선택 — 이메일 주소 인증 (W4)',
            value: selected.contains('email'),
            onChanged: (v) => onToggle('email', v),
          ),
          ChannelToggleCard(
            icon: Icons.send_outlined,
            name: 'Telegram',
            description: '선택 — 1인 워커 인디 친화 (W5)',
            value: selected.contains('telegram'),
            onChanged: (v) => onToggle('telegram', v),
          ),
        ],
      ),
    );
  }
}

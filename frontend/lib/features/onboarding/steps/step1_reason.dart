import 'package:flutter/material.dart';

import '../../../theme/colors.dart';
import '../../../theme/typography.dart';
import '../onboarding_flow.dart';

/// Step 1 — 이유 (관찰 중립 톤, DESIGN.md P2).
class Step1Reason extends StatelessWidget {
  const Step1Reason({super.key, required this.onNext});

  final VoidCallback onNext;

  @override
  Widget build(BuildContext context) {
    return OnboardingStepScaffold(
      title: '사용 패턴을 분석해\n집중력이 흩어지는\n시간대를 찾아드려요.',
      subtitle: '데이터는 기기 안에만 남습니다. 매출 환산은 나중에 시간당 가치를 입력하면 추가로 보여드려요.',
      ctaLabel: '다음',
      onCta: onNext,
      child: Center(
        child: Text(
          '거울 같은 친구.\n압박하지 않고, 비난하지 않고,\n객관적으로.',
          textAlign: TextAlign.center,
          style: AppTypography.bodyLarge.copyWith(color: AppColors.textSecondary),
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';

import '../../../theme/colors.dart';
import '../../../theme/spacing.dart';
import '../../../theme/typography.dart';
import '../onboarding_flow.dart';

/// Step 2 — PACKAGE_USAGE_STATS 권한 안내.
/// 실제 권한 요청 (Settings 이동)은 W4에서 platform channel로 구현.
class Step2Permission extends StatelessWidget {
  const Step2Permission({super.key, required this.onNext});

  final VoidCallback onNext;

  @override
  Widget build(BuildContext context) {
    return OnboardingStepScaffold(
      title: '사용 통계 접근 권한',
      subtitle: '다음 화면에서 시스템 설정으로 이동합니다. 끊기가 앱별 사용 시간을 읽을 수 있도록 허용해주세요.',
      ctaLabel: '권한 설정으로 이동',
      onCta: onNext, // W4: UsageStats Settings intent
      secondaryLabel: '나중에 (수동 입력으로 시작)',
      onSecondary: onNext,
      child: Column(
        children: const [
          _Bullet(text: '기기 외부 전송 없음', sub: '모든 분석은 본인 기기 안에서'),
          SizedBox(height: AppSpacing.md),
          _Bullet(text: '언제든 권한 해제 가능', sub: '거부해도 수동 입력으로 사용 가능'),
        ],
      ),
    );
  }
}

class _Bullet extends StatelessWidget {
  const _Bullet({required this.text, required this.sub});

  final String text;
  final String sub;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 6,
          height: 6,
          margin: const EdgeInsets.only(top: 8, right: AppSpacing.sm),
          decoration: const BoxDecoration(
            color: AppColors.accent,
            shape: BoxShape.circle,
          ),
        ),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(text, style: AppTypography.bodyMedium),
              Text(sub, style: AppTypography.labelSmall),
            ],
          ),
        ),
      ],
    );
  }
}

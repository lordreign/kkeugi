import 'package:flutter/material.dart';

import '../../../shared/widgets/hero_numeral.dart';
import '../../../theme/colors.dart';
import '../../../theme/typography.dart';
import '../onboarding_flow.dart';

/// Step 3 — shock (어제 사용 시간 reveal).
/// 데이터 없으면 (방금 가입) fallback 카피.
class Step3Shock extends StatelessWidget {
  const Step3Shock({super.key, required this.onNext, this.yesterdayMinutes});

  final VoidCallback onNext;
  final int? yesterdayMinutes; // W4 연결 전엔 null → fallback

  @override
  Widget build(BuildContext context) {
    final hasData = yesterdayMinutes != null;
    return OnboardingStepScaffold(
      title: hasData ? '어제, 이만큼 흩어졌어요.' : '내일부터 데이터가 모입니다.',
      subtitle: hasData
          ? 'SNS·쇼츠·웹툰으로 빠진 시간이 내일 일정 위에 올라갑니다.'
          : '오늘 사용부터 추적이 시작돼요. 첫 회고 카드는 다음 일요일 22:00에 도착합니다.',
      ctaLabel: '다음',
      onCta: onNext,
      child: Center(
        child: hasData
            ? HeroNumeral(value: '+$yesterdayMinutes', unit: '분')
            : Text(
                '데이터가 모이는 중',
                style: AppTypography.bodyLarge.copyWith(
                  color: AppColors.textTertiary,
                ),
              ),
      ),
    );
  }
}

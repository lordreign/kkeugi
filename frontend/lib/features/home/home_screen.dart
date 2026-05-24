import 'package:flutter/material.dart';

import '../../shared/widgets/hero_numeral.dart';
import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';

/// W3 skeleton — 실제 데이터 연결 W4 (UsageStatsManager) 이후.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: Text(
          '끊기',
          style: AppTypography.titleLarge.copyWith(color: AppColors.textSecondary),
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: AppSpacing.lg),
              Text(
                '내일 일정에 더해질 시간 빚',
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              const HeroNumeral(value: '+47', unit: '분'),
              const SizedBox(height: AppSpacing.lg),
              Text(
                '오늘 SNS·쇼츠·웹툰으로 흩어진 시간이 내일 일정 위에 올라갑니다.',
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: AppSpacing.xl2),
              Text(
                '오늘 · 카테고리별',
                style: AppTypography.monoSmall(),
              ),
              const SizedBox(height: AppSpacing.md),
              const _CategoryRow(name: 'SNS', minutes: 18, ratio: 0.38),
              const _CategoryRow(name: '쇼츠', minutes: 14, ratio: 0.30),
              const _CategoryRow(name: '웹툰', minutes: 11, ratio: 0.23),
              const _CategoryRow(name: '게임', minutes: 4, ratio: 0.09),
            ],
          ),
        ),
      ),
    );
  }
}

class _CategoryRow extends StatelessWidget {
  const _CategoryRow({required this.name, required this.minutes, required this.ratio});

  final String name;
  final int minutes;
  final double ratio;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: AppSpacing.sm),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(name, style: AppTypography.bodyMedium),
              Text(
                '$minutes분',
                style: AppTypography.bodyMedium.copyWith(
                  fontFeatures: const [],
                  color: AppColors.textSecondary,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Container(
            height: 2,
            decoration: BoxDecoration(
              color: AppColors.divider,
              borderRadius: BorderRadius.circular(1),
            ),
            child: FractionallySizedBox(
              alignment: Alignment.centerLeft,
              widthFactor: ratio,
              child: Container(
                decoration: BoxDecoration(
                  color: AppColors.textPrimary,
                  borderRadius: BorderRadius.circular(1),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

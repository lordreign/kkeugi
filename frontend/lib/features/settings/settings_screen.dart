import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import '../auth/presentation/auth_provider.dart';
import '../channel/channel_toggle_card.dart';

/// 설정 화면 — DESIGN.md IA tree 6 섹션.
class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: Text('설정', style: AppTypography.titleLarge),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
          children: [
            const _SectionLabel('시간당 가치 · 매출 환산'),
            const _NavRow(title: '시간당 가치', trailing: '₩30,000'),
            const _NavRow(title: '매출 환산 표시', trailing: 'OFF'),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('작업 시간대 (V1.5)'),
            const _NavRow(title: '작업 시간', trailing: '09:00 - 18:00'),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('알림 채널'),
            ChannelToggleCard(
              icon: Icons.notifications_outlined,
              name: 'FCM 푸시',
              description: '기본 알림',
              value: true,
              enabled: false,
              onChanged: null,
            ),
            ChannelToggleCard(
              icon: Icons.mail_outline,
              name: '이메일',
              description: '주간 회고 카드 (W4)',
              value: false,
              onChanged: (_) {},
            ),
            ChannelToggleCard(
              icon: Icons.send_outlined,
              name: 'Telegram',
              description: '주간 회고 카드 (W5)',
              value: false,
              onChanged: (_) {},
            ),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('목표 설정'),
            const _NavRow(title: '카테고리별 일일 한도', trailing: '미설정'),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('개인정보 · 계정'),
            const _NavRow(title: '개인정보처리방침'),
            const _NavRow(title: '이용약관'),
            _NavRow(
              title: '로그아웃',
              onTap: () => ref.read(authProvider.notifier).logout(),
            ),
            const _NavRow(title: '회원 탈퇴', danger: true),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('앱 정보'),
            const _NavRow(title: '버전', trailing: '0.1.0'),
            const SizedBox(height: AppSpacing.xl),
          ],
        ),
      ),
    );
  }
}

class _SectionLabel extends StatelessWidget {
  const _SectionLabel(this.text);

  final String text;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(
        top: AppSpacing.md,
        bottom: AppSpacing.sm,
        left: AppSpacing.xs,
      ),
      child: Text(text, style: AppTypography.monoSmall()),
    );
  }
}

class _NavRow extends StatelessWidget {
  const _NavRow({
    required this.title,
    this.trailing,
    this.onTap,
    this.danger = false,
  });

  final String title;
  final String? trailing;
  final VoidCallback? onTap;
  final bool danger;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
        decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: AppColors.divider)),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: AppTypography.bodyLarge.copyWith(
                color: danger ? AppColors.danger : AppColors.textPrimary,
              ),
            ),
            if (trailing != null)
              Text(
                trailing!,
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              )
            else if (onTap != null && !danger)
              const Icon(Icons.chevron_right, color: AppColors.accent, size: 20),
          ],
        ),
      ),
    );
  }
}

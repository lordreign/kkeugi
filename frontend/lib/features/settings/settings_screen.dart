import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import '../auth/presentation/auth_provider.dart';
import '../channel/channel_toggle_card.dart';
import '../channel/telegram_provider.dart';
import '../payments/payments_providers.dart';
import '../payments/paywall_screen.dart';
import '../thresholds/thresholds_provider.dart';
import '../thresholds/thresholds_screen.dart';

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
        title: const Text('설정', style: AppTypography.titleLarge),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
          children: [
            const _SectionLabel('시간당 가치 · 매출 환산'),
            const _NavRow(title: '시간당 가치', trailing: '₩30,000'),
            _RevenueRow(ref: ref),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('작업 시간대 (V1.5)'),
            const _NavRow(title: '작업 시간', trailing: '09:00 - 18:00'),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('알림 채널'),
            const ChannelToggleCard(
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
              onChanged: (on) => ref.read(analyticsProvider).track(
                    AnalyticsEvents.channelToggled,
                    {'channel': 'email', 'on': on},
                  ),
            ),
            _TelegramCard(ref: ref),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('목표 설정'),
            _ThresholdsRow(ref: ref),
            const SizedBox(height: AppSpacing.lg),

            const _SectionLabel('개인정보 · 계정'),
            const _NavRow(title: '개인정보처리방침'),
            const _NavRow(title: '이용약관'),
            _NavRow(
              title: '로그아웃',
              onTap: () => ref.read(authProvider.notifier).logout(),
            ),
            _NavRow(
              title: '회원 탈퇴',
              danger: true,
              onTap: () => _confirmDeleteAccount(context, ref),
            ),
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

/// 카테고리별 한도 행 — 설정 개수 표시 + 한도 화면 진입.
class _ThresholdsRow extends StatelessWidget {
  const _ThresholdsRow({required this.ref});

  final WidgetRef ref;

  @override
  Widget build(BuildContext context) {
    final count = ref.watch(thresholdsListProvider).valueOrNull?.length ?? 0;
    return _NavRow(
      title: '카테고리별 일일 한도',
      trailing: count > 0 ? '$count개' : '미설정',
      onTap: () => Navigator.of(context).push(
        MaterialPageRoute<void>(builder: (_) => const ThresholdsScreen()),
      ),
    );
  }
}

/// 매출 환산 행 — entitlement 반영. 무료면 잠금 + paywall 진입.
class _RevenueRow extends StatelessWidget {
  const _RevenueRow({required this.ref});

  final WidgetRef ref;

  @override
  Widget build(BuildContext context) {
    final paid = ref.watch(entitlementProvider).valueOrNull?.paid ?? false;
    return _NavRow(
      title: '매출 환산',
      trailing: paid ? 'ON' : '잠김 · Pro',
      onTap: paid
          ? null
          : () => Navigator.of(context).push(
                MaterialPageRoute<void>(builder: (_) => const PaywallScreen()),
              ),
    );
  }
}

/// 회원 탈퇴 확인 — DESIGN 톤(압박 X, 객관). 30일 grace 안내.
Future<void> _confirmDeleteAccount(BuildContext context, WidgetRef ref) async {
  final confirmed = await showDialog<bool>(
    context: context,
    builder: (ctx) => AlertDialog(
      backgroundColor: AppColors.surface,
      title: const Text('회원 탈퇴'),
      content: const Text(
        '계정과 사용 기록이 삭제됩니다. 30일 안에 다시 로그인하면 복구할 수 있고, '
        '이후에는 영구 삭제돼요.',
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(ctx, false),
          child: const Text('취소'),
        ),
        TextButton(
          onPressed: () => Navigator.pop(ctx, true),
          child: const Text('탈퇴', style: TextStyle(color: AppColors.danger)),
        ),
      ],
    ),
  );
  if (confirmed == true) {
    await ref.read(authProvider.notifier).deleteAccount();
  }
}

/// Telegram 채널 카드 — 실제 연결 상태 반영 + 연결/해제 플로우.
class _TelegramCard extends StatelessWidget {
  const _TelegramCard({required this.ref});

  final WidgetRef ref;

  @override
  Widget build(BuildContext context) {
    final status = ref.watch(telegramStatusProvider);
    final subscribed = status.valueOrNull?.subscribed ?? false;
    final desc = switch (status) {
      AsyncData(:final value) when value.subscribed => '연결됨 · 주간 회고 카드',
      AsyncData() => '주간 회고 카드 — 연결하기',
      AsyncError() => '상태 확인 실패 · 다시 시도',
      _ => '주간 회고 카드',
    };

    return ChannelToggleCard(
      icon: Icons.send_outlined,
      name: 'Telegram',
      description: desc,
      value: subscribed,
      onChanged: status.isLoading
          ? null
          : (on) async {
              final messenger = ScaffoldMessenger.of(context);
              await ref.read(analyticsProvider).track(
                AnalyticsEvents.channelToggled,
                {'channel': 'telegram', 'on': on},
              );
              if (on) {
                final ok = await startTelegramLink(ref);
                messenger.showSnackBar(
                  SnackBar(
                    content: Text(
                      ok
                          ? 'Telegram에서 시작을 누르면 연결돼요. 돌아와서 새로고침하세요.'
                          : 'Telegram을 열 수 없어요. 앱 설치를 확인해주세요.',
                    ),
                  ),
                );
                // 복귀 후 상태 재확인용
                ref.invalidate(telegramStatusProvider);
              } else {
                await unsubscribeTelegram(ref);
                messenger.showSnackBar(
                  const SnackBar(content: Text('Telegram 알림을 껐어요.')),
                );
              }
            },
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

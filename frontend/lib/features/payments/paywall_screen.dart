import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import 'billing_service.dart';
import 'payments_providers.dart';

/// 끊기 Pro paywall — DESIGN 톤(압박 X, 객관). D7 리포트 후 / 매출 환산 진입 시 노출.
class PaywallScreen extends ConsumerStatefulWidget {
  const PaywallScreen({super.key});

  @override
  ConsumerState<PaywallScreen> createState() => _PaywallScreenState();
}

class _PaywallScreenState extends ConsumerState<PaywallScreen> {
  String _selectedId = 'kkeugi.monthly'; // 기본 추천
  bool _busy = false;

  BillingProduct get _selected =>
      kCatalog.firstWhere((p) => p.id == _selectedId);

  Future<void> _purchase() async {
    setState(() => _busy = true);
    final messenger = ScaffoldMessenger.of(context);
    final navigator = Navigator.of(context);
    final error = await purchase(ref, _selected, trial: _selected.hasTrial);
    if (!mounted) return;
    setState(() => _busy = false);
    if (error == null) {
      messenger.showSnackBar(
        const SnackBar(content: Text('끊기 Pro가 시작됐어요. 회복한 시간을 매출로 보여드릴게요.')),
      );
      navigator.pop(true);
    } else {
      messenger.showSnackBar(SnackBar(content: Text(error)));
    }
  }

  @override
  Widget build(BuildContext context) {
    final sub = _selected.isSubscription;
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: const Text('끊기 Pro'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: AppSpacing.md),
              const Text(
                '흩어진 시간을\n매출로 환산해드려요.',
                style: AppTypography.headlineMedium,
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                '주간 회고 + 시간 빚의 매출 환산 + 카테고리별 한도 알림. '
                '압박 없이, 객관적으로.',
                style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(height: AppSpacing.xl),
              for (final p in kCatalog)
                _PlanCard(
                  product: p,
                  selected: p.id == _selectedId,
                  onTap: () => setState(() => _selectedId = p.id),
                ),
              const Spacer(),
              if (sub)
                Padding(
                  padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                  child: Text(
                    '7일 무료 체험 후 결제 · 언제든 해지 가능',
                    style: AppTypography.bodyMedium.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _busy ? null : _purchase,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
                    child: _busy
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : Text(sub ? '7일 무료로 시작' : '구매하기'),
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              Center(
                child: Text(
                  'Google Play 결제 · 구독은 Play 스토어에서 해지',
                  style: AppTypography.bodyMedium.copyWith(
                    color: AppColors.textSecondary,
                    fontSize: 12,
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
            ],
          ),
        ),
      ),
    );
  }
}

class _PlanCard extends StatelessWidget {
  const _PlanCard({
    required this.product,
    required this.selected,
    required this.onTap,
  });

  final BillingProduct product;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.sm),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: selected ? AppColors.accent : AppColors.divider,
              width: selected ? 2 : 1,
            ),
          ),
          child: Row(
            children: [
              Icon(
                selected ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                color: selected ? AppColors.accent : AppColors.textSecondary,
                size: 22,
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(product.title, style: AppTypography.bodyLarge),
                    if (product.hasTrial)
                      Text(
                        '7일 무료 체험',
                        style: AppTypography.bodyMedium.copyWith(
                          color: AppColors.accent,
                        ),
                      ),
                  ],
                ),
              ),
              Text(product.priceLabel, style: AppTypography.bodyLarge),
            ],
          ),
        ),
      ),
    );
  }
}

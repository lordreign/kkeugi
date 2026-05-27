import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../../core/notifications/local_notifications.dart';
import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import '../payments/payments_providers.dart';
import '../payments/paywall_screen.dart';
import 'thresholds_api.dart';
import 'thresholds_provider.dart';

const _allCategories = ['sns', 'shorts', 'game', 'webtoon', 'other'];

/// 카테고리별 일일 한도 — 초과 시 로컬 알람(Step 3). 생성은 유료.
class ThresholdsScreen extends ConsumerWidget {
  const ThresholdsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final list = ref.watch(thresholdsListProvider);
    final paid = ref.watch(entitlementProvider).valueOrNull?.paid ?? false;

    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: const Text('카테고리별 한도'),
      ),
      body: SafeArea(
        child: list.when(
          loading: () => const Center(child: CircularProgressIndicator(strokeWidth: 2)),
          error: (e, _) => Center(child: Text('불러오기 실패: $e')),
          data: (items) {
            final used = items.map((t) => t.category).toSet();
            final canAdd = used.length < _allCategories.length;
            return Column(
              children: [
                Expanded(
                  child: items.isEmpty
                      ? Center(
                          child: Padding(
                            padding: const EdgeInsets.all(AppSpacing.lg),
                            child: Text(
                              '한도를 설정하면 초과할 때 조용히 알려드려요.\n압박은 없어요.',
                              textAlign: TextAlign.center,
                              style: AppTypography.bodyMedium
                                  .copyWith(color: AppColors.textSecondary),
                            ),
                          ),
                        )
                      : ListView(
                          padding: const EdgeInsets.all(AppSpacing.md),
                          children: [
                            for (final t in items) _ThresholdRow(item: t, ref: ref),
                          ],
                        ),
                ),
                Padding(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: !canAdd
                          ? null
                          : () {
                              if (paid) {
                                Navigator.of(context).push(
                                  MaterialPageRoute<void>(
                                    builder: (_) => AddThresholdScreen(used: used),
                                  ),
                                );
                              } else {
                                Navigator.of(context).push(
                                  MaterialPageRoute<void>(
                                    builder: (_) => const PaywallScreen(),
                                  ),
                                );
                              }
                            },
                      child: Padding(
                        padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
                        child: Text(canAdd ? '한도 추가' : '모든 카테고리 설정됨'),
                      ),
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _ThresholdRow extends StatelessWidget {
  const _ThresholdRow({required this.item, required this.ref});

  final ThresholdItem item;
  final WidgetRef ref;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppSpacing.sm),
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.divider),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(item.label, style: AppTypography.bodyLarge),
                Text(
                  '하루 ${item.dailyLimitMinutes}분',
                  style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
          Switch(
            value: item.enabled,
            onChanged: (v) async {
              await ref.read(thresholdsApiProvider).update(item.id, enabled: v);
              ref.invalidate(thresholdsListProvider);
            },
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline, color: AppColors.textSecondary),
            onPressed: () async {
              await ref.read(thresholdsApiProvider).delete(item.id);
              ref.invalidate(thresholdsListProvider);
            },
          ),
        ],
      ),
    );
  }
}

/// 한도 추가 — 카테고리 + 분 선택, 하단 저장 CTA.
class AddThresholdScreen extends ConsumerStatefulWidget {
  const AddThresholdScreen({super.key, required this.used});

  final Set<String> used;

  @override
  ConsumerState<AddThresholdScreen> createState() => _AddThresholdScreenState();
}

class _AddThresholdScreenState extends ConsumerState<AddThresholdScreen> {
  late String _category;
  int _minutes = 30;
  bool _busy = false;

  static const _minuteOptions = [15, 30, 45, 60, 90, 120];

  @override
  void initState() {
    super.initState();
    _category = _allCategories.firstWhere((c) => !widget.used.contains(c));
  }

  Future<void> _save() async {
    setState(() => _busy = true);
    final messenger = ScaffoldMessenger.of(context);
    final navigator = Navigator.of(context);
    try {
      await ref.read(thresholdsApiProvider).create(_category, _minutes);
      await ref.read(analyticsProvider).track(
        AnalyticsEvents.thresholdCreated,
        {'category': _category, 'minutes': _minutes},
      );
      // 한도 알람을 보내려면 알림 권한 필요 — 설정 직후 자연스러운 시점에 요청.
      await LocalNotifications.instance.requestPermission();
      ref.invalidate(thresholdsListProvider);
      if (!mounted) return;
      navigator.pop();
    } catch (_) {
      if (!mounted) return;
      setState(() => _busy = false);
      messenger.showSnackBar(const SnackBar(content: Text('저장에 실패했어요.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final available = _allCategories.where((c) => !widget.used.contains(c)).toList();
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: const Text('한도 추가'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: AppSpacing.md),
              Text('카테고리', style: AppTypography.monoSmall()),
              const SizedBox(height: AppSpacing.sm),
              Wrap(
                spacing: AppSpacing.sm,
                children: [
                  for (final c in available)
                    ChoiceChip(
                      label: Text(thresholdCategoryLabels[c] ?? c),
                      selected: _category == c,
                      onSelected: (_) => setState(() => _category = c),
                    ),
                ],
              ),
              const SizedBox(height: AppSpacing.lg),
              Text('하루 한도 (분)', style: AppTypography.monoSmall()),
              const SizedBox(height: AppSpacing.sm),
              Wrap(
                spacing: AppSpacing.sm,
                children: [
                  for (final m in _minuteOptions)
                    ChoiceChip(
                      label: Text('$m분'),
                      selected: _minutes == m,
                      onSelected: (_) => setState(() => _minutes = m),
                    ),
                ],
              ),
              const Spacer(),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _busy ? null : _save,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
                    child: _busy
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('저장'),
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

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../shared/widgets/hero_numeral.dart';
import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import '../thresholds/thresholds_provider.dart';
import '../usage/category_map.dart';
import '../usage/usage_api.dart';
import '../usage/usage_channel.dart';
import '../usage/usage_providers.dart';

/// 카테고리 한글 라벨.
const _categoryLabels = {
  'sns': 'SNS',
  'shorts': '쇼츠',
  'game': '게임',
  'webtoon': '웹툰',
  'other': '기타',
};

String _categoryLabel(String category) => _categoryLabels[category] ?? category;

/// W4 — UsageStatsManager 자동 import 실데이터 연결.
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final permission = ref.watch(usagePermissionProvider);
    final stats = ref.watch(todayStatsProvider);
    // 한도 알람 활성화 (fire-and-forget) — 초과 시 로컬 알림. 값은 쓰지 않음.
    ref.watch(thresholdAlarmProvider);

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
        child: RefreshIndicator(
          color: AppColors.accent,
          onRefresh: () async {
            ref.invalidate(usagePermissionProvider);
            ref.invalidate(todayStatsProvider);
            await ref.read(todayStatsProvider.future);
          },
          child: permission.when(
            loading: () => const _Centered(child: CircularProgressIndicator(strokeWidth: 2)),
            error: (e, _) => _Centered(child: Text('권한 확인 실패: $e')),
            data: (granted) {
              if (!granted) return _PermissionGate(ref: ref);
              return stats.when(
                loading: () =>
                    const _Centered(child: CircularProgressIndicator(strokeWidth: 2)),
                error: (e, _) => _Centered(child: Text('불러오기 실패: $e')),
                data: (data) => _StatsBody(data: data),
              );
            },
          ),
        ),
      ),
    );
  }
}

class _Centered extends StatelessWidget {
  const _Centered({required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) => ListView(
        physics: const AlwaysScrollableScrollPhysics(),
        children: [
          SizedBox(
            height: MediaQuery.sizeOf(context).height * 0.6,
            child: Center(child: child),
          ),
        ],
      );
}

/// 권한 미허용 — 설정으로 유도 (DESIGN 압박 X 톤).
class _PermissionGate extends StatelessWidget {
  const _PermissionGate({required this.ref});
  final WidgetRef ref;

  @override
  Widget build(BuildContext context) {
    return ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
      children: [
        const SizedBox(height: AppSpacing.xl2),
        const Text('사용 통계 접근이 필요해요.', style: AppTypography.headlineMedium),
        const SizedBox(height: AppSpacing.md),
        Text(
          '앱별 사용 시간을 읽어 흩어진 시간을 보여드려요. '
          '데이터는 기기 안에 남고, 언제든 권한을 해제할 수 있어요.',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
        ),
        const SizedBox(height: AppSpacing.xl),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: () async {
              await openUsagePermissionSettings(ref);
            },
            child: const Padding(
              padding: EdgeInsets.symmetric(vertical: AppSpacing.xs),
              child: Text('권한 설정으로 이동'),
            ),
          ),
        ),
        const SizedBox(height: AppSpacing.sm),
        Center(
          child: TextButton(
            onPressed: () {
              ref.invalidate(usagePermissionProvider);
              ref.invalidate(todayStatsProvider);
            },
            child: const Text('허용했어요 · 새로고침'),
          ),
        ),
      ],
    );
  }
}

class _StatsBody extends StatelessWidget {
  const _StatsBody({required this.data});
  final TodayStats data;

  @override
  Widget build(BuildContext context) {
    final total = data.totalMinutes;
    final maxMinutes = data.byCategory.isEmpty
        ? 1
        : data.byCategory.map((c) => c.minutes).reduce((a, b) => a > b ? a : b);

    return ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
      children: [
        const SizedBox(height: AppSpacing.lg),
        Text(
          '내일 일정에 더해질 시간 빚',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
        ),
        const SizedBox(height: AppSpacing.sm),
        HeroNumeral(value: total == 0 ? '0' : '+$total', unit: '분'),
        const SizedBox(height: AppSpacing.lg),
        Text(
          total == 0
              ? '오늘은 아직 흩어진 시간이 없어요. 데이터가 모이면 여기에 쌓입니다.'
              : '오늘 SNS·쇼츠·웹툰으로 흩어진 시간이 내일 일정 위에 올라갑니다.',
          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
        ),
        const SizedBox(height: AppSpacing.xl2),
        if (data.byCategory.isNotEmpty) ...[
          Text('오늘 · 카테고리별', style: AppTypography.monoSmall()),
          const SizedBox(height: AppSpacing.md),
          for (final c in data.byCategory)
            _CategoryRow(
              name: _categoryLabel(c.category),
              minutes: c.minutes,
              ratio: maxMinutes == 0 ? 0 : c.minutes / maxMinutes,
            ),
        ],
        if (data.byApp.isNotEmpty) ...[
          const SizedBox(height: AppSpacing.xl2),
          _AppBreakdown(apps: data.byApp),
        ],
        const SizedBox(height: AppSpacing.xl),
      ],
    );
  }
}

/// 앱별 drill-down — 카테고리 요약 아래에서 실제 앱을 그대로 보여준다.
/// 이름·아이콘은 appMetaProvider(로컬 PackageManager)로 해석, 분은 서버 집계.
class _AppBreakdown extends ConsumerWidget {
  const _AppBreakdown({required this.apps});
  final List<AppStat> apps;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final meta = ref.watch(appMetaProvider).valueOrNull ?? const {};
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text('오늘 · 앱별', style: AppTypography.monoSmall()),
        const SizedBox(height: AppSpacing.md),
        for (final a in apps)
          _AppRow(
            app: a,
            meta: meta[a.packageName],
          ),
      ],
    );
  }
}

class _AppRow extends StatelessWidget {
  const _AppRow({required this.app, required this.meta});

  final AppStat app;
  final AppMeta? meta;

  @override
  Widget build(BuildContext context) {
    final name = meta?.displayName ?? app.packageName;
    final category = _categoryLabel(categoryForPackage(app.packageName));
    final icon = meta?.icon;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: AppSpacing.sm),
      child: Row(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: icon != null
                ? Image.memory(icon, width: 32, height: 32, gaplessPlayback: true)
                : Container(
                    width: 32,
                    height: 32,
                    color: AppColors.divider,
                    alignment: Alignment.center,
                    child: Text(
                      name.isNotEmpty ? name.characters.first : '?',
                      style: AppTypography.bodyMedium
                          .copyWith(color: AppColors.textSecondary),
                    ),
                  ),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: AppTypography.bodyMedium,
                ),
                Text(
                  category,
                  style: AppTypography.labelSmall
                      .copyWith(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Text(
            '${app.minutes}분',
            style: AppTypography.bodyMedium.copyWith(
              fontFeatures: const [],
              color: AppColors.textSecondary,
            ),
          ),
        ],
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
              widthFactor: ratio.clamp(0.0, 1.0),
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

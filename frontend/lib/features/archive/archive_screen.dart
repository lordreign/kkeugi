import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import 'reports_api.dart';
import 'reports_provider.dart';
import 'share_card.dart';

/// 회고 탭 — 주간 리포트 archive (최신순). DESIGN 톤(거울 같은 친구).
class ArchiveScreen extends ConsumerStatefulWidget {
  const ArchiveScreen({super.key});

  @override
  ConsumerState<ArchiveScreen> createState() => _ArchiveScreenState();
}

class _ArchiveScreenState extends ConsumerState<ArchiveScreen> {
  bool _viewedTracked = false;

  @override
  Widget build(BuildContext context) {
    final reports = ref.watch(reportsListProvider);
    // 리포트가 실제로 렌더되는 시점에 1회 열람 KPI.
    if (!_viewedTracked && reports.valueOrNull?.isNotEmpty == true) {
      _viewedTracked = true;
      ref.read(analyticsProvider).track(AnalyticsEvents.reportViewed);
    }
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: const Text('회고', style: AppTypography.titleLarge),
      ),
      body: SafeArea(
        child: RefreshIndicator(
          color: AppColors.accent,
          onRefresh: () async {
            ref.invalidate(reportsListProvider);
            await ref.read(reportsListProvider.future);
          },
          child: reports.when(
            loading: () => const _Center(child: CircularProgressIndicator(strokeWidth: 2)),
            error: (e, _) => _Center(child: Text('불러오기 실패: $e')),
            data: (list) => list.isEmpty
                ? const _EmptyState()
                : ListView.builder(
                    physics: const AlwaysScrollableScrollPhysics(),
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.md,
                      vertical: AppSpacing.md,
                    ),
                    itemCount: list.length,
                    itemBuilder: (_, i) => _ReportCard(report: list[i]),
                  ),
          ),
        ),
      ),
    );
  }
}

class _Center extends StatelessWidget {
  const _Center({required this.child});
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

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) => ListView(
        physics: const AlwaysScrollableScrollPhysics(),
        children: [
          SizedBox(
            height: MediaQuery.sizeOf(context).height * 0.55,
            child: Center(
              child: Padding(
                padding: const EdgeInsets.all(AppSpacing.lg),
                child: Text(
                  '첫 회고가 도착하면 여기에 모입니다.\n일요일 22:00에 한 주가 정리돼요.',
                  textAlign: TextAlign.center,
                  style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                ),
              ),
            ),
          ),
        ],
      );
}

class _ReportCard extends StatelessWidget {
  const _ReportCard({required this.report});
  final WeeklyReportCard report;

  String get _weekLabel {
    final parts = report.weekStartDate.split('-');
    if (parts.length == 3) return '${int.parse(parts[1])}월 ${int.parse(parts[2])}일 주';
    return report.weekStartDate;
  }

  @override
  Widget build(BuildContext context) {
    final recovered = report.recoveredMinutes;
    final recoveredLabel = recovered >= 0
        ? '지난주보다 $recovered분 회복'
        : '지난주보다 ${-recovered}분 증가';

    return Container(
      margin: const EdgeInsets.only(bottom: AppSpacing.md),
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.divider),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(child: Text(_weekLabel, style: AppTypography.monoSmall())),
              Text(
                '${report.totalMinutes}분',
                style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(width: AppSpacing.xs),
              InkWell(
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (_) => ReportSharePreviewScreen(report: report),
                  ),
                ),
                customBorder: const CircleBorder(),
                child: const Padding(
                  padding: EdgeInsets.all(AppSpacing.xs),
                  child: Icon(Icons.ios_share, size: 18, color: AppColors.accent),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Text(report.cardText, style: AppTypography.bodyLarge),
          if (report.cardInsight != null) ...[
            const SizedBox(height: AppSpacing.sm),
            Text(
              report.cardInsight!,
              style: AppTypography.bodyMedium.copyWith(color: AppColors.accent),
            ),
          ],
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              Text(
                recoveredLabel,
                style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
              ),
              if (report.recoveredWon != null) ...[
                Text(
                  '  ·  ',
                  style: AppTypography.bodyMedium.copyWith(color: AppColors.divider),
                ),
                Text(
                  '${_won(report.recoveredWon!)}원',
                  style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }

  String _won(int won) {
    final v = won.abs();
    final s = v.toString().replaceAllMapped(
          RegExp(r'(\d)(?=(\d{3})+$)'),
          (m) => '${m[1]},',
        );
    return won >= 0 ? '+$s' : '-$s';
  }
}

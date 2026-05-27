import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

import '../../core/analytics/analytics.dart';
import '../../core/analytics/analytics_provider.dart';
import '../../shared/widgets/hero_numeral.dart';
import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import 'reports_api.dart';

/// 공유 카드 논리 크기. pixelRatio 3 → 1080×1920 (DESIGN: 인스타 스토리 9:16).
const _cardW = 360.0;
const _cardH = 640.0;
const _exportPixelRatio = 3.0;

String _weekLabel(String weekStartDate) {
  final parts = weekStartDate.split('-');
  if (parts.length == 3) {
    return '${int.parse(parts[1])}월 ${int.parse(parts[2])}일 주';
  }
  return weekStartDate;
}

String _formatWon(int won) {
  final v = won.abs().toString().replaceAllMapped(
        RegExp(r'(\d)(?=(\d{3})+$)'),
        (m) => '${m[1]},',
      );
  return won >= 0 ? v : '-$v';
}

/// 1080×1920 공유 이미지로 렌더되는 카드. DESIGN "주간 리포트 = 편지":
/// 한 단락 본문 + embedded hero numeral, 차트 없음.
class ShareCard extends StatelessWidget {
  const ShareCard({super.key, required this.report});

  final WeeklyReportCard report;

  @override
  Widget build(BuildContext context) {
    // 매출환산(유료)이 있으면 그 숫자를, 없으면 회복 시간을 hero로.
    final won = report.recoveredWon;
    final minutes = report.recoveredMinutes;
    final heroLabel = won != null
        ? '이번 주 되찾은 가치'
        : (minutes >= 0 ? '이번 주 되찾은 시간' : '이번 주 늘어난 시간');

    return SizedBox(
      width: _cardW,
      height: _cardH,
      child: ColoredBox(
        color: AppColors.bg,
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.xl),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(_weekLabel(report.weekStartDate), style: AppTypography.monoSmall()),
              const Spacer(flex: 2),
              Text(
                heroLabel,
                style: AppTypography.bodyMedium
                    .copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(height: AppSpacing.sm),
              if (won != null)
                // ₩ + tabular 숫자: heroNumeral 음수 트래킹이 글자를 겹치게 해
                // ₩와 숫자 사이를 분리(가독성).
                HeroNumeral(value: '₩ ${_formatWon(won)}', size: 52)
              else
                HeroNumeral(
                  value: minutes >= 0 ? '+$minutes' : '$minutes',
                  unit: '분',
                  size: 60,
                ),
              const SizedBox(height: AppSpacing.lg),
              Text(report.cardText, style: AppTypography.bodyLarge),
              if (report.cardInsight != null) ...[
                const SizedBox(height: AppSpacing.sm),
                Text(
                  report.cardInsight!,
                  style: AppTypography.bodyMedium.copyWith(color: AppColors.accent),
                ),
              ],
              const Spacer(flex: 3),
              Row(
                children: [
                  Container(
                    width: 6,
                    height: 6,
                    decoration: const BoxDecoration(
                      color: AppColors.accent,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Text(
                    '끊기 · Focus Accountant',
                    style: AppTypography.labelSmall
                        .copyWith(color: AppColors.textTertiary),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// 공유 미리보기 — 실제 공유될 카드를 그대로 보여주고 1-tap 공유.
/// RepaintBoundary를 화면에 실제로 그려 캡처 신뢰성 확보(오프스크린 캡처 회피).
class ReportSharePreviewScreen extends ConsumerStatefulWidget {
  const ReportSharePreviewScreen({super.key, required this.report});

  final WeeklyReportCard report;

  @override
  ConsumerState<ReportSharePreviewScreen> createState() =>
      _ReportSharePreviewScreenState();
}

class _ReportSharePreviewScreenState
    extends ConsumerState<ReportSharePreviewScreen> {
  final _cardKey = GlobalKey();
  bool _busy = false;

  Future<void> _share() async {
    setState(() => _busy = true);
    final messenger = ScaffoldMessenger.of(context);
    try {
      // 폰트(IBM Plex Mono 동적 로드)·레이아웃이 완료된 프레임 이후 캡처.
      await WidgetsBinding.instance.endOfFrame;
      final boundary = _cardKey.currentContext!.findRenderObject()
          as RenderRepaintBoundary;
      final image = await boundary.toImage(pixelRatio: _exportPixelRatio);
      final data = await image.toByteData(format: ui.ImageByteFormat.png);
      if (data == null) throw StateError('이미지 인코딩 실패');
      final bytes = data.buffer.asUint8List();

      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/kkeugi_report.png');
      await file.writeAsBytes(bytes, flush: true);

      await ref.read(analyticsProvider).track(AnalyticsEvents.reportShared);
      await Share.shareXFiles(
        [XFile(file.path, mimeType: 'image/png')],
        text: '끊기로 이번 주 흩어진 시간을 되찾았어요.',
      );
    } catch (_) {
      messenger.showSnackBar(
        const SnackBar(content: Text('공유 이미지를 만들지 못했어요. 다시 시도해주세요.')),
      );
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: AppBar(
        backgroundColor: AppColors.bg,
        elevation: 0,
        title: const Text('카드 공유'),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: DecoratedBox(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(AppRadius.lg),
                      border: Border.all(color: AppColors.divider),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(AppRadius.lg),
                      // 실제 캡처 대상은 360×640. FittedBox는 표시용 스케일만.
                      child: FittedBox(
                        child: RepaintBoundary(
                          key: _cardKey,
                          child: ShareCard(report: widget.report),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(AppSpacing.lg),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _busy ? null : _share,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
                    child: _busy
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('이미지로 공유하기'),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

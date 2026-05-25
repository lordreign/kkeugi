import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';
import 'steps/step1_reason.dart';
import 'steps/step2_permission.dart';
import 'steps/step3_shock.dart';
import 'steps/step4_hourly_value.dart';
import 'steps/step5_channel_select.dart';

/// 온보딩 5단계 (P5: 이유 → 권한 → shock → 시간당 가치 → 채널 선택).
/// DESIGN.md memorable thing — 압박 X, 관찰 중립 톤.
class OnboardingFlow extends ConsumerStatefulWidget {
  const OnboardingFlow({super.key, required this.onComplete});

  /// (hourlyValue, selectedChannels) — 완료 시 backend 반영용.
  final void Function(int? hourlyValue, Set<String> channels) onComplete;

  @override
  ConsumerState<OnboardingFlow> createState() => _OnboardingFlowState();
}

class _OnboardingFlowState extends ConsumerState<OnboardingFlow> {
  final _controller = PageController();
  int _page = 0;

  // 온보딩 수집 상태
  int? _hourlyValue;
  final Set<String> _channels = {'fcm'}; // FCM 기본 강제

  static const _pageCount = 5;

  void _next() {
    if (_page < _pageCount - 1) {
      _controller.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    } else {
      widget.onComplete(_hourlyValue, _channels);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      body: SafeArea(
        child: Column(
          children: [
            // progress dots
            Padding(
              padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(
                  _pageCount,
                  (i) => AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    margin: const EdgeInsets.symmetric(horizontal: 3),
                    width: i == _page ? 20 : 6,
                    height: 6,
                    decoration: BoxDecoration(
                      color: i == _page ? AppColors.accent : AppColors.divider,
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),
                ),
              ),
            ),
            Expanded(
              child: PageView(
                controller: _controller,
                physics: const NeverScrollableScrollPhysics(),
                onPageChanged: (i) => setState(() => _page = i),
                children: [
                  Step1Reason(onNext: _next),
                  Step2Permission(onNext: _next),
                  Step3Shock(onNext: _next),
                  Step4HourlyValue(
                    onNext: (value) {
                      _hourlyValue = value;
                      _next();
                    },
                  ),
                  Step5ChannelSelect(
                    selected: _channels,
                    onToggle: (ch, on) => setState(() {
                      if (on) {
                        _channels.add(ch);
                      } else {
                        _channels.remove(ch);
                      }
                    }),
                    onComplete: _next,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// 온보딩 step 공통 레이아웃.
class OnboardingStepScaffold extends StatelessWidget {
  const OnboardingStepScaffold({
    super.key,
    required this.title,
    this.subtitle,
    required this.child,
    required this.ctaLabel,
    required this.onCta,
    this.secondaryLabel,
    this.onSecondary,
  });

  final String title;
  final String? subtitle;
  final Widget child;
  final String ctaLabel;
  final VoidCallback onCta;
  final String? secondaryLabel;
  final VoidCallback? onSecondary;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: AppSpacing.xl),
          Text(title, style: AppTypography.headlineMedium),
          if (subtitle != null) ...[
            const SizedBox(height: AppSpacing.md),
            Text(
              subtitle!,
              style: AppTypography.bodyMedium.copyWith(
                color: AppColors.textSecondary,
              ),
            ),
          ],
          const SizedBox(height: AppSpacing.xl),
          Expanded(child: child),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: onCta,
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
                child: Text(ctaLabel),
              ),
            ),
          ),
          if (secondaryLabel != null)
            Center(
              child: TextButton(
                onPressed: onSecondary,
                child: Text(secondaryLabel!),
              ),
            ),
          const SizedBox(height: AppSpacing.md),
        ],
      ),
    );
  }
}

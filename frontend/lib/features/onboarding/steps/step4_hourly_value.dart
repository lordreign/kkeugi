import 'package:flutter/material.dart';

import '../../../theme/spacing.dart';
import '../onboarding_flow.dart';

/// Step 4 — 시간당 가치 입력 (skip 가능, ₩30K default).
class Step4HourlyValue extends StatefulWidget {
  const Step4HourlyValue({super.key, required this.onNext});

  final void Function(int? hourlyValue) onNext;

  @override
  State<Step4HourlyValue> createState() => _Step4HourlyValueState();
}

class _Step4HourlyValueState extends State<Step4HourlyValue> {
  final _controller = TextEditingController(text: '30000');

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  int? get _value => int.tryParse(_controller.text.replaceAll(',', ''));

  @override
  Widget build(BuildContext context) {
    return OnboardingStepScaffold(
      title: '본업 시간당 가치는\n얼마인가요?',
      subtitle: '입력하면 회복한 시간을 매출로 환산해드려요. 나중에 설정에서 바꿀 수 있어요.',
      ctaLabel: '다음',
      onCta: () => widget.onNext(_value),
      secondaryLabel: '건너뛰기',
      onSecondary: () => widget.onNext(null),
      child: Column(
        children: [
          TextField(
            controller: _controller,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              prefixText: '₩ ',
              hintText: '30,000',
            ),
          ),
          const SizedBox(height: AppSpacing.sm),
        ],
      ),
    );
  }
}

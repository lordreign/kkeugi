import 'package:flutter/material.dart';

import '../../theme/colors.dart';
import '../../theme/spacing.dart';
import '../../theme/typography.dart';

/// DESIGN.md ChannelToggleCard — multi-channel 선택 widget.
class ChannelToggleCard extends StatelessWidget {
  const ChannelToggleCard({
    super.key,
    required this.icon,
    required this.name,
    required this.description,
    required this.value,
    required this.onChanged,
    this.enabled = true,
  });

  final IconData icon;
  final String name;
  final String description;
  final bool value;
  final ValueChanged<bool>? onChanged;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    return Opacity(
      opacity: enabled ? 1.0 : 0.6,
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        margin: const EdgeInsets.only(bottom: AppSpacing.sm),
        decoration: BoxDecoration(
          color: AppColors.surface,
          border: Border.all(color: AppColors.divider),
          borderRadius: BorderRadius.circular(AppRadius.md),
        ),
        child: Row(
          children: [
            Icon(icon, size: 24, color: AppColors.textPrimary),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(name, style: AppTypography.bodyLarge),
                  Text(description, style: AppTypography.labelSmall),
                ],
              ),
            ),
            Switch(
              value: value,
              onChanged: enabled ? onChanged : null,
            ),
          ],
        ),
      ),
    );
  }
}

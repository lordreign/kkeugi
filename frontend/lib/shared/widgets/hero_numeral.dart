import 'package:flutter/material.dart';

import '../../theme/colors.dart';
import '../../theme/typography.dart';

/// DESIGN.md signature — 매 화면 가장 큰 요소.
/// "+47" 또는 "₩68,250" 등 단일 numeral.
/// IBM Plex Mono, tabular figures.
class HeroNumeral extends StatelessWidget {
  const HeroNumeral({
    super.key,
    required this.value,
    this.unit,
    this.size = 72,
    this.color,
  });

  final String value; // "+47", "68,250" 등
  final String? unit; // "분", "원"
  final double size;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    final unitSize = size * 0.44;
    return RichText(
      text: TextSpan(
        text: value,
        style: AppTypography.heroNumeral(size: size).copyWith(
          color: color ?? AppColors.textPrimary,
        ),
        children: unit == null
            ? null
            : [
                TextSpan(
                  text: unit,
                  style: TextStyle(
                    fontFamily: AppTypography.heroNumeral().fontFamily,
                    fontSize: unitSize,
                    color: AppColors.textSecondary,
                    fontWeight: FontWeight.w400,
                  ),
                ),
              ],
      ),
    );
  }
}

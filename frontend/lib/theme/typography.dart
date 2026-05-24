import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'colors.dart';

/// DESIGN.md typography tokens.
///
/// Pretendard for Hangul + Latin body.
/// IBM Plex Mono for hero numerals only (signature departure).
class AppTypography {
  AppTypography._();

  static const _pretendard = 'Pretendard';

  /// Hero numeral — IBM Plex Mono 64-80sp, tabular-nums.
  /// Used on Home (+47분) and Weekly Report (₩68,250) only.
  static TextStyle heroNumeral({double size = 72}) => GoogleFonts.ibmPlexMono(
        fontWeight: FontWeight.w600,
        fontSize: size,
        letterSpacing: -size * 0.04,
        height: 1.0,
        color: AppColors.textPrimary,
        fontFeatures: const [FontFeature.tabularFigures()],
      );

  static const displayLarge = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w700,
    fontSize: 56,
    letterSpacing: -1.68, // -0.03em
    height: 1.0,
    color: AppColors.textPrimary,
  );

  static const headlineLarge = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w600,
    fontSize: 32,
    letterSpacing: -0.64, // -0.02em
    color: AppColors.textPrimary,
  );

  static const headlineMedium = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w600,
    fontSize: 28,
    letterSpacing: -0.56,
    color: AppColors.textPrimary,
  );

  static const titleLarge = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w600,
    fontSize: 20,
    letterSpacing: -0.2, // -0.01em
    color: AppColors.textPrimary,
  );

  static const bodyLarge = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w400,
    fontSize: 16,
    height: 1.6,
    color: AppColors.textPrimary,
  );

  static const bodyMedium = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w400,
    fontSize: 14,
    height: 1.6,
    color: AppColors.textPrimary,
  );

  static const labelSmall = TextStyle(
    fontFamily: _pretendard,
    fontWeight: FontWeight.w400,
    fontSize: 13,
    color: AppColors.textSecondary,
  );

  /// IBM Plex Mono small labels (e.g. "SUN · MAY 22 · WEEK 21")
  static TextStyle monoSmall() => GoogleFonts.ibmPlexMono(
        fontSize: 12,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.96, // 0.08em
        color: AppColors.textTertiary,
      );

  static TextTheme textTheme(BuildContext context) {
    // Pretendard bundled in assets/fonts/ — applied as default fontFamily in theme.dart
    return const TextTheme(
      displayLarge: displayLarge,
      headlineLarge: headlineLarge,
      headlineMedium: headlineMedium,
      titleLarge: titleLarge,
      bodyLarge: bodyLarge,
      bodyMedium: bodyMedium,
      labelSmall: labelSmall,
    );
  }
}

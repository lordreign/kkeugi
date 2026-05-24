import 'package:flutter/material.dart';

/// DESIGN.md color tokens — V1 light mode only.
/// Dark mode 추가는 V2 (Phase 1 매출 ₩200만/월 후).
class AppColors {
  AppColors._();

  // Backgrounds
  static const bg = Color(0xFFFAFAF7); // warm off-white
  static const surface = Color(0xFFFFFFFF);
  static const surface2 = Color(0xFFF5F2EC); // subtle grouping

  // Text
  static const textPrimary = Color(0xFF1A1A1A); // hero numeral default
  static const textSecondary = Color(0xFF8A8A85); // warm gray, labels
  static const textTertiary = Color(0xFFBCBBB7); // weakest text, placeholder

  // Accent (signature)
  static const accent = Color(0xFF8B5A3C); // clay — kkeugi signature
  static const accentSoft = Color(0xFFE8DDD4); // tint (rare use)

  // Structural
  static const divider = Color(0xFFE8E5DE);

  // Semantic (muted, rare use)
  static const success = Color(0xFF2E4A3F); // deep ink-green
  static const danger = Color(0xFF8B3C3C); // muted red — permission denied, error
}

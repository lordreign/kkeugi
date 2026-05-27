import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../theme/colors.dart';
import '../../../theme/spacing.dart';
import '../../../theme/typography.dart';

/// V1 Login Screen — DESIGN.md memorable thing 적용.
/// 차분 · 어른 도구 · 압박 X.
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key, required this.onGoogleLogin, this.onDevLogin});

  final VoidCallback onGoogleLogin;
  final VoidCallback? onDevLogin; // dev build에만 노출

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Spacer(flex: 3),
              const Text('끊기', style: AppTypography.displayLarge),
              const SizedBox(height: AppSpacing.sm),
              Text(
                '한국 1인 워커를 위한 Focus Accountant',
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const Spacer(flex: 5),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: onGoogleLogin,
                  child: const Padding(
                    padding: EdgeInsets.symmetric(vertical: AppSpacing.xs),
                    child: Text('Google로 시작'),
                  ),
                ),
              ),
              if (kDebugMode && onDevLogin != null) ...[
                const SizedBox(height: AppSpacing.sm),
                Center(
                  child: TextButton(
                    onPressed: onDevLogin,
                    child: const Text('Dev Login (debug build only)'),
                  ),
                ),
              ],
              const SizedBox(height: AppSpacing.lg),
              const Text(
                '시작하면 이용약관 · 개인정보처리방침에 동의하는 것으로 간주됩니다.',
                style: AppTypography.labelSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.md),
            ],
          ),
        ),
      ),
    );
  }
}

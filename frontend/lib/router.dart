import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'features/auth/domain/auth_state.dart';
import 'features/auth/presentation/auth_provider.dart';
import 'features/auth/presentation/login_screen.dart';
import 'features/onboarding/onboarding_flow.dart';
import 'shell.dart';

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final auth = ref.read(authProvider);
      final loc = state.matchedLocation;

      switch (auth.status) {
        case AuthStatus.unknown:
          return null; // splash 유지
        case AuthStatus.unauthenticated:
          return loc == '/login' ? null : '/login';
        case AuthStatus.authenticated:
          if (loc == '/login' || loc == '/') return '/home';
          return null;
      }
    },
    routes: [
      GoRoute(path: '/', builder: (_, __) => const _Splash()),
      GoRoute(
        path: '/login',
        builder: (context, state) {
          final notifier = ref.read(authProvider.notifier);
          return LoginScreen(
            onGoogleLogin: () {
              // W3.5: Google Sign-In은 google_sign_in package 연결 (W4)
              // 현재는 dev login으로 대체
              notifier.devLogin(email: 'me@test.com', name: 'Test User');
            },
            onDevLogin: () =>
                notifier.devLogin(email: 'dev@test.com', name: 'Dev User'),
          );
        },
      ),
      GoRoute(
        path: '/onboarding',
        builder: (context, state) => OnboardingFlow(
          onComplete: (hourlyValue, channels) async {
            // 시간당 가치 backend 반영 (/v1/me PATCH). 채널은 W4 endpoint 후 연결.
            if (hourlyValue != null) {
              await ref.read(authProvider.notifier).updateHourlyValue(hourlyValue);
            }
            if (context.mounted) context.go('/home');
          },
        ),
      ),
      GoRoute(path: '/home', builder: (_, __) => const HomeShell()),
    ],
    refreshListenable: _AuthListenable(ref),
  );
});

/// auth state 변경 시 router refresh.
class _AuthListenable extends ChangeNotifier {
  _AuthListenable(Ref ref) {
    ref.listen(authProvider, (_, __) => notifyListeners());
  }
}

class _Splash extends ConsumerStatefulWidget {
  const _Splash();

  @override
  ConsumerState<_Splash> createState() => _SplashState();
}

class _SplashState extends ConsumerState<_Splash> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(authProvider.notifier).restore();
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: CircularProgressIndicator(strokeWidth: 2)),
    );
  }
}

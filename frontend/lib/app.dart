import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'features/auth/presentation/login_screen.dart';
import 'features/home/home_screen.dart';
import 'theme/colors.dart';
import 'theme/spacing.dart';
import 'theme/theme.dart';
import 'theme/typography.dart';

class KkeugiApp extends ConsumerWidget {
  const KkeugiApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp(
      title: '끊기',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(context),
      locale: const Locale('ko', 'KR'),
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [Locale('ko', 'KR'), Locale('en', 'US')],
      home: const _RootSwitch(),
    );
  }
}

/// W3 stub — auth state 따라 LoginScreen ↔ HomeShell.
/// W3.5에서 Riverpod AuthProvider + go_router로 교체.
class _RootSwitch extends ConsumerStatefulWidget {
  const _RootSwitch();

  @override
  ConsumerState<_RootSwitch> createState() => _RootSwitchState();
}

class _RootSwitchState extends ConsumerState<_RootSwitch> {
  bool _loggedIn = false;

  @override
  Widget build(BuildContext context) {
    if (!_loggedIn) {
      return LoginScreen(
        onGoogleLogin: () => setState(() => _loggedIn = true),
        onDevLogin: () => setState(() => _loggedIn = true),
      );
    }
    return const HomeShell();
  }
}

/// Bottom tab navigation — DESIGN.md IA tree.
class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int _index = 0;

  static const _pages = <Widget>[
    HomeScreen(),
    _ArchivePlaceholder(),
    _SettingsPlaceholder(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        backgroundColor: AppColors.surface,
        indicatorColor: AppColors.accentSoft,
        destinations: const <NavigationDestination>[
          NavigationDestination(
            icon: Icon(Icons.bar_chart_outlined),
            selectedIcon: Icon(Icons.bar_chart),
            label: '홈',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_outlined),
            selectedIcon: Icon(Icons.history),
            label: '회고',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings),
            label: '설정',
          ),
        ],
      ),
    );
  }
}

class _ArchivePlaceholder extends StatelessWidget {
  const _ArchivePlaceholder();
  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: AppColors.bg,
        body: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.lg),
              child: Text(
                '첫 회고가 도착하면 여기에 모입니다.',
                textAlign: TextAlign.center,
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
            ),
          ),
        ),
      );
}

class _SettingsPlaceholder extends StatelessWidget {
  const _SettingsPlaceholder();
  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: AppColors.bg,
        body: SafeArea(
          child: Center(
            child: Text(
              '설정 (W3.5)',
              style: AppTypography.titleLarge,
            ),
          ),
        ),
      );
}

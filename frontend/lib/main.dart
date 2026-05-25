import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

import 'app.dart';
import 'core/api/env.dart';
import 'features/usage/usage_worker.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // W4 Trigger B: 8h 백그라운드 usage sync (Android만). 실패해도 앱 구동엔 무관.
  if (Platform.isAndroid) {
    try {
      await initUsageBackgroundSync();
    } catch (_) {
      // WorkManager 초기화 실패는 무시 — foreground sync가 1차 freshness 담당.
    }
  }

  if (Env.sentryDsn.isNotEmpty) {
    await SentryFlutter.init(
      (o) {
        o.dsn = Env.sentryDsn;
        o.tracesSampleRate = 0.05;
        o.environment = Env.isProduction ? 'production' : 'development';
      },
      appRunner: () => runApp(const ProviderScope(child: KkeugiApp())),
    );
  } else {
    runApp(const ProviderScope(child: KkeugiApp()));
  }
}

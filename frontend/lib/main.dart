import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

import 'app.dart';
import 'core/api/env.dart';
import 'core/notifications/local_notifications.dart';
import 'features/usage/usage_worker.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // W7: 로컬 알람(한도 초과) 플러그인 + 채널 초기화. 실패해도 앱 구동엔 무관.
  try {
    await LocalNotifications.instance.init();
  } catch (_) {
    // 알람 초기화 실패는 무시 — 통계·결제 등 핵심 흐름과 독립.
  }

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

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

import 'app.dart';
import 'core/api/env.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

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

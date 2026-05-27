import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../auth/presentation/auth_provider.dart';
import 'reports_api.dart';

final reportsApiProvider = Provider<ReportsApi>(
  (ref) => ReportsApi(ref.watch(dioProvider)),
);

final reportsListProvider = FutureProvider<List<WeeklyReportCard>>(
  (ref) => ref.watch(reportsApiProvider).list(),
);

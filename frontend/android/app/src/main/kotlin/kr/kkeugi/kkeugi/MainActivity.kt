package kr.kkeugi.kkeugi

import android.app.AppOpsManager
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Process
import android.provider.Settings
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

/**
 * UsageStatsManager 브리지 (wedge #2: 사용 시간 자동 import).
 *
 * Flutter platform channel "kr.kkeugi/usage":
 *  - hasPermission()            → Boolean (PACKAGE_USAGE_STATS 허용 여부)
 *  - openUsageAccessSettings()  → 시스템 사용 통계 접근 설정 화면 열기
 *  - queryUsageSessions(start,end) → 포그라운드 세션 리스트
 *      [{ packageName, startMs, durationMs }]
 *
 * 세션은 queryEvents의 MOVE_TO_FOREGROUND/BACKGROUND 쌍으로 재구성한다
 * (aggregate가 아닌 세션 단위 → 정확한 occurred_at + 작업시간대 판별 가능).
 */
class MainActivity : FlutterActivity() {
    private val channelName = "kr.kkeugi/usage"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            channelName,
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "hasPermission" -> result.success(hasUsagePermission())
                "openUsageAccessSettings" -> {
                    openUsageAccessSettings()
                    result.success(null)
                }
                "queryUsageSessions" -> {
                    val start = call.argument<Number>("startMs")?.toLong()
                    val end = call.argument<Number>("endMs")?.toLong()
                    if (start == null || end == null) {
                        result.error("BAD_ARGS", "startMs/endMs required", null)
                    } else {
                        try {
                            result.success(queryUsageSessions(start, end))
                        } catch (e: SecurityException) {
                            result.error("NO_PERMISSION", e.message, null)
                        }
                    }
                }
                else -> result.notImplemented()
            }
        }
    }

    private fun hasUsagePermission(): Boolean {
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
        val mode =
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                appOps.unsafeCheckOpNoThrow(
                    AppOpsManager.OPSTR_GET_USAGE_STATS,
                    Process.myUid(),
                    packageName,
                )
            } else {
                @Suppress("DEPRECATION")
                appOps.checkOpNoThrow(
                    AppOpsManager.OPSTR_GET_USAGE_STATS,
                    Process.myUid(),
                    packageName,
                )
            }
        return mode == AppOpsManager.MODE_ALLOWED
    }

    private fun openUsageAccessSettings() {
        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        startActivity(intent)
    }

    private fun queryUsageSessions(startMs: Long, endMs: Long): List<Map<String, Any>> {
        val usm = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
        val events = usm.queryEvents(startMs, endMs)
        val sessions = ArrayList<Map<String, Any>>()
        val foregroundStart = HashMap<String, Long>() // packageName → 진입 시각
        val e = UsageEvents.Event()

        while (events.hasNextEvent()) {
            events.getNextEvent(e)
            val pkg = e.packageName ?: continue
            when (e.eventType) {
                UsageEvents.Event.MOVE_TO_FOREGROUND ->
                    foregroundStart[pkg] = e.timeStamp
                UsageEvents.Event.MOVE_TO_BACKGROUND -> {
                    val s = foregroundStart.remove(pkg)
                    if (s != null && e.timeStamp > s) {
                        sessions.add(
                            mapOf(
                                "packageName" to pkg,
                                "startMs" to s,
                                "durationMs" to (e.timeStamp - s),
                            ),
                        )
                    }
                }
            }
        }
        // 쿼리 종료 시점에도 포그라운드인 앱 → 종료 시각을 endMs로 마감
        for ((pkg, s) in foregroundStart) {
            if (endMs > s) {
                sessions.add(
                    mapOf(
                        "packageName" to pkg,
                        "startMs" to s,
                        "durationMs" to (endMs - s),
                    ),
                )
            }
        }
        return sessions
    }
}

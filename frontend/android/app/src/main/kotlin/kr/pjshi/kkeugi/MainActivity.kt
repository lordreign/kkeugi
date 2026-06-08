package kr.pjshi.kkeugi

import android.app.AppOpsManager
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.drawable.Drawable
import android.os.Build
import android.os.Process
import android.provider.Settings
import android.util.Base64
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.ByteArrayOutputStream

/**
 * UsageStatsManager 브리지 (wedge #2: 사용 시간 자동 import).
 *
 * Flutter platform channel "kr.pjshi/usage":
 *  - hasPermission()            → Boolean (PACKAGE_USAGE_STATS 허용 여부)
 *  - openUsageAccessSettings()  → 시스템 사용 통계 접근 설정 화면 열기
 *  - queryUsageSessions(start,end) → 포그라운드 세션 리스트
 *      [{ packageName, startMs, durationMs }]
 *      런처에 뜨는 사용자 앱만 (시스템 UI·런처·자기 자신 등 노이즈 제외).
 *  - getAppMeta(packages) → [{ packageName, label, iconBase64 }]
 *      사람이 읽는 앱 이름·아이콘. 서버는 package_name만 보관하므로
 *      앱별 drill-down 표시 직전에 로컬에서 해석한다 (개인정보 최소).
 *
 * 세션은 queryEvents의 MOVE_TO_FOREGROUND/BACKGROUND 쌍으로 재구성한다
 * (aggregate가 아닌 세션 단위 → 정확한 occurred_at + 작업시간대 판별 가능).
 */
class MainActivity : FlutterActivity() {
    private val channelName = "kr.pjshi/usage"

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
                "getAppMeta" -> {
                    val packages = call.argument<List<String>>("packages")
                    if (packages == null) {
                        result.error("BAD_ARGS", "packages required", null)
                    } else {
                        result.success(getAppMeta(packages))
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

    /**
     * 런처에 노출되는 사용자 앱 패키지 집합. 시스템 UI·런처·IME 등
     * ACTION_MAIN/CATEGORY_LAUNCHER가 없는 패키지를 한 번에 걸러낸다.
     * 자기 자신(끊기)도 제외 — 앱을 켠 시간은 추적 대상이 아님.
     */
    private fun launchablePackages(): Set<String> {
        val intent = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        val resolved = packageManager.queryIntentActivities(intent, 0)
        val set = HashSet<String>()
        for (ri in resolved) {
            val pkg = ri.activityInfo?.packageName ?: continue
            if (pkg != packageName) set.add(pkg)
        }
        return set
    }

    private fun queryUsageSessions(startMs: Long, endMs: Long): List<Map<String, Any>> {
        val usm = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
        val userApps = launchablePackages()
        val events = usm.queryEvents(startMs, endMs)
        val sessions = ArrayList<Map<String, Any>>()
        val foregroundStart = HashMap<String, Long>() // packageName → 진입 시각
        val e = UsageEvents.Event()

        while (events.hasNextEvent()) {
            events.getNextEvent(e)
            val pkg = e.packageName ?: continue
            if (pkg !in userApps) continue // 시스템 노이즈 제외
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

    /** package_name 리스트 → 앱 이름·아이콘(PNG base64). 삭제된 앱은 label=패키지명. */
    private fun getAppMeta(packages: List<String>): List<Map<String, Any>> {
        val pm = packageManager
        val out = ArrayList<Map<String, Any>>(packages.size)
        for (pkg in packages) {
            try {
                val ai = pm.getApplicationInfo(pkg, 0)
                out.add(
                    mapOf(
                        "packageName" to pkg,
                        "label" to pm.getApplicationLabel(ai).toString(),
                        "iconBase64" to drawableToBase64(pm.getApplicationIcon(ai)),
                    ),
                )
            } catch (e: PackageManager.NameNotFoundException) {
                // 삭제됐거나 조회 불가 → 패키지명을 라벨로, 아이콘은 빈 문자열.
                out.add(
                    mapOf("packageName" to pkg, "label" to pkg, "iconBase64" to ""),
                )
            }
        }
        return out
    }

    /** drawable → 96×96 PNG → base64 (NO_WRAP). 어댑티브 아이콘 포함 렌더. */
    private fun drawableToBase64(drawable: Drawable): String {
        val size = 96
        val bitmap = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.width, canvas.height)
        drawable.draw(canvas)
        val stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
        bitmap.recycle()
        return Base64.encodeToString(stream.toByteArray(), Base64.NO_WRAP)
    }
}

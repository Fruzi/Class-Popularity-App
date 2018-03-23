package rawnsangels.bgu.application

import android.Manifest
import android.annotation.TargetApi
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import io.realm.Realm

import kotlinx.android.synthetic.main.activity_main.*
import android.net.wifi.WifiManager
import android.os.AsyncTask
import android.os.Build
import android.support.v4.app.NotificationCompat
import android.util.Log
import android.widget.Toast
import org.json.JSONArray
import org.json.JSONObject
import java.lang.ref.WeakReference
import java.net.Socket


class MainActivity : AppCompatActivity() {

    private lateinit var mRealm: Realm
    private lateinit var mWifiManager: WifiManager
    var depsCourses: Map<String, List<Course>> = mutableMapOf()

    private lateinit var mBroadcastReceiver: BroadcastReceiver

    private lateinit var mNotificationManager: NotificationManager
    private lateinit var mNotificationBuilder: NotificationCompat.Builder

    private var currentLecture = "Operating Systems"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

        mRealm = Realm.getDefaultInstance()

        // remove this
        /*mRealm.executeTransaction {
            mRealm.deleteAll()
        }*/

        mWifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager

        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M
                && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(arrayOf(Manifest.permission.ACCESS_COARSE_LOCATION),
                    PERMISSIONS_REQUEST_CODE_ACCESS_COARSE_LOCATION)
        } else {
            processWifiScan()
        }

        setupReceiver()
        setupNotification()

        // Notification test
        showNotification(currentLecture)
    }

    fun processWifiScan() {
        if (mWifiManager.isWifiEnabled) {
            if (mWifiManager.startScan()) {
                val hotspots = JSONArray()
                val scans = mWifiManager.scanResults
                Log.v(" abc ", scans.size.toString())
                scans?.let {
                    if (!scans.isEmpty()) {
                        for (scan in it) {
                            val hotspotObj = JSONObject()
                            hotspotObj.put("BSSID", scan.BSSID)
                            hotspotObj.put("SNR", scan.level.toString())
                            hotspots.put(hotspotObj)

                            //  Log.v(" BSSID ", " ${scan.BSSID}, Level: ${scan.level}")
                        }
                        Log.v(" abc ", hotspots.toString())

                        //val tempObj = JSONObject("""{"dep":"1"}""")
                       // var temp = JSONArray(JSONObject("""{"dep":"202"}"""))
                        //SocketTask(this, "132.73.195.156",8000,"course_screen",tempObj).execute()
                        CourseScreenRequestTask(this, "132.73.195.156",8000,"course_screen",JSONObject()).execute()
                    }
                }
            }
        }
    }

    private fun setupReceiver() {
        mBroadcastReceiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                val action = intent.action ?: return
                when (action) {
                    getString(R.string.action_rate_lesson) -> {
                        Toast.makeText(context, "\"Rate\" clicked", Toast.LENGTH_SHORT).show()
                    }
                    getString(R.string.action_didnt_go) -> {
                        Toast.makeText(context, "\"Didn't go\" clicked", Toast.LENGTH_SHORT).show()
                    }
                    else -> Log.v("onReceive", "error")
                }
            }
        }
        val intentFilter = IntentFilter()
        intentFilter.addAction(getString(R.string.action_rate_lesson))
        intentFilter.addAction(getString(R.string.action_didnt_go))
        registerReceiver(mBroadcastReceiver, intentFilter)
    }

    private fun setupNotification() {
        mNotificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        mNotificationBuilder = NotificationCompat.Builder(this, getString(R.string.notification_channel_id))
                .setSmallIcon(android.R.drawable.ic_dialog_alert)
                .setContentTitle(getString(R.string.notification_title))
                .setContentIntent(PendingIntent.getActivity(this, 0,
                        Intent(this, MainActivity::class.java),
                        PendingIntent.FLAG_UPDATE_CURRENT))
                .addAction(android.R.drawable.ic_notification_overlay,
                        getString(R.string.notification_title),
                        PendingIntent.getBroadcast(this, 0,
                                Intent(getString(R.string.action_rate_lesson)),
                                PendingIntent.FLAG_UPDATE_CURRENT))
                .addAction(android.R.drawable.ic_notification_overlay,
                        getString(R.string.notification_title),
                        PendingIntent.getBroadcast(this, 0,
                                Intent(getString(R.string.action_didnt_go)),
                                PendingIntent.FLAG_UPDATE_CURRENT))
                .setAutoCancel(true)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            setupNotificationChannel()
        }
        mNotificationBuilder.build()
    }

    private fun showNotification(lecture: String) {
        mNotificationBuilder.setContentText("How was $lecture?")
        mNotificationManager.notify(R.integer.notification_id, mNotificationBuilder.build())

    }

    @TargetApi(Build.VERSION_CODES.O)
    private fun setupNotificationChannel() {
        val notificationChannel = NotificationChannel(
                getString(R.string.notification_channel_id),
                getString(R.string.app_name),
                NotificationManager.IMPORTANCE_LOW)
        notificationChannel.enableVibration(false)
        notificationChannel.enableLights(false)
        mNotificationManager.createNotificationChannel(notificationChannel)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>,
                                            grantResults: IntArray) {
        if (requestCode == PERMISSIONS_REQUEST_CODE_ACCESS_COARSE_LOCATION
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            // Do something with granted permission
            processWifiScan()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(mBroadcastReceiver)
        mNotificationManager.cancelAll()
        mRealm.close()
    }

    class CourseScreenRequestTask(activity: MainActivity,
                                  val ip: String,
                                  val port: Int,
                                  val funcName: String,
                                  val jsonObject: JSONObject)
        : AsyncTask<Void, Void, String?>() {

        val activityRef: WeakReference<MainActivity> = WeakReference(activity)

        override fun doInBackground(vararg params: Void?): String? {
            return try {
                val req =  "POST /$funcName HTTP/1.1\r\nContent-Length: ${jsonObject.toString().length}\r\n\r\n$jsonObject\r\n\r\n"
                val socket =  Socket(ip, port)
                Log.v("SocketTask", "Sending $req")
                socket.getOutputStream().write(req.toByteArray())
                socket.shutdownOutput()
                val bufferedReader = socket.getInputStream().bufferedReader()
                bufferedReader.use {
                    it.readLine() // HTTP/1.1 200 OK
                    val contentLength = it.readLine() // Content-Length: 13035
                    var toRead = Integer.parseInt(contentLength.filter { it.isDigit() })
                    it.readLine() // Empty line
                    val stringBuilder = StringBuilder()
                    while (toRead > 0) {
                        stringBuilder.append(it.read().toChar())
                        toRead--
                    }
                    stringBuilder.toString()
                }
            } catch (e: Exception) {
                null
            }
        }

        override fun onPostExecute(result: String?) {
            val activity = activityRef.get()!!
            if (result == null) {
                Log.e("SocketTask", "Connection failed")
                activity.finish()
            }
            val depsCourses = JSONArray(result)
            val depsJson = depsCourses.get(0) as JSONArray // [department_id: Int, department_num: Int, department_name: String]
            val coursesJson = depsCourses.get(1) as JSONArray // [course_id: Int, course_number: String, name: String,  department_id: Int]

            var depMap: Map<Int, String> = mapOf()

            for (i in 0 until depsJson.length()) {
                val dep = depsJson.get(i) as JSONArray
                val depId = dep.get(0) as Int
                val depNum = dep.get(1) as Int
                val depName = dep.get(2).toString()
                depMap += depId to "$depNum $depName"
            }

            for (i in 0 until coursesJson.length()) {
                val course = coursesJson.get(i) as JSONArray
                val courseId = course.get(0) as Int
                val courseNumber = course.get(1).toString()
                val name = course.get(2).toString()
                val depId = course.get(3) as Int
                val courseObj = Course(courseId, courseNumber, name, depId)
                val tempCourseList = activity.depsCourses[depMap[depId]!!] ?: listOf()
                activity.depsCourses += depMap[depId]!! to tempCourseList + courseObj
            }
        }
    }

    companion object {
        const val PERMISSIONS_REQUEST_CODE_ACCESS_COARSE_LOCATION = 222
    }
}

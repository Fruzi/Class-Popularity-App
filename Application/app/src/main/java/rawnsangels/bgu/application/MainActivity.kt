package rawnsangels.bgu.application

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import io.realm.Realm

import kotlinx.android.synthetic.main.activity_main.*
import android.net.wifi.WifiManager
import android.os.AsyncTask
import android.os.Build
import android.util.Log
import org.json.JSONArray
import org.json.JSONObject
import java.net.Socket


class MainActivity : AppCompatActivity() {

    private lateinit var realm: Realm
    private lateinit var mWifiManager: WifiManager
    var depsCourses: Map<String, List<String>> = mapOf()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

        realm = Realm.getDefaultInstance()

        // remove this
        realm.executeTransaction {
            realm.deleteAll()
        }

        depsCourses = mapOf(
                "201 Mathematics" to listOf("20114312 Algebra"),
                "202 Computer Science" to listOf("20213521 Operating Systems",
                                               "20218745 Intro to CS")
        )

        mWifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager

        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M
                && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(arrayOf(Manifest.permission.ACCESS_COARSE_LOCATION),
                    PERMISSIONS_REQUEST_CODE_ACCESS_COARSE_LOCATION)
            //After this point you wait for callback in onRequestPermissionsResult(int, String[], int[]) overriden method
        } else {
            processWifiScan()
            //do something, permission was previously granted; or legacy device
        }
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

                        val tempObj = JSONObject("""{"dep":"1"}""")
                       // var temp = JSONArray(JSONObject("""{"dep":"202"}"""))
                        SocketTask("132.73.195.156",8000,"fetch_courses",tempObj).execute()
                    }
                }
            }
        }
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
        realm.close()
    }

    class SocketTask(val ip: String, val port: Int, val funcName: String, val jsonObject: JSONObject)
        : AsyncTask<Void, Void, String?>() {

        override fun doInBackground(vararg params: Void?): String? {
            val req =  "POST /$funcName HTTP/1.1\r\nContent-Length: ${jsonObject.toString().length}\r\n\r\n$jsonObject\r\n\r\n"
            var socket =  Socket(ip, port)
            Log.v("SocketTask", "Sending $req")
            socket.getOutputStream().write(req.toByteArray())
            socket.shutdownOutput()
            val data = socket.getInputStream().bufferedReader().use {
                it.readText()
            }
            return data
        }

        override fun onPostExecute(result: String?) {
            Log.v("SocketTask", "Response: $result")
        }
    }

    companion object {
        const val PERMISSIONS_REQUEST_CODE_ACCESS_COARSE_LOCATION = 222
    }
}

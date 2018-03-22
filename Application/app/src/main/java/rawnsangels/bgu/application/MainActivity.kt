package rawnsangels.bgu.application

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import io.realm.Realm

import kotlinx.android.synthetic.main.activity_main.*
import android.net.wifi.WifiManager
import android.os.Build
import android.util.Log
import org.json.JSONArray
import org.json.JSONObject


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

                        val tempArr = JSONArray()
                        tempArr.put(JSONObject("""{"dep":"202"}"""))
                       // var temp = JSONArray(JSONObject("""{"dep":"202"}"""))
                        request("132.73.222.44",8000,"fetch_courses",tempArr)
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

    fun request (ip :String,port :Int ,funcName:String,jsonArray: JSONArray )
    {
        val req =  "POST /$funcName HTTP1.1\r\nContent-Length: ${jsonArray.toString().length}\r\n\r\n$jsonArray\r\n\r\n"
        var socket =  Socket(ip, port)
        socket.getOutputStream().write(req.toByteArray())
        val data = socket.getInputStream().bufferedReader().use { it.readText() }
        Log.v("Response:\n", data)
    }

    companion object {
        const val PERMISSIONS_REQUEST_CODE_ACCESS_COARSE_LOCATION = 222
    }
}

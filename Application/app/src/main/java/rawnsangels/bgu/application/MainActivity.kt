package rawnsangels.bgu.application

import android.content.Context
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import io.realm.Realm

import kotlinx.android.synthetic.main.activity_main.*
import android.net.wifi.WifiManager
import android.util.Log
import org.json.JSONArray
import org.json.JSONObject


class MainActivity : AppCompatActivity() {

    private lateinit var realm: Realm
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

        val wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        if (wifiManager.isWifiEnabled) {
            if (wifiManager.startScan()) {
                val hotspots = JSONArray()
                val scans = wifiManager.scanResults
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
                    }
                }
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        realm.close()
    }
}

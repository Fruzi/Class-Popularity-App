#!/usr/bin/python
import db
import sendssl
import json

sendssl.insert_to_db(limit=1)

user_id = db.add_user("11:11:11:11:11", "uzi")
db.register_to_course(user_id, 1)
db.register_to_course(user_id, 6)
db.register_to_course(user_id, 8)
db.add_antenna(user_id, json.dumps([{"bssid": "aa:aa:aa", "snr": -50},
                                    {"bssid": "bb:bb:bb", "snr": -30},
                                    {"bssid": "cc:cc:cc", "snr": -30}]))

user_id = db.add_user("22:22:22:22:22", "amit")
db.register_to_course(user_id, 2)
db.register_to_course(user_id, 5)
db.register_to_course(user_id, 8)
db.add_antenna(user_id, json.dumps([{"bssid": "aa:aa:aa", "snr": -50},
                                    {"bssid": "bb:bb:bb", "snr": -30},
                                    {"bssid": "cc:cc:cc", "snr": -30}]))

user_id = db.add_user("33:33:33:33:33", "ron")
db.register_to_course(user_id, 1)
db.register_to_course(user_id, 5)
db.register_to_course(user_id, 8)
db.add_antenna(user_id, json.dumps([{"bssid": "aa:aa:aa", "snr": -50},
                                    {"bssid": "bb:bb:bb", "snr": -30},
                                    {"bssid": "dd:dd:dd", "snr": -30}]))

user_id = db.add_user("44:44:44:44:44", "oz")
db.register_to_course(user_id, 1)
db.register_to_course(user_id, 5)
db.register_to_course(user_id, 8)
db.add_antenna(user_id, json.dumps([{"bssid": "aa:aa:aa", "snr": -50},
                                    {"bssid": "cc:cc:cc", "snr": -30}]))
#!/usr/bin/python
import db
import sendssl

sendssl.insert_to_db(limit=2)

user_id = db.add_user("11:11:11:11:11", "uzi")
db.register_to_course(user_id, 1)
db.register_to_course(user_id, 6)
db.register_to_course(user_id, 8)
db.add_antenna(user_id, )

user_id = db.add_user("22:22:22:22:22", "amit")
db.register_to_course(user_id, 2)
db.register_to_course(user_id, 5)
db.register_to_course(user_id, 8)

user_id = db.add_user("33:33:33:33:33", "ron")
db.register_to_course(user_id, 1)
db.register_to_course(user_id, 5)
db.register_to_course(user_id, 8)

user_id = db.add_user("44:44:44:44:44", "oz")
db.register_to_course(user_id, 1)
db.register_to_course(user_id, 5)
db.register_to_course(user_id, 8)

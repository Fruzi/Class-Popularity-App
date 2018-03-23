import sqlite3
import os
import datetime
import time
import json


def main():
   jobj1 = [{"bssid" : "uirh34hui", "snr" : 6} , {"bssid" : "47gih4", "snr" : 33}]
   print jobj1
   print json.dumps(jobj1)
    

def create_db():
    db_existed = os.path.isfile('example.db')
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        if not db_existed:
            cursor.execute("""CREATE TABLE Departments (
                            department_id INTEGER PRIMARY KEY NOT NULL,
                            department_num INTEGER NOT NULL,
                            department_name TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE Courses (
                            course_id INTEGER PRIMARY KEY NOT NULL,
                            course_number TEXT NOT NULL,
                            name TEXT NOT NULL,
                            department_id INTEGER NOT NULL REFERENCES  Departments(department_id))""")
            cursor.execute("""CREATE TABLE Lectures (
                            lecture_id INTEGER PRIMARY KEY NOT NULL,
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id),
                            day INTEGER NOT NULL,
                            start_time INTEGER,
                            end_time INTEGER,
                            location TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE Users(
                            user_id INTEGER PRIMARY KEY NOT NULL,
                            mac TEXT NOT NULL,
                            name TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE Ratings(
                            rating_id INTEGER PRIMARY KEY NOT NULL,
                            rating INTEGER,
                            user_id INTEGER NOT NULL REFERENCES Users(user_id),
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id),
                            lecture_id INTEGER NOT NULL REFERENCES  Lectures(lecture_id),
                            rate_date INTEGER)""")
            cursor.execute("""CREATE TABLE Users_In_Courses(
                            user_id INTEGER NOT NULL REFERENCES Users(user_id),
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id))""")
            cursor.execute("""CREATE TABLE Users_Near_Antennas(
                            user_id INTEGER NOT NULL REFERENCES Users(user_id),
                            bssid TEXT NOT NULL,
                            signal INTEGER NOT NULL,
                            time_stamp INTEGER NOT NULL)""")


def add_antenna(_user_id, _antenna_data):
    curr_time = int(time.time())
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""DELETE FROM Users_Near_Antennas WHERE (user_id)=(?)""", (_user_id,))
        data = json.loads(_antenna_data)
        for antenna in data:
            _bssid = antenna["bssid"]
            _signal = antenna["snr"]
            cursor.execute("""INSERT INTO Users_Near_Antennas (user_id, bssid, signal, time_stamp) VALUES(?, ?, ?, ?)""", (_user_id, _bssid, _signal, curr_time))
    return cursor.lastrowid


def fetch_users_near_antena(_bssid, _max_time, _min_signal):
    # This function expectes _max_time in minutes
    _max_time = _max_time * 60
    _max_time += int(time.time())
    
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT user_id FROM Users_Near_Antennas WHERE bssid = (?) AND
                          time_stamp <= ? AND signal >= ?""",
                       (_bssid, _max_time, _min_signal))
        return map(lambda x: x[0], cursor.fetchall())

        
def fetch_bsids_near_user(_user_id, _max_time, _min_signal):
    # This function expectes _max_time in minutes
    _max_time = _max_time * 60
    _max_time += int(time.time())

    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT bssid FROM Users_Near_Antennas WHERE user_id = ? AND
                          time_stamp <= ? AND signal >= ?""",
                       (_user_id, _max_time, _min_signal))
        return map(lambda x: x[0], cursor.fetchall())

def nearby_users(user_id, _max_time, _min_siganl):
    bssid_list = fetch_bsids_near_user(user_id, _max_time, _min_siganl)
    
    users = list()
    
    for bssid in bssid_list:
        users += fetch_users_near_antena(bssid, _max_time, _min_siganl)

    return list(set(users))


def add_department(_num, _name):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Departments (department_num, department_name) VALUES(?, ?)""",
                       (_num, _name))
        return cursor.lastrowid


def add_course(_num, _name, _dep):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Courses (course_number, name, department_id) VALUES (?,?,?)""",
                       (_num, _name, _dep))
        return cursor.lastrowid


def add_lecture(_course_id, _day, _start_time, _end_time, _location):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Lectures (course_id, day, start_time,
                          end_time, location) VALUES (?, ?, ?, ?, ?)""",
                       (_course_id, _day, _start_time, _end_time, _location))
        return cursor.lastrowid


def fetch_departments():
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Departments""")
        return cursor.fetchall()


def fetch_courses(dep=None):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        if dep:
            cursor.execute("""SELECT * FROM Courses WHERE department_id = (?)""", (dep,))
        else:
            cursor.execute("""SELECT * FROM Courses""")
        return cursor.fetchall()


def fetch_lectures(_course=None):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Lectures WHERE course_id = (?)""", (_course,))
        return cursor.fetchall()


def fetch_lecture_rating(_lecture):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Rating WHERE lecture_id = (?)""", (_lecture,))
        return cursor.fetchall()


def add_user(_mac, _name):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Users (mac, name)VALUES (?, ?)""",
                       (_mac, _name))
        return cursor.lastrowid


def add_rating(_rating, _user_id, _course_id, _lecture_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Ratings (rating, user_id, course_id, lecture_id, rate_date)
                          VALUES (?, ?, ?, ? ,?)""", (_rating, _user_id, _course_id, _lecture_id, int(time.time())))


def fetch_users():
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Users""")
        return cursor.fetchall()


def get_courses_of_user(_user_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT course_id FROM Users_In_Courses WHERE user_id=(?)""", (_user_id, ))
        return cursor.fetchall()


def get_users_of_course(_course_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT user_id FROM Users_In_Courses WHERE course_id = (?)""", (_course_id,))
        return cursor.fetchall()
        

def register_to_course(_user_id, _course_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Users_In_Courses (course_id, user_id) VALUES (?, ?)""", (_course_id, _user_id))


def fetch_user_rating(_user):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Rating WHERE user_id = (?)""", (_user,))
        return cursor.fetchall()


def get_lecture_dates(lecture):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT lecture_date FROM Ratings WHERE lecture_id = (?)""", (lecture,))
        return list(set(cursor.fetchall()))


def get_avg_density(lecture):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        dates = get_lecture_dates(lecture)
        total_density = 0
        for date in dates:
            cursor.execute("""SELECT * FROM Ratings WHERE lecture_date = (?)""", (date[0],))
            date_density = len(cursor.fetchall())
            total_density += date_density
        return float(total_density)/len(dates)


def get_avg_rating(lecture):
    ratings = fetch_lecture_rating(lecture)
    num = 0
    score = 0
    for i in ratings:
        if i[1]:
            num += 1
            score += i[1]
    return float(score)/num


def times_attended_this_week(lecture, user):
    result = 0
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT lecture_date FROM Ratings WHERE user_id=(?) AND lecture_id=(?)""", (user, lecture))
        dates = cursor.fetchall()
        for d in dates:
            datetime_object = time.strptime(d[0], '%b %d %Y')
            now = datetime.datetime.now().isocalendar()[1]
            if datetime_object.isocalender()[1] == now:
                result += 1
        return result
        
        
def fetch_lectures_by_user_and_time(_user, _time):
    result = 0
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT l.lecture_id, l.course_id as course_id, day, location, c.name
                          FROM Lectures as l
                            JOIN Users_In_Courses as uic ON uic.course_id = l.course_id
                            JOIN Courses as c ON uic.course_id = c.course_id
                          WHERE uic.user_id=?
                            AND l.start_time <= ? AND ? <= l.end_time""", (_user, _time, _time))
        return list(cursor.fetchall())


def course_screen():
    return fetch_departments(), fetch_courses()


def lectures_screen(_course):
    lectures = fetch_lectures(_course)
    result = list()
    for l in lectures:
        rating = get_avg_rating(l[0])
        density = get_avg_density(l[0])
        result.append((l, rating, density))
    return result


def enrich(ids, full):
    def get_lec_by_id(id):
        for lec in full:
            if lec[0] == id:
                return lec

    result = []
    
    for id in ids:
        result.append(get_lec_by_id(id))

    return result


def get_possible_lecture(user_id):
    now = datetime.datetime.now()
    now = now.hour * 60 + now.minute
    
    #print "REMOVEEEEEEEEEEEEEE"
    #now = 13 * 60 + 30

    near_users = nearby_users(user_id, 10, -40)

    my_lectures_full = set(fetch_lectures_by_user_and_time(user_id, now))
    
    my_lectures = my_lectures_full
    my_lectures = set([lecture_id for lecture_id, course_id, day, location, course_name in my_lectures])
    counter = dict()
    

    for near_user_id in near_users:
        lectures = fetch_lectures_by_user_and_time(user_id, now)
        lectures = set([lecture_id for lecture_id, course_id, day, location, course_name in lectures])

        for lecture_id in my_lectures:
            if lecture_id in lectures:
                if lecture_id not in counter.keys():
                    counter[lecture_id] = 0

                counter[lecture_id] += 1

    ids = sorted(counter.iteritems(), key=lambda (k,v): (v,k), reverse=True)
    
    # At least two students near by
    ids = filter(lambda x: x[1] >= 2, ids)
    
    ids = [lecture_id for lecture_id, count in ids]
    
    return enrich(ids, my_lectures_full)

if __name__ == '__main__':
    main()


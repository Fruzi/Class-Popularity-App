import sqlite3
import os
import datetime
import time


def main():
    create_db()
    print times_attended_this_week(1, 1)


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
                            class_id INTEGER PRIMARY KEY NOT NULL,
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id),
                            day INTEGER NOT NULL,
                            start_time INTEGER,
                            end_time INTEGER,
                            location TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE Users(
                            user_id INTEGER PRIMARY KEY NOT NULL,
                            mac TEXT NOT NULL,
                            name TEXT NOT NULL,
                            last_antenna_data TEXT)""")
            cursor.execute("""CREATE TABLE Ratings(
                            rating_id INTEGER PRIMARY KEY NOT NULL,
                            rating INTEGER,
                            user_id INTEGER NOT NULL REFERENCES Users(user_id),
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id),
                            class_id INTEGER NOT NULL REFERENCES  Lectures(class_id),
                            date TEXT)""")
            cursor.execute("""CREATE TABLE Users_In_Courses(
                            user_id INTEGER NOT NULL REFERENCES Users(user_id),
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id))""")


def add_department(_num, _name):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Departments (department_num, department_name) VALUES(?, ?)""",
                       (_num, _name))
        cursor.execute("""SELECT * FROM Departments WHERE department_name=(?) AND department_num=(?)""", (_name, _num))
        ret = cursor.fetchall()
        if (ret):
            return ret[0]
        return -1


def add_course(_num, _name, _dep):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Courses (course_number, name, department_id) VALUES (?,?,?)""",
                       (_num, _name, _dep))
        cursor.execute("""SELECT * FROM Courses WHERE course_number=(?) AND
                          name=(?) AND department_id=(?)""", (_num, _name, _dep))
        ret = cursor.fetchall()
        if (ret):
            return ret[0]
        return -1


def add_lecture(_course_id, _day, _start_time, _end_time, _location):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Lectures (course_id, day, start_time,
                          end_time, room, building) VALUES (?, ?, ?, ?, ?)""",
                       (_course_id, _day, _start_time, _end_time, _location))
        cursor.execute(
            """SELECT * FROM Lectures WHERE course_id =(?) AND day = (?) AND start_time =(?) AND location=(?) """,
            (_course_id, _day, _start_time, _location))
        ret = cursor.fetchall()
        if ret:
            return ret[0]
        return -1


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


def fetch_lectures(_course):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Lectures WHERE course_id = (?)""", (_course,))
        return cursor.fetchall()


def fetch_lecture_rating(_lecture):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Rating WHERE class_id = (?)""", (_lecture,))
        return cursor.fetchall()


def add_user(_mac, _name, _last_antenna_data):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Users (mac, name, last_antenna_data)VALUES (?, ?, ?)""",
                       (_mac, _name, _last_antenna_data))
        cursor.execute("""SELECT * FROM Users WHERE mac = (?)""", (_mac,))
        ret = cursor.fetchall()
        if ret:
            return ret[0]
        return -1


def update_last_antena_data(data, _user_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""UPDATE Users SET last_antenna_data = (?) WHERE user_id = (?)""",
                       (data, _user_id))


def add_rating(_rating, _user_id, _course_id, _class_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Ratings (rating, user_id, course_id, class_id, date)
                          VALUES (?, ?, ?, ? ,CURRENT_DATE)""", (_rating, _user_id, _course_id, _class_id))


def add_rating_test(_user_id, _course_id, _lecture_id, _rating, date):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Ratings (rating, user_id, course_id, lecture_id, lecture_date)
                          VALUES (?, ?, ?, ? ,?)""", (_rating, _user_id, _course_id, _lecture_id, date))


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


if __name__ == '__main__':
    main()


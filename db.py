import sqlite3
import os


def main():
    create_db()
    add_user("Amit", "other fake data")
    update_last_antena_data("new fake data", 1)
    print globals()


def create_db():
    db_existed = os.path.isfile('example.db')
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        if not db_existed:
            cursor.execute("""CREATE TABLE Departments (
                            department_id INTEGER PRIMARY KEY NOT NULL,
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
                            room INTEGER NOT NULL,
                            building INTEGER NOT NULL)""")
            cursor.execute("""CREATE TABLE Users(
                            user_id INTEGER PRIMARY KEY NOT NULL,
                            name TEXT NOT NULL,
                            last_antenna_data TEXT)""")
            cursor.execute("""CREATE TABLE Ratings(
                            rating_id INTEGER PRIMARY KEY NOT NULL,
                            rating INTEGER,
                            user_id INTEGER NOT NULL REFERENCES Users(user_id),
                            course_id INTEGER NOT NULL REFERENCES Courses(course_id),
                            class_id INTEGER NOT NULL REFERENCES  Lectures(class_id),
                            date TEXT)""")


def fetch_departments():
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Departments""")
        return cursor.fetchall()


def fetch_courses(dep=None):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        if dep:
            cursor.execute("""SELECT * FROM Courses WHERE department_id = (?)""", dep)
        else:
            cursor.execute("""SELECT * FROM Courses""")
        return cursor.fetchall()


def fetch_lectures(_course):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Lectures WHERE course_id = (?)""", _course)
        return cursor.fetchall()


def fetch_lecture_rating(_lecture):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Rating WHERE class_id = (?)""", _lecture)
        return cursor.fetchall()


def fetch_users():
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Users""")
        return cursor.fetchall()


def fetch_user_rating(_user):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""SELECT * FROM Rating WHERE user_id = (?)""", _user)
        return cursor.fetchall()


def add_department(_name):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Departments (name) VALUES (?)""", _name)


def add_course(_num, _name, _dep):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Courses (course_number, name, department) VALUES (?,?,?)""",
                       (_num, _name, _dep))


def add_lecture(_course_id, _day, _start_time, _end_time, _room, _building):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Lectures (course_id, day, start_time,
                          end_time, room, building) VALUES (?, ?, ?, ?, ?, ?)""",
                       (_course_id, _day, _start_time, _end_time, _room, _building))


def add_user(_name, _last_antenna_data):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Users (name, last_antenna_data)VALUES (?, ?)""",
                       (_name, _last_antenna_data))


def update_last_antena_data(data, _user_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""UPDATE Users SET last_antenna_data = (?) WHERE user_id = (?)""",
                       (data, _user_id))


def add_rating(_rating, _user_id, _course_id, _class_id):
    with sqlite3.connect('example.db') as dbcon:
        cursor = dbcon.cursor()
        cursor.execute("""INSERT INTO Ratings (rating, user_id, course_id, class_id, date)
                          VALUES (?, ?, ?, ? ,now())""", (_rating, _user_id, _course_id, _class_id))

if __name__ == '__main__':
    main()


#!/usr/bin/python
import socket, ssl, select, sys, re
from xml.dom import minidom

HOST = "bgu4u.bgu.ac.il"
PORT = 443

def https(req, host=HOST, port=PORT):
    ssl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(ssl_sock)
    ssl_sock.connect((host, port))
    ssl_sock.sendall(req)
    
    data = ssl_sock.recv(4096)
    headers, data = data.split("\r\n\r\n")
    
    data_len = int(headers.split("Content-Length:")[1].split("\n")[0].strip())
    
    while len(data) < data_len:
        tmp = ssl_sock.recv(4096)
        if not tmp:
            break
        
        data += tmp
    
    ssl_sock.close()
    return data.decode("cp1255").encode("utf8")

def course_list_raw(departemnt):
    data = """rc_rowid=&lang=he&st=s&step=2&oc_course_name=&on_course_ins=0&on_course_ins_list=0&on_course_department={departemnt}&on_course_department_list={departemnt}&on_course_degree_level=&on_course_degree_level_list=&on_course=&on_semester=&on_year=0&on_hours=&on_credit_points=&oc_lecturer_first_name=&oc_lecturer_last_name=&on_common=&oc_end_time=&oc_start_time=&on_campus=""".format(departemnt=departemnt)
    
    return https("""POST /pls/scwp/!app.ann HTTP/1.1
Host: bgu4u.bgu.ac.il
Connection: keep-alive
Content-Length: {contentlen}
Cache-Control: max-age=0
Origin: https://bgu4u.bgu.ac.il
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://bgu4u.bgu.ac.il/pls/scwp/!app.ann
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,he;q=0.8

{data}

""".format(contentlen=len(data), data=data))

def course_details_raw(course_num, departemnt, year, semester, degree_level):
    data = """rc_rowid=&lang=he&st=s&step=3&rn_course={course_num}&rn_course_details=&rn_course_department={departemnt}&rn_course_degree_level={degree_level}&rn_course_ins=0&rn_year={year}&rn_semester={semester}&oc_course_name=&oc_end_time=&oc_lecturer_first_name=&oc_lecturer_last_name=&oc_start_time=&on_campus=&on_common=&on_course=&on_course_degree_level=&on_course_degree_level_list=&on_course_department={departemnt}&on_course_department_list={departemnt}&on_course_ins=0&on_course_ins_list=0&on_credit_points=&on_hours=&on_semester=&on_year=0""".format(course_num=course_num, departemnt=departemnt, year=year, semester=semester, degree_level=degree_level)
    
    return https("""POST /pls/scwp/!app.ann HTTP/1.1
Host: bgu4u.bgu.ac.il
Connection: keep-alive
Content-Length: {contentlen}
Cache-Control: max-age=0
Origin: https://bgu4u.bgu.ac.il
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://bgu4u.bgu.ac.il/pls/scwp/!app.ann
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,he;q=0.8

{data}

""".format(contentlen=len(data), data=data))

def departemnt_list_raw():
    data = """rc_rowid=&lang=he&st=s&step=1"""

    return https("""POST /pls/scwp/!app.ann HTTP/1.1
Host: bgu4u.bgu.ac.il
Connection: keep-alive
Content-Length: {contentlen}
Cache-Control: max-age=0
Origin: https://bgu4u.bgu.ac.il
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://bgu4u.bgu.ac.il/pls/scwp/!app.ann?lang=he
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,he;q=0.8

{data}


""".format(contentlen=len(data), data=data))

def course_list(departemnt):
    html = course_list_raw(departemnt)
    
    courses = []
    
    for m in re.finditer("javascript:goCourseSemester\('([^']+)','([^']+)','([^']+)','([^']+)','([^']+)'\)", html):
        departemnt, degree_level, course_num, year, semester = m.groups()
        
        course = dict(zip(("departemnt", "degree_level", "course_num", "year", "semester"), m.groups()))
        course["course_num"] = course["course_num"].rjust(4, "0")
        
        courses.append(course)

    return courses

def course_details(course_num, departemnt, year, semester, degree_level):
    html = course_details_raw(course_num, departemnt, year, semester, degree_level)
    
    def get_course_info(info):
        for m in re.finditer("""<li>.+?<p class="key">(.+?)</p>.+?<p class="val">(.+?)</p>.+?</li>""", html, re.DOTALL):
            k, v = m.groups()
            
            #print k, v, m.groups()
            
            if info == k:
                return v

    def get_course_name():
        return get_course_info('\xf9\xed \xe4\xf7\xe5\xf8\xf1:')
    
    def get_course_lectures():
        if "dataTable_header" not in html:
            return dict()
    
        lecture = html.split("dataTable_header")[1]
    
        for m in re.finditer("""<tr.+?>.+?<td.+?>(.+?)</td>.+?<td.+?>(.+?)</td>.+?<td.+?>(.+?)</td>.+?<td.+?>(.+?)</td>.+?<td.+?>(.+?)</td>.+?</tr>""", lecture, re.DOTALL):
            return dict(zip(("group_num", "group_type", "lecturer", "time", "place"), m.groups()))

    return get_course_lectures()

    
    courses = []
    
    for m in list(re.finditer("javascript:goCourseSemester\('([^']+)','([^']+)','([^']+)','([^']+)','([^']+)'\)", html)):
        departemnt, degree_level, course_num, year, semester = m.groups()
        
        course = dict(zip(("departemnt", "degree_level", "course_num", "year", "semester"), m.groups()))
        course["course_num"] = course["course_num"].rjust(4, "0")
        
        courses.append(course)

    return courses

def departemnt_list():
    html = departemnt_list_raw().split("""<OPTION SELECTED value="">""")[1]
    
    departemnts = []
    
    for line in html.splitlines():
        if not line.startswith("<OPTION"):
            continue
        
        x = line.split(">")[1].split("-")
        d = dict(zip(("departemnt_num", "departemnt_name"), x))
        
        d["departemnt_num"] = d["departemnt_num"].strip()
        d["departemnt_name"] = d["departemnt_name"].strip()
        departemnts.append(d)
    
    return departemnts

def departemnt_courses(departemnt):
    courses = list()
    
    for c in course_list(departemnt):
        courses.append(course_details(course_num=int(c["course_num"]), departemnt=int(c["departemnt"]), year=int(c["year"]), semester=int(c["semester"]), degree_level=int(c["degree_level"])))
    
    return courses

def insert_to_db(limit=2):
    import db
    db.create_db()

    for departemnt in departemnt_list()[:limit]:
        #print departemnt["departemnt_name"]
        #return
        db.add_department(departemnt["departemnt_name"].decode("utf8"))
        return
    
    for departemnt in departemnt_list()[:limit]:
        for course in departemnt_courses(int(departemnt["departemnt_num"])):
            db.add_course(_num="myname",
                          _name="",
                          _dep="")

insert_to_db()
    
#print departemnt_courses(1)
#print departemnt_courses(2)
#print departemnt_courses(3)
#print departemnt_courses(201)
#print departemnt_courses(202)


#print course_details(course_num=1011, departemnt=202, year=2018, semester=2, degree_level=1)
#print course_list(201)
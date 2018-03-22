#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import json
import  db

PORT = 8000

def edit_answer(self, result):
    if result == 1:
        print "add succeeded"
    if result == -1:
        print "add failed"
    data = json.dumps(result)
    print "result from db: " + data
    str = "HTTP/1.1 200 OK\r\nContent-Length: {contentlen}\r\n\r\n{data}".format(contentlen=len(data), data=data)
    print str
    self.wfile.write(str)
    
class MyHttpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        #IPython.embed()
        print self.path.format
        
    def do_POST(self):
        jsonobj = self.rfile.read().strip()

        kwargs = json.loads(jsonobj)
        func_name = self.path.format().strip('/')
        print func_name
        #IPython.embed()
        if func_name in dir(db):
            f = getattr(db, func_name)
            result = f(**kwargs)
            edit_answer(self, result)
        else:
            print "ERROR: no such function"
            
Handler = MyHttpHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
db.create_db()
httpd.serve_forever()


#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import json
import IPython

PORT = 8000
#global GetStudents

def GetStudents(self, *args):			
			print "in GetStudents"
			#print args
			self.wfile.write(json.dumps(args))
			self.wfile.write("\n")
			#IPython.embed()
			

class MyHttpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

	def do_GET(self):
		#IPython.embed()
		print self.path.format
		
	def do_POST(self):
		import IPython
		import json
		jsonobj = self.rfile.read().strip()
		kwargs = json.loads(jsonobj)
		func_name = self.path.format().strip('/')
		if func_name in globals():
			f = globals()[func_name]
			f(self, *kwargs)
		else:
			print "ERROR: no such function"
			
		

Handler = MyHttpHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()


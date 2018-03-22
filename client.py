#!/usr/bin/python
import socket
import sys
import json

def request(ip, port, func_name, **kwargs):
    req = json.dumps(kwargs)

    s = socket.socket()
    s.connect((ip, port))
    s.sendall("POST /{func_name} HTTP/1.1\r\nContent-Length: {contentlen}\r\n\r\n{req}\r\n\r\n".format(
        func_name=func_name,
        contentlen=len(req),
        req=req))

    s.shutdown(socket.SHUT_WR)
    data = s.recv(4096)
    
    headers, data = data.split("\r\n\r\n")
    
    data_len = int(headers.split("Content-Length:")[1].split("\n")[0].strip())
    
    while len(data) < data_len:
        tmp = s.recv(4096)
        if not tmp:
            break
        
        data += tmp
    
    s.close()
    return data

kwargs = dict(zip(sys.argv[2::2], sys.argv[3::2]))
print json.loads(request("localhost", 8000, sys.argv[1], **kwargs))

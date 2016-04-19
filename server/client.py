#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, select, string, sys, json, base64, threading, httplib2

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

class FileDownload(threading.Thread):
    def __init__(self, host, webport, link, callback):
        threading.Thread.__init__(self)
        self.link = 'http://%s:%d%s' % (host, webport, link)
        self.callback = callback

    def run(self):
        h = httplib2.Http(timeout = 1)
        (resp_headers, content) = h.request(self.link, "GET")
        self.callback(resp_headers, content)

def downloadend(resp_headers, content):
    #with open("./test", "wb") as f:
    #    f.write(content)
    s.send(json.dumps(dict(
        action = 0, # user type
        behave = 'file_program',
        size = len(content)
    )) + separator)

if len(sys.argv) < 3:
    print 'Usage : python ', __file__,' hostname port'
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
device_id = 'test'
auth_key = '8f5aff8cb424d2cf39b206619f8d1461'
separator = '\0'

if len(sys.argv) > 4:
    device_id = sys.argv[3]
    auth_key = sys.argv[4]

if len(sys.argv) > 5:
    separator = sys.argv[5]

filelink = None
webport = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to remote host
try :
    s.connect((host, port))
    s.setblocking(0)
except :
    print 'Unable to connect'
    sys.exit()


print 'Connected to remote host. Start sending messages'
print "Input 'auth', 'keyup code', 'keydown code', 'switch id' to send default message"
print "Or you can send message directly."
prompt()

exit = False

while not exit:
    rlist = [sys.stdin, s]

    # Get the list sockets which are readable
    read_list, write_list, error_list = select.select(rlist , [], [])


    for sock in read_list:
        #incoming message from remote server
        if sock == s:
            data = sock.recv(4096)
            if not data :
                print '\nDisconnected from chat server'
                sys.exit()
            else :
                #print datan
                remain = ''
                datalist = data.split(separator)[:-1]
                for data in datalist:
                    data = remain + data
                    print '\n Server: ',
                    try:
                        data = json.loads(data)
                        remain = ''
                    except ValueError, e:
                        remain += separator + data
                        continue

                    sys.stdout.write(json.dumps(data))

                    if data.get("status", None) == 0:
                        filelink = data.get("filelink")
                        webport = data.get("webport")

                    if data.get('action', None) == 0 and data['behave'] == 'file_upload':
                        filethread = FileDownload(host, webport, filelink, downloadend)
                        filethread.start()
                    print
                prompt()

        #user entered a message
        else :
            msg = sys.stdin.readline()
            msg = msg[:-1]
            try:
                if msg == 'auth':
                    s.send(json.dumps(dict(
                        action = 0,
                        behave = 'authorization',
                        device_id = device_id,
                        auth_key = auth_key
                    )) + separator)
                elif msg.startswith('keyup'):
                    a, b = msg.split(' ')
                    s.send(json.dumps(dict(
                        action = 2,
                        code = b
                    )) + separator)
                elif msg.startswith('keydown'):
                    a, b = msg.split(' ')
                    s.send(json.dumps(dict(
                        action = 1,
                        code = b
                    )) + separator)
                elif msg.startswith('switchon'):
                    a, b = msg.split(' ')
                    s.send(json.dumps(dict(
                        action = 3,
                        id = b
                    )) + separator)
                elif msg.startswith('switchoff'):
                    a, b = msg.split(' ')
                    s.send(json.dumps(dict(
                        action = 4,
                        id = b
                    )) + separator)
                elif msg.startswith('buttonpress'):
                    a, b = msg.split(' ')
                    s.send(json.dumps(dict(
                        action = 5,
                        id = b
                    )) + separator)
                elif msg == 'exit':
                    exit = True
                else:
                    s.send(msg + separator)
            except Exception, e:
                print e.message
            prompt()
s.close()

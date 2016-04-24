#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, select, string, sys, json, base64, threading, httplib2

from config import Type, Action, Status, Info
OperationReverse = dict()
OperationReverse['1'] = 'key_pressed'
OperationReverse['2'] = 'switch_on'
OperationReverse['3'] = 'switch_off'
OperationReverse['4'] = 'button_pressed'
OperationReverse['5'] = 'button_released'

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

class FileDownload(threading.Thread):
    def __init__(self, host, webport, link, filetype, callback):
        threading.Thread.__init__(self)
        self.link = 'http://%s:%d%s%s' % (host, webport, link, filetype)
        self.callback = callback

    def run(self):
        h = httplib2.Http(timeout = 1)
        (resp_headers, content) = h.request(self.link, "GET")
        self.callback(resp_headers, content)

def downloadend(resp_headers, content):
    #with open("./test", "wb") as f:
    #    f.write(content)
    s.send(json.dumps(dict(
        type = Type.status,
        status = "bit_file_program",
        size = len(content)
    )) + separator)

if len(sys.argv) < 3:
    print 'Usage : python ', __file__,' hostname port'
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
device_id = 'test'
auth_key = '8f5aff8cb424d2cf39b206619f8d1461'
separator = '\n'

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
                    messageType = data.get('type', None)

                    if messageType == Type.action:
                        pass
                    elif messageType == Type.status:
                        status = data.get("status", None)
                        if status == Status.authorized:
                            filelink = data.get("filelink")
                            webport = data.get("webport")
                        elif status == Status.file_upload:
                            filethread = FileDownload(host, webport, filelink, data['file']['type'], downloadend)
                            filethread.start()
                    elif messageType == Type.operation:
                        operation = data.get("operation", None)
                        if operation is not None:
                            status = OperationReverse.get(str(operation), None)
                            if status is not None:
                                keyname = 'key_code'
                                value = data.get("key_code", None)
                                if value is None:
                                    value = data.get('id', -1)
                                    keyname = 'id'
                                sendDict = dict(
                                    type = Type.status,
                                    status = status,
                                )
                                sendDict[keyname] = value
                                s.send(json.dumps(sendDict) + separator)
                    elif messageType == Type.info:
                        print 'User change to %s' % data.get('user', None)

                    print
                prompt()

        #user entered a message
        else :
            msg = sys.stdin.readline()
            msg = msg[:-1]
            try:
                if msg == 'auth':
                    s.send(json.dumps(dict(
                        type = Type.action,
                        action = Action.authorize,
                        device_id = device_id,
                        auth_key = auth_key,
                    )) + separator)
                elif msg.startswith('keypress'):
                    a, b = msg.split(' ')
                    b = int(b)
                    s.send(json.dumps(dict(
                        type = Type.status,
                        status = 'key_pressed',
                        key_code = b
                    )) + separator)
                elif msg.startswith('switchon'):
                    a, b = msg.split(' ')
                    b = int(b)
                    s.send(json.dumps(dict(
                        type = Type.status,
                        status = 'switch_on',
                        id = b
                    )) + separator)
                elif msg.startswith('switchoff'):
                    a, b = msg.split(' ')
                    b = int(b)
                    s.send(json.dumps(dict(
                        type = Type.status,
                        status = 'switch_off',
                        id = b
                    )) + separator)
                elif msg.startswith('buttonpress'):
                    a, b = msg.split(' ')
                    b = int(b)
                    s.send(json.dumps(dict(
                        type = Type.status,
                        status = 'button_pressed',
                        id = b
                    )) + separator)
                elif msg.startswith('buttonrelease'):
                    a, b = msg.split(' ')
                    b = int(b)
                    s.send(json.dumps(dict(
                        type = Type.status,
                        status = 'button_released',
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

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

def printHelp():
    print '''
Connected to remote host. Start sending messages
1 Input
  'auth'
  to send authorization message,
2 Input
  'keypress code',
  'switchon id', 'switchoff id',
  'buttonpress id' 'buttonrelease id'
  to send status message.
3 Or you can just input message and this message would be sent directly.
4 Input
  'exit'
  to exit this program.
    '''

class ServerSocket:
    class FileDownload(threading.Thread):
        def __init__(self, host, webport, link, filetype, callback):
            threading.Thread.__init__(self)
            self.link = 'http://%s:%d%s%s' % (host, webport, link, filetype)
            self.callback = callback

        def run(self):
            h = httplib2.Http(timeout = 10)
            (resp_headers, content) = h.request(self.link, "GET")
            self.callback(resp_headers, content)

    def __init__(self, host, port, device_id, auth_key, separator):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            s.connect((host, port))
            s.setblocking(0)
            self.s = s
        except :
            print 'Unable to connect'
            sys.exit()
        self.filelink = None
        self.webport = None
        self.host = host
        self.port = port
        self.device_id = device_id
        self.auth_key = auth_key
        self.separator = separator
        self.buffer = ''

    def downloadend(self, resp_headers, content):
        #with open("./test", "wb") as f:
        #    f.write(content)
        self.send_Status("bit_file_programmed", size = len(content))

    def download(self, filetype):
        filethread = self.FileDownload(self.host, self.webport, self.filelink, filetype, self.downloadend)
        filethread.start()

    def send(self, message):
        self.s.send(message + self.separator)

    def send_JSON(self, **kw):
        self.send(json.dumps(kw))

    def send_Type(self, msgtype, **kw):
        kw['type'] = msgtype
        self.send_JSON(**kw)

    def send_Action(self, message, **kw):
        kw['action'] = message
        self.send_Type(Type.action, **kw)

    def send_authorize(self, device_id=None, auth_key=None):
        if device_id == None:
            device_id = self.device_id
        if auth_key == None:
            auth_key = self.auth_key
        self.send_Action(Action.authorize, device_id = device_id, auth_key = auth_key)

    def send_Status(self, message, **kw):
        kw['status'] = message
        self.send_Type(Type.status, **kw)

    def send_keyPress(self, key_code):
        self.send_Status('key_pressed', key_code = key_code)

    def send_switchOn(self, id):
        self.send_Status('switch_on', id = id)

    def send_switchOff(self, id):
        self.send_Status('switch_off', id = id)

    def send_buttonPress(self, id):
        self.send_Status('button_pressed', id = id)

    def send_buttonRelease(self, id):
        self.send_Status('button_released', id = id)

    def handleOperation(self, data):
        operation = data.get("operation", None)
        if operation is not None:
            status = OperationReverse.get(str(operation), None)
            if status is not None:
                keyname = 'key_code'
                value = data.get("key_code", None)
                if value is None:
                    value = data.get('id', -1)
                    keyname = 'id'
                d = dict()
                d[keyname] = value
                self.send_Status(status, **d)

    def handleStatus(self, data):
        status = data.get("status", None)
        if status == Status.authorized:
            self.filelink = data.get("filelink")
            self.webport = data.get("webport")
        elif status == Status.file_upload:
            self.download(data['file']['type'])

    def handleInfo(self, data):
        info = data.get('info', None)
        if info == Info.user_changed:
            print 'User change to %s' % data.get('user', None)

    def dataRecv(self, data):
        l = data.split(self.separator)
        remain = l[-1]
        for message in l[:-1]:
            self.buffer += message
            self.on_read(self.buffer)
            self.buffer = ''
        self.buffer = l[-1]

    def on_read(self, message):
        data = json.loads(message)

        print '\nserver', json.dumps(data)
        messageType = data.get('type', None)

        if messageType == Type.action:
            pass
        elif messageType == Type.status:
            self.handleStatus(data)
        elif messageType == Type.operation:
            self.handleOperation(data)
        elif messageType == Type.info:
            self.handleInfo(data)

if __name__ == '__main__':
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

    printHelp()

    prompt()

    exit = False

    server = ServerSocket(host, port, device_id, auth_key, separator)

    while not exit:
        rlist = [sys.stdin, server.s]

        # Get the list sockets which are readable
        read_list, write_list, error_list = select.select(rlist , [], [])

        for sock in read_list:
            #incoming message from remote server
            if sock == server.s:
                data = sock.recv(4096)
                print data
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    server.dataRecv(data)
                    prompt()

            #user entered a message
            else:
                msg = sys.stdin.readline()
                msg = msg[:-1]
                try:
                    funcEqual = {
                        'auth' : server.send_authorize,
                        'exit' : sys.exit,
                    }
                    funcOneParam = {
                        'keypress' : server.send_keyPress,
                        'switchon' : server.send_switchOn,
                        'switchoff': server.send_switchOff,
                        'buttonpress': server.send_buttonPress,
                        'buttonrelease': server.send_buttonRelease,
                    }
                    access = False
                    try:
                        for (key, func) in funcEqual.items():
                            if msg == key:
                                func()
                                access = True
                                break
                    except Exception, e:
                        pass
                    try:
                        a, b = msg.split(' ')
                        for (key, func) in funcOneParam.items():
                            if a == key:
                                b = int(b)
                                func(b)
                                access = True
                                break
                    except Exception, e:
                        pass
                    if not access:
                        server.send(msg)
                except Exception, e:
                    print e.message
                prompt()

    server.s.close()

'''
使用select.select实现聊天室服务器
将server端和client端放到了同一个文件中
'''
import select
import socket
import sys
import signal
import cPickle
import struct
import argparse

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

def send(channel, *args):
    buffer = cPickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack('L', value)
    channel.send(size)
    channel.send(buffer)

def receive(channel):
    size = struct.calcsize('L')
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack('L', size)[0])
    except struct.error as e:
        return ''

    buf = ''
    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    return cPickle.loads(buf)[0]

class ChatServer(object):
    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print 'Server listening to port %s ...' % port
        self.server.listen(backlog)

        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        print 'Shutting down server...'
        for output in self.outputs:
            output.close()
        self.server.close()

    def getClientName(self, client):
        info = self.clientmap[client]
        host = info[0][0]
        name = info[1]
        return '@'.join((name, host))

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []

        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    client, address = self.server.accept()
                    print 'Chat server: got connection %d from %s' % (client.fileno(), address)

                    cname = receive(client).split('NAME: ')[1]

                    self.clients += 1
                    send(client, 'CLIENT: '+str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)

                    msg = '\n(Conneted: New client (%d) from %s)' % (self.clients, self.getClientName(client))
                    for output in self.outputs:
                       # print msg
                        send(output, msg)
                    self.outputs.append(client)

                elif sock == sys.stdin:
                    junk = sys.stdin.readline()
                    running = False

                else:
                    try:
                        data = receive(sock)
                        if data:
                            msg = '\n[' + self.getClientName(sock)[0] + '] : ' + data

                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                        else:
                            print 'Chat server: %d hung up' % sock.fileno()
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            msg = '\n(Now hung up: Client from %s)' % self.getClientName(sock)

                            for ouput in self.outputs:
                                send(output, msg)

                    except socket.error as e:
                        if sock in inputs:
                            inputs.remove(sock)
                        if sock in self.outputs:
                            self.outputs.remove(sock)

        self.server.close()

class ChatClient(object):
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port

        self.prompt = '@'.join((name, socket.gethostname().split('.')[0])) + '> '

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print 'Now connected to chat server@ port %d' % self.port
            self.connected = True
           
            send(self.sock, 'NAME: '+self.name)
            
            data = receive(self.sock)
            print data
            addr = data.split('CLIENT: ')[1]
            self.prompt = '@'.join((self.name, addr)) + '> '
        except socket.error as e:
            print 'Failed to connetc to chat server @ port %d' % self.port
            sys.exit(1)

    def run(self):
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                readable, writeable, exceptional = select.select([0, self.sock], [], [])

                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)

                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print 'Client shutting down.'
                            self.connected = False
                            break

                        else:
                            sys.stdout.write(data+'\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print ' Client interrupted. '
                self.sock.close()
                break
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--name', action='store', dest='name', required=True)
    parser.add_argument('--port', action='store', dest='port',type=int, required=True)
    givenArgs = parser.parse_args()

    port = givenArgs.port
    name = givenArgs.name

    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name, port)
        client.run()

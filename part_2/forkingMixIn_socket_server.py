import os
import socket
import threading
import SocketServer

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 0     #random port
BUF_SIZE = 1024
ECHO_MSG = 'Hello Server!'

class ForkingClient(object):
    def __init__(self, ip, port):
       self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.sock.connect((ip, port))

    def run(self):
        currentProcessId = os.getpid()
        print 'Client\'s PID:', currentProcessId

        sentDataLen = self.sock.send(ECHO_MSG)
        print 'Send %d characters' % sentDataLen

        response = self.sock.recv(BUF_SIZE)
        print 'PID %s Received: %s' % (currentProcessId, response)

    def shutdown(self):
        self.sock.close()

class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        currentProcessId = os.getpid()
        response = '%s: %s' % (currentProcessId, data)
        print response
        self.request.send(response)

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address

    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.setDaemon(True)
    serverThread.start()
    print 'Server\'s PID:', os.getpid()

    client1 = ForkingClient(ip, port)
    client1.run()

    client2 = ForkingClient(ip, port)
    client2.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()
















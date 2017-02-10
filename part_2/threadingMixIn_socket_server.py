import os
import socket
import threading
import SocketServer

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 0     #random port
BUF_SIZE = 1024
ECHO_MSG = 'Hello Server!'

class ThreadedServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        currentThread = threading.current_thread()
        response = '%s: %s' % (currentThread.name, data)
        #print response
        self.request.send(response)

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(BUF_SIZE)
        print 'Client received:', response
    except Exception as e:
        pass
    finally:
        sock.close()

if __name__ == '__main__':
    server = ThreadedServer((SERVER_HOST, SERVER_PORT), ThreadedServerRequestHandler)
    ip, port = server.server_address

    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.setDaemon(True)
    serverThread.start()
    print 'Server thread name:', serverThread.name

    client(ip, port, 'I\'m client1')
    client(ip, port, 'I\'m client2')
    client(ip, port, 'I\'m client3')

    server.shutdown()















import socket
import sys
import argparse

host = 'localhost'
dataPayload = 2048

def echoServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    while True:
        print 'Waiting to receive message from client'
        client, address = sock.accept()
        data = client.recv(2048)

        if data:
            print 'Data:', data
            client.send('Received!')
            print "Send back to", address

#        client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action='store', dest='port', type=int, required=True)
    givenArgs = parser.parse_args()
    port = givenArgs.port
    echoServer(port)

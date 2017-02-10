import socket
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action='store', dest='host', required=False)
    parser.add_argument('--port', action='store', dest='port', required=False, type=int)
    parser.add_argument('--file', action='store', dest='file', required=False)
    args = parser.parse_args()

    host = args.host
    port = args.port
    filename = args.file

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print e
        sys.exit(1)

    try:
        s.connect((host, port))
    except socket.gaierror, e:
        print 'Address-related error connection to server: %s' % e
        sys.exit(1)
    except socket.error, e:
        print 'Connection Error: %s' % e
        sys.exit(1)
    
    try:
        s.sendall('GET %s HTTP/1.0\r\n\r\n' % filename)
    except socket.error, e:
        print 'Error sending data: %s' % e
        sys.exit(1)

    while True:
        try:
            buf = s.recv(2048)
        except socket.error, e:
            print 'Error receiving data: %s' % e
            sys.exit(1)

            if not len(buf):
                break

            sys.stdout.write(buf)

if __name__ == '__main__':
    main()















































    

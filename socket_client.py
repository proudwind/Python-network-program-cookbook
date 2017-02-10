import socket
import sys
import argparse

host = 'localhost'

def echoClient(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Connecting %s:%s' % (host, port)
    sock.connect((host, port))

    try:
        message = 'Test message'
        sock.sendall(message)
        print 'Sending...'

        recv_len = 1
        response = ''
        while recv_len:
            data = sock.recv(16)
            recv_len = len(data)
            response += data

            if recv_len < 16:
                break
        print 'Receive:', response
    except socket.errno as e:
        print 'Socket error:', e
    except Exception as e:
        print '[-]', e
    finally:
        sock.close()

if __name__ == '__main__':
    echoClient(8008)

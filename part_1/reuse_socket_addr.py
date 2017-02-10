import socket
import sys

def reuse_socket_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    oldState = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print 'Old sock state: %s' % oldState

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    newState = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print 'New sock state: %s' % newState

    localPort = 8009
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', localPort))
    server.listen(1)
    print 'Listening on port %d' % localPort

    while True:
        try:
            connnect, addr = server.accept()
            print 'Connected by %s:%s' % (addr[0], addr[1])
        except KeyboardInterrupt:
            break
        except socket.error, e:
            print e

if __name__ == '__main__':
    reuse_socket_addr()

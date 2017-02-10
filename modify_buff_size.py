import socket 

SEND_BUF_SZIE = 4096 
RECV_BUF_SZIE = 4096

def modifyBufSize():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bufSize = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print 'Buffer size is %s' % bufSize
    
    s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SZIE)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SZIE)

    bufSize = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print 'Buffer size is %s' % bufSize
    
if __name__ == '__main__':
    modifyBufSize()

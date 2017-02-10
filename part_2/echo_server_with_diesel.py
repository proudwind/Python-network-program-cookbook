'''
使用并发库Diesel实现多路复用回显服务器
需先安装Diesel框架
pip install diesel 即可
'''
import diesel
import argparse

class EchoServer(object):
    def handler(self, remoteAddr):
        host = remoteAddr[0]
        port = remoteAddr[1]
        print 'Echo client connected %s:%d' % (host, port)
        
        while True:
            try:
                message = diesel.until_eol()
                yourMsg = 'You said: ' + message
                diesel.send(yourMsg)
            except Exception as e:
                print '[-]', e
                break   #书中没有这个break，在断开客户端连接的时候会导致服务端进入死循环。加上之后客户端断开连接，服务端并没有结束，而是等待下一个连接
def main(serverPort):
    app = diesel.Application()
    server = EchoServer()
    
    app.add_service(diesel.Service(server.handler, serverPort))
    app.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Echo Server with Diesel')
    parser.add_argument('--port', action='store', dest='port', type=int, required=True)
    givenArgs = parser.parse_args()
    port = givenArgs.port

    main(port)


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
                break

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


#!/usr/bin/python2.7
#-*-coding:utf-8-*-
import socket

def test_socket_timeout():
    s = socket.socket()
    print "Default socket timeout: %s" % s.gettimeout()
    s.settimeout(100)
    print "Current socket timeout: %s" % s.gettimeout()

if __name__ == '__main__':
    test_socket_timeout()

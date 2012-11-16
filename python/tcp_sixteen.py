#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import sys, socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


HOST = sys.argv.pop() if len(sys.argv) ==3 else '127.0.0.1'
PORT = 36666

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('not enough data')
        data += more
    return data

if sys.argv[1:] == ['server']:
#    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print 'listening at: ', s.getsockname()
        sc, sockname = s.accept()
        print 'we accept a client:', sockname
        print 'server  connect is :', sc.getsockname()
        message = recv_all(sc, 16)
        print 'incoming message is:', repr(message)
        sc.sendall('nice to see you!')
        sc.close()
        print 'reply send, socket closed'
elif sys.argv[1:] == ['client']:
    s.connect((HOST,PORT))
    print 'client has been assigned socket: ', s.getsockname()
    s.sendall('Hi there, server')
    reply = recv_all(s,16)
    print 'The server replies: ', repr(reply)
    s.close()
else:
    print >>sys.stderr, 'usage tcp_sixteen server|client [host]'



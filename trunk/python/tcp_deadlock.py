#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 36666

if sys.argv[1:] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print 'listening at :', s.getsockname()
        sc, sockname = s.accept()
        print 'Processing up to 1024 bytes from',sockname
        n = 0
        while True:
            msg = sc.recv(1024)
            if not msg:
                break
            sc.sendall(msg.upper())
            n += len(msg)
            print '\r%d bytes have processed'%n
            sys.stdout.flush()
        print
        sc.close()
        print 'Complete processing'
elif len(sys.argv) == 3 and sys.argv[1] == 'client' and sys.argv[2].isdigit():
    bytes_to_send = (int(sys.argv[2])+15)/16*16
    msg = 'capitalize this!'
    print 'sending', bytes_to_send, 'in chunk of 16 bytes'
    s.connect((HOST, PORT))
    sent = 0
    while sent < bytes_to_send:
        s.sendall(msg)
        sent += len(msg)
        print '\r%d bytes sent by now'%sent
        sys.stdout.flush()
    print
    s.shutdown(socket.SHUT_WR)
    print 'Receiving all the data the server sent'
    received = 0
    while True:
        data = s.recv(42)
        if not received:
            print 'The first data received says ', repr(data)
        received += len(data)
        if not data:
            break
        print '\r %d bytes of data received'%received
else:
    print >> sys.stderr, 'usage: tcp_deallock.py server|client number'


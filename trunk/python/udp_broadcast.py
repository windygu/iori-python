#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
MAX = 65535
PORT = 36666
if 2<= len(sys.argv) <= 3 and sys.argv[1] == 'server':
    interface = sys.argv[2] if len(sys.argv)>2 else ''
    s.bind((interface, PORT))
    print 'Listening at', s.getsockname()
    while True:
        data, addr = s.recvfrom(MAX)
        if random.randint(0,1): # generate a 1
            print 'The client at', addr, 'says', repr(data)
            s.sendto('YOur data was %d bytes'%len(data), addr)
        else: # no reply
            print 'Pretending to drop package from', addr
elif len(sys.argv) == 3 and sys.argv[1] == 'client':
    hostname = sys.argv[2]
    s.connect((hostname, PORT))
    print 'Client socket name is ', s.getsockname()
    delay = 0.1
    while True:
        s.send('This is another message')
        print 'waiting up to ', delay, 'seconds for a reply'
        s.settimeout(delay)
        try:
            data = s.recv(MAX)
        except socket.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('I think server may be down')
        except :
            raise
        else:
            break
    print 'server says', repr(data)
else:
    print >>sys.stderr, 'usage'


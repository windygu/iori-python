#!/usr/bin/env python
# -*_ coding: utf-8 -*-

import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX = 65536
PORT = 1060
if sys.argv[1:] == ['server']:
	s.bind(('127.0.0.1', PORT))
	print 'listening at', s.getsockname()
	while True:
		data, address = s.recvfrom(MAX)
		print 'The client at', address, 'says', repr(data)
		s.sendto('Your data was %d length'%len(data),address)
elif sys.argv[1:] == ['client']:
	print 'Address before sending:', s.getsockname()
	s.sendto('This is my message', ('127.0.0.1',PORT))
	print 'After sending:', s.getsockname()
	data, address = s.recvfrom(MAX)
	print 'The server', address, 'says', repr(data)
else:
	print >> std.error, 'usage udp_local.py server|client'


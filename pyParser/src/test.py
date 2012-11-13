#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
class A(object):
    def __init__(self, n=None):
        self.a = 'a'
        self.b = 'b'
        self.n = n
class MyJson(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, A):
            return json.JSONEncoder.default(self, o.__dict__)
        

if __name__ == '__main__':
    a = A()
    b = A(a)
    print MyJson().encode(a)
    print MyJson().encode(b)
    

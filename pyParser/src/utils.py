#/usr/bin/python
# -*- coding: utf-8 -*-

import imp

def hex2long(s):
    return long(''.join(['%x'%ord(i) for i in reversed(s)]), 16)

def pyc_generate(filename):
    ' generate a pyc file from filename'
    (fp, pathname, desc) = imp.find_module(filename)
    try:
        imp.load_module(filename, fp, pathname, desc)
    finally:
        if fp:
            fp.close()

class StringBuffer(object):
    def __init__(self, s):
        self.data = s
        self.index = 0
    def __getitem__(self, n):
        ' return next n elements based on current index'
        temp = self.index
        self.index += n
        return self.data[temp:self.index]
    def peek(self):
        return self.data[self.index]
    def skip(self,  n=1):
        self.index += n
    def eof(self):
        return self.index == len(self.data)
    


def main():
    pyc_generate('simpler')

    

if __name__ == '__main__':
    main()
#!/usr/bin/python
# -*- coding: utf-8 -*-
from xml.dom.minidom import getDOMImplementation
import os
import datetime
import utils

class PyModule(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
        self.filename = filename
        self.buff = utils.StringBuffer(data)
        self.magic = self.buff[4]
        timestamp = self.buff[4]
        self.timestamp = datetime.datetime.fromtimestamp(utils.hex2long(timestamp))    
        self.interned = []      
        self.document = getDOMImplementation().createDocument(None, self.filename, None)
        root = self.document.documentElement
        self.code = PyCode(self, root)  
    def parse(self):
        return self.code

        
    def xml(self):
        return self.document.toxml()
    def xml_to_file(self, filename=''):
        if not filename:
            filename = os.path.splitext(self.filename)[0] + '.xml'
        with open(filename, 'wb') as f:
            f.write(self.document.toxml())
           
class PyCode(object):
    def __init__(self, module, root=None):
        self.module = module
        self.root = root
        self.data = module.buff
        self.interned = module.interned
        self.type = self.data[1]  # read object type
        self.co_argcount = str(self.read_int())
        self.co_nlocals = str(self.read_int())
        self.co_stacksize = str(self.read_int())
        self.co_flags = str(self.read_int())
        self.co_code  = self.parse()
        self.co_consts = self.parse()
        self.co_names = self.parse()
        self.co_varname=self.parse()
        self.co_freevar=self.parse()
        self.co_cellvar=self.parse()
        self.o_filename=self.parse()
        self.co_name=self.parse()
        self.co_firstlineno=str(self.read_int())
        self.co_lnotab=self.parse()
        if not self.root :
            self.root = self.module.document.createElement(self.co_name)
        self.xml()

    def xml(self):
        document = self.module.document
        attrs = ("co_argcount",
                "co_nlocals",
                "co_stacksize",
                "co_flags",
                "co_code",
                "co_consts",
                "co_names",
                "co_varname",
                "co_freevar",
                "co_cellvar",
                "o_filename",
                "co_name",
                "co_firstlineno",
                "co_lnotab",)
        for attr in attrs:
            value = getattr(self, attr)
            elem = document.createElement(attr)
            if attr == 'co_code':
                value = 'binary'
            if isinstance(value, list):
                elem.setAttribute('count',str(len(value)))
                for item in value:
                    if isinstance(item, PyCode):
                        sub_elem = item.root
                    else:
                        sub_elem = document.createElement('sub')
                        sub_elem.setAttribute('value', item)
                    elem.appendChild(sub_elem)
            else:  
                elem.setAttribute('value', value)
            self.root.appendChild(elem)
        return self.root    
    def parse(self):
        t = self.data.peek()
        if t == 'R':  # string are interned by string reference
            return self.parse_string_ref()
        elif t == 's': # string type
            return self.parse_string()
        elif t == 'i':  # int type
            return self.parse_int()
        elif t == '(':  # tuple type
            return self.parse_tuple()
        elif t == 't':  # interned type
            return self.parse_interned()

        elif t == 'c':   # an code object inside another
            return PyCode(self.module)
        elif t == 'N':
            return self.parse_none()
    
    def parse_none(self):
        self.data.skip()
        return 'none'
        
    def read_int(self):
        ' parse an int object from self.data'
        value = self.data[4] 
        ret = long(''.join(['%x' % ord(i) for i in reversed(value)]), 16)
        return ret
    def parse_string_ref(self):
        self.data.skip()
        index = self.read_int()
        return self.interned[index]
        pass 
    def parse_string(self):
        self.data.skip()
        size = self.read_int()
        return self.data[size]
    def parse_int(self):
        self.data.skip()
        return str(self.read_int())
    def parse_tuple(self):
        ret = []
        self.data.skip() # tuple type
        size = self.read_int()
        for i in range(size):
            ret.append(self.parse())
        return ret
             
    def parse_interned(self): 
        self.data.skip()  # remove type char 
        size = self.read_int()
        value = self.data[size]
        self.interned.append(value)
        return value   # return the last position 
       
        
def main():
    m = PyModule('demo.pyc')
    m.xml_to_file()
if __name__ == '__main__':
    main()

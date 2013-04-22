#!/usr/bin/env python
# -*- coding: utf-8 -*

import unittest

from my115 import *
class Test115(unittest.TestCase):


    def setUp(self):
        self.user = get_115()
        self.data = [('name1.txt',  'http://g.cn/item1', 34569),
                     ('name2.txt',  'http://g.cn/item2', 5678),
                     ('name3.txt',  'http://g.cn/item3',4320),
                     ]
        for item in self.data:
            self.user.upload_file(*item)
        pass


    def tearDown(self):
        self.user.clear_task()
        pass


    def testName(self):
        self.assertEqual(self.user.get_task_info()['count'], '3')
        
        taskids = self.user.search_task('name')
        self.assertEqual(len(taskids),3)
        self.user.del_task(taskids)
        self.assertEqual(self.user.get_task_info()['count'], '0')
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
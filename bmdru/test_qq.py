#!/usr/bin/env python
# -*- coding: utf-8 -*



import unittest
import qq

class TestFenXiang(unittest.TestCase):
    def setUp(self):
        self.fen = qq.get_fenxiang()
        pass

    @unittest.skip("unittest passed already")
    def test_fast_upload(self):
        
        # test use form
        form='B15EFA59FF8677F49ED77C83D58E66870A2CF5CB#3013#How.the.universe.works.2010.BDRip.X264-BMDruCHinYaN.md5'
        self.assertTrue(self.fen.fast_upload(form)[0])

        
    #@unittest.skip("unittest passed already")
    def test_get_dir_info(self):
        
        for name in ['Everybodys.Fine.2009.BDRip.X264-BMDruCHinYaN', u'新建文件夹']:
            info = self.fen.get_dir_info(name)
            if info:
                self.assertIn(name, info['filename'])

    @unittest.skip("unittest passed already")
    def test_import_from_lixian(self):
        
        dir_name = 'universe'
        dir_info = self.fen.get_dir_info(dir_name)
        self.fen.import_from_lixian(dir_info['mid'])

    def test_share_dir(self):
        
        dir_name = 'Everybodys.Fine.2009.BDRip.X264-BMDruCHinYaN'
        res = self.fen.share_dir(dir_name)
        print res
        self.assertTrue(res)

    @unittest.skip("unittest passed already")
    def get_http_from_url(self):

        url = 'http://urlxf.qq.com/?QZzEvyr'

        res = qq.get_http_from_url(url)
        print res
        self.assertTrue(res)
                          
if __name__ == '__main__':
    unittest.main()
        
        

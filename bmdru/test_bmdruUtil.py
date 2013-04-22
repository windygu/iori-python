#!/usr/bin/env python
# -*- coding: utf-8 -*

'''
Created on 2013-3-6

@author: Administrator
'''


import unittest
from bmdruUtil import *

class testBmdru(unittest.TestCase):
    @unittest.skip("unittest passed already")
    def test_get_ftp_imdb(self):

        ftp = get_ftp()
        path = 'Gambit.2012.BDRip.X264-BMDruCHinYaN'
        imdb = 'tt0404978'

        res = get_ftp_imdb(path, ftp)
        self.assertEqual(res[1], imdb)
    @unittest.skip("unittest passed already")
    def test_upload_ftp_115(self):
        ftp = get_ftp()
        path = 'Gambit.2012.BDRip.X264-BMDruCHinYaN'
        name = 'tt0404978.z'
        url = 'ftp://admin:bmdru2012@120.192.81.203:6066/Gambit.2012.BDRip.X264-BMDruCHinYaN/tt0404978.z'   
        size = '2197824183'
        
        res = upload_ftp_115(path, None)
        
        self.assertTupleEqual(res, (url, size, name))
        
    @unittest.skip("unittest passed already")    
    def test_get_imdb(self):
        path = 'Hitchcock.2012.BDRip.X264-BMDruCHinYaN'
        fpath = os.path.join(LAN_BASE, path)
        imdb = get_imdb(fpath)
        self.assertEqual(imdb, 'tt0975645')
    @unittest.skip("unittest passed already")    
    def test_get_115upload_info(self):
        path = 'Hitchcock.2012.BDRip.X264-BMDruCHinYaN'
        size = '2198948609'
        name = 'tt0975645.z'
        url = r'http://222.175.240.166:42176/Hitchcock.2012.BDRip.X264-BMDruCHinYaN/Hitchcock.2012.BDRip.X264-BMDruCHinYaN.mkv'
        res = get_115upload_info(path)
        self.assertTupleEqual(res[0], (name, url, size))
    
    @unittest.skip("unittest passed already")    
    def test_upload_115vip(self):
        path = 'Hitchcock.2012.BDRip.X264-BMDruCHinYaN'
        
        cnt = upload_115vip(path)
        self.assertEqual(cnt,1)
        
    def test_batch_collect(self):
        forms = ['DA9B2954F538705E8B5E9C950385466C11531541#2198948609#tt0975645.z']
        res = batch_collect(forms)
        self.assertEqual(len(res), 1)



if __name__ == '__main__':

    unittest.main()



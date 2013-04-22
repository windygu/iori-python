#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import qq
import bmdruUtil
import os
def main():
    li = qq.get_lixian()
    path = '/How.the.universe.works.2010.BDRip.X264-BMDruCHinYaN/'
    for url in bmdruUtil.get_ftp_url(path):
        li.add_file_to_lixian(url)



def upload_115():
    path='Les.Gendarmes.1964-1982.BDRip.X264-BMDruCHinYaN'
    #os.chdir(bmdruUtil.LAN_BASE)  不要用这个
    for f in os.listdir(os.path.join(bmdruUtil.LAN_BASE, path)):
        bmdruUtil.upload_115vip(os.path.join(path, f))
    
if __name__ == '__main__':
    upload_115()
    pass

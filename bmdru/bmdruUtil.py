#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import re
import ftplib, ftputil
import ConfigParser
import my115

FTP_URL = '120.192.81.203'
FTP_PORT = 6066
FTP_USER = 'admin'
FTP_PASS = 'bmdru2012'
FTP_BASE = 'ftp://%s:%s@%s:%d'%(FTP_USER, FTP_PASS, FTP_URL,FTP_PORT)
LOCAL_BASE = 'http://222.175.240.166:42176'
LAN_BASE = r'z:' 
CONFIG_115 = '115.conf'
ACCOUNT_115 = 'account.txt'
SHARE_FILE = 'share.txt'

def get_ftp():
    ''' 返回一个可用的 ftp 对象'''
    class MySession(ftplib.FTP):
        def __init__(self,host, port ,user, password):
            ftplib.FTP.__init__(self)
            self.connect(host, port)
            self.login(user, password)
            
    host = ftputil.FTPHost(FTP_URL, FTP_PORT, FTP_USER,FTP_PASS,
                           session_factory=MySession)  
    return host

def get_ftp_url(path, ftp=None):
    '''
        返回指定目录下全部文件的 ftp链接，访问整个目录树，目录不存在则返回空
    '''
    if not ftp: ftp = get_ftp()
    res = []
    if ftp.path.isdir(path):
        for root, dirs, files in ftp.walk(path):
            res.extend(['%s/%s'%(root,f) for f in files])
        res = map(lambda f: '%s%s'%(FTP_BASE,f), res)
    return res


def get_ftp_imdb(path, ftp=None):
    ''' 通过查看 nfo文件来获取影片的 imdb号， 返回影片名和imdb号元组'''
    if not ftp: ftp = get_ftp()
    nfo = filter(lambda f: f.endswith('nfo'), ftp.listdir(path))
    if nfo:
        nfo = nfo[0]
        with ftp.file(ftp.path.join(path, nfo), 'r') as fp:
            for line in fp:
                imdb = re.findall(r'http://www.imdb.com/title/(tt\d+)', line)
                if imdb:
                    imdb = imdb[0]
                    break
            else:
                imdb = ''
        return (nfo[:-4], imdb)
    return (path.strip('/'), '')
            
            
def upload_ftp_115(path, acc115, ftp=None):
    ''' 从默认 ftp中上传mkv文件到 默认的115 vip中 '''
    if not ftp: ftp = get_ftp()
    # 1. 查找 mkv文件
    def_ext = '.z'
    mkv = filter(lambda f: f.endswith(def_ext), ftp.listdir(path))
    mkv = mkv[0]
    fpath = ftp.path.join(path, mkv)
    size = str(ftp.path.getsize(fpath))
    imdb = get_ftp_imdb(path, ftp)
    imdb = imdb[1] 
    fname = '%s.z'%imdb
    url = '%s%s'%(FTP_BASE, ftp.path.abspath(fpath))
    user = my115.get_115()
    user.upload_file(fname, url, size)
    return (url, size, fname)


def get_imdb(path, host=''):
    if not host: host = os
    nfo = filter(lambda f: f.endswith('.nfo'), host.listdir(path))
    if nfo:
        nfo = nfo[0]
        fpath = host.path.join(path, nfo)
        fp = open(fpath, 'r') if host == os else host.file(fpath)
        for line in fp:
            imdb = re.findall(r'http://www.imdb.com/title/(tt\d+)', line)
            if imdb:
                return imdb[0]
    return ''
                   
def get_115upload_info(path, host=''):
    ''' 产生指定目录下电影文件的信息 (imdb_name, filesize, url)
     path 为是相对路径，不 以 /或\开头， 但处理一层路径
    '''
    if not host:
        host = os
        url_base=  LOCAL_BASE
        if os.path.exists(path):
            lpath = path
            path = path.replace(LAN_BASE, '')
        else:
            lpath = os.path.join(LAN_BASE, path)
    else:
        url_base = FTP_BASE
        lpath = path
    def_ext = '.mkv'
    mkvs = filter(lambda f: f.endswith(def_ext), host.listdir(lpath))
    if not mkvs:
        return None
    mkvs.sort()

    imdb = get_imdb(lpath, host)
    res = []
    for i in range(len(mkvs)):
        size = str(host.path.getsize(host.path.join(lpath, mkvs[i])))
        url = '/'.join([url_base, path, mkvs[i]])
        url = url.replace('\\', '/')
        imdb_name = '%s-i.z'%imdb
        res.append((imdb_name, url, size))
    if len(res) == 1: # just one moive, correct name
        res[0] = ('%s.z'%imdb, url, size)
    return res

class Config115():
    def __init__(self, f=CONFIG_115):
        self.f = f
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.f)
    def __enter__(self):
        return self.conf
    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.f, 'wb') as fp:
            self.conf.write(fp)
            
def walk_upload_info(path=''):
    ''' 遍历目录树， 将相应的结果写入文件供后续使用  '''
    if not path:
        path = LAN_BASE
    res = {}
    for root, dirs, files in os.walk(path):
        for folder in dirs:
            if folder.endswith('BMDruCHinYaN'):
                info = get_115upload_info(os.path.join(root, folder))
                if info:
                    res[folder] = info
    if res:
        with Config115() as conf:
            for folder in res:
                if conf.has_section(folder):
                    print '%s done already'%folder
                else:
                    conf.add_section(folder)
                    for item in res[folder]:
                        if item:
                            fname = os.path.split(item[1])[1]
                            conf.set(folder, fname, '|'.join(item))
    return len(res)
                            
def default_upload115():
    ''' 批量上传文件到115vip中 '''
    ret = {}
    with Config115() as conf:
        user = my115.get_115()
        for section in conf.sections():
            if section in ('done', 'upload_done'): continue
            for item in conf.items(section):
                name, url, size = item[1].split('|')
                res =user.upload_file(name, url, size)
                ret[name] = res
    return res
    
def upload_115vip(path, host=''):
    with Config115() as conf:
        if  conf.has_section(path):  # 上传过，不再重复
            print '%s done already'%path
            return
        res = get_115upload_info(path, host)
        conf.add_section(path)
        user = my115.get_115()
        for item in res: # items = (imdbname, url, size)
            print item
            fname = os.path.split(item[1])[1]
            conf.set(path, fname, '|'.join(item))
            user.upload_file(*item)
    ret = []
    for item in res:
        ret.extend(user.search_task(item[0]))
    return len(ret)
    
def get_task_form():
    ''' 对完成的任务， 获取其标准式, 同时设置upload_done节
            返回格式为 {'section':{'name':'form'}}
    '''
    ret = {}
    with Config115() as conf:
        user = my115.get_115()
        tasks = user.get_task_info()
        for section in conf.sections():
            if section in ('done', 'upload_done'):continue
            ret[section] = {}
            for item in conf.items(section):
                name = item[1].split('|')[0]
                # 查找进行中任务的任务项， 通过比较文件来进行
                for task in tasks['data']: 
                    if task['n'] == name:
                        break
                else:
                    continue
                # 任务完成了
                if task['dest'] == u'已下载文件': # 下载完成的任务
                    pickcode = task['pc']
                    if not pickcode: continue
                    sha1 = user.getsha1(pickcode)
                    form = '#'.join([sha1, task['s'], task['n']])
                    
                    ret[section][item[0]] = form
        for section in ret:
            for fname in ret[section]:
                conf.set("upload_done", fname, ret[section][fname])
                conf.remove_option(section, fname)
            conf.remove_section(section)
    return ret

class LoadAccount(object):
    def __init__(self):
        self.fp = open(ACCOUNT_115, 'r+')
        self.users = [user.strip() for user in self.fp.read().split('\n') if user.strip()]
    def __enter__(self):
        return self.users
    def __exit__(self,  exc_type, exc_val, exc_tb):
        self.fp.seek(0)
        self.fp.write('\n'.join(self.users))
        self.fp.close()
                      
def batch_collect(forms):  
    ''' 收藏标准式， 返回收藏的结果 
    [('ae7hcby5', 'DA9B2954F538705E8B5E9C950385466C11531541#2198948609#tt0975645.z', '4732782')]
    '''
    with LoadAccount() as accounts:   
        done = []
        info = accounts[0].split()
        user = my115.get_115(info[0], info[1])
        for form in forms:
            size = int(form.split('#')[1])
            while user.get_remain_space() < size:
                accounts.pop(0)
                info = accounts[0].split()
                user = my115.get_115(info[0], info[1])
            pc = user.collect(form)
            if not pc:
                print '%s fail '%form
            else:
                done.append((pc, form, info[0]))
    return  done
             
def update_done():
    ''' 上传完成同时获取标准式后， 收藏标准式，同时生成必贴文件及清除上传的文件 '''
    with Config115() as conf:
        items = [item for item in conf.items('upload_done')]
        done = batch_collect([item[1] for item in items])
        fshare = open(SHARE_FILE, 'ab')
        clean_up = []
        for info in done:
            for item in items:
                if item[1] == info[1]:
                    break
            else:
                continue
            conf.set('done', item[0], '|'.join(info))
            conf.remove_option('upload_done', item[0])
            clean_up.append(item[1].split('#')[2])
            fshare.write('\n'.join([item[0], '[code]', item[1], '[/code]']))
    vip = my115.get_115()
    for item in clean_up:
        vip.del_file(item)
    return done

def clean_up():
    ''' 一般情况下应该不用 '''
    with Config115() as conf:
        user = my115.get_115()
        for item in conf.items('done'):
            name = item[1].split('|')[1].split('#')[2]
            ret =user.del_file(name)
            if not ret:
                print '%s fail to delete'%name


###  一般情况下，直接使用下面两个函数就 行
def auto_upload_115(debug=0):
    
    ret = walk_upload_info() # 生成文件信息
    if debug:
        print ret 
    ret = default_upload115() #进行上传
    if debug:
        print 'default_upload115 resutl:'
        print ret
        
def auto_collect(debug=0):
    ''' 此时文件上传完成 '''
    ret = get_task_form()
    if debug:
        print ret 
    ret = update_done()
    if debug:
        print ret     
               
if __name__ == '__main__':
    clean_up()

    pass
    


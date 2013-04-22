#!/usr/bin/env python
# -*- coding: utf-8 -*

'''
   qq功能模块
'''


import time
import urllib,urllib2, cookielib
import hashlib, random
import re, json, base64



def hexchar2bin(s):
    ''' 每次取 s中的两个字符，当作16进制数，然后将其傎作为结果串中的一个字符的 ascii码'''
    return ''.join([chr(int(s[i:i+2], 16)) for i in range(0,len(s),2)])

def uin2hex(s):
    h = '{:0>16X}'.format(int(s))
    return hexchar2bin(h)


class QQ(object):
    '''
        返回一个可用的 qq对象
    '''
    def __init__(self, qq, password):
        self.qq = qq
        self.password = password
        self.cookie = ''
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.login()
    def encrypt_password(self, verifycode):
        ''' qq的加密算法 '''
        I = hexchar2bin(hashlib.md5(self.password).hexdigest())
        uin= uin2hex(self.qq)
        H=hashlib.md5(I+uin).hexdigest().upper()
        P=hashlib.md5(H+verifycode.upper()).hexdigest().upper()
        return P        
    def get_verifycode(self):
        ''' 获取 qq登陆时候 的验证码， 在一定条件 下，直接能取得值，另一些条件下会要用户输入 '''
        url='http://check.ptlogin2.qq.com/check?uin=%s' %self.qq + \
            '&appid=567008010&r=%s' % random.Random().random()
        res = self.opener.open(url).read()
        # ptui_checkVC('0','!FQK','\x00\x00\x00\x00\x00\x33\x7b\x13')
        # 第一个为0，则表示不用要求输入验证码，第二项为验证码
        info = re.findall(r"'([^']*)'", res)
        if info[0] == '0':
            return info[1]
        return None
    def do_login(self, verifycode):
        ''' 实际登陆方法， 前提是取得验证码'''
        pp = self.encrypt_password(verifycode)
        url = 'http://ptlogin2.qq.com/login?' +\
            'action=6-43-357229&' + \
            'aid=567008010&'    +\
            'dumy=&'            +\
            'fp=loginerroralert&'   +\
            'from_ui=1&'    +\
            'g=1&'          +\
            'h=1&'          +\
            'mibao_css=&'   +\
            'p=%s&'%pp      +\
            'ptlang=2052&'  +\
            'ptredirect=1&' +\
            't=1&'          +\
            'u=%s&'%self.qq +\
            'u1=http%3A%2F%2Ffenxiang.qq.com&'    + \
            'verifycode=%s'%verifycode
        headers={'Referer':'http://ui.ptlogin2.qq.com/cgi-bin/login?uin=&appid=567008010&f_url=loginerroralert&hide_title_bar=1&style=1&s_url=http%3A//fenxiang.qq.com&lang=0&enable_qlogin=1&css=http%3A//imgcache.qq.com/ptcss/r1/txyjy/567008010/login_mode_new.css%3F',
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; SIMBAR={E540A73C-FFAE-11E1-A7F7-002618241525})'
                 }
        req = urllib2.Request(url=url, headers=headers)
        res = self.opener.open(req)
        # ptuiCB('3','0','','0','您输入的帐号或密码不正确，请重新输入。', '3373843');
        # ptuiCB('4','3','','0','登录失败，请重试!*', '3373843');
        # ptuiCB('4','0','','0','您输入的验证码不正确，请重新输入。', '3373843')
        # ptuiCB('0','0','http://fenxiang.qq.com','1','登录成功！', 'Diamomd');
        info = re.findall(r"'([^']*)'", res.read())
        if info[0] == '0':
            self.cookie = ';'.join([ re.findall(r'(?<=Set-Cookie:)[^;]+',item)[0] \
                                        for item in res.info().getallmatchingheaders('Set-Cookie')])
            print 'login success'
        else:
            print 'login fail'
        
    def login(self):
        verifycode = self.get_verifycode()
        if verifycode:
            self.do_login(verifycode)
        else:
            print 'fail'
    

class LiXian(object):
    def __init__(self, qq, password):
        self._qq = QQ(qq, password)
        self.cookie = self._qq.cookie
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;; SIMBAR={E540A73C-FFAE-11E1-A7F7-002618241525})',
                 'Referer':'http://lixian.qq.com/main.html',
                 'x-requested-with':'XMLHttpRequest',
                 'Accept': 'application/json, text/javascript, */*; q=0.01',
                 'Cookie': self.cookie,
                 }
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.login()
    def gen_time(self):
        return int((round(abs(random.Random().random() - 1) * 2147483647) *(int(time.time())*1000)) % 10000000000)
    def getACSRFToken(self, s):
        hash_key = 5381
        for i in s:
            hash_key = hash_key + (hash_key<<5) + ord(i)
        return hash_key & 0x7fffffff
    def extract_cookie(self, key):
        'Cookie: name=value; name=value '
        cookie =self.cookie
        if cookie[-1] != ';': cookie = cookie +';'
        match = re.search(r'(?<=%s=)[^;]+'%key, cookie)
        if match:
            return match.group(0)
    def login(self):
        ''' 主要是获取 qq lixian的授权'''
        token = self.extract_cookie('skey')
        if token:
            token = self.getACSRFToken(token)
        data = urllib.urlencode({'g_tk':token})
        '用在qq号登陆以，获取相应的PHPSESSIONID来进行相应的操作'
        req = urllib2.Request(url='http://lixian.qq.com/handler/lixian/do_lixian_login.php',
                              headers=self.headers,
                              data=data
                              )
        res =self.opener.open(req)
        cookies =  ';'.join([ re.findall(r'(?<=Set-Cookie:)[^;]+',item)[0] \
                            for item in res.info().getallmatchingheaders('Set-Cookie')])
        self.cookie = ';'.join([self.cookie,cookies,
                                 'pgv_pvid='+str(self.gen_time()),
                                 'pgvReferrer=&ssid=s'+str(self.gen_time()),
                                 'pgv_pvi='+ str(self.gen_time()),])
        self.headers['Cookie'] = self.cookie # update cookie in header
        
    def get_lixian_list(self):
        '''获取帐号里面的全部离线文件信息列表， 并存到文件 lixian_info.txt中， 是一个Json格式内容'''
        req = urllib2.Request(url='http://lixian.qq.com/handler/lixian/get_lixian_list.php',
                              headers=self.headers,
                              data='',  # to make it a post request
                              )
        res = self.opener.open(req).read()
        info = json.loads(res)
        if info['ret'] == 0:
            return info['data']
        
    def add_file_to_lixian(self,down_link):
        '添加文件到离线空间'
        # we assume protocol://host/path/filename in this form
        data=urllib.urlencode({'down_link':down_link,
                               'filename': down_link.split('/')[-1],
                               'filesize': 0,
                               })
        req = urllib2.Request(url='http://lixian.qq.com/handler/lixian/add_to_lixian.php',
                              data=data,
                              headers=self.headers)
        res = self.opener.open(req)
    def post_req(self, url, data):
        req = urllib2.Request(url=url, data=data, headers=self.headers)
        res = self.opener.open(req)
        data= json.loads(res.read())
        return data             
    def clear_lixian_task(self):
        url = 'http://lixian.qq.com/handler/lixian/del_lixian_task.php'
        mids = ','.join([item['mid'] for item in self.get_lixian_list()])
        data = urllib.urlencode({'mids':mids})
        res = self.post_req(url, data)
            
        if res['ret'] == 0:
            print 'clear success'

def get_lixian():
    li = LiXian('3373843', 'aitianxin')
    return li

def test_lixian():
    li = LiXian('3373843', 'aitianxin')
    url='ftp://admin:bmdru2012@120.192.81.203:6066/Umizaru.3.The.Last.Message.2010.BDRip.X264-BMDruCHinYaN/Umizaru.3.The.Last.Message.2010.BDRip.X264-BMDruCHinYaN.nfo'
    
    def test_clear():
        li.clear_lixian_task()
    test_clear()
    
    
    
class FenXiang(object):
    def __init__(self, qqnum, password):
        
        self.qq = QQ(qqnum, password)
        self.qqnum = qqnum
        self.cookie = self.qq.cookie
        self.headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;; SIMBAR={E540A73C-FFAE-11E1-A7F7-002618241525})',
                 'Referer':'http://fenxiang.qq.com/',
                 'x-requested-with':'XMLHttpRequest',
                 'Accept': 'application/json, text/javascript, */*; q=0.01',
                 'Cookie': self.cookie,
                 }
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.login()
    def gen_time(self):
        return int((round(abs(random.Random().random() - 1) * 2147483647) *(int(time.time())*1000)) % 10000000000)
    def login(self):
        headers=dict(self.headers,
                    **{'Referer':'http://ui.ptlogin2.qq.com/cgi-bin/login?uin=&appid=567008010&f_url=loginerroralert&hide_title_bar=1&style=1&s_url=http%3A//fenxiang.qq.com&lang=0&enable_qlogin=1&css=http%3A//imgcache.qq.com/ptcss/r1/txyjy/567008010/login_mode_new.css%3F',}
                )
        req = urllib2.Request(url='http://fenxiang.qq.com',
                              headers=headers,
                              )
        res =self.opener.open(req)
        cookie =  ';'.join([ re.findall(r'(?<=Set-Cookie:)[^;]+',item)[0] \
                            for item in res.info().getallmatchingheaders('Set-Cookie')])
        self.cookie = ';'.join([self.cookie, cookie,
                                    'pgv_pvid='+str(self.gen_time()),
                                    'pgvReferrer=&ssid=s'+str(self.gen_time()),
                                    'ptui_loginuin='+self.qqnum,
                                    ])

        self.headers['Cookie']  = self.cookie
    def get_list(self, mid='0'*72):
        ''' 根是 长度为72个0的串'''
        url = 'http://fenxiang.qq.com/upload/index.php/upload/api_c/get_list?mid=%s&&tp=a&&f=0&&ob=3&&s=0'%mid
        req = urllib2.Request(url=url, headers=self.headers)
        res = self.opener.open(req)
        info = json.loads(res.read())
        if info['ret'] == 0:  # success
            return info['data']
        else:
            return None   
    def add_dir(self, name, parent='0'*72):
        ''' name should be utf8 encode, parent is mid of a folder'''
        data = urllib.urlencode({'dirName': name,
                                  'dir_id': parent,
                                  'task_id': '0'
                                  })
        url = 'http://fenxiang.qq.com/upload/index.php/upload/api_c/add_dir?'
        req = urllib2.Request(url=url, headers=self.headers, data=data)
        res = self.opener.open(req)
               
        #{"ret":0,"msg":"\u6210\u529f(success)","data":{"mid":"38c2eb0b0d601b2a3fd704000000000095cf3cd4212bcf2caa867dcd73c90f943d6c2c8a","task-id":"0"}}
        info = json.loads(res.read())
        if info['ret'] == 0: # success
            return info['data']['mid']
        else:
            return None

    def pre_upload(self, form, task_id, dir_id='0'*72):
        (sha1,size,filename)=form.split('#',2)
        data=urllib.urlencode({'fileSha1': sha1.upper(),
                               'fileSize': size,
                               'fileName': filename,
                               'dir_id': dir_id,
                               'task_id': task_id,
                               })
        url = 'http://fenxiang.qq.com/upload/index.php/upload/upload_c/preUpload'
        req = urllib2.Request(url=url, data=data, headers=self.headers)
        res = self.opener.open(req)
        data= json.loads(res.read())
        if str(data['errno']) != '0':
            return None
        return data
    def post_upload(self, form,  info, dir_id='0'*72):
        (sha1,size,filename)=form.split('#',2)
        if info is None:
            return 'fail do pre_upload: %s '%filename
        try:
            data=urllib.urlencode({'fileSha1':sha1.lower(),
                                   'mid': info['mid'],
                                   'fileSize':size,
                                   'fileName':filename,
                                   'task_id': info['task_id'],
                                   'file_exist': info['file_exist'],                      
                                   'errcode': info['errno'],
                                   'uploadspeed': info['file_uploaded'],
                                   'dir_id': dir_id
                                   })
            url = 'http://fenxiang.qq.com/upload/index.php/upload/upload_c/postUpload'
            req = urllib2.Request(url=url, data=data, headers=self.headers)
            self.opener.open(req)
            return (True, filename)
        except KeyError:
            return (False, filename)  
    def fast_upload(self, form, task_id=0,dir_id='0'*72):
        info = self.pre_upload(form, task_id, dir_id)
        if info:
            res = self.post_upload(form, info, dir_id)
            return res

    def get_lixian_list(self):
        req = urllib2.Request(url='http://fenxiang.qq.com/upload/index.php/upload/api_c/get_lixian_list',
                              headers=self.headers,
                              data='')
        res = self.opener.open(req)
        info = json.loads(res.read())
        if info['ret'] == 0:
            return info['data']
        else:
            return None
    def import_from_lixian(self, dir_id='0'*72):
        info = self.get_lixian_list()
        for i,item in enumerate(info):
            form = '#'.join([str(item['hash']),str(item['file_size']), item['file_name']])
            res = self.fast_upload(form, i, dir_id)
            print res
    def get_dir_info(self, name):
        for item in self.get_list():
            if name in item['filename'] and item['type'] == '1':
                return item
        return None
    
    def post_req(self, url, data):    
        req = urllib2.Request(url=url, data=data, headers=self.headers)
        res = self.opener.open(req)
        data= json.loads(res.read())
        return data        
    def rm_dir(self, name):
        info = self.get_dir_info(name)
        if info:
            url = 'http://fenxiang.qq.com/upload/index.php/upload/api_c/rm_dir'
            data = urllib.urlencode({'dirName': info['filename'],
                                     'mid': info['mid'],
                                     'task_id': 0
                                     })
            res = self.post_req(url, data)
            if res['ret'] == 0:
                print 'del %s success' %info['filename']
            else:
                print 'del %s fail'%info['filename']
        else:
            print '%s not foud'%name

    def share(self, forms):
        ' 由 forms指定的文件来生成分享 url forms now are  hash#size#name#mid'
        data={"uin": self.qq.qq,
              "siteid":'200000056',
              "filelist":[]
              }
        for form in forms.split('\n'):
            if form:
                info = form.split('#')
                if len(info) < 4: continue  # form now at least have four item.
                data['filelist'].append({"filehash": info[0].upper(),
                                         "filename": ''.join(info[2:-1]), 
                                         "filesize": info[1],
                                         })
        # first convert possible ' to ", then remove space,mybe it's not important
        data = json.dumps(data, separators=(',', ':')).decode('unicode-escape').encode('utf-8')
      #  data = data.replace("'", '"')
        data = urllib.urlencode({'data':data})
        url='http://fenxiang.qq.com/upload/index.php/upload/upload_c/startShare'
        res = self.post_req(url, data)
        # { "data" : { "code" : "2iiMvVZ7dfROaQ6JTuX2wPMRR4bitH03wmM:", "expire_time" : 1367159931, "url" : "http://urlxf.qq.com/?FnYBBbU" }, "msg" : "ok", "ret" : 0 } 
        print res
        if res['ret'] == 0:
            return res['data']['url']
        else:
            print res
        
    def share_dir(self, name):
        dir_info = self.get_dir_info(name)
        if not dir_info:
            raise Exception, '%s not found'%name
        file_list = []
        for item in self.get_list(dir_info['mid']):
            form = '#'.join([ item['hash'], item['filesize'],
                              item['filename'], item['mid']])
            file_list.append(form)
        return self.share('\n'.join(file_list))
            




def get_fenxiang():
     return  FenXiang('3373843', 'aitianxin')

def share_dir(dir_name):
    import os
    dir_name = dir_name.strip('/')
    dir_name = os.path.split(dir_name.strip('/'))[1]
    fen = get_fenxiang()
    mid = fen.add_dir(dir_name)
    fen.import_from_lixian(mid)
    print fen.share_dir(mid)

####   some utils about qq
def get_qqdl(url):
    '获取指定网址中的全部 qqdl:// 网址'
    if not 'fenxiang.qq.com' in url:
        response = urllib2.urlopen(url)
        data = response.read()
        url = re.search(r'\"([^"]+)', data).group(1)
    response = urllib2.urlopen(url)
    data=response.read()

    # 下面的用处是除掉获取的链接中出现的重复的内容
    qqdls = re.findall(r'qqdl:[^"]+', data) 
    qqdl_set=set()
    for qqdl in qqdls:
        qqdl_set.add(qqdl)
        
    return qqdl_set

def batch_qqdl(urls):
    '批量获取 url中 qqdl:// , urls为以回车分割的多个url'
    res=[]
    for url in urls.split('\n'):
        if url.strip():
            url_set = get_qqdl(url)
            res.extend(url_set)
    return '\n'.join(res)
def batch_qqdl_http(urls, kind='ftn_handler'):
    ''' 指url qq fenxiang 链接转换， 默认转成 ftp_handler形式，还支持 weibo形式
        同时也能将  qqdl:// 的转成 http://

    '''
    res=[]
    try:
        urls = urls.split('\n')
    except Exception:
        pass
    for url in urls:
        if url.strip():
            temp = url.strip()
            if 'qqdl://'  in url:
                temp = base64.decodestring(url.strip()[7:]).decode('gbk').encode('utf-8')
            if kind == 'ftn_handler':
                temp = temp.replace('weibo/', 'ftn_handler')
            elif kind == 'weibo' :
                temp = temp.replace('ftn_handler', 'weibo/')
            res.append(temp)
    return '\n'.join(res) 
    
def get_http_from_url(url):
    urls = get_qqdl(url)
    res =  batch_qqdl_http(urls)
    return '%s\n%s'%(url, res)


def batch_http_url():
    urls='''http://urlxf.qq.com/?vmiiU33
http://urlxf.qq.com/?JVNvEbB
http://urlxf.qq.com/?Urm2uqeM
http://urlxf.qq.com/?YbINrmv
http://urlxf.qq.com/?MF3U7bV
http://urlxf.qq.com/?niINVzz
http://urlxf.qq.com/?Az2uiqn'''
    urls = batch_qqdl(urls)
    print batch_qqdl_http(urls)
    

if __name__ == '__main__':
    batch_http_url()


    
    

    
        
        

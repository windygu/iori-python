#!/usr/bin/env python
# -*- coding: utf-8 -*-



import urllib, urllib2, cookielib
import time, re, json, base64
import datetime


USER = '8933333'
PASSWORD = 'ccisgood'
class My115(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.opener = None
        self.storage_info = {}
        self.headers = {'Referer':'http://115.com/',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                 }
        self.form = []
        self.oofa = ''
        self.uid=''
        self.login()
    def login(self):
        '登陆115网盘， 成功返回True, 失败返回False'
        cj = cookielib.MozillaCookieJar()            
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        param = urllib.urlencode({'login[account]' : self.username,
                                        'login[passwd]':self.password,
                                        'back': 'http://www.115.com'
                                        })
        headers = {"Content-type": "application/x-www-form-urlencoded",
                                "Accept": "text/plain",
                                "Referer" : "http://www.115.com"
                                }
        login_url = 'http://passport.115.com/?ac=login'
        request = urllib2.Request(login_url, param, headers)
        response = self.opener.open(request)
        # 不成功是没有 Set-Cookie字段，会出现异常
        match = re.search(r'OOFA=([^;]+)', ''.join(response.info().getheader('Set-Cookie')))
        if not match:
                self.opener = None
                return  False
        else:
                self.oofa = urllib.unquote(match.group(1))
                info_url='http://web.api.115.com/files/friendrecomm?_t=' + str(time.time())
                headers = { 'Referer':'http://web.api.115.com/bridge.html?namespace=Core.DataAccess&api=DataAPI&_t=v2'
                                        }
                request = urllib2.Request(info_url, None, headers)
                response = self.opener.open(request)
                info = json.loads(response.read())
                self.uid = info[u'curr_user'][u'user_id']
                return True

    def collect(self, form):
        '收藏标准式： sha1#size#name, 收藏成功：返回 Pickcode'
        if len(form.split('#')) != 3:
            return 'Incorrect form : %s' %form
        (sha1, size, name)=form.split('#')
        query = { 'cmd':'upload',
              'cookie': base64.b64encode(self.oofa),
              'user_id': self.uid,
              'sha1': sha1,
              'filesize':size,
              'filename': ''.join([ '%%%X'%ord(i) for i in name]),
              'aid': '1',
              'cid': '0',
              'pickcode':'',
              'isp':'0',
              'web':'1',
              'version':'v1.7.1.2'
              }
        url_collect = 'http://lb.u.115.com/api/index.php?'
        url_collect += '&'.join([ '%s=%s'%(k,query[k]) for k in query.keys()])
        headers= {"Host": "lb.u.115.com",
          "User-Agent": "u115Client"
          }
        request = urllib2.Request(url_collect, None, headers)
        response = self.opener.open(request)
        reply = response.read()
        match=re.search(r'<pickcode>([^<]+)', reply)
        if match:
            return match.group(1)
        else:
            return None

    
    def get_remain_space(self):
        self.get_storage_info()
        return self.storage_info['1']['total'] - self.storage_info['1']['used']
        
    def batch_collect(self, forms):
        ' forms are utf-8 encode  返回为新的提取码'
        if not isinstance(forms, list):
            forms = forms.split('\n')
        info = []
        for form in forms:
            form = form.strip()
            if form:
                info.append(self.collect(form))
        return '\n'.join(info)
                
    def getsha1(self,pickcode):
        ''' return sha1 of a specified pickcode， files's owner is current user
        '''
        query = urllib.urlencode({ "_t" : str(time.time()),
                                'ac':'download',
                                'ct':'pickcode',
                                'pickcode':pickcode
                                })
        pickcode_url = 'http://115.com/?' + query 
        headers = { "Referer": "http://115.com/",

                 }
        response = self.opener.open(urllib2.Request(pickcode_url, '', headers))
        match = re.search(r"AddDownTask\(([^)]+)", response.read())
        if match is  None:
            return None
        else:
            return match.group(1).split(',')[4].replace("'",'')          

    def get_fileinfo(self, cid, limit=500):
        # cause , here time parameter don't 1000*
        query = urllib.urlencode({ "_t" :int(time.time()),
                                "aid":1,
                                "asc"    :    0,
                                "cid"    :    cid,
                                "format"    :    "json",
                                "is_share":''    ,
                                "limit":        str(limit),
                                "o"    :    '',
                                "offset":    0,
                                "show_dir"    :    1,
                                "source":    ''    ,
                                "star":    '',
                                "type":'' }) 
        headers = { "Referer": "http://web.api.115.com/bridge.html?namespace=Core.DataAccess&api=DataAPI&_t=v2",
                 }
        url = "http://web.api.115.com/files?" + query
        response = self.opener.open(urllib2.Request(url = url, headers = headers))
        return response.read()
    def get_recent_lixian(self, days=2, ext='.z'):
        '返回标准式便于收藏'
        info = self.get_fileinfo(cid='2204674',limit=30)
        info = json.loads(info)
        forms = []
        for item in info['data']:
            if 's' in item.keys(): # s starnds for size, only a file has it
                ctime = item['t']  # this form "2013-01-12 15:40" we use datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")
                upload_time = datetime.datetime.strptime(ctime, "%Y-%m-%d %H:%M")
                today = datetime.datetime.today()
                delta = today - upload_time
                if delta.days > days or not item['n'].endswith(ext):
                    continue
                sha1 = self.getsha1(item['pc'])
                name = item['n']
                size = item['s']
                forms.append('#'.join([sha1, name, size]))
        return forms
                                    
      
    def traverse115(self, cid=0):
        data = self.get_fileinfo(cid)
        items = json.loads(data)
        for item in items['data']:
            if 's' in item.keys(): # a file
                pickcode = item['pc']
                #sha1 = self.getsha1(pickcode)
                sha1=''
                size = item['s']
                if int(size) < 2000: continue
                name= item['n']
                self.form.append([pickcode,sha1, size, name])
                pass
            else:
                # here we make 1 to be a string
                if item['aid'] != '1': continue
                self.traverse115(item['cid'])


    def upload_file(self, fname, url, size):
        '从指定的url处上传http链接的文件'
        data = urllib.urlencode({'n': fname,
                                  's': str(size),
                                  'u': url,
                                  })
        headers={'Referer':'http://115.com/',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                 }
        url = 'http://115.com/?ct=offline&ac=add_task'
        req = urllib2.Request(url, data, headers)
        res = self.opener.open(req).read()
        info = json.loads(res)
        return info['state']
    def get_storage_info(self):
        if self.storage_info: return
        query = urllib.urlencode({'_': str(int(time.time())),
                                  'ac':'get_storage_info',
                                  'ct':'ajax',})
        url = "http://115.com/index.php?{query}".format(**locals()) # readable method
        req = urllib2.Request(url=url, headers=self.headers)
        res = self.opener.open(req).read()
        self.storage_info = json.loads(res)  
    def send_req(self, url, data=''):
        ''' 发送 GET请求， 如果结果是json格式则作相应转换，否则返回结果'''
        if not data:
            req = urllib2.Request(url=url, headers=self.headers)
        else:
            req = urllib2.Request(url=url, data=data, headers=self.headers)
        res = self.opener.open(req)
        try:
            return json.loads(res.read())
        except Exception:
            return res
        
    def get_task_info(self):        
        ''' 获取离线下载的情况 '''
        url = 'http://115.com/?ct=offline&ac=list_task&offset=0&_=%s'%str(int(time.time()))
        info = self.send_req(url)
        #{"state":true,"offset":0,"data":[{"tkid":"32183","st":"1","pc":"","n":"\"Hitchcock.2012.BDRip.X264-BMDruCHinYaN.mkv\";","aid":"1","cid":"0","ctid":"1","s":"2198948609","t":"1362884404","fd":"0","ico":"mkv\";","pr":"0.0%"}],"count":"1","page_size":25}
        return info
    
    def del_task(self, taskids):
        ''' 删除任务过程 taskids为任务列表     {u'state': True, u'data': {u'43727': 1}} '''
        url = 'http://115.com/?ct=offline&ac=del_task'
        data = urllib.urlencode(dict([('tkid[%d]', taskids[i]) for i in range(len(taskids))]))
        info = self.send_req(url, data)
        return info  
       
    def clear_task(self):
        info = self.get_task_info()
        taskids = [item['tkid'] for item in info['data']]
        self.del_task(taskids)
        info = self.get_task_info()
        return info['count']

    def search_task(self, name):
        ''' 摸查指定名称的 任务列表'''
        taskids = []
        info = self.get_task_info()
        for item in info['data']:
            if name in item['n']: # find one
                taskids.append(item['tkid'])
        return taskids
    
    def get_process(self, taskid):
        url = 'http://115.com/?ct=offline&ac=process&tkid=%s'%taskid
        res = self.send_req(url)
        return res
    
    def del_file(self, name):
        taskids = self.search_task(name)
        if taskids:
            ret =self.del_task(taskids)
            return ret['state']
        else:
            '%s not found'%name
        

                                                                                                                                                            
                                                                    
def get_115(username='', password=''):
    if username == '':
        return My115(USER, PASSWORD)
    else:
        return My115(username, password)
    
    
def test_upload():
    fname = 'tt0404978.z'
    url = 'ftp://admin:bmdru2012@120.192.81.203:6066/Gambit.2012.BDRip.X264-BMDruCHinYaN/tt0404978.z'   
    size = '2197824183'
    user = get_115()
    user.upload_file(fname, url, size)
def main():
#    username='w39m84a72m77y92@bmdru.co.cc'
#    password = 'bmdruchinyan'
    #username='1398332'
    #password = 'bmdruisgood'
    #form='AE01BA7F1829BB59270E4C607CA9DB032D4D603F#17067964#tt2041321s.z'
    username='1118469'
    password='12345abc'
    user = My115(username, password)
    user.login()
    user.get_storage_info()
    print user.get_recent_lixian(ext='.uue')
if __name__ == '__main__':
    user = get_115()
    name = 'tt0060450.z'
    user.del_file(name)
        

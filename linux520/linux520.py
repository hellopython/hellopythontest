#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#python version:2.7.2

import urllib2
import re
import os
import sys
import urllib
from os.path import basename
from urlparse import urlsplit
try:
  import psutil
except:
  print "please install psutil ex:pypm install psutil"
  sys.exit()

base_url="http://221.232.247.43"
#s_url=[]
#url=[]
#渗透测试类
stcs=['http://221.232.247.43/stcs/index.html',
      'http://221.232.247.43/stcs/index_2.html',
      'http://221.232.247.43/stcs/index_3.html',
      'http://221.232.247.43/stcs/index_4.html',
      'http://221.232.247.43/stcs/index_5.html'
     ]
#安全防护类
aqfh=['http://221.232.247.43/aqfh/index.html']
#最新漏洞类
zxld=['http://221.232.247.43/zxld/index.html','http://221.232.247.43/zxld/index_2.html']
#编程语言
bcyy=['http://221.232.247.43/bcyy/index.html','http://221.232.247.43/bcyy/index_2.html']
#国外视频
gwsp=['http://221.232.247.43/gwsp/index.html',
	  'http://221.232.247.43/gwsp/index_2.html',
	  'http://221.232.247.43/gwsp/index_4.html',
	  'http://221.232.247.43/gwsp/index_5.html',
	  'http://221.232.247.43/gwsp/index_6.html',
	  'http://221.232.247.43/gwsp/index_7.html',
	  'http://221.232.247.43/gwsp/index_8.html'
	 ]
#新手入门
xsrm=['http://221.232.247.43/xsrm/index.html',
	  'http://221.232.247.43/xsrm/index_2.html',
	  'http://221.232.247.43/xsrm/index_3.html'	
	 ]

def real_name(url_list):
	s_url=[]
	url=[]
	d_url=[]
	for x in url_list:
		a=urllib2.urlopen(urllib2.Request(x)).read()
		s=re.findall(r"""\<dt\><a\shref\=\"(.*?)\"\stitle\=\"(.*?)\"\>""",a)
		s_url.extend(s)
	#print s_url
	for x in s_url:
		a=urllib2.urlopen(urllib2.Request(base_url+x[0])).read()
		try:
			s=re.findall(r"""window.open\(\'(.*?)\'""",a)
		except: 
			continue
		if len(s)==0:
			continue
		else:
			url.append((s[0],x[1]))
	for x in url:
		if 'video' in x[0]:
			a=urllib2.urlopen(urllib2.Request(urllib.quote(x[0].lstrip(),safe='://'))).read()
			try:
				s=re.findall(r"""<param name\=\"src\"\svalue\=\"(.*?)\"\/>""",a)
			except:
				continue
			if len(s)==0:
				continue
			else:
				tmp=urllib.quote(x[0].lstrip(),safe='://')+s[0]
				url_tmp=tmp[0:tmp.rfind('/')+1]
				d_url.append((s[0],url_tmp,x[1]))
	return d_url

def url2name(url):
    return basename(urlsplit(url)[2])
#下载指定的文件
def download(url, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url:
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName:
        # we can force to save the file as specified name
        localName = localFileName
    f = open(localName, 'wb')
    f.write(r.read())
    f.close()
#通过进程名获取进程ID
def getpid(process_name):
    p_list=psutil.get_process_list()
    for x in p_list:
      if process_name in str(x):
        return x.pid
      else:
        return 0
#杀死指定进程ID
def killpid(pid):
    p_kill=psutil.Process(pid)
    try:
      p_kill.kill()
    except:
      return 0
#使用swfdump对flash文件进行分析，并提取真实的文件名
def analy_swf(swf_path):
    a=os.popen(r"swfdump.exe -a "+swf_path)
    for x in a:
      real_name=re.findall(r"""<uri>([\S\s]*?)</uri>""",x)
      if len(real_name)>0:
        return real_name[0]
        killpid(getpid("swfdump.exe"))

#下载真实的视频文件
def download_realvideo(swf_url,url,name):
  download(swf_url,'tmp.swf')     
  r_name=analy_swf("tmp.swf")
  print url+r_name
  download(url+r_name,name+"."+r_name.split('.')[1])
  os.remove('tmp.swf')


def video_download(url_list,path):
	#print url_list
	#print path
	for s in url_list:
		#print s[0]
		if '#' in s[0]:
			try:
				real_name=re.findall(r"""<uri>([\S\s]*?)</uri>""",urllib2.urlopen(urllib2.Request(s[1]+s[0].split('_')[0]+'_config.xml')).read())
				#print path+s[2].encode(sys.getfilesystemencoding())+'.'+real_name[0].split('.')[1]
				print s[1]+real_name[0]
				download(s[1]+real_name[0],path+s[2]+'.'+real_name[0].split('.')[1])
			except Exception, e:
				print e
				continue
		elif 'swf' in s[0]:
			try:
				download_realvideo(s[1]+s[0],s[1],path+s[2])
			except:
				continue
		else:
			try:
				print s[1]+s[0]
				download(s[1]+s[0],path+s[2]+'.'+s[0].split('.')[1])
			except:
				continue



#print u'1 处理国外视频'
#b=real_name(gwsp)
#path='gwsp/'
#video_download(b,path)
print u'2 处理渗透测试'
b=real_name(stcs)
path='stcs/'
video_download(b,path)
print u'3 处理安全防护'
b=real_name(aqfh)
path='aqfh/'
video_download(b,path)
print u'4 处理编程语言'
b=real_name(bcyy)
path='bcyy/'
video_download(b,path)
print u'5 处理新手入门'
b=real_name(xsrm)
path='xsrm/'
video_download(b,path)
print u'6 处理最新漏洞'
b=real_name(zxld)
path='zxld/'
video_download(b,path)
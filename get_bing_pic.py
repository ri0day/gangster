#!/bin/python
#-*- coding utf-8 -*-

import re,urllib,os
import time,json
DownLoadDir = '/tmp/pic/'
filename = time.strftime('%Y-%m-%d')+'.jpg'

#the hard way ,find pic url in html source
IDX_URL='http://cn.bing.com'
response = urllib.urlopen(IDX_URL).read()
url = re.search('{url:(.*);}',response)
today_pic_url = url.groups()[0].split(',')[0].replace('\'','')


def fetch_img(url,filename):
	if not os.path.exists(DownLoadDir):
		os.mkdir(DownLoadDir)
	if os.path.exists(DownLoadDir+filename):
		print 'pic already downloaded'
		return 0
	else:
		print 'downloading %s to %s'%(url,DownLoadDir+filename)
		return urllib.urlretrieve(url,DownLoadDir+filename)



#the esay way ,get pic url from api 
#http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1361089515117&FORM=HYLH1
#this api will response json liked text about index page background image.
#the nc parameter is timestamp from local time which we can generate by python module `int(time.mktime(time.localtime()))`

API_URL='http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=%d&FORM=HYLH1'%(int(time.mktime(time.localtime())))
response_easy = urllib.urlopen(API_URL).read()
d = json.loads(response_easy)
today_pic_url_easy = d['images'][0]['url']

#fetch_img(today_pic_url,filename)
fetch_img(today_pic_url_easy,filename)

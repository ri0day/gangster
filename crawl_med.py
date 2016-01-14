#-*-coding:utf-8
import requests
import lxml.html
import sys
tfile = '/tmp/2.html'
def getfile():
    with open(tfile, 'wb') as handle:
        playload = {"curPage":1,"pageSize":4000,"toPage":1}
        url = "http://www.nifdc.org.cn/sell/sgoodsQuery.do?formAction=queryGuestList"
        r = requests.post(url,data = playload)
        if not r.ok:
            print 'no response'
            sys.exit()
        for block in r.iter_content(1024):
            handle.write(block)

def get_data(filepath):
    s = open(filepath,'r').read()
    st = "".join(["%c"%ord(i) for i in s]).decode("gbk")
    doc = lxml.html.fromstring(st)
    for child in doc.xpath('//*[@class="list_tab003"]/tr'):
        status = child.xpath('./td/font/text()') or [u'有货']
        print u"| ".join(child.xpath('./td/input/@value')) + u"|"+ u"|".join(status)

getfile()
get_data(tfile)

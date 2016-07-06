#coding:utf-8
#!/usr/bin/env python

d={'NH':u'南汇','L':u'linux','W':'windows','P':u'生产环境','T':u'测试环境','S':u'预生产环境','QS':u'秋实楼','HZ':u'杭州机房'}

def parse_hostname(hostname):
    hostname=str(hostname)
    localtion=hostname[:2]
    os=hostname[2:3]
    env=hostname[3:4]
    hstr = hostname[4:].split('.')
    serices,ip,domain = (hstr[0],hstr[1],hstr[2]+'.'+hstr[3])
    for item in (localtion,os,env,serices,ip,domain):
        print d.get(item,item)


print '-------------------------------------------'
#generate fake hostname for test
from random import choice
l = choice(['QS','HZ','NH']) 
o = choice(['L','W']) 
e = choice(['P','T','S'])
s = choice(['WEB','DB','LB','cache'])
ip = choice(['10-1-10-10','10-0-1-2','1-0-1-3']) 
dom = choice(['fake.corp','apple.com','google.net']) 

fake_hostname = l+o+e+s+'.'+ip+'.'+dom 

print fake_hostname
parse_hostname(fake_hostname)

print '-------------------------------------------'

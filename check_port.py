#!/usr/bin/python
import sys
import MySQLdb
import ConfigParser
config=ConfigParser.ConfigParser()
config.readfp(open('/tmp/DNS.conf'))
pick_list=config.get('DNS','ip')
hostlist=map(str,pick_list.split(','))

#monitor_user=config.get('check_mysql','username')
#monitor_password=config.get('check_mysql','passwd')

def pingcmd(ip,port):
    import socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)             
    try:
        sk.connect((ip,port))
	yield 'succ'                      #if connection succ make a tag for this connection
    except Exception:
        print ip,port                     # if cant not connection target print ip and port
    	sk.close()


ip_pool_swap=[]
for hosts in hostlist:
	ip=hosts.split(':')[-2]
	port=int(hosts.split(':')[-1])
	try:
    	   ping_stats=pingcmd(ip,port)	
	       status=ping_stats
	except Exception,e:
    		print >> sys.stderr, "ping port error:",e
#    		sys.exit(1)
	if next(status,'over') == 'succ':
#	if (slave_status['Slave_IO_Running'] == 'Yes' and
#    		slave_status['Slave_SQL_Running'] == 'Yes' and
#    		slave_status['Seconds_Behind_Master'] == 0):
#    		print "Cool"
    		isok=1
		    ip_pool_swap.append(ip)
	else:
    		print 'repilication ouch...%s %s'%(ip,port)
    		isok=0
#UNIQ ip pool
ip_pool=list(set(ip_pool_swap))
#print "ip_pool_swap is %s"%ip_pool_swap
#print "real ip pool %s"%ip_pool

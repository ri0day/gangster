#!/usr/bin/python
import sys
import MySQLdb
import ConfigParser
config=ConfigParser.ConfigParser()
config.readfp(open('/tmp/DNS.conf'))
pick_list=config.get('DNS','ip')
hostlist=map(str,pick_list.split(','))

monitor_user=config.get('check_mysql','username')
monitor_password=config.get('check_mysql','passwd')


def runCmd(cmd,ip,port):
    cnx = MySQLdb.connect(user=monitor_user,host=ip,passwd=monitor_password,port=port,connect_timeout=2)
    cur = cnx.cursor()
    cur.execute(cmd)
    columns = tuple( [d[0].decode('utf8') for d in cur.description] )
#    print columns
    row = cur.fetchone()
#    print row
    if row is None:
        raise StandardError("MySQL Server not configured as Slave")
    else:
        result = dict(zip(columns, row))
#	print result
        cur.close()
        cnx.close()
    return result


#b=runCmd('show slave status')
#print b['Slave_IO_Running']
ip_pool_swap=[]
for hosts in hostlist:
	ip=hosts.split(':')[-2]
	port=int(hosts.split(':')[-1])
	try:
    		slave_status = runCmd("SHOW SLAVE STATUS",ip,port)
	except MySQLdb.Error,e:
    		print >> sys.stderr, "There was a MySQL error:",e
    		sys.exit(1)

	if (slave_status['Slave_IO_Running'] == 'Yes' and
    		slave_status['Slave_SQL_Running'] == 'Yes' and
    		slave_status['Seconds_Behind_Master'] == 0):
    		print "Cool"
    		isok=1
		ip_pool_swap.append(ip)
	else:
    		print 'repilication ouch...'
    		isok=0
#UNIQ ip pool
ip_pool=list(set(ip_pool_swap))
#print "ip_pool_swap is %s"%ip_pool_swap
#print "real ip pool %s"%ip_pool

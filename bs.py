#!/usr/local/bin/python
import sys
import MySQLdb
import ConfigParser            
config=ConfigParser.ConfigParser()
config.readfp(open('/tmp/DNS.conf'))
pick_list=config.get('DNS','ip')
hostlist=map(str,pick_list.split(','))

monitor_user=config.get('check_mysql','username')
monitor_password=config.get('check_mysql','passwd')

def pingcmd(ip,port):
    import socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)
    try:
        sk.connect((ip,port))
    except Exception:
        print "exception %s %s"%(ip,port)
        sk.close()
        return (ip,port,'fail')
    return (ip,port,'sucss')


def runCmd(cmd,ip,port):
    cnx = MySQLdb.connect(user=monitor_user,host=ip,passwd=monitor_password,port=port,connect_timeout=2)
    cur = cnx.cursor()
    cur.execute(cmd)
    columns = tuple( [d[0].decode('utf8') for d in cur.description] )                                                               
    row = cur.fetchone()
    if row is None:
        print "not slave config"
#        raise StandardError("MySQL Server not configured as Slave")
        return (ip,port,'fail')
    else:
        result = dict(zip(columns, row))                                                                                            
        cur.close()
        cnx.close()
    return result


def check_all_memcached():
        memcache_ip_pool=[]
        for hosts in hostlist:
                ip=hosts.split(':')[-2]
                port=int(hosts.split(':')[-1])
                try:
                        ping_stats=pingcmd(ip,port)
                except Exception,e:
                        print >> sys.stderr, "ping port error:",e
                if ping_stats[2] == "sucss":
                    memcache_ip_pool.append(ping_stats[0])
                else:
                    print "can't conn to %s: %s"%(ip,port)

        if len(memcache_ip_pool) == 0:
            memcache_ip_pool=['0.0.0.0']
        return memcache_ip_pool

print check_all_memcached()



def check_mysql_host():
    mysql_ip_pool=[]
    config.readfp(open('/tmp/DNS.conf'))
    mysql_pick_list=config.get('check_mysql','ip')
    mysql_hostlist=map(str,mysql_pick_list.split(','))
    for host in mysql_hostlist:
        ip=host.split(':')[-2]
        port=int(host.split(':')[-1])
        try:
            mysql_status=runCmd("show slave status",ip,port)
        except MySQLdb.Error,e:
            print >> sys.stderr, "There was a MySQL error:",e
            sys.exit(1)
        print mysql_status[0],mysql_status[1],mysql_status[2]
#        if  (mysql_status['Slave_IO_Running'] == 'Yes' and
#            mysql_status['Slave_SQL_Running'] == 'Yes' and
#            mysql_status['Seconds_Behind_Master'] == 0):
#            print "Cool"
        mysql_ip_pool.append(ip)

#        else:
#            print "replication ouch... %s"%(ip,port)
    return mysql_ip_pool

print check_mysql_host()

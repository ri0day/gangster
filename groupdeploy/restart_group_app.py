#!/usr/bin/python
from util import MySSH
from ejupay_deploy_config import config46 

project = "account-inrpc cash-inrpc gateway-inrpc kabin-inrpc msg2-inrpc bill-inrpc channel-inrpc gateway-outrpc mb-inrpc timer-inrpc channel-outrpc access-outrpc gateway-mock query-control access-pos access-posfangjs info-inrpc monitor-inrpc console-outrpc"

group = 'group1'

for p in project.split():
    print p,config46[p][group][0]
    print 'running command: '+config46[p]['instance_dir']+'/kill_tom.sh %s'%p 
    s = MySSH(config46[p][group][0])
    s.run(config46[p]['instance_dir']+'/kill_tom.sh %s'%p)
    

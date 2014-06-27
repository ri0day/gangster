text = open('nginx_log.txt','r').readlines()
data={}
for line in text:
    client_ip=line.split()[1]
    bit=line.split()[9]
    if client_ip in data:
        data[client_ip] = {'count':data[client_ip]['count']+1,'bandwidth':int(data[client_ip]['bandwidth'])+int(bit)}
    else:
        data[client_ip]={'count':1,'bandwidth':bit} 

#print data
for ip in data.keys():
	print "ip: %s visit: %s bandwidth: %d KB"%(ip ,data[ip]['count'] ,int(data[ip]['bandwidth'])/1024)

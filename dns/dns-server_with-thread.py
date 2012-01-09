import socket
# -*- coding: utf-8 -*-
import sys, os, time, atexit
import threading,SocketServer
import subprocess
from random import sample

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


class DNSQuery:
  def __init__(self, data):
    self.data=data
    self.dominio=''

    tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.dominio+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])

  def respuesta(self, ip):
    packet=''
    packet+=self.data[:2] + "\x81\x80"
    packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
    packet+=self.data[12:]                                         # Original Domain Name Question
    packet+='\xc0\x0c'                                             # Pointer to domain name
    packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
    packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) 
    return packet


class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        from check import check_mysql_host, check_all_memcached  
        try:
            data = self.request[0]
            addr = self.client_address
            sock = self.request[1]
            p=DNSQuery(data)
            check_func={}
            check_func["www.bs.com."]=check_mysql_host
            check_func["www.sk2.com."]=check_all_memcached
            if p.dominio not in check_func:
                print "iiii"
                cmd="nslookup %s 202.96.209.133|grep -A 5 answer|awk -F: '/Address/{print $NF}'"%p.dominio
                ip=subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
                sock.sendto(p.respuesta(ip), addr)
            else:
                ip="".join(sample(check_func[p.dominio](),1))
                sock.sendto(p.respuesta(ip), addr)
                
            print 'Respuesta: %s -> %s' % (p.dominio, ip)
        except socket.timeout:
            print "socket timeout....!"
            sock.close()
        
        
if __name__ == "__main__":
    server = ThreadedUDPServer(('0.0.0.0', 53), MyUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
   

#!/usr/bin/python
import socket,select
# -*- coding: utf-8 -*-
import sys, os, time, atexit
from signal import SIGTERM
class Daemon:
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the _run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/tmp/dns.stdout', stderr='/tmp/dns.stderr'):
	self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def _daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.chdir("/")
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)
    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self._daemonize()
        self._run()
    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()
    def _run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

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

if __name__ == '__main__':
  class MyDaemon(Daemon):
    def _run(self):
      udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      udps.bind(('',53))
      try:
        while 1:
          infds,outfds,errfds = select.select([udps,],[],[])
          if len(infds) != 0:
            import random
            import subprocess
            from bs import check_all_memcached,check_mysql_host
            data, addr = udps.recvfrom(1024)
            p=DNSQuery(data)
            check_func={}
            check_func["www.bs.com."]=check_mysql_host
            check_func["www.sk2.com."]=check_all_memcached
            if p.dominio not in check_func:
                cmd="nslookup %s 202.96.209.133|grep -A 5 answer|awk -F: '/Address/{print $NF}'"%p.dominio
                ip=subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
                udps.sendto(p.respuesta(ip), addr)
            else:
                ip="".join(random.sample(check_func[p.dominio](),1))
                udps.sendto(p.respuesta(ip), addr)
            print 'Respuesta: %s -> %s' % (p.dominio, ip)
          else:
            print 'no job'
      except KeyboardInterrupt:
            print 'killed by keyboard'
            udps.close()
      finally:
            print 'End'
            udps.close()

  daemon = MyDaemon('/tmp/daemon-example.pid')
  if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
  else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

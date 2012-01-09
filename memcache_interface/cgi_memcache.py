#/usr/bin/python
import pylibmc
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import logging

def Big_Brother_Is_Watching_U(key,msg):
    logger = logging.getLogger(key)
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%Y-%H:%M:%S',)
    file_handler = logging.FileHandler("/data0/m.log")
    file_handler.setFormatter(formatter)  
    logger.addHandler(file_handler)  
    logger.warn(msg)  


class example():
    host = ""
    server = ""
    def __init__(self, host='10.10.93.16',port=11211):                                                                              
        self.host = "%s:%s"%(host, port)
        self.server = pylibmc.Client([self.host])
    def set(self, key, vaule, expiry=0):
        return self.server.set(key, vaule, expiry)

    def get(self, key):
        return self.server.get(key)

    def delete(self,key):
        return self.server.delete(key) 

    def stats(self):
        return self.server.get_stats() 

    def flush_all(self):
        return self.server.flush_all() 


class CacheHandler(BaseHTTPRequestHandler):
#   """test:
#   curl -d "authkey=aaa" -d "action=delete" -d "cachekey=wumin"  http://10.10.93.16:801
#   """
    def address_string(self):
	host,port = self.client_address[:2]
        return host
    def do_GET(self):
        pass

    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            fs = cgi.FieldStorage(fp = self.rfile,headers = self.headers,environ={ 'REQUEST_METHOD':'POST',\
				     'CONTENT_TYPE':self.headers['Content-Type'],'Content-Length':length})

            authkey = fs.getlist('authkey')[0]
            action = fs.getlist('action')[0]
	    try:
                fs_key = fs.getlist('cachekey')[0]
            except:
                fs_key = None

	    try:
                fs_expire = fs.getlist('expire')[0]
            except:
                fs_expire = 0
	    
	    try:
		fs_vaule = fs.getlist('vaule')[0]
	    except:
		fs_vaule = None
            authgroup={'xWJ0FKgrfz6alUX7iY':['10.0.7.15',19861,'jiatao'],\
 		      'GHGIocGYvh4OmEI83R':['10.0.7.15',19862,'jiatao'],\
		      'Xbud1a1SXJcouWzA34':['10.0.7.15',19863,'yejin'],\
                     'lwhDkGfBNhhKgTYkbE':['10.0.7.15',19864,'menggenhua'],\
                     'tyhkA5EfQxDQEaPAI6':['10.0.7.15',19865,'yuanweiqi'],\
                     'wYG4SIxEdKl6hXUneC':['10.0.7.15',19866,'liuyaohua'],\
		     'jYhkA5BfQxDQuaPAIX':['10.0.7.15',19867,'moweirong']}

            if authgroup.get(authkey,'FAIL') != 'FAIL':
                c_host,c_port,c_username =authgroup.get(authkey)
#                print "c_host: %s, c_port: %s" %(c_host,c_port)
                Cache= example(host=c_host,port=int(c_port))
            else:
                self.send_error(500,'invaild key, not allowed')
		Big_Brother_Is_Watching_U(c_username,'AuthKeyError:'+"action: %s fs_key: %s fs_vaule: %s"%(action,fs_key,fs_vaule))
                raise Exception("invaild key")
            if action == "add" and fs_key is not None and fs_vaule is not None:
                Cache.set(fs_key,fs_vaule,int(fs_expire))
                self.send_response(200)        
                self.end_headers()             
                self.wfile.write("True")
            elif action == "delete" and fs_key is not None:
                Cache.delete(fs_key)
                self.send_response(200)
		self.end_headers()
                self.wfile.write("True")
            elif action == "flush_all":
                Cache.flush_all()
                self.send_response(200)
                self.end_headers()
                self.wfile.write("True")
            elif action == "get" and fs_key is not None:
                context=Cache.get(fs_key)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(context)
            else:
                self.send_error(500,'no this action,or your argument wrong')
		Big_Brother_Is_Watching_U(c_username,'CommandError:'+"action: %s fs_key: %s fs_vaule: %s"%(action,fs_key,fs_vaule))

        except Exception,e:
            print "POST ERROR",e
	    msg=e+'ProgramError'+"action: %s fs_key: %s fs_vaule: %s"%(action,fs_key,fs_vaule)
	    print msg
	    Big_Brother_Is_Watching_U(c_username,msg)


def main():

    try:
        server = HTTPServer(('192.168.5.21', 801), CacheHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

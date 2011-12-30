#!/usr/bin/python
from  gevent.pywsgi import WSGIServer
import pylibmc
from cgi import parse_qs
from gevent import monkey
monkey.patch_all()

class Cache_Instance():
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

def app(env, start_response):
    status = '200 OK'
    if env.get('REQUEST_METHOD') != "POST":
        status = '403 Forbiden'
        start_response(status, [('Content-Type', 'text/html')])
        yield 'Only POST ACCEPT'
    else:
        CONTENT_LENGTH = int(env.get('CONTENT_LENGTH',0))
        request_body = env['wsgi.input'].read(CONTENT_LENGTH)
        req_real_string=parse_qs(request_body)
        authkey = req_real_string.get('authkey')[0]
        action = req_real_string.get('action')[0]
        try:
            fs_key = req_real_string.get('cachekey')[0]
        except:
            fs_key = None

        try:
            fs_expire = req_real_string.get('expire')[0]
        except:
            fs_expire = 0

        try:
            fs_vaule = req_real_string.get('vaule')[0]
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
            c_host,c_port =authgroup.get(authkey)
            Cache= Cache_Instance(host=c_host,port=int(c_port))                                                                        
            if action == "add" and fs_key is not None:
                Cache.set(fs_key,fs_vaule,int(fs_expire))
                start_response(status, [('Content-Type', 'text/html')])
                yield 'True'   
            elif action == "delete" and fs_key is not None:
                Cache.delete(fs_key)           
                start_response(status, [('Content-Type', 'text/html')])
                yield 'True'
            elif action == "flush_all":        
                Cache.flush_all()              
                start_response(status, [('Content-Type', 'text/html')])
                yield 'True'
            elif action == "get" and fs_key is not None:
                context=Cache.get(fs_key)      
                start_response(status, [('Content-Type', 'text/html')])
                if context is None:
                    yield 'Null'
                else:
                    yield context
            else:
                status = '500 INTERNAL SERVER ERROR'
                start_response(status, [('Content-Type', 'text/html')])
                yield 'NO This Action'
        else:
            status='403 Forbiden'
            start_response(status, [('Content-Type', 'text/html')])                                     
            yield 'Invaild Key'


def main():

    try:
        server = WSGIServer(('192.168.5.21',801),app)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.kill()

if __name__ == '__main__':
    main()



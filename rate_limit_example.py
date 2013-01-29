#!/usr/bin/python
import pylibmc
import time                   
import hashlib 
from gevent.pywsgi import WSGIServer


cache=pylibmc.Client(['10.10.93.16:11211'])


def application(env, start_response):
 
    token=hashlib.sha1(env['HTTP_COOKIE']).hexdigest()
    print token


    if cache.get(token) is None:

        print 'in'
        stime=time.time()
        count=1
        d={'first_time':stime,'last_time':stime,'count':count,'block_time':None}
        cache.set(token,d,1800)
        return 'new request'
    
    elif (cache.get(token)['last_time'] - cache.get(token)['first_time'])/cache.get(token)['count'] < 0.5:
        print 'block area..'           
        count=cache.get(token)['count'] + 1
        first_time=cache.get(token)['first_time']
        stime=time.time()
        block_time=stime+30            
        d={'first_time':first_time,'last_time':stime,'count':count,'block_time':block_time}
        cache.set(token,d,1800)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'block'
    elif cache.get(token)['block_time'] is not None and time.time() > cache.get(token)['block_time']:  
        print 'in time'
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'blocked'          

    else:
        count=cache.get(token)['count'] + 1
        first_time=cache.get(token)['first_time']
        stime=time.time()
        d={'first_time':first_time,'last_time':stime,'count':count,'block_time':None}
        cache.set(token,d,1800) 
        start_response('200 OK', [('Content-Type', 'text/html')])
        return 'regular request, pass'

if __name__ == '__main__':
    print 'Serving on 8088...'
    WSGIServer(('', 8088), application).serve_forever()

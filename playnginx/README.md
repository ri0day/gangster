# Transcript:
### 运维场景:
#### 1.static server
nginx.conf
`
curl http://localhost 
`
#### 2.http/TCP Reverse proxy
conf.d/http_proxy.conf

`
curl -x127.0.0.1:80 http://httpin.example.com
curl -x127.0.0.1:80 http://httpin.example.com
`

#### 3.location manipulation (rewrite,redirect)
conf.d/loc_manipulation.conf

`  
curl -x127.0.0.1:80 http://loc.example.com/last.html  
curl -x127.0.0.1:80 http://loc.example.com/redirect.html -i -L
curl -x127.0.0.1:80 http://forcehttps.example.com/abz
`
`
curl -x127.0.0.1:80 http://loc.example.com/fake/distro/geek/fake.php -i
curl -x127.0.0.1:80 http://loc.example.com/fake/distro/geek/login.php -i
curl -x127.0.0.1:80 http://loc.example.com/fake/distro/geek/login.jsp -i
`
`
curl -x127.0.0.1:80 http://loc.example.com/saymyname?name=abc -i -L
`

#### 4.basic security handler (url ,arg, useragent , ratelimit ,bandwidth limit)
conf.d/security_play.conf
`
curl -x127.0.0.1:80 http://sec.example.com/protected/secret.html -i
curl -x192.168.0.69:80 http://sec.example.com/protected/secret.html -i
`
`
curl -A "m googlebot xya" -x192.168.0.69:80 http://sec.example.com/crawl
curl  -x192.168.0.69:80 http://sec.example.com/crawl
`
`
curl http://sec.example.com/siege/flood.html
wget http://sec.example.com/download/xyz.img
`

#### 5.cache server 
conf.d/cache.conf
`
curl  http://cache.example.com/index.html -I
`
### 开发场景:
#### 1.api gateway
conf.d/gateway.conf
`
curl -x127.0.0.1:80 http://gateway.example.com/api/services
curl -x127.0.0.1:80 http://gateway.example.com/api/users
`
#### 2.basic auth protection
conf.d/auth.conf
`
curl  -x127.0.0.1:80 http://auth.example.com/index.html 
curl  -x127.0.0.1:80 http://auth.example.com/index.html -u wumin
`
#### 3.http code injection
conf.d/injection.conf
`
curl -x127.0.0.1:80 http://inject.example.com
`
#### 4.http cors headers handler
conf.d/ajax.conf
`
my labtop chrome :http://192.168.0.69/ajax.html
`
#### 5.cookie based routing
conf.d/kbr.conf
`
curl -x127.0.0.1:80  http://cookie.example.com
curl -x127.0.0.1:80 -b 'version_id=v1' http://cookie.example.com
curl -x127.0.0.1:80 -b 'version_id=v2' http://cookie.example.com
`

#### 6.nginx与第三方集成
1.nginx redis lua integration  
conf.d/lua_redis.conf  
conf.d/routing.conf  
conf.d/routing.lua  
conf.d/lua_backend.conf  
`
curl 'http://localhost:8099/redis_set?key=name&val=wumin'
curl 'http://localhost:8099/redis_get?key=name'
`
`
curl -x127.0.0.1:8090 http://lua.example.com/
/opt/nginx/conf.d/routing lua.example.com 127.0.0.1:9001
`
`
for i in $(seq 5); do curl -x127.0.0.1:8090 http://lua.example.com/ ; done
`

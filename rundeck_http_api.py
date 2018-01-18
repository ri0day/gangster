#!/usr/bin/env python
#coding: utf-8
import requests
import json

TOKEN = 'v5zrOoeGRwsKFmFDxcX6McEySA39cYIL'

class RDC(object):
    def __init__(self,token):
        self.headers = {
          'Content-Type':'application/json',
          'Accept': 'application/json',
          'X-Rundeck-Auth-Token': token
        }

    def get(self,url):
        r = requests.get(url,headers = self.headers )
        return r.json()

    def post(self,url,data):
        print data
        r = requests.post(url, data=data, headers = self.headers)
        return json.loads(r.content)


x = RDC(TOKEN)



#print x.get('http://192.168.10.97:4440/api/18/project/tangxiaoseng/jobs')


datas = {
    "loglevel": "debug",
    "argString": "-node node1"
    }



print x.post('http://192.168.0.69:4440/api/18/job/ae25af4e-be17-461f-b2ff-3060d4e7b358/executions', data = json.dumps(datas))

# -*- coding: utf-8 -*-
"""
Spyder Editor

zabbix http api use case
https://www.zabbix.com/documentation/3.0/manual/api
"""

import requests
import json
from random import randint

ZABBIX_URL = 'http://monitor.xyz.com/api_jsonrpc.php'
ZABBIX_HEADER = {'Content-Type':'application/json'}
ZABBIX_USER = 'username'
ZABBIX_PASSWORD = 'password'

def zabbix_request(json_data):
    resp = requests.post(url=ZABBIX_URL,data=json.dumps(json_data),headers=ZABBIX_HEADER,timeout=10)
    if not resp.status_code:
        raise SystemExit('http request failed')
        
    if 'result' not in resp.json():
        raise SystemExit('zabbix api request failed: {}'.format(str(resp.json()['error'])))
    
    return resp.json()
    
    

def zabbix_login(username,password):
    auth_data={
    'jsonrpc' : '2.0',
    'method' : 'user.login',
    'params' : {
          'user' : username,
          'password' : password
    },
    'id':1,
    }
    
    token = zabbix_request(auth_data)['result']
    
    return token
    


def prepare_json_payload(method,params,auth_code):
    json_data=dict()
    json_data.setdefault('method',method)
    json_data.setdefault('params',params)
    json_data.setdefault('jsonrpc',2.0)
    json_data.setdefault('auth', auth_code)
    json_data.setdefault('id', randint(0, 9999))
    return json_data
    
#fetch hosts from specificed hostgroup
#full palyload from api
#fangjs_host_payload= {
#    'jsonrpc': '2.0',
#    'method': 'hostgroup.get',
#    'params': {
#        'output': ['hosts','groupid'],
#        'selectHosts': ['hostid','name','host'],
#        'filter': {
#            'name': [
#                'WWW.xyz.com'
#            ]
#        }
#    }
#}

method = 'hostgroup.get'
query = {
        'output': ['hosts','groupid'],
        'selectHosts': ['hostid','name','host'],
        'filter': {
            'name': [
                'WWW.xyz.com'
            ]
        }
 }

auth_code = zabbix_login(ZABBIX_USER,ZABBIX_PASSWORD)    
final_payload = prepare_json_payload(method,query,auth_code)
result = zabbix_request(final_payload)
print result







#!/bin/env python
# -*- coding: utf-8 -*- 
import time,commands,re
from flask import Flask,g,request,make_response
import hashlib
import xml.etree.ElementTree as ET
api_token = 'your token in here'
app = Flask(__name__)
app.debug=True
@app.route('/auth',methods=['GET','POST'])

def wechat_auth():
    if request.method == 'GET':
        token = api_token
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
	else:
	    return make_response('invalid access')
    else:
        recived_string = request.stream.read()
        xml_recive = ET.fromstring(recived_string)
        touser = xml_recive.find('ToUserName').text
        fromuser = xml_recive.find('FromUserName').text
        content = xml_recive.find('Content').text
	msg_type =  xml_recive.find('MsgType').text
        text_xml_reply_tpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
	if 'cmd' in content:
	    cmd_str = re.search('^cmd.(.*)',content)
	    cmd_str = cmd_str.groups()[0]
	    reply_content = commands.getoutput(cmd_str)
            response = make_response(text_xml_reply_tpl % (fromuser,touser,str(int(time.time())), reply_content))
            response.content_type='application/xml'
            return response
	else:
	    
	    response = make_response(text_xml_reply_tpl % (fromuser,touser,str(int(time.time())), 'no function for you text:%s'%content))
	    return response
if __name__ == '__main__':
	app.run('0.0.0.0',8080)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from datetime import datetime
import sys

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

class Aliyunsms(object):
    """aliyun provider"""
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"
    ACCESS_KEY_ID = "yourkeyid"
    ACCESS_KEY_SECRET = "yourkeysecret"
    sign_name = "yoursignname"
    template_code = "SMS_44360358"

    def __init__(self):
        super(Aliyunsms, self).__init__()
        self.acs_client = AcsClient(Aliyunsms.ACCESS_KEY_ID, Aliyunsms.ACCESS_KEY_SECRET, Aliyunsms.REGION)
        region_provider.modify_point(Aliyunsms.PRODUCT_NAME,Aliyunsms.REGION,Aliyunsms.DOMAIN)

    def send_sms(self, phone_numbers, template_param=None):
        
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(Aliyunsms.template_code)

        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)
        _business_id = uuid.uuid1()
        smsRequest.set_OutId(_business_id)
        smsRequest.set_SignName(Aliyunsms.sign_name);
        smsRequest.set_PhoneNumbers(phone_numbers)
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        with open('/tmp/sms.log',"a") as f:
            f.write("timestamp : %s ,Request params: phone: %s  msg: %s \n"%(timestamp,phone_numbers,template_param))
            f.write("Response: %s \n"%smsResponse)
        return smsResponse

if __name__ == '__main__':

    mobile=str(sys.argv[1]).strip()
    msg=str(sys.argv[2])

    sms = Aliyunsms()
    print sms.send_sms(mobile,msg)


#!/usr/bin/env python
#coding: utf-8
import requests
from lxml import  etree
url = 'http://ws.qunar.com/holidayService.jcp?lane=%E4%B8%8A%E6%B5%B7-%E9%95%BF%E6%B2%99'
r = requests.get(url).text.encode('utf-8')
root = etree.fromstring(r)

for node in root[0]:
        if node.attrib["date"] in [ "2018-02-10","2018-02-11","2018-02-12" ]:
                for child in node:
                        for child_detail in child.attrib.keys():
                                 if child.attrib["type"] == "go" and int(child.attrib["price"])<=650:
                                        print child_detail,child.attrib[child_detail]


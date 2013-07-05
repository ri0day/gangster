#!/usr/bin/python
import requests
import os
import sys
import time,datetime,json

class Logstash:
    def __init__(self,logstash_host,logstash_port,logstash_index,logstash_query_pattern,logstash_time_from,logstash_time_to,fetch_size=0,order_field="@timestamp"):
        self.logstash_host=logstash_host
        self.logstash_port=logstash_port
	self.logstash_index=logstash_index
	self.logstash_query_pattern=logstash_query_pattern
	self.logstash_time_from=logstash_time_from
	self.logstash_time_to=logstash_time_to
	self.fetch_size=fetch_size
	self.order_field=order_field

        self.sample={ "size" : fetch_size,"query": { "filtered": { "query": { "query_string": { "default_operator": "OR", "default_field": "_all", "query": logstash_query_pattern } }, "filter": { "and": { "filters": [ { "range": { "@timestamp": { "from":logstash_time_from, "to": logstash_time_to } } } ] } } } }, "from": 0, "sort": {order_field: { "order" : "ASC" } } }

	self.url='http://'+logstash_host+':'+logstash_port+'/'+logstash_index+'/'+'_search?pretty=true'
	self.data=str(self.sample).replace('\'','\"')
	print str(self.sample).replace('\'','\"')
	print self.url

    def fetch_and_extract(self):
	data=requests.post(self.url,self.data)
	j = data.json()
#	print json.dumps(j,sort_keys=True , indent=4)
	for x in j['hits']['hits']:
	    yield x['_source']['@message']
	

if __name__ == '__main__':

    
    today=datetime.date.today()
    oneday=datetime.timedelta(1)
    yestoday=today-oneday
    query_from_time=yestoday.strftime('%Y-%m-%d')+'T00:00:00+08:00'
    query_to_time=today.strftime('%Y-%m-%d')+'T00:00:00+08:00'
    print "fromtime is %s"%query_from_time
    print "totime is %s"%query_to_time
    index_from_time=yestoday.strftime('%Y.%m.%d')
    index_to_time=today.strftime('%Y.%m.%d')
    print "index fromtime is %s"%'logstash-'+index_from_time
    print "index totime is %s"%'logstash-'+index_to_time
    index_string='logstash-'+index_from_time+','+'logstash-'+index_to_time
    print index_string

    es_host='10.71.216.175'
    es_port='9200'
    query_patterns=['@tags:php AND Fatal','@tags:mysql_slow_log']

    for query_pattern in query_patterns:
	if query_pattern == '@tags:mysql_slow_log':
	    out_filename='mysql_slow.log'
	else:
	    out_filename='php_fatal_error.log'
        log=Logstash(es_host,es_port,index_string,query_pattern,query_from_time,query_to_time,fetch_size=10,order_field="@timestamp")
        for h in log.fetch_and_extract():
            fp=open(out_filename,'a+')
	    fp.write(h+'\n')
        fp.close()

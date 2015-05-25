#!/usr/bin/python
from flask import Flask,request
import xml.etree.ElementTree as etree
from mail import SendMail
app = Flask(__name__)


@app.route('/rundeck/<mailto>',methods=['GET', 'POST'])
def api(mailto):
	#print type(request.data)
	xml = request.data
	root = etree.fromstring(xml)
	jobname = root.getiterator('name')[0].text
	jobid = root.getiterator('execution')[0].attrib['id']
	jobstatus = root.getiterator('execution')[0].attrib['status']
	job_project = root.getiterator('execution')[0].attrib['project']
	job_follow_url = root.getiterator('execution')[0].attrib['href']
	job_start_time = root.getiterator('date-started')[0].text
	job_end_time = root.getiterator('date-ended')[0].text
	
#	print " jobname: %s\n jobid: %s \n jobstatus: %s\n job_project: %s\n job_follow_url: %s\n job_start_time: %s\n job_end_time: %s\n"%(jobname \
#	,jobid,jobstatus,job_project,job_follow_url,job_start_time,job_end_time)
	
	msg = " job name: %s\n jobid: %s \n job status: %s\n job_project: %s\n job_follow_url: %s\n job_start_time: %s\n job_end_time: %s\n"%(jobname \
	,jobid,jobstatus,job_project,job_follow_url,job_start_time,job_end_time)

	subject='rundeck notification: job <%s> %s'%(jobname,jobstatus)
	sender = SendMail('mail.xxx.com','sender@xxx.com',mailto,'sender@xxx.com','sender_password')
	sender.send(msg,subject,filename=None)
	return 'ok'

app.run(host='0.0.0.0',port=555,debug=True)
#example curl htpp://127.0.0.1:555/rundeck/xxx@example.com

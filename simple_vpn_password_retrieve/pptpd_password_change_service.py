#!/usr/bin/env python
import fileinput
import sys,re
from flask import Flask, request,render_template
cfgfile = '/etc/ppp/chap-secrets.bak'
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('chp.html')

@app.route('/resetpwd',methods=['GET','POST'])
def resetpwd():
	if request.method != 'POST':
		return 'only accept post request'
	
	user, oldpassword, newpassword = request.form['username'], request.form['password'], request.form['newpassword']
	i = "\\b%s\\b" % user+' '+'pptpd'+' '+ oldpassword+' '+'*'
        userinfo = open(cfgfile).read()
        match = re.search(i,userinfo)
	print match,user,oldpassword
        if not match:
                return 'username or password incorrect'
	for line in fileinput.input(cfgfile, inplace=1):
		username, password = line.split()[0],line.split()[2]
		if user == username and oldpassword == password:
			pattern_old=username+' '+'pptpd'+' '+oldpassword+' '+'*'
			pattern_new=username+' '+'pptpd'+' '+newpassword+' '+'*'
			line = line.replace(pattern_old,pattern_new)
			sys.stdout.write(line)
		else:
			sys.stdout.write(line)
	return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

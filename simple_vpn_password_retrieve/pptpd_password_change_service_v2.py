#!/usr/bin/env python
import fileinput
import sys,re
from tempfile import mkstemp
from shutil import move
from os import remove, close
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
	if not match:
		return 'username or password incorrect'
	fh, abs_path = mkstemp()
    	new_file = open(abs_path,'w')
    	old_file = open(cfgfile)
    	for line in old_file:
        	username, password = line.split()[0],line.split()[2]
        	if user == username and oldpassword == password:
            		pattern_old=username+' '+'pptpd'+' '+oldpassword+' '+'*'
            		pattern_new=username+' '+'pptpd'+' '+newpassword+' '+'*'
            		new_file.write(line.replace(pattern_old, pattern_new))
            	else:
			new_file.write(line)
    #close temp file
    	new_file.close()
    	close(fh)
    	old_file.close()
    #Remove original file
    	remove(cfgfile)
    #Move new file
    	move(abs_path,cfgfile)
	return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

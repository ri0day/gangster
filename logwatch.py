#!/usr/bin/env python
import os,sys
posfile='/tmp/pos.txt'
"""
usage: python logwatch.py /tmp/logfile.log keyword
"""
def PosCheck(posfile):
	try:
		with open(posfile,'r') as pos:
			position = pos.read()
			if int(position) > 1:
				return int(position)
			else:
				return 0
	except:
		return 'pos file missing or null'

def UpdatePos(position):
	try:
		with open(posfile,'w+')  as pos:
			return pos.write(str(position))
	except:
		return	'pos file missing or permission deine'


def LogMonitor(file, keyword):
	with open(file,'r') as fp:
#		print "os.path.getsize = %d ,Poscheck = %d"%(os.path.getsize(file),PosCheck(posfile))
		if os.path.getsize(file) < PosCheck(posfile):
			text = fp.readlines()
			UpdatePos(fp.tell())
		else:
			fp.seek(PosCheck(posfile),1)
			text = fp.readlines()
			UpdatePos(fp.tell())
		if text:
			for line in text:
				if keyword in line:
					return line
				else:
					return 'not fond'
		else:
			return 'no update'

logstatus = LogMonitor(sys.argv[1],sys.argv[2])
if logstatus == "no update" or logstatus == "not fond":
	print 'OK'
else:
	print 'Fatal Error Appeared: \n'+logstatus

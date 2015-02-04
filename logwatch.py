#!/usr/bin/env python
import os
posfile='/tmp/pos.txt'
import sys
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
		text =  fp.readlines()
		current_pos = int(fp.tell())
		last_pos = PosCheck(posfile)
		print 'current_pos :%s last_pos: %s '%(current_pos ,last_pos)
		if current_pos < last_pos:
			UpdatePos(current_pos)
			if text:
                        	for line in text:
                                	if keyword in line:
                                        	return line
                              		else:
                                        	return 'not fond'
			else:
				return 'emptyfile'	
		elif current_pos == last_pos:
			return 'no update'
		else:
			UpdatePos(current_pos)
			orig_file=open(file,'r')
			orig_file.seek(last_pos,1)
			txt=orig_file.readlines()
			if txt:
				for line in txt:
					if keyword in line:
						return line
					else:
						return 'not fond'
			else:
				return 'emptyfile'
logstatus=LogMonitor(sys.argv[1],sys.argv[2])
if logstatus == "emptyfile":
	print 'File is Empty'
elif logstatus == "not fond":
	print 'not fond keyword in File'
elif logstatus == 'no update':
	print 'File No Update'
else:
	print 'fond keyword %s in %s'%(sys.argv[2],logstatus)

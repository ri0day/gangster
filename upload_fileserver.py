#!/usr/bin/python

# Copyright Jon Berg , turtlemeat.com
# Modified by nikomu @ code.google.com     

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sys import exit
import os # os. path

CWD = os.path.abspath('.')
## print CWD

# PORT = 8080     
UPLOAD_PAGE = 'upload.html' # must contain a valid link with address and port of the server     s




# -----------------------------------------------------------------------

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            
            if self.path == '/' :     
                page = make_index( '.' )
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write('exploit me!')
                return     


            if self.path.endswith(".html"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)
                

                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
                

            else : # default: just send the file     
                
                filepath = self.path[1:] # remove leading '/'     
            
                f = open( os.path.join(CWD, filepath), 'rb' ) 
                #note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                #self.send_header('Content-type',	'application/octet-stream')
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            return # be sure not to fall into "except:" clause ?       
                
        except IOError :  
            # debug     
#            print e
#            self.send_error(404,'File Not Found: %s' % self.path)
             print "get error"
     

    def do_POST(self):
        # global rootnode ## something remained in the orig. code     
		#example curl -F "upfile=@file.txt" -F "keys=1232"  10.10.93.7:801
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))     

            if ctype == 'multipart/form-data' :     

                # original version :     
                '''
                query=cgi.parse_multipart(self.rfile, pdict)
                upfilecontent = query.get('upfile')
                print "filecontent", upfilecontent[0]
                '''

                # using cgi.FieldStorage instead, see 
                # http://stackoverflow.com/questions/1417918/time-out-error-while-creating-cgi-fieldstorage-object     
                fs = cgi.FieldStorage( fp = self.rfile, 
                                       headers = self.headers, # headers_, 
                                       environ={ 'REQUEST_METHOD':'POST' } # all the rest will come from the 'headers' object,     
                                       # but as the FieldStorage object was designed for CGI, absense of 'POST' value in environ     
                                       # will prevent the object from using the 'fp' argument !     
                                     )
                ## print 'have fs'

            else: raise Exception("Unexpected POST request")
                
                
            fs_up = fs['upfile']
            fs_key=fs['keys']
            filename = os.path.split(fs_up.filename)[1]
            fullname = os.path.join(CWD, filename)
            now=time.strftime("%Y-%m-%d_%H:%M:%S",time.localtime())
            if fs_key.value != "28@238sdHDDGC":
                self.send_error(500,'not allowed')
                raise Exception("invaild key")
            # check for copies :     
            if os.path.exists( fullname ): 
                print "fullname is %s" % fullname
                print "fullname+now is %s" % fullname+now
                os.rename(fullname,fullname+now)
#                os.remove(fullname)			
#                fullname_test = fullname + '.copy'
#                i = 0
#                while os.path.exists( fullname_test ):
#                    fullname_test = "%s.copy(%d)" % (fullname, i)
#                    i += 1
#                fullname = fullname_test
                
            if not os.path.exists(fullname):
                o=open(fullname, 'wb')
                    # self.copyfile(fs['upfile'].file, o)
                o.write( fs_up.file.read() )     


            self.send_response(200)
            self.end_headers()
            
            self.wfile.write("<HTML><HEAD></HEAD><BODY>POST OK.<BR><BR>");
            self.wfile.write( "File uploaded under name: " + os.path.split(fullname)[1] );
            self.wfile.write(  '<BR><A HREF=%s>back</A>' % ( UPLOAD_PAGE, )  )
            self.wfile.write("</BODY></HTML>");
            os.popen('/bin/bash /usr/local/tomcat2/bin/restart.sh')
            
        except Exception:
            # pass
#            print e
#            self.send_error(404,'POST to "%s" failed: %s' % (self.path, str(e)) )
             print 'POST ERROR'

def main():

    try:
        server = HTTPServer(('', 801), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()



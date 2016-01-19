import re

class Ngx_Conf_Summary(object):

    def __init__(self,conf_file_path):
        self.r = {}
        self.backend = []
        self.conf_path = conf_file_path
        with open(self.conf_path,'r') as f:
            self.conf_text = f.read().strip()
        self.backend_pattern = r'upstream +(.+)+ {([^}]*)}'
        #self.backend_host_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        self.backend_host_pattern = r'server+\s+.+[:]\d+|server+\s+[a-z1-9.+\w]+'
        self.location_pattern = r'location (.+){'
        self.server_name_pattern = r'server_name (.+);'
        print "-----parse conf file: %s------"%self.conf_path


    def get_server_names(self):
        return "".join(re.findall(r'server_name (.+);',self.conf_text)).split()

    def get_backend_hosts(self):
        backend_list = re.match(self.backend_pattern,self.conf_text).group(2).split(';')
        for backend_text in backend_list:
            if backend_text.strip().startswith('#') or not backend_text:
                pass
            else:
                backend_host = re.findall(self.backend_host_pattern,backend_text.strip())
                backend_host = "".join(backend_host).replace('server ',"")
                if backend_host:
                    self.backend.append(backend_host)

        return self.backend

    def get_location(self):
        return  re.findall(r'location (.+){',self.conf_text)


    def summary(self):
        self.r['file'] = self.conf_path
        self.r['server_names'] = self.get_server_names()
        self.r['location'] = self.get_location()
        self.r['backends'] = self.get_backend_hosts()
        return self.r


ngx_conf=Ngx_Conf_Summary('/tmp/2.vhost')
print ngx_conf.summary()


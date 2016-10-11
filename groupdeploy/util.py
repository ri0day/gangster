#!/anaconda/bin/python
import commands
from ejupay_deploy_config import config46
from os import makedirs, path
from sys import exit
import paramiko
import socket
from time import strftime 


class MySSH(object):
    def __init__(self,host,port=22):
        self.host = host
        self.port = port

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        try:
            self.ssh.connect(host,port,timeout=3)
        except (socket.error, paramiko.AuthenticationException,paramiko.SSHException) as message:
            print message
            exit(1)    
    def __del__(self):
        self.ssh.close()

    def run(self,cmd):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        out , err = ssh_stdout.read() , ssh_stderr.read()
        if out:
            print out
        if err:
           print err


class deploy_instance(object):
    def __init__(self, config, project):
        self.fetch_dir = config['fetch_dir']
        self.full_host = config[project]['groupfull']
        self.group1 = config[project]['group1']
        self.group2 = config[project]['group2']
        self.port = config[project]['port']
        self.instance_dir = config[project]['instance_dir']
        self.war_filename = config[project]['war_filename']
        self.war_file_fullpath = config[project]['war_file_fullpath']
        self.project = project
        self.source_host = config['source_host']
        self.config = config

    def pre_deploy(self):
        if not path.isdir(self.fetch_dir):
            makedirs(self.fetch_dir)

        print 'fetching {project} war file {war_filename} from host {source_host}:{war_file_fullpath} to {fetch_dir}'.format( project=self.project, war_filename=self.war_filename,
            source_host=self.source_host, war_file_fullpath=self.war_file_fullpath, fetch_dir=self.fetch_dir)

        cmd = 'rsync -avzr -e ssh root@{source_host}:{war_file_fullpath} {fetch_dir}'.format(
            source_host=self.source_host, war_file_fullpath=self.war_file_fullpath, fetch_dir=self.fetch_dir)
        
        commands.getoutput(cmd)
        print '[x]runing: {cmd}'.format(cmd=cmd)

    def deploy(self, target):
        if target not in ['group1','group2','groupfull']:
            print 'no such group .break'
            exit(1)
        for host in self.config[self.project][target]:
            webroot = '/data/tomcat/ejupay-'+self.project+'/webapps/'+self.project
            backupdir = '/data/tomcat/backup'
            print 'backup project {projectname} webroot {webroot} to /data/backup on host {remote}'.format(projectname=self.project,webroot=webroot,remote=host)
            backup_cmd = 'mv {webroot} {backupdir}/{project}.{timestamp}'.format(webroot=webroot,backupdir=backupdir,project=self.project,timestamp=strftime('%Y%m%d%H%M%S'))
            print backup_cmd  
            client = MySSH(host,port=22)
            client.run(backup_cmd)
            update_config_cmd = 'svn update --username usertest --password 123456 /opt/app_config/{project}'.format(project=self.project.split('-')[0])
            print '[x] updating project config file'
            client.run(update_config_cmd)
            rsync_cmd = 'rsync -e ssh -avzr {fetch_dir}/{war_filename} {host}:{webroot}'.format(fetch_dir=self.fetch_dir, war_filename=self.war_filename ,host=host ,webroot=self.instance_dir+'/webapps/')
            print '[x] ship code to target host {host}'.format(host=host)
            print rsync_cmd
            commands.getoutput(rsync_cmd)
            restart_tomcat_cmd = '{instance_dir}/kill_tom.sh {project}'.format(instance_dir=self.instance_dir ,project=self.project)                 
            print restart_tomcat_cmd
            client.run(restart_tomcat_cmd)

    def post_deploy(self):
        pass


#d = deploy_instance(config46, 'cash-inrpc')
#d.pre_deploy()
#d.deploy("groupfull")

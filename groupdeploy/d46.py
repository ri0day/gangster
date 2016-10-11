#!/usr/bin/python
from util import deploy_instance
from ejupay_deploy_config import config46 
import sys
print   sys.argv[1] ,sys.argv[2]


project = sys.argv[1]
group = sys.argv[2]

d = deploy_instance(config46, project)
d.pre_deploy()
d.deploy(group)


#!/bin/bash
cd /opt/ejupaydeploy
if  [ $# -nt 2 ]
then
  echo "usage: $0  project-inrpc group1"
  exit 1
else
  project=$1
  group=$2

  python d46.py $project $group

fi


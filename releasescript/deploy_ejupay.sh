#!/bin/bash
deploy_root=/data0/ejupay_deploy
svnuser=usertest
svnpassword=123456
timestamp="$(date +%Y%m%d%H%M%S)"
svn_base_url=http://10.10.88.80/svn/ejupay
dst_host="10.0.57.44"

checkout_code() {

project_name=${1:?"please input valid project name"}
mkdir -p $deploy_root
cd $deploy_root
rm -rf $project_name
if [ -z "$RD_OPTION_CUSTOM_SVN_URL" ]
then
    echo "NO custom svn url ,using default"
    svn --username $svnuser --password $svnpassword -q  co $svn_base_url/trunk/$project_name $project_name
else
    echo "cumstom svn url $RD_OPTION_CUSTOM_SVN_URL"
    svn --username $svnuser --password $svnpassword -q  co $RD_OPTION_CUSTOM_SVN_URL $project_name
fi
echo "[stage-1] check out code... [done] "
}

build_project() {
project_name=${1:?"please input valid project name"}
sub_project_name=${2:?"please input valid sub project name"}

cd $deploy_root/$project_name
if [ -f "pom.xml" ]
echo "[stage-2] in $(pwd)"
then
    source /etc/bashrc
    mvn -q  -f ./pom.xml  -U clean -Dmaven.test.skip=True  package
    if  [ -f "$project_name-war-$sub_project_name/target/$project_name-$sub_project_name.war" ]
        then
           echo "[stage-2]generated WAR package: $project_name-war-$sub_project_name/target/$project_name-$sub_project_name.war" 
     else
           echo "some project build failed,check it $project_name-war-$sub_project_name/target/$project_name-$sub_project_name.war"
           exit
     fi
else
    echo "can not find pom.xml,exit"
    exit
fi
echo "[stage-2] build WAR package [done]"
}

ship_code() {
project_name=${1:?"please input valid project name"}
sub_project_name=${2:?"please input valid sub project name"}
tomcat_base=/data/tomcat/ejupay-$project_name-$sub_project_name
cd $deploy_root/$project_name
war_file=$(find ./ -name $project_name-$sub_project_name.war)
filename=${war_file##*/}
war_file_extract_dir=${filename/.war/}
for host in $dst_host
do
    ssh  root@$host "mv  $tomcat_base/webapps/$filename /data/tomcat/backup/$filename.$timestamp ;mv $tomcat_base/webapps/$war_file_extract_dir /data/tomcat/backup/$war_file_extract_dir.$timestamp"
    echo "[stage-3] update app config-file /opt/app_config/$project_name "
    ssh root@$host "cd /opt/app_config/$project_name;svn --username usertest --password 123456 update"
    echo "[stage-3] copy war file $war_file to $host $tomcat_base/webapps/"
    rsync -avzr -e ssh $war_file root@$host:$tomcat_base/webapps/
done
echo "[stage-3]  done."
}


restart_tomcat() {
project_name=${1:?"please input valid project name"}
sub_project_name=${2:?"please input valid sub project name"}
tomcat_base=/data/tomcat/ejupay-$project_name-$sub_project_name
for host in $dst_host
do
     echo "[stage-4] restart tomcat instance: $tomcat_base"
     ssh root@$host "$tomcat_base/kill_tom.sh $project_name-$sub_project_name"
done

echo "[stage-4] done."
}

wrap() {
project_name=${1:?"please input valid project name"}
sub_project_name=${2:?"please input valid sub project name"}

checkout_code $project_name
build_project $project_name $sub_project_name
ship_code $project_name $sub_project_name
restart_tomcat $project_name $sub_project_name

}
echo "running with: wrap $RD_OPTION_PROJECT_NAME $RD_OPTION_SUB_PROJECT_NAME"
wrap "$RD_OPTION_PROJECT_NAME" "$RD_OPTION_SUB_PROJECT_NAME"
#wrap channel inrpc


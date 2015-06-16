#!/bin/bash
deploy_dir="/data/deploy_root"
webroot="/data/app/wwwroot"
timestamp="$(date +%Y%m%d%H%M%S)"
. /opt/release
deploy_index(){
cd $deploy_dir
if [ ! -d "$deploy_dir/$1" ]
        then
                git clone git@git.ipo.com:dev1/$1.git --recursive
		cd $1
		mkdir version
        else
                echo "remove old version index,and fech newist version"
		mkdir -p $deploy_dir/$1/version
		mv $deploy_dir/$1/version /tmp/
		rm -rf $deploy_dir/$1	
		git clone git@git.ipo.com:dev1/$1.git --recursive
		mv /tmp/version $deploy_dir/$1/
fi
cd $deploy_dir/$1
version=$(cat .git/refs/heads/master)
echo "fetch index code version: $version success"
echo $version >version.txt
chown www.www $deploy_dir/$1/  -R
echo "---start sync local deploy dir to local webroot---"
rsync  -ar --delete $deploy_dir/$1/ $webroot/$1/
echo "---sync local deploy dir to local webroot done---"

do_sync "$WEBS" "$webroot/$1/"
}

deploy_project(){
cd $deploy_dir
mkdir -p "$deploy_dir/$1/"
cd "$deploy_dir/$1/"
if [ $# -lt 2 ]
then
	echo "usage :deploy_project cms ga or deploy_project cms beta "
	exit
else
	if [[ "$2" == "beta_to_beta" ]]
	then
		git clone  git@git.ipo.com:dev1/$1.git $timestamp --recursive
		cd $timestamp
		git checkout -b beta origin/beta
		echo "$timestamp" > $deploy_dir/index/version/$1.beta
		version=$(cat .git/refs/heads/master)
		echo "fetch index code version: $version success"
		echo $version >version.txt
		echo "---start sync local deploy dir to local webroot---"
		chown www.www $deploy_dir/$1/$timestamp -R
		rsync  -ar --delete $deploy_dir/$1/$timestamp $webroot/$1/
		cp -a $deploy_dir/index/version/$1.beta  $webroot/index/version/
		do_sync "$WEBS" "$webroot/$1/$timestamp/"
		do_sync "$WEBS" "$webroot/index/version/$1.beta"
		echo "---sync local deploy dir to local webroot done---"
	elif [[ "$2" == "master_to_beta" ]]
	then
		git clone  git@git.ipo.com:dev1/$1.git $timestamp --recursive
                cd $timestamp
		echo "$timestamp" > $deploy_dir/index/version/$1.beta
		echo "$timestamp" > $deploy_dir/index/version/$1.ga
                version=$(cat .git/refs/heads/master)
                echo "fetch index code version: $version success"
                echo $version >version.txt
                echo "---start sync local deploy dir to local webroot---"
		chown www.www $deploy_dir/$1/$timestamp -R
                rsync  -ar --delete $deploy_dir/$1/$timestamp $webroot/$1/
		cp -a $deploy_dir/index/version/$1.beta  $webroot/index/version/
		echo "---sync local deploy dir to local webroot done---"
		do_sync "$WEBS" "$webroot/$1/$timestamp/"
		do_sync "$WEBS" "$webroot/index/version/$1.beta"
	elif [[ "$2" == "master_to_ga" ]]
	then
		if [ -f "$deploy_dir/index/version/$1.ga" ]
		then
			v="$(cat $deploy_dir/index/version/$1.ga)"
			if [ -d "$webroot/$1/$v" ]
			then
				echo "****release $1 to ga ,TimeStamp: $v ,git_version: $(cat $webroot/$1/$v/version.txt)****"
				cp -a $deploy_dir/index/version/$1.ga  $webroot/index/version/
				do_sync "$WEBS" "$webroot/index/version/$1.ga"
			else
				echo "no ga dir $v in $1"
				exit 1
			fi
		else
			echo "no $1.ga file in $deploy_dir/index/version/"
		fi
	else
		echo "there is no branch $1"
	fi
fi
}
#THIS IS START FOR MANUALLY DEPPLOY INSTRUCTION: 
#1.when add new project,create project dir on production webserver webroot first.#(rundeck or ssh  mkdir -p /data/app/wwwroot/$prjectname)
#2.start deploy manually (defualt project deploy process: beta_to_beta-->master_to_beta-->master_to_ga ,index style project process: just ship code to production server)
#3.configure the rundeck ,add job
#4.config nginx ,sync nginx configuration to all webservers

#example of add touchweb project to deploy pipeline

#1.pre deploy:create project dir on production webserver 

#for host in 10.0.16.3 10.0.16.4 10.0.16.5 10.0.16.8  10.0.16.10 10.0.16.11
#    do
#         ssh $host (/bin/mkdir -p /data/app/wwwroot/touchweb;/bin/chown www.www /data/app/wwwroot/touchweb)
#    done

#2.ship code to production webserver   

#deploy_project touchweb beta_to_beta
#deploy_project touchweb master_to_beta
#deploy_project touchweb master_to_ga

#3. login rundeck , add job http://10.0.5.7:4440
#4. config nginx, sync config file. reload nginx

deploy_index wxadmin

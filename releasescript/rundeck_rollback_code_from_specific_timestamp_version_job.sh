#!/bin/bash
debug_output() {
echo "@option.project_name@ , @option.version_timestamp@" 
}

project="@option.project_name@"
timestamp="@option.version_timestamp@"
index_version_root="/data/app/wwwroot/index/version"
webroot="/data/app/wwwroot/"

rollback_code() {
if [ -z "$project" -o  -z "$timestamp" ]
then
    echo "arg project or timestamp is null,check again"
elif [ ! -f "$index_version_root"/"$project".ga  ] 
then
    echo "project route ga file :"$index_version_root"/"$project".ga not exist,check again"
elif [ ! -d "$webroot"/"$project"/"$timestamp" ]
then
    echo "rollback dir "$webroot"/"$project"/"$timestamp" not exist."
else
     current_version=$(cat "$index_version_root"/"$project".ga)
     current_git_version=$(cat "$webroot"/"$project"/"$current_version"/version.txt)
     to_git_version=(cat "$webroot"/"$project"/"$timestamp"/version.txt)
     /bin/cp -a "$index_version_root"/"$project".ga "$index_version_root"/"$project".ga.$RANDOM
     echo "$timestamp" > "$index_version_root"/"$project".ga
     echo "rollback $project from {timestamp: $current_version ,git-version: $current_git_version} to {timestamp: $timestamp ,git-version: $to_git_version } success"
fi  

}

rollback_code

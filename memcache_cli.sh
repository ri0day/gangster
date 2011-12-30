#!/bin/bash
#filename cm.sh
#author:wumin 
#---Date:2011.12.29 pm---

#notice:not suport kind of ubuntu and debian system.(debian not suport /dev/tcp/host/port stye ) 


usage() {
	format_usage="Usage:\n
	\t\t $0 [-hpck] \n \
	\t\t [-h]\t memcached hostname or ip. \n \
	\t\t [-p]\t memcached port.\n \
	\t\t [-c]\t command. \n \
	\t\t [-k]\t key or prefix key."
	echo -e $format_usage
}

sendmsg()
{
	msg=$1
	echo -e  "$1\r">&8
	getout
}

getout()
{
       while read -u 8 -d $'\r' name
        do
        if [ "${name}" == "END"  -o "${name}" == "ERROR" ];then
            break
        fi
        echo $name
        done
}


stats() {
	sendmsg "stats"
	sendmsg "quit"

}

list_items_num() {
	sendmsg "stats items"
	sendmsg "quit"

}
get_last_items_id() {
	LastID=$(list_items_num|tail -n 1|awk -F':' '{print $2}')
	sendmsg "quit"
	echo $LastID
	return $LastID
}

list_all_key() {
	:>/dev/shm/cm_all_keys_$MCSERVER_$MCPORT.txt
	max_item_num=$(get_last_items_id)
	for i in `seq 1 $max_item_num`
	  do
		echo -e "stats cachedump $i 0\r"|nc $MCSERVER $MCPORT|awk '{print $2}'
	        #这里有点问题,以后看看,先nc粗暴解决一下

	       #sendmsg "stats cachedump $i 0"
	      #1>>/dev/shm/cm_all_keys_$MCSERVER_$MCPORT.txt
	done >>/dev/shm/cm_all_keys_$MCSERVER_$MCPORT.txt 
	sed -i '/^$/d' /dev/shm/cm_all_keys_$MCSERVER_$MCPORT.txt
}

get() {
	sendmsg "get $1"
	sendmsg "quit"
}

purge() {
	sendmsg "delete $1\r\n"
	sendmsg "quit"
}

superpurge() {
	list_all_key
	if [ ! -z "/dev/shm/cm_all_keys_$MCSERVER_$MCPORT.txt" ];then
	   grep "$1" /dev/shm/cm_all_keys_$MCSERVER_$MCPORT.txt >/dev/shm/temp.swap.$MCSERVER_$MCPORT.txt
	fi
	while read keys 
	   do
	  #这里也有一些问题.我擦.没理由啊.nc暴力解决
	  #sendmsg "delete ${keys}\r"
	  echo -e "delete ${keys}\r"|nc $MCSERVER $MCPORT
	done </dev/shm/temp.swap.$MCSERVER_$MCPORT.txt

	rm -rf /dev/shm/temp.swap.$MCSERVER_$MCPORT.txt
}



if [ "$?" != "0" ];then
    echo "open $host  $port fail!"
    exit 1
fi

if [ "$#" -le 4 ];then
    usage
    exit 1
fi

while getopts  "h:p:c:k:" flag
  do
    case $flag in
        h)MCSERVER=$OPTARG
        echo "host = $MCSERVER"
        ;;
        p)MCPORT=$OPTARG
        echo "PORT = $MCPORT"
        ;;
        c)command=${OPTARG:="stats"}
        echo "command = $command"
        ;;
        k)key=$OPTARG
        echo "key is $key"
    esac
done

exec 8<>/dev/tcp/${MCSERVER}/${MCPORT}

eval $command "$key"



exec 8<&-
exec 8>&-
exit 0

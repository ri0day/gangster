#!/bin/bash
#hostfile format like :
#1,10.0.2.24, map_pic_storage,wumin,22
#2,10.0.2.25,dcserver,wumin,22

VERSION="0.01"
TITLE="~~simple~portal~~ $VERSION"
HOSTSFILE="/opt/ip.txt"
STATUS_FILE=/opt/selection.txt
WIDTH=40
HEIGHT=30
MENUSIZE=8
DIALOG='/usr/bin/dialog'
ALINES=($(awk 'BEGIN{FS=","} {print $1}' $HOSTSFILE | wc -l))
LINES=($(awk 'BEGIN{FS=","} {print $1,$2}' $HOSTSFILE))
HOSTNAMES=($(awk 'BEGIN{FS=","} {print $3}' $HOSTSFILE))
USERNAME=($(awk 'BEGIN{FS=","} {print $4}' $HOSTSFILE))
HOSTIP=($(awk 'BEGIN{FS=","} {print $2}' $HOSTSFILE))
HOSTPORT=($(awk 'BEGIN{FS=","} {print $5}' $HOSTSFILE))

MENUSIZE=$ALINES
$DIALOG  --cancel-label "Exit" --ok-label "Connect" --menu "$TITLE" $HEIGHT $WIDTH $MENUSIZE ${LINES[*]} 2>$STATUS_FILE
idx=$(cat $STATUS_FILE)
dix=$(($idx-1))
[[ -z "$idx" ]]&&exit||ssh ${USERNAME[dix]}@${HOSTIP[dix]} -p ${HOSTPORT[dix]}
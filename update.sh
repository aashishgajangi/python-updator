#!/bin/bash
passwd=$1
ropath=$2
exe_unzip=$3
exe_zip=$4
backuplocation=$5
targetfirmware=$6
temp=$7
unzip_folder=$8
#unzip proccess 
rm -rf $unzip_folder
$exe_unzip -q -P $passwd $targetfirmware -d $temp &&
cd $unzip_folder
#backup 
if md5sum -c md5sum.md5; then
#run killall script
#/home/epcnc/bin/killscript.sh
#####Backup###################
#### Remounting#bin############## 
#mount -o remount,rw /dev/mmcblk1p2
cp * $ropath
#tar -czvf $5 $2/*.vxe $2/*.out

#else
echo "Akash" > /root/eplogs
#fi
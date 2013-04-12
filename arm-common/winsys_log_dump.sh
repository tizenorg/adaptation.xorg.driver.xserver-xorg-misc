#!/bin/sh

#--------------------------------------
#   winsys
#--------------------------------------
export DISPLAY=:0.0
WINSYS_DEBUG=$1/winsys
E17_HOME=/home/app
mkdir -p ${WINSYS_DEBUG}
xinfo -p 2> ${WINSYS_DEBUG}/ping.log
xinfo -xwd_topvwins ${WINSYS_DEBUG}
cp -af /opt/var/log/keygrab_status.txt ${WINSYS_DEBUG}
screenshot bmp ${WINSYS_DEBUG}/slp_screenshot.bmp
xinfo -topvwins 2> ${WINSYS_DEBUG}/xinfo_topvwins.txt
xdbg clist > ${WINSYS_DEBUG}/xdbg_clist.log 2>&1
xdbg drmevent_pending > ${WINSYS_DEBUG}/drmevent_pending.log 2>&1
xberc drmmode_dump > ${WINSYS_DEBUG}/drmmode_dump.log
find /var/log/ -name "*Xorg*" -exec cp {} ${WINSYS_DEBUG}/ \;
xprop -root -f _E_LOG 8s -set _E_LOG ${E17_HOME}/e.log
cat ${E17_HOME}/e.log > ${WINSYS_DEBUG}/e.log
border_win_info -p ALL -f ${E17_HOME}/e_illume2.log
cat ${E17_HOME}/e_illume2.log > ${WINSYS_DEBUG}/e_illume2.log
e_comp_util -l DUMP_INFO -f ${E17_HOME}/e_comp.log
cat ${E17_HOME}/e_comp.log > ${WINSYS_DEBUG}/e_comp.log
cat ${E17_HOME}/e_comp.log_move > ${WINSYS_DEBUG}/e_comp.log_move
rm ${E17_HOME}/e.log
rm ${E17_HOME}/e_comp.log
rm ${E17_HOME}/e_comp.log_move
rm ${E17_HOME}/e_illume2.log

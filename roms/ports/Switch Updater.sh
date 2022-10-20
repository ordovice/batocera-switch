#!/bin/sh
######################################################################
#
#             SWITCH EMULATORS UPDATER FOR BATOCERA
#             /userdata/roms/ports/UDPATE-SWITCH.sh
# 
#             -> github.com/ordovice/batocera-switch
#
######################################################################
FONTSIZE=44
###########
function batocera-switch-updater {
######################################################################
file_yuzuea=/userdata/system/switch/yuzuEA.AppImage
file_yuzu=/userdata/system/switch/yuzu.AppImage
file_ryujinx=/userdata/system/switch/Ryujinx.AppImage
file_ryujinxavalonia=/userdata/system/switch/Ryujinx-Avalonia.AppImage
######################################################################
R='\033[1;31m' # Red
W='\033[0;37m' # White
echo -e "${R}-------------------------------------"
echo -e "${W}SWITCH EMULATORS UPDATER FOR BATOCERA"
echo
sleep 0.5
######################################################################
#### YUZU EA #########################################################
echo -e "${R}   ///////////////"
echo -e "${R}  ///// ${W}1/4${R} /////    ${W}UPDATING YUZU EA..."
echo -e "${R} ///////////////"
wget -q --show-progress -O $file_yuzuea $(curl -s https://api.github.com/repos/pineappleEA/pineapple-src/releases | grep "browser_download_url.*Yuzu-EA-.*AppImage" | head -n 1 | cut -d : -f 2,3 | tr -d \")
chmod a+x $file_yuzuea 2>/dev/null
size_yuzuea=$(($(wc -c $file_yuzuea | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${R}$file_yuzuea ${R}($size_yuzuea( )MB) ${W}OK" | sed 's/( )//g'
echo
######################################################################
#### YUZU ############################################################
echo -e "${R}   ///////////////"
echo -e "${R}  ///// ${W}2/4${R} /////    ${W}UPDATING YUZU..."
echo -e "${R} ///////////////"
wget -q --show-progress -O $file_yuzu $(curl -s https://api.github.com/repos/yuzu-emu/yuzu-mainline/releases/latest | grep "browser_download_url.*AppImage" | cut -d : -f 2,3 | sed 1q | tr -d \")
chmod a+x $file_yuzu 2>/dev/null
size_yuzu=$(($(wc -c $file_yuzu | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${R}$file_yuzu ${R}($size_yuzu( )MB) ${W}OK" | sed 's/( )//g'
echo
######################################################################
#### RYUJINX #########################################################
echo -e "${R}   ///////////////"
echo -e "${R}  ///// ${W}3/4${R} /////    ${W}UPDATING RYUJINX..."
echo -e "${R} ///////////////"
wget -q --show-progress -O $file_ryujinx https://github.com/qurious-pixel/Ryujinx/releases/download/continuous/Ryujinx-x86_64.AppImage
chmod a+x $file_ryujinx 2>/dev/null
size_ryujinx=$(($(wc -c $file_ryujinx | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${R}$file_ryujinx ${R}($size_ryujinx( )MB) ${W}OK" | sed 's/( )//g'
echo
######################################################################
#### RYUJINX-AVALONIA ################################################
echo -e "${R}   ///////////////"
echo -e "${R}  ///// ${W}4/4${R} /////    ${W}UPDATING RYUJINX AVALONIA..."
echo -e "${R} ///////////////"
wget -q --show-progress -O $file_ryujinxavalonia https://github.com/qurious-pixel/Ryujinx/releases/download/avalonia-build/Ryujinx-x86_64.AppImage
chmod a+x $file_ryujinxavalonia 2>/dev/null
size_ryujinxavalonia=$(($(wc -c $file_ryujinxavalonia | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${R}$file_ryujinxavalonia ${R}($size_ryujinxavalonia( )MB) ${W}OK" | sed 's/( )//g'
echo
######################################################################
sleep 0.5
echo -e "${R}-------------------------------------"
echo -e "${W}          SWITCH EMULATORS UPDATED OK"
echo -e "${W}"
sleep 1
}
######################################################################
export -f batocera-switch-updater
######################################################################
DISPLAY=:0.0 LC_CTYPE=en_US.UTF-8 xterm -bg black -fa 'Monospace' -fs $FONTSIZE -e bash -c "batocera-switch-updater" 2>/dev/null
######################################################################
exit 0
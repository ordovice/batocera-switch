#!/usr/bin/env bash
######################################################################
#                SWITCH EMULATORS UPDATER FOR BATOCERA               #
#               ----------------------------------------             #
#                    > https://discord.gg/hH5AfThG                   #
#                > github.com/ordovice/batocera-switch               #
######################################################################
#   EMULATORS    /                                                   #
#===============/                                                    #
EMULATORS="YUZU YUZUEA RYUJINX RYUJINXAVALONIA"                      #
# DEFAULT:                                                           #
# EMULATORS="YUZU YUZUEA RYUJINX RYUJINXAVALONIA"                    #
# EMULATORS="RYUJINX YUZU" -> will only update ryujinx & then yuzu   #
# EMULATORS="YUZUEA"       -> will only update yuzu early access     #
######################################################################
#   CONFIG    /
#============/
TEXT_SIZE=AUTO
TEXT_COLOR=WHITE
THEME_COLOR=WHITE
THEME_COLOR_OK=WHITE
THEME_COLOR_YUZU=RED
THEME_COLOR_YUZUEA=RED
THEME_COLOR_RYUJINX=BLUE
THEME_COLOR_RYUJINXAVALONIA=BLUE
# AVAILABLE COLORS:
# WHITE,BLACK,RED,GREEN,BLUE,YELLOW,PURPLE,CYAN
# DARKRED,DARKGREEN,DARKBLUE,DARKYELLOW,DARKPURPLE,DARKCYAN#
######################################################################
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@                @@@@@            @@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@                   @@@@@                @@@@@@@@@@@@@@@
# @@@@@@@@@@@     @@@@@@@@@@@@    @@@@@                  @@@@@@@@@@@@@
# @@@@@@@@@     @@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@@@      @@@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@         @@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@@        @@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@   %@@@@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@       @@@@        @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@     @@@@@@@@      @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@    @@@@@@@@@@     @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@     @@@@@@@@      @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@        @@         @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@@
# @@@@@@@@@@     @@@@@@@@@@@@@    @@@@@                  @@@@@@@@@@@@@
# @@@@@@@@@@@@      @@@@@@@@@@    @@@@@                @@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@                 @@@@@             @@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                > github.com/ordovice/batocera-switch               #
#                    > https://discord.gg/hH5AfThG                   #
######################################################################
######################################################################
######################################################################
######################################################################
# PREPARE SHORTCUTS FOR F1-APPLICATIONS MENU
# -------------------------------------------------------------------
function generate-shortcut-launcher {
# FOR GUI APPS: 
SCALE=1.50
Name=$1
name=$2
# --------
extra=/userdata/system/switch/extra/$Name.desktop
shortcut=/usr/share/applications/$Name.desktop
launcher=/userdata/system/switch/extra/batocera-switch-launcher-$Name
# --------
rm -rf $shortcut 2>/dev/null && rm -rf $launcher 2>/dev/null
echo "[Desktop Entry]" >> $shortcut
echo "Version=1.0" >> $shortcut
echo "Icon=/userdata/system/switch/extra/switch.png" >> $shortcut
echo "Exec=$launcher" >> $shortcut
echo "Terminal=false" >> $shortcut
echo "Type=Application" >> $shortcut
echo "Categories=Game;batocera.linux;" >> $shortcut
echo "Name=$name" >> $shortcut
echo "#!/bin/bash" >> $launcher
echo "DISPLAY=:0.0 QT_SCALE_FACTOR=$SCALE GDK_SCALE=$SCALE /userdata/system/switch/$Name.AppImage" >> $launcher
chmod a+x $launcher
cp $shortcut $extra 2>/dev/null
} # -----------------------------------------------------------------
generate-shortcut-launcher 'yuzu' 'yuzu'
generate-shortcut-launcher 'yuzuEA' 'yuzuea'
generate-shortcut-launcher 'Ryujinx' 'ryujinx'
generate-shortcut-launcher 'Ryujinx-Avalonia' 'ryujinx-avalonia'
# -------------------------------------------------------------------
# PREPARE STARTUP FILE
# -------------------------------------------------------------------
startup=/userdata/system/switch/extra/batocera-switch-startup
rm -rf $startup
echo '#!/bin/bash' >> $startup 
echo 'extra=/userdata/system/switch/extra' >> $startup
echo 'cp $extra/batocera-switch-lib* /lib/ 2>/dev/null' >> $startup
echo 'cp $extra/lib* /lib/ 2>/dev/null' >> $startup
echo 'cp $extra/*.desktop /usr/share/applications/ 2>/dev/null' >> $startup
chmod a+x $startup
# -------------------------------------------------------------------
# ADD TO BATOCERA AUTOSTART > /USERDATA/SYSTEM/CUSTOM.SH 
# -------------------------------------------------------------------
customsh=/userdata/system/custom.sh
startup=/userdata/system/switch/extra/batocera-switch-startup
if [[ -e "$startup" ]] && [[ $(wc -c $startup) != "0" ]]; then 
  if [[ "$(cat $customsh | grep $startup)" = "" ]]; then
   echo $startup >> $customsh
  fi
  if [[ "$(cat $customsh | grep $startup | grep "#")" != "" ]]; then
   echo $startup >> $customsh
  fi
fi
######################################################################
######################################################################
######################################################################
######################################################################
if [[ "$EMULATORS" = "DEFAULT" ]] || [[ "$EMULATORS" = "default" ]] \
|| [[ "$EMULATORS" = "ALL" ]] || [[ "$EMULATORS" = "all" ]]; then
EMULATORS="YUZU YUZUEA RYUJINX RYUJINXAVALONIA"; fi
if [ "$(echo $EMULATORS | grep "-")" = "" ]; then 
EMULATORS="$EMULATORS-"; fi
EMULATORS=$(echo $EMULATORS | sed 's/ /-/g')
# -------------------------------------------------------------------
temp=/userdata/system/switch/extra/downloads
mkdir $temp 2>/dev/null && clear 
# TEXT & THEME COLORS: 
###########################
RED='\033[1;31m'      	  # red
BLUE='\033[1;34m'         # blue
GREEN='\033[1;32m'        # green
YELLOW='\033[1;33m'       # yellow
PURPLE='\033[1;35m'       # purple
CYAN='\033[1;36m'         # cyan
#-------------------------#
DARKRED='\033[0;31m'      # darkred
DARKBLUE='\033[0;34m'     # darkblue
DARKGREEN='\033[0;32m'    # darkgreen
DARKYELLOW='\033[0;33m'   # darkyellow
DARKPURPLE='\033[0;35m'   # darkpurple
DARKCYAN='\033[0;36m'     # darkcyan
#-------------------------#
WHITE='\033[0;37m'        # white
BLACK='\033[0;30m'        # black
###########################
# PARSE COLORS FOR THEMING:
# ---------------------------------------------------------------------------------- 
if [ "$TEXT_COLOR" = "RED" ]; then TEXT_COLOR="$RED"; fi
if [ "$TEXT_COLOR" = "BLUE" ]; then TEXT_COLOR="$BLUE"; fi
if [ "$TEXT_COLOR" = "GREEN" ]; then TEXT_COLOR="$GREEN"; fi
if [ "$TEXT_COLOR" = "YELLOW" ]; then TEXT_COLOR="$YELLOW"; fi
if [ "$TEXT_COLOR" = "PURPLE" ]; then TEXT_COLOR="$PURPLE"; fi
if [ "$TEXT_COLOR" = "CYAN" ]; then TEXT_COLOR="$CYAN"; fi
if [ "$TEXT_COLOR" = "DARKRED" ]; then TEXT_COLOR="$DARKRED"; fi
if [ "$TEXT_COLOR" = "DARKBLUE" ]; then TEXT_COLOR="$DARKBLUE"; fi
if [ "$TEXT_COLOR" = "DARKGREEN" ]; then TEXT_COLOR="$DARKGREEN"; fi
if [ "$TEXT_COLOR" = "DARKYELLOW" ]; then TEXT_COLOR="$DARKYELLOW"; fi
if [ "$TEXT_COLOR" = "DARKPURPLE" ]; then TEXT_COLOR="$DARKPURPLE"; fi
if [ "$TEXT_COLOR" = "DARKCYAN" ]; then TEXT_COLOR="$DARKCYAN"; fi
if [ "$TEXT_COLOR" = "WHITE" ]; then TEXT_COLOR="$WHITE"; fi
if [ "$TEXT_COLOR" = "BLACK" ]; then TEXT_COLOR="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
if [ "$THEME_COLOR" = "RED" ]; then THEME_COLOR="$RED"; fi
if [ "$THEME_COLOR" = "BLUE" ]; then THEME_COLOR="$BLUE"; fi
if [ "$THEME_COLOR" = "GREEN" ]; then THEME_COLOR="$GREEN"; fi
if [ "$THEME_COLOR" = "YELLOW" ]; then THEME_COLOR="$YELLOW"; fi
if [ "$THEME_COLOR" = "PURPLE" ]; then THEME_COLOR="$PURPLE"; fi
if [ "$THEME_COLOR" = "CYAN" ]; then THEME_COLOR="$CYAN"; fi
if [ "$THEME_COLOR" = "DARKRED" ]; then THEME_COLOR="$DARKRED"; fi
if [ "$THEME_COLOR" = "DARKBLUE" ]; then THEME_COLOR="$DARKBLUE"; fi
if [ "$THEME_COLOR" = "DARKGREEN" ]; then THEME_COLOR="$DARKGREEN"; fi
if [ "$THEME_COLOR" = "DARKYELLOW" ]; then THEME_COLOR="$DARKYELLOW"; fi
if [ "$THEME_COLOR" = "DARKPURPLE" ]; then THEME_COLOR="$DARKPURPLE"; fi
if [ "$THEME_COLOR" = "DARKCYAN" ]; then THEME_COLOR="$DARKCYAN"; fi
if [ "$THEME_COLOR" = "WHITE" ]; then THEME_COLOR="$WHITE"; fi
if [ "$THEME_COLOR" = "BLACK" ]; then THEME_COLOR="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
if [ "$THEME_COLOR_OK" = "RED" ]; then THEME_COLOR_OK="$RED"; fi
if [ "$THEME_COLOR_OK" = "BLUE" ]; then THEME_COLOR_OK="$BLUE"; fi
if [ "$THEME_COLOR_OK" = "GREEN" ]; then THEME_COLOR_OK="$GREEN"; fi
if [ "$THEME_COLOR_OK" = "YELLOW" ]; then THEME_COLOR_OK="$YELLOW"; fi
if [ "$THEME_COLOR_OK" = "PURPLE" ]; then THEME_COLOR_OK="$PURPLE"; fi
if [ "$THEME_COLOR_OK" = "CYAN" ]; then THEME_COLOR_OK="$CYAN"; fi
if [ "$THEME_COLOR_OK" = "DARKRED" ]; then THEME_COLOR_OK="$DARKRED"; fi
if [ "$THEME_COLOR_OK" = "DARKBLUE" ]; then THEME_COLOR_OK="$DARKBLUE"; fi
if [ "$THEME_COLOR_OK" = "DARKGREEN" ]; then THEME_COLOR_OK="$DARKGREEN"; fi
if [ "$THEME_COLOR_OK" = "DARKYELLOW" ]; then THEME_COLOR_OK="$DARKYELLOW"; fi
if [ "$THEME_COLOR_OK" = "DARKPURPLE" ]; then THEME_COLOR_OK="$DARKPURPLE"; fi
if [ "$THEME_COLOR_OK" = "DARKCYAN" ]; then THEME_COLOR_OK="$DARKCYAN"; fi
if [ "$THEME_COLOR_OK" = "WHITE" ]; then THEME_COLOR_OK="$WHITE"; fi
if [ "$THEME_COLOR_OK" = "BLACK" ]; then THEME_COLOR_OK="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
if [ "$THEME_COLOR_YUZU" = "RED" ]; then THEME_COLOR_YUZU="$RED"; fi
if [ "$THEME_COLOR_YUZU" = "BLUE" ]; then THEME_COLOR_YUZU="$BLUE"; fi
if [ "$THEME_COLOR_YUZU" = "GREEN" ]; then THEME_COLOR_YUZU="$GREEN"; fi
if [ "$THEME_COLOR_YUZU" = "YELLOW" ]; then THEME_COLOR_YUZU="$YELLOW"; fi
if [ "$THEME_COLOR_YUZU" = "PURPLE" ]; then THEME_COLOR_YUZU="$PURPLE"; fi
if [ "$THEME_COLOR_YUZU" = "CYAN" ]; then THEME_COLOR_YUZU="$CYAN"; fi
if [ "$THEME_COLOR_YUZU" = "DARKRED" ]; then THEME_COLOR_YUZU="$DARKRED"; fi
if [ "$THEME_COLOR_YUZU" = "DARKBLUE" ]; then THEME_COLOR_YUZU="$DARKBLUE"; fi
if [ "$THEME_COLOR_YUZU" = "DARKGREEN" ]; then THEME_COLOR_YUZU="$DARKGREEN"; fi
if [ "$THEME_COLOR_YUZU" = "DARKYELLOW" ]; then THEME_COLOR_YUZU="$DARKYELLOW"; fi
if [ "$THEME_COLOR_YUZU" = "DARKPURPLE" ]; then THEME_COLOR_YUZU="$DARKPURPLE"; fi
if [ "$THEME_COLOR_YUZU" = "DARKCYAN" ]; then THEME_COLOR_YUZU="$DARKCYAN"; fi
if [ "$THEME_COLOR_YUZU" = "WHITE" ]; then THEME_COLOR_YUZU="$WHITE"; fi
if [ "$THEME_COLOR_YUZU" = "BLACK" ]; then THEME_COLOR_YUZU="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
if [ "$THEME_COLOR_YUZUEA" = "RED" ]; then THEME_COLOR_YUZUEA="$RED"; fi
if [ "$THEME_COLOR_YUZUEA" = "BLUE" ]; then THEME_COLOR_YUZUEA="$BLUE"; fi
if [ "$THEME_COLOR_YUZUEA" = "GREEN" ]; then THEME_COLOR_YUZUEA="$GREEN"; fi
if [ "$THEME_COLOR_YUZUEA" = "YELLOW" ]; then THEME_COLOR_YUZUEA="$YELLOW"; fi
if [ "$THEME_COLOR_YUZUEA" = "PURPLE" ]; then THEME_COLOR_YUZUEA="$PURPLE"; fi
if [ "$THEME_COLOR_YUZUEA" = "CYAN" ]; then THEME_COLOR_YUZUEA="$CYAN"; fi
if [ "$THEME_COLOR_YUZUEA" = "DARKRED" ]; then THEME_COLOR_YUZUEA="$DARKRED"; fi
if [ "$THEME_COLOR_YUZUEA" = "DARKBLUE" ]; then THEME_COLOR_YUZUEA="$DARKBLUE"; fi
if [ "$THEME_COLOR_YUZUEA" = "DARKGREEN" ]; then THEME_COLOR_YUZUEA="$DARKGREEN"; fi
if [ "$THEME_COLOR_YUZUEA" = "DARKYELLOW" ]; then THEME_COLOR_YUZUEA="$DARKYELLOW"; fi
if [ "$THEME_COLOR_YUZUEA" = "DARKPURPLE" ]; then THEME_COLOR_YUZUEA="$DARKPURPLE"; fi
if [ "$THEME_COLOR_YUZUEA" = "DARKCYAN" ]; then THEME_COLOR_YUZUEA="$DARKCYAN"; fi
if [ "$THEME_COLOR_YUZUEA" = "WHITE" ]; then THEME_COLOR_YUZUEA="$WHITE"; fi
if [ "$THEME_COLOR_YUZUEA" = "BLACK" ]; then THEME_COLOR_YUZUEA="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
if [ "$THEME_COLOR_RYUJINX" = "RED" ]; then THEME_COLOR_RYUJINX="$RED"; fi
if [ "$THEME_COLOR_RYUJINX" = "BLUE" ]; then THEME_COLOR_RYUJINX="$BLUE"; fi
if [ "$THEME_COLOR_RYUJINX" = "GREEN" ]; then THEME_COLOR_RYUJINX="$GREEN"; fi
if [ "$THEME_COLOR_RYUJINX" = "YELLOW" ]; then THEME_COLOR_RYUJINX="$YELLOW"; fi
if [ "$THEME_COLOR_RYUJINX" = "PURPLE" ]; then THEME_COLOR_RYUJINX="$PURPLE"; fi
if [ "$THEME_COLOR_RYUJINX" = "CYAN" ]; then THEME_COLOR_RYUJINX="$CYAN"; fi
if [ "$THEME_COLOR_RYUJINX" = "DARKRED" ]; then THEME_COLOR_RYUJINX="$DARKRED"; fi
if [ "$THEME_COLOR_RYUJINX" = "DARKBLUE" ]; then THEME_COLOR_RYUJINX="$DARKBLUE"; fi
if [ "$THEME_COLOR_RYUJINX" = "DARKGREEN" ]; then THEME_COLOR_RYUJINX="$DARKGREEN"; fi
if [ "$THEME_COLOR_RYUJINX" = "DARKYELLOW" ]; then THEME_COLOR_RYUJINX="$DARKYELLOW"; fi
if [ "$THEME_COLOR_RYUJINX" = "DARKPURPLE" ]; then THEME_COLOR_RYUJINX="$DARKPURPLE"; fi
if [ "$THEME_COLOR_RYUJINX" = "DARKCYAN" ]; then THEME_COLOR_RYUJINX="$DARKCYAN"; fi
if [ "$THEME_COLOR_RYUJINX" = "WHITE" ]; then THEME_COLOR_RYUJINX="$WHITE"; fi
if [ "$THEME_COLOR_RYUJINX" = "BLACK" ]; then THEME_COLOR_RYUJINX="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "RED" ]; then THEME_COLOR_RYUJINXAVALONIA="$RED"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "BLUE" ]; then THEME_COLOR_RYUJINXAVALONIA="$BLUE"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "GREEN" ]; then THEME_COLOR_RYUJINXAVALONIA="$GREEN"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "YELLOW" ]; then THEME_COLOR_RYUJINXAVALONIA="$YELLOW"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "PURPLE" ]; then THEME_COLOR_RYUJINXAVALONIA="$PURPLE"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "CYAN" ]; then THEME_COLOR_RYUJINXAVALONIA="$CYAN"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "DARKRED" ]; then THEME_COLOR_RYUJINXAVALONIA="$DARKRED"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "DARKBLUE" ]; then THEME_COLOR_RYUJINXAVALONIA="$DARKBLUE"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "DARKGREEN" ]; then THEME_COLOR_RYUJINXAVALONIA="$DARKGREEN"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "DARKYELLOW" ]; then THEME_COLOR_RYUJINXAVALONIA="$DARKYELLOW"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "DARKPURPLE" ]; then THEME_COLOR_RYUJINXAVALONIA="$DARKPURPLE"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "DARKCYAN" ]; then THEME_COLOR_RYUJINXAVALONIA="$DARKCYAN"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "WHITE" ]; then THEME_COLOR_RYUJINXAVALONIA="$WHITE"; fi
if [ "$THEME_COLOR_RYUJINXAVALONIA" = "BLACK" ]; then THEME_COLOR_RYUJINXAVALONIA="$BLACK"; fi
# ---------------------------------------------------------------------------------- 
# PREPARE COOKIE FOR FUNCTIONS: 
rm -rf /userdata/system/switch/updater.settings
echo "TEXT_SIZE=$TEXT_SIZE" >> /userdata/system/switch/updater.settings
echo "TEXT_COLOR=$TEXT_COLOR" >> /userdata/system/switch/updater.settings
echo "THEME_COLOR=$THEME_COLOR" >> /userdata/system/switch/updater.settings
echo "THEME_COLOR_YUZU=$THEME_COLOR_YUZU" >> /userdata/system/switch/updater.settings
echo "THEME_COLOR_YUZUEA=$THEME_COLOR_YUZUEA" >> /userdata/system/switch/updater.settings
echo "THEME_COLOR_RYUJINX=$THEME_COLOR_RYUJINX" >> /userdata/system/switch/updater.settings
echo "THEME_COLOR_RYUJINXAVALONIA=$THEME_COLOR_RYUJINXAVALONIA" >> /userdata/system/switch/updater.settings
echo "THEME_COLOR_OK=$THEME_COLOR_OK" >> /userdata/system/switch/updater.settings
echo "EMULATORS=$EMULATORS" >> /userdata/system/switch/updater.settings
####################################################################################
function update_emulator {
E=$1 && N=$2
# ---------------------------------------------------------------------------------- 
# LINKS & RESOLVERS:
# ---------------------------------------------------------------------------------- 
# YUZU
release_yuzu=$(curl -s https://github.com/yuzu-emu/yuzu-mainline/releases | grep /releases/tag/ | head -n 1 | cut -d = -f 4 | cut -d \" -f 2 | cut -d "/" -f 6)
date_yuzu=$(curl -s https://github.com/yuzu-emu/yuzu-mainline/releases/tag/$release_yuzu | grep "datetime=" | sed 's/^.*datetime/datetime/g' | cut -d \" -f 2 | cut -c 1-10 | sed 's/-//g')
subrelease_yuzu=$(curl -s https://github.com/yuzu-emu/yuzu-mainline/releases/tag/$release_yuzu | grep data-hovercard-url | grep commit-link | head -n 1 | cut -d "=" -f 4 | cut -d "/" -f 7 | cut -c 1-9)
  link_yuzu=https://github.com/yuzu-emu/yuzu-mainline/releases/download/$release_yuzu/yuzu-mainline-$date_yuzu-$subrelease_yuzu.AppImage
# ---------------------------------------------------------------------------------- 
# YUZU EA
release_yuzuea=$(curl -s https://github.com/pineappleEA/pineapple-src | grep /releases/ | cut -d "=" -f 5 | cut -d / -f 6 | cut -d '"' -f 1)
  link_yuzuea=https://github.com/pineappleEA/pineapple-src/releases/download/$release_yuzuea/Linux-Yuzu-$release_yuzuea.AppImage
# ---------------------------------------------------------------------------------- 
# RYUJINX
  link_ryujinx=https://github.com/qurious-pixel/Ryujinx/releases/download/continuous/Ryujinx-x86_64.AppImage
# ---------------------------------------------------------------------------------- 
# RYUJINX-AVALONIA
  link_ryujinxavalonia=https://github.com/qurious-pixel/Ryujinx/releases/download/avalonia-build/Ryujinx-x86_64.AppImage
# ---------------------------------------------------------------------------------- 
# PATHS: 
path_yuzu=/userdata/system/switch/yuzu.AppImage
path_yuzuea=/userdata/system/switch/yuzuEA.AppImage
path_ryujinx=/userdata/system/switch/Ryujinx.AppImage
path_ryujinxavalonia=/userdata/system/switch/Ryujinx-Avalonia.AppImage
#
temp=/userdata/system/switch/extra/downloads
# ---------------------------------------------------------------------------------- 
# READ SETTINGS FROM COOKIE: 
TEXT_SIZE=$(cat /userdata/system/switch/updater.settings | grep "TEXT_SIZE=" | cut -d "=" -f 2)
TEXT_COLOR=$(cat /userdata/system/switch/updater.settings | grep "TEXT_COLOR=" | cut -d "=" -f 2)
THEME_COLOR=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR=" | cut -d "=" -f 2)
THEME_COLOR_YUZU=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZU=" | cut -d "=" -f 2)
THEME_COLOR_YUZUEA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZUEA=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINX=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINX=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXAVALONIA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINXAVALONIA=" | cut -d "=" -f 2)
THEME_COLOR_OK=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_OK=" | cut -d "=" -f 2)
EMULATORS=$(cat /userdata/system/switch/updater.settings | grep "EMULATORS=" | cut -d "=" -f 2)
# ---------------------------------------------------------------------------------- 
# RUN UPDATER FOR SELECTED EMULATOR:
# ---------------------------------------------------------------------------------- 
if [ "$3" = "YUZU" ]; then
T=$THEME_COLOR_YUZU
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING YUZU ..."
echo -e "${T} ///////////////"
echo -e "${T}$link_yuzu" | sed 's,https://,> ,g' 2>/dev/null
rm -rf $temp/yuzu 2>/dev/null
mkdir $temp/yuzu 2>/dev/null
cd $temp/yuzu
curl --progress-bar --remote-name --location $link_yuzu
cd $temp
mv $temp/yuzu/* $path_yuzu 2>/dev/null
chmod a+x /userdata/system/switch/yuzu.AppImage 2>/dev/null
size_yuzuea=$(($(wc -c /userdata/system/switch/yuzu.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path_yuzu ${T}($size_yuzuea( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
# ---------------------------------------------------------------------------------- 
if [ "$3" = "YUZUEA" ]; then
T=$THEME_COLOR_YUZUEA
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING YUZU EA ..."
echo -e "${T} ///////////////"
echo -e "${T}$link_yuzuea" | sed 's,https://,> ,g' 2>/dev/null
rm -rf $temp/yuzuea 2>/dev/null
mkdir $temp/yuzuea 2>/dev/null
cd $temp/yuzuea
curl --progress-bar --remote-name --location $link_yuzuea
cd $temp
mv $temp/yuzuea/* $path_yuzuea 2>/dev/null
chmod a+x $path_yuzuea 2>/dev/null
size_yuzuea=$(($(wc -c $path_yuzuea | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path_yuzuea ${T}($size_yuzuea( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
# ---------------------------------------------------------------------------------- 
if [ "$3" = "RYUJINX" ]; then
T=$THEME_COLOR_RYUJINX
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING RYUJINX ..."
echo -e "${T} ///////////////"
echo -e "${T}$link_ryujinx" | sed 's,https://,> ,g'
rm -rf $temp/ryujinx 2>/dev/null
mkdir $temp/ryujinx 2>/dev/null
cd $temp/ryujinx
curl --progress-bar --remote-name --location $link_ryujinx
cd $temp
mv $temp/ryujinx/* $path_ryujinx 2>/dev/null
chmod a+x $path_ryujinx 2>/dev/null
size_ryujinx=$(($(wc -c $path_ryujinx | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path_ryujinx ${T}($size_ryujinx( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
# ---------------------------------------------------------------------------------- 
if [ "$3" = "RYUJINXAVALONIA" ]; then
T=$THEME_COLOR_RYUJINXAVALONIA
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING RYUJINX AVALONIA ..."
echo -e "${T} ///////////////"
echo -e "${T}$link_ryujinxavalonia" | sed 's,https://,> ,g'
rm -rf $temp/ryujinxavalonia 2>/dev/null
mkdir $temp/ryujinxavalonia 2>/dev/null
cd $temp/ryujinxavalonia
curl --progress-bar --remote-name --location $link_ryujinxavalonia
cd $temp
mv $temp/ryujinxavalonia/* $path_ryujinxavalonia 2>/dev/null
chmod a+x $path_ryujinxavalonia 2>/dev/null
size_ryujinxavalonia=$(($(wc -c $path_ryujinxavalonia | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path_ryujinxavalonia ${T}($size_ryujinxavalonia( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
}
export -f update_emulator
######################################################################
function batocera_update_switch { 
######################################################################
# EMULATOR FILES & PATHS: --------------------------------------------
path=/userdata/system/switch
YUZUEA=/userdata/system/switch/yuzuEA.AppImage
YUZU=/userdata/system/switch/yuzu.AppImage
RYUJINX=/userdata/system/switch/Ryujinx.AppImage
RYUJINXAVALONIA=/userdata/system/switch/Ryujinx-Avalonia.AppImage
# --------------------------------------------------------------------
######################################################################
# READ SETTINGS FROM COOKIE: -----------------------------------------
TEXT_SIZE=$(cat /userdata/system/switch/updater.settings | grep "TEXT_SIZE=" | cut -d "=" -f 2)
TEXT_COLOR=$(cat /userdata/system/switch/updater.settings | grep "TEXT_COLOR=" | cut -d "=" -f 2)
THEME_COLOR=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR=" | cut -d "=" -f 2)
THEME_COLOR_YUZU=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZU=" | cut -d "=" -f 2)
THEME_COLOR_YUZUEA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZUEA=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINX=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINX=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXAVALONIA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINXAVALONIA=" | cut -d "=" -f 2)
THEME_COLOR_OK=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_OK=" | cut -d "=" -f 2)
EMULATORS=$(cat /userdata/system/switch/updater.settings | grep "EMULATORS=" | cut -d "=" -f 2)
# -------------------------
F=$TEXT_COLOR
T=$THEME_COLOR
# REREAD TEXT/THEME COLORS:
###########################
RED='\033[1;31m'          # red
BLUE='\033[1;34m'         # blue
GREEN='\033[1;32m'        # green
YELLOW='\033[1;33m'       # yellow
PURPLE='\033[1;35m'       # purple
CYAN='\033[1;36m'         # cyan
#-------------------------#
DARKRED='\033[0;31m'      # darkred
DARKBLUE='\033[0;34m'     # darkblue
DARKGREEN='\033[0;32m'    # darkgreen
DARKYELLOW='\033[0;33m'   # darkyellow
DARKPURPLE='\033[0;35m'   # darkpurple
DARKCYAN='\033[0;36m'     # darkcyan
#-------------------------#
WHITE='\033[0;37m'        # white
BLACK='\033[0;30m'        # black
###########################
clear
echo -e "${T}-------------------------------------"
echo -e "${F}SWITCH EMULATORS UPDATER FOR BATOCERA"
echo
# UPDATE 4 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" != "" ]]; then
update_emulator 1 4 $(echo "$EMULATORS" | cut -d "-" -f 1)
update_emulator 2 4 $(echo "$EMULATORS" | cut -d "-" -f 2)
update_emulator 3 4 $(echo "$EMULATORS" | cut -d "-" -f 3)
update_emulator 4 4 $(echo "$EMULATORS" | cut -d "-" -f 4)
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}      ${TEXT_COLOR}4/4${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# UPDATE 3 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" != "" ]]; then
update_emulator 1 3 $(echo "$EMULATORS" | cut -d "-" -f 1)
update_emulator 2 3 $(echo "$EMULATORS" | cut -d "-" -f 2)
update_emulator 3 3 $(echo "$EMULATORS" | cut -d "-" -f 3)
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}      ${TEXT_COLOR}3/3${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# UPDATE 2 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 2)" != "" ]]; then
update_emulator 1 2 $(echo "$EMULATORS" | cut -d "-" -f 1)
update_emulator 2 2 $(echo "$EMULATORS" | cut -d "-" -f 2)
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}      ${TEXT_COLOR}2/2${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# UPDATE 1 EMULATOR ---------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 2)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 1)" != "" ]]; then
update_emulator 1 1 $(echo "$EMULATORS" | cut -d "-" -f 1)
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}                  EMULATOR UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# CLEAR TEMP & COOKIE:
rm -rf /userdata/system/switch/extra/downloads
rm /userdata/system/switch/extra/display.settings
# KEEP OUTPUT FOR VISIBILITY:
sleep 3
exit 0
}
export -f batocera_update_switch
######################################################################
# PREPARE DISPLAY OUTPUT: 
function get-xterm-fontsize {
#\
  tput="/userdata/system/switch/extra/batocera-switch-tput"
  libtinfo="/userdata/system/switch/extra/batocera-switch-libtinfo.so.6"
  url_tput="https://github.com/ordovice/batocera-switch/raw/main/system/switch/extra/batocera-switch-tput"
  url_libtinfo="https://github.com/ordovice/batocera-switch/raw/main/system/switch/extra/batocera-switch-libtinfo.so.6"
  settings="/userdata/system/switch/extra/display.settings"
  rm $settings 2>/dev/null
  if [[ -e "$tput" ]]; then
      if [[ $(wc -c $tput | awk '{print $1}') = "0" ]]; then
      wget -q -O $tput $url_tput
      chmod +x $tput
      fi
  else
  wget -q -O $tput $url_tput
  chmod +x $tput
  fi
  if [[ -e "/lib/libtinfo.so.6" ]]; then
      if [[ $(wc -c /lib/libtinfo.so.6 | awk '{print $1}') = "0" ]]; then
      wget -q -O $libtinfo $url_libtinfo
      cp $libtinfo /lib/ 2>/dev/null
      fi
  else
  wget -q -O $libtinfo $url_libtinfo
  cp $libtinfo /lib/ 2>/dev/null
  fi
  DISPLAY=:0.0 xterm -fullscreen -bg "black" -fa "Monospace" -e bash -c "sleep 0.042 && $tput cols >> $settings" 2>/dev/null
  cols=$(cat $settings | tail -1) 2>/dev/null
  TEXT_SIZE=$(bc <<<"scale=0;$cols/16") 2>/dev/null
#/
}
export -f get-xterm-fontsize 2>/dev/null
# --------------------------------------------------------------------
# FIND PROPER TEXT SIZE: 
get-xterm-fontsize 2>/dev/null
settings="/userdata/system/switch/extra/display.settings"
cols=$(cat $settings | tail -1) 2>/dev/null
until [[ "$cols" != "80" ]] 
do 
get-xterm-fontsize 2>/dev/null
cols=$(cat $settings | tail -1) 2>/dev/null
done 
######################################################################
# RUN THE UPDATER: 
  DISPLAY=:0.0 xterm -bg black -fa 'Monospace' -fs $TEXT_SIZE -e bash -c "batocera_update_switch" 2>/dev/null 
######################################################################
exit 0
######

#!/bin/bash
######################################################################
#=====================================================================
#                                                                    |
#                SWITCH EMULATORS UPDATER FOR BATOCERA               |
#               ----------------------------------------             |
#                            save this as:                           |
#                /userdata/roms/ports/UPDATE-SWITCH.sh               |
#               ----------------------------------------             |
#                                                                    |
#                    > https://discord.gg/hH5AfThG                   |
#                > github.com/ordovice/batocera-switch               |
#                                                                    |
#=====================================================================
#######################################################################
#   _________     //
#   EMULATORS    //
#===============//
#
EMULATORS="YUZU YUZUEA RYUJINX RYUJINXAVALONIA"
#
# DEFAULT:
# EMULATORS="YUZU YUZUEA RYUJINX RYUJINXAVALONIA"
#
# EMULATORS="RYUJINX YUZU"   ->   will only update ryujinx & then yuzu
# EMULATORS="YUZUEA"         ->   will only update yuzu early access
######################################################################
#   ______     //
#   CONFIG    //
#============//
#
TEXT_SIZE=AUTO
# TRY 22 TO 66 IF AUTO DOESN'T WORK / ALSO SEE BELOW * * * * * * * * * 
#
# --------------
TEXT_COLOR=WHITE
THEME_COLOR=WHITE
THEME_COLOR_OK=WHITE
THEME_COLOR_YUZU=RED
THEME_COLOR_YUZUEA=RED
THEME_COLOR_RYUJINX=BLUE
THEME_COLOR_RYUJINXAVALONIA=BLUE
#
# AVAILABLE COLORS:
# WHITE,BLACK,RED,GREEN,BLUE,YELLOW,PURPLE,CYAN
# DARKRED,DARKGREEN,DARKBLUE,DARKYELLOW,DARKPURPLE,DARKCYAN#
######################################################################
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@                @@@@@            @@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@                   @@@@@                @@@@@@@@@@@@@@
# @@@@@@@@@@@@     @@@@@@@@@@@@    @@@@@                  @@@@@@@@@@@@
# @@@@@@@@@@     @@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@@      @@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@         @@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@        @@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@   %@@@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@     @@@@@@@@      @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@    @@@@@@@@@@     @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@     @@@@@@@@      @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@        @@         @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@    @@@@@@@@@@@@@@@    @@@@@                   @@@@@@@@@@@
# @@@@@@@@@@@     @@@@@@@@@@@@@    @@@@@                  @@@@@@@@@@@@
# @@@@@@@@@@@@@      @@@@@@@@@@    @@@@@                @@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@                 @@@@@             @@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
#               > github.com/ordovice/batocera-switch
#                   > https://discord.gg/hH5AfThG
#
######################################################################
# * * *
# * * *
# * * *) RE: AUTO TEXT SIZE 
#
# auto text size doesn't always work well, depending on many things, 
# including some really, really weird stuff. if it doesn't work for you 
# try changing base font size: 
------------------------------
------------------------------
BASE_FONT_SIZE=14
------------------------------
------------------------------
# settings this ^ with TEXT_SIZE=AUTO helps the updater to adjust size 
# if you change resolutions in batocera. otherwise if you only use one
# resolution in batocera you can just use TEXT_SIZE= in the beginning
#
# ---------------------------------------------------------------------
# ps. you can also use EMULATORS=ALL
#######################################################################
#
if [[ "$EMULATORS" = "DEFAULT" ]] || [[ "$EMULATORS" = "default" ]] \
|| [[ "$EMULATORS" = "ALL" ]] || [[ "$EMULATORS" = "all" ]]; then
EMULATORS="YUZU YUZUEA RYUJINX RYUJINXAVALONIA"; fi
if [ "$(echo $EMULATORS | grep "-")" = "" ]; then 
EMULATORS="$EMULATORS-"; fi
EMULATORS=$(echo $EMULATORS | sed 's/ /-/g')
#
######################################################################
# prepare settings for functions
#
# text/theme colors: 
###########################
RED='\033[1;31m'      	  # red
BLUE='\033[1;34m'         # blue
GREEN='\033[1;32m'        # green
YELLOW='\033[1;33m'       # yellow
PURPLE='\033[1;35m'       # purple
CYAN='\033[1;36m'         # cyan
#                         |
DARKRED='\033[0;31m'      # darkred
DARKBLUE='\033[0;34m'     # darkblue
DARKGREEN='\033[0;32m'    # darkgreen
DARKYELLOW='\033[0;33m'   # darkyellow
DARKPURPLE='\033[0;35m'   # darkpurple
DARKCYAN='\033[0;36m'     # darkcyan
#                         |
WHITE='\033[0;37m'        # white
BLACK='\033[0;30m'        # black
###########################
# parse colors to code:
#
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
#
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
#
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
#
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
#
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
#
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
#
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
#
# prepare a temporary cookie file for functions: 
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
######################################################################
#
# - - - - -
#
######################################################################
function update_emulator {
E=$1 && N=$2
############################
# read settings from cookie: 
TEXT_SIZE=$(cat /userdata/system/switch/updater.settings | grep "TEXT_SIZE=" | cut -d "=" -f 2)
TEXT_COLOR=$(cat /userdata/system/switch/updater.settings | grep "TEXT_COLOR=" | cut -d "=" -f 2)
THEME_COLOR=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR=" | cut -d "=" -f 2)
THEME_COLOR_YUZU=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZU=" | cut -d "=" -f 2)
THEME_COLOR_YUZUEA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZUEA=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINX=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINX=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXAVALONIA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINXAVALONIA=" | cut -d "=" -f 2)
THEME_COLOR_OK=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_OK=" | cut -d "=" -f 2)
EMULATORS=$(cat /userdata/system/switch/updater.settings | grep "EMULATORS=" | cut -d "=" -f 2)
path=/userdata/system/switch
############################
# check todo:
if [ "$3" = "YUZUEA" ]; then
T=$THEME_COLOR_YUZUEA
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING YUZU EA ..."
echo -e "${T} ///////////////"
wget -q --show-progress -O $path/yuzuEA.AppImage $(curl -s https://api.github.com/repos/pineappleEA/pineapple-src/releases | grep "browser_download_url.*Yuzu-EA-.*AppImage" | head -n 1 | cut -d : -f 2,3 | tr -d \")
chmod a+x $path/yuzuEA.AppImage 2>/dev/null
size_yuzuea=$(($(wc -c $path/yuzuEA.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path/yuzuEA.AppImage ${T}($size_yuzuea( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
if [ "$3" = "YUZU" ]; then
T=$THEME_COLOR_YUZU
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING YUZU ..."
echo -e "${T} ///////////////"
wget -q --show-progress -O $path/yuzu.AppImage $(curl -s https://api.github.com/repos/yuzu-emu/yuzu-mainline/releases/latest | grep "browser_download_url.*AppImage" | cut -d : -f 2,3 | sed 1q | tr -d \")
chmod a+x $path/yuzu.AppImage 2>/dev/null
size_yuzuea=$(($(wc -c $path/yuzu.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path/yuzu.AppImage ${T}($size_yuzuea( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
if [ "$3" = "RYUJINX" ]; then
T=$THEME_COLOR_RYUJINX
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING RYUJINX ..."
echo -e "${T} ///////////////"
wget -q --show-progress -O $path/Ryujinx.AppImage https://github.com/qurious-pixel/Ryujinx/releases/download/continuous/Ryujinx-x86_64.AppImage
chmod a+x $path/Ryujinx.AppImage 2>/dev/null
size_yuzuea=$(($(wc -c $path/Ryujinx.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path/Ryujinx.AppImage ${T}($size_yuzuea( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
if [ "$3" = "RYUJINXAVALONIA" ]; then
T=$THEME_COLOR_RYUJINXAVALONIA
 if [ "$N" = "1" ]; then C="///////////////"; else C="///// ${F}$E/$N ${T}/////"; fi
echo -e "${T}   ///////////////"
echo -e "${T}  $C    ${F}UPDATING RYUJINX AVALONIA ..."
echo -e "${T} ///////////////"
wget -q --show-progress -O $path/Ryujinx-Avalonia.AppImage https://github.com/qurious-pixel/Ryujinx/releases/download/avalonia-build/Ryujinx-x86_64.AppImage
chmod a+x $path/Ryujinx-Avalonia.AppImage 2>/dev/null
size_yuzuea=$(($(wc -c $path/Ryujinx-Avalonia.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
echo -e "${T}$path/Ryujinx-Avalonia.AppImage ${T}($size_yuzuea( )MB) ${THEME_COLOR_OK}OK" | sed 's/( )//g'
echo
fi
}
#
export -f update_emulator
######################################################################
#
# - - - - -
#
######################################################################
function batocera_update_switch { 

######################################################################
# EMULATOR FILES CONFIG ----------------------------------------------
# --------------------------------------------------------------------
# paths should not be changed unless done upstream -------------------
# goto > github.com/ordovice/batocera-switch -------------------------
# --------------------------------------------------------------------
path=/userdata/system/switch
YUZUEA=/userdata/system/switch/yuzuEA.AppImage
YUZU=/userdata/system/switch/yuzu.AppImage
RYUJINX=/userdata/system/switch/Ryujinx.AppImage
RYUJINXAVALONIA=/userdata/system/switch/Ryujinx-Avalonia.AppImage
# --------------------------------------------------------------------
######################################################################
# read settings from cookie: -----------------------------------------
TEXT_SIZE=$(cat /userdata/system/switch/updater.settings | grep "TEXT_SIZE=" | cut -d "=" -f 2)
TEXT_COLOR=$(cat /userdata/system/switch/updater.settings | grep "TEXT_COLOR=" | cut -d "=" -f 2)
THEME_COLOR=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR=" | cut -d "=" -f 2)
THEME_COLOR_YUZU=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZU=" | cut -d "=" -f 2)
THEME_COLOR_YUZUEA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_YUZUEA=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINX=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINX=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXAVALONIA=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_RYUJINXAVALONIA=" | cut -d "=" -f 2)
THEME_COLOR_OK=$(cat /userdata/system/switch/updater.settings | grep "THEME_COLOR_OK=" | cut -d "=" -f 2)
EMULATORS=$(cat /userdata/system/switch/updater.settings | grep "EMULATORS=" | cut -d "=" -f 2)
F=$TEXT_COLOR
T=$THEME_COLOR
# redefine colors: --------
###########################
RED='\033[1;31m'      	  # red
BLUE='\033[1;34m'         # blue
GREEN='\033[1;32m'        # green
YELLOW='\033[1;33m'       # yellow
PURPLE='\033[1;35m'       # purple
CYAN='\033[1;36m'         # cyan
#                         |
DARKRED='\033[0;31m'      # darkred
DARKBLUE='\033[0;34m'     # darkblue
DARKGREEN='\033[0;32m'    # darkgreen
DARKYELLOW='\033[0;33m'   # darkyellow
DARKPURPLE='\033[0;35m'   # darkpurple
DARKCYAN='\033[0;36m'     # darkcyan
#                         |
WHITE='\033[0;37m'        # white
BLACK='\033[0;30m'        # black
###########################
echo -e "${T}-------------------------------------"
echo -e "${F}SWITCH EMULATORS UPDATER FOR BATOCERA"
echo
sleep 0.5
# update 4 emulators -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" != "" ]]; then
update_emulator 1 4 $(echo "$EMULATORS" | cut -d "-" -f 1)
update_emulator 2 4 $(echo "$EMULATORS" | cut -d "-" -f 2)
update_emulator 3 4 $(echo "$EMULATORS" | cut -d "-" -f 3)
update_emulator 4 4 $(echo "$EMULATORS" | cut -d "-" -f 4)
sleep 1
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}      ${TEXT_COLOR}4/4${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# update 3 emulators -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" != "" ]]; then
update_emulator 1 3 $(echo "$EMULATORS" | cut -d "-" -f 1)
update_emulator 2 3 $(echo "$EMULATORS" | cut -d "-" -f 2)
update_emulator 3 3 $(echo "$EMULATORS" | cut -d "-" -f 3)
sleep 1
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}      ${TEXT_COLOR}3/3${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# update 2 emulators -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 2)" != "" ]]; then
update_emulator 1 2 $(echo "$EMULATORS" | cut -d "-" -f 1)
update_emulator 2 2 $(echo "$EMULATORS" | cut -d "-" -f 2)
sleep 1
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}      ${TEXT_COLOR}2/2${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# update 1 emulator --------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 2)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 1)" != "" ]]; then
update_emulator 1 1 $(echo "$EMULATORS" | cut -d "-" -f 1)
sleep 1
echo -e "${THEME_COLOR}-------------------------------------${W}"
echo -e "${TEXT_COLOR}                  EMULATOR UPDATED ${THEME_COLOR_OK}OK ${W}"
fi
# clear cookie: 
rm /userdata/system/switch/updater.settings
# keep ui output for visibility:
sleep 1
exit 0
}
# --------------------------------------------------------------------
######################################################################
#
export -f batocera_update_switch
#
######################################################################
# --------------------------------------------------------------------
# calculate auto text size: 
# |
TEXT_SIZE=$(echo $TEXT_SIZE | sed 's/ //g')
if [[ "$TEXT_SIZE" = "AUTO" ]] || [[ "$TEXT_SIZE" = "Auto" ]] || [[ "$TEXT_SIZE" = "auto" ]]; then
 RX=$(DISPLAY=:0.0 xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f1 2>/dev/null)
 RY=$(DISPLAY=:0.0 xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f2 2>/dev/null)
 SF=$(($BASE_FONT_SIZE*$RX/1280)) && FS=$(printf "%.0f\n" $SF) && TEXT_SIZE=$FS
fi
# --------------------------------------------------------------------
######################################################################
# --------------------------------------------------------------------
# run the updater: 
# | 
  DISPLAY=:0.0 xterm -bg black -fa 'Monospace' -fs $TEXT_SIZE -e bash -c "batocera_update_switch" 2>/dev/null 
 
exit 0
######

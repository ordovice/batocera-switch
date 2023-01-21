#!/usr/bin/env bash
################################################################################
# v3.0                SWITCH EMULATORS UPDATER FOR BATOCERA                    #
#                   ----------------------------------------                   #
#                     > github.com/ordovice/batocera-switch                    #
#                         > https://discord.gg/hH5AfThG                        #     
################################################################################
#
#   SETTINGS: 
#  -----------
#
EMULATORS="YUZU YUZUEA RYUJINX RYUJINXLDN RYUJINXAVALONIA" 
#        |
#        default: "YUZU YUZUEA RYUJINX RYUJINXLDN RYUJINXAVALONIA"
#
#   EMULATORS="RYUJINX YUZU"  -->  will only update ryujinx & then yuzu   
#   EMULATORS="YUZUEA"  -->  will only update yuzu early access     
#
#
#
################################################################################
#
MODE=DISPLAY
#   |
#   default: DISPLAY 
#
#   MODE=DISPLAY  -->  for ports; uses fullscreen xterm process to show updater  
#   MODE=CONSOLE  -->  for ssh/console/xterm; no colors, no additional display  
#                
    ANIMATION=YES
#   plays loading animation when starting the udpater    
#
#
#
################################################################################
#
TEXT_SIZE=AUTO
#        |
#        default: AUTO
#
#   TEXT_SIZE=10  -->  will use custom font size, = 10  
#
#
# 
################################################################################
#
#   THEMING: 
#   --------
#
TEXT_COLOR=WHITE
THEME_COLOR=WHITE
THEME_COLOR_OK=WHITE
THEME_COLOR_YUZU=RED
THEME_COLOR_YUZUEA=RED
THEME_COLOR_RYUJINX=BLUE
THEME_COLOR_RYUJINXLDN=BLUE
THEME_COLOR_RYUJINXAVALONIA=BLUE
#
#   AVAILABLE COLORS:
#   |
#   WHITE,BLACK,RED,GREEN,BLUE,YELLOW,PURPLE,CYAN
#   DARKRED,DARKGREEN,DARKBLUE,DARKYELLOW,DARKPURPLE,DARKCYAN#
#
#
#
################################################################################
#
UPDATES=LOCKED
#      | 
#      default: LOCKED
#       
#   UPDATES=LOCKED  -->  limit ryujinx to version 1.1.382 for compatibility 
#   UPDATES=UNLOCKED  -->  download latest versions of ryujinx emulators 
#
#   *) use this option if you want to update ryujinx to latest releases, 
#   and use manual controller config (you can do it in 
#   [[ f1 menu ]] --> ryujinx-avalonia   
#
#
#
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
# --------------------------------------------------------------------
# PREPARE SHORTCUTS FOR F1-APPLICATIONS MENU
# --------------------------------------------------------------------
function generate-shortcut-launcher {
# SCALING FOR F1 APPS, DEFAULT 128@1  
DPI=128
SCALE=1
# --------
Name=$1
name=$2
# --------
extra=/userdata/system/switch/extra/$Name.desktop
shortcut=/usr/share/applications/$Name.desktop
launcher=/userdata/system/switch/extra/batocera-switch-launcher-$Name
# --------
rm -rf $shortcut 2>/dev/null
rm -rf $launcher 2>/dev/null
   echo "[Desktop Entry]" >> $shortcut
   echo "Version=1.0" >> $shortcut
      if [[ "$(echo $name | grep yuzu)" != "" ]]; then
         echo "Icon=/userdata/system/switch/extra/icon_yuzu.png" >> $shortcut
      else
         echo "Icon=/userdata/system/switch/extra/icon_ryujinx.png" >> $shortcut
      fi
   echo "Exec=$launcher" >> $shortcut
   echo "Terminal=false" >> $shortcut
   echo "Type=Application" >> $shortcut
   echo "Categories=Game;batocera.linux;" >> $shortcut
   echo "Name=$name-config" >> $shortcut
   ####
   echo "#!/bin/bash" >> $launcher
   echo "DISPLAY=:0.0 QT_FONT_DPI=$DPI QT_SCALE_FACTOR=$SCALE GDK_SCALE=$SCALE QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME="/userdata/system/configs" XDG_DATA_HOME="/userdata/system/configs" XDG_CACHE_HOME="/userdata/system/cache" QT_QPA_PLATFORM="xcb" /userdata/system/switch/$Name.AppImage" >> $launcher
      dos2unix "$launcher"
      chmod a+x "$launcher"
         dos2unix "$shortcut"
         chmod a+x "$shortcut"
cp "$shortcut" "$extra" 2>/dev/null
} # -----------------------------------------------------------------
#
# remove old version dekstop shortcuts from ~/.local/share/applications 
rm /userdata/system/.local/share/applications/yuzu-config.desktop 2>/dev/null
rm /userdata/system/.local/share/applications/yuzuEA-config.desktop 2>/dev/null
rm /userdata/system/.local/share/applications/ryujinx-config.desktop 2>/dev/null
rm /userdata/system/.local/share/applications/ryujinxavalonia-config.desktop 2>/dev/null
rm /userdata/system/.local/share/applications/ryujinxldn-config.desktop 2>/dev/null
# remove old version dekstop shortcuts from /usr/share/applications:
rm /usr/share/applications/yuzu-config.desktop 2>/dev/null
rm /usr/share/applications/yuzuEA-config.desktop 2>/dev/null
rm /usr/share/applications/ryujinx-config.desktop 2>/dev/null
rm /usr/share/applications/ryujinxavalonia-config.desktop 2>/dev/null
rm /usr/share/applications/ryujinxldn-config.desktop 2>/dev/null
rm /usr/share/applications/yuzu-config.desktop 2>/dev/null
rm /usr/share/applications/yuzuea-config.desktop 2>/dev/null
rm /usr/share/applications/ryujinx-config.desktop 2>/dev/null
rm /usr/share/applications/ryujinxavalonia-config.desktop 2>/dev/null
rm /usr/share/applications/ryujinxldn-config.desktop 2>/dev/null
# generate new desktop shortcuts: 
generate-shortcut-launcher 'yuzu' 'yuzu'
generate-shortcut-launcher 'yuzuEA' 'yuzuEA'
generate-shortcut-launcher 'Ryujinx' 'ryujinx'
generate-shortcut-launcher 'Ryujinx-LDN' 'ryujinx-LDN'
generate-shortcut-launcher 'Ryujinx-Avalonia' 'ryujinx-Avalonia'
######################################################################
######################################################################
######################################################################
######################################################################
if [[ "$EMULATORS" = "DEFAULT" ]] || [[ "$EMULATORS" = "default" ]] \
|| [[ "$EMULATORS" = "ALL" ]] || [[ "$EMULATORS" = "all" ]]; then
EMULATORS="YUZU YUZUEA RYUJINX RYUJINXLDN RYUJINXAVALONIA"; fi
if [ "$(echo $EMULATORS | grep "-")" = "" ]; then 
EMULATORS="$EMULATORS-"; fi
EMULATORS=$(echo $EMULATORS | sed 's/ /-/g')
# -------------------------------------------------------------------
rm /tmp/updater-settings 2>/dev/null
if [[ "$UPDATES" = "LOCKED" ]] || [[ "$UPDATES" = "locked" ]]; then 
echo "updates=locked" >> /tmp/updater-settings 
fi 
if [[ "$UPDATES" = "UNLOCKED" ]] || [[ "$UPDATES" = "unlocked" ]]; then 
echo "updates=unlocked" >> /tmp/updater-settings 
fi 
# -------------------------------------------------------------------
rm /tmp/updater-mode 2>/dev/null
echo "MODE=$MODE" >> /tmp/updater-mode 
# -------------------------------------------------------------------
# get animation
if [[ "$MODE" = "DISPLAY" ]] || [[ "$MODE" = "display" ]]; then 
   if [[ ( "$ANIMATION" = "YES" ) || ( "$ANIMATION" = "yes" ) ]]; then
   url_loader=https://github.com/uureel/batocera-switch/raw/main/system/switch/extra/loader.mp4
   loader=/userdata/system/switch/extra/loader.mp4 
      if [[ ! -e "$loader" ]]; then 
         wget -q -O $loader $url_loader
      fi 
      if [[ -e "$loader" ]] && [[ "$(wc -c $loader | awk '{print $1}')" < "6918849" ]]; then 
         wget -q -O $loader $url_loader   
      fi
   fi
fi
# -------------------------------------------------------------------
rm /tmp/updater-textsize 2>/dev/null
   if [[ "$(echo $TEXT_SIZE | grep "AUTO")" != "" ]] || [[ "$(echo $TEXT_SIZE | grep "auto")" != "" ]]; then 
      echo "$TEXT_SIZE" >> /tmp/updater-textsize 
   fi
# -------------------------------------------------------------------
temp=/userdata/system/switch/extra/downloads
mkdir /userdata/system/switch 2>/dev/null
mkdir /userdata/system/switch/extra 2>/dev/null
mkdir /userdata/system/switch/extra/downloads 2>/dev/null
clear 
# TEXT & THEME COLORS: 
###########################
X='\033[0m'               # / resetcolor
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
if [ "$THEME_COLOR_RYUJINXLDN" = "RED" ]; then THEME_COLOR_RYUJINXLDN="$RED"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "BLUE" ]; then THEME_COLOR_RYUJINXLDN="$BLUE"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "GREEN" ]; then THEME_COLOR_RYUJINXLDN="$GREEN"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "YELLOW" ]; then THEME_COLOR_RYUJINXLDN="$YELLOW"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "PURPLE" ]; then THEME_COLOR_RYUJINXLDN="$PURPLE"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "CYAN" ]; then THEME_COLOR_RYUJINXLDN="$CYAN"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "DARKRED" ]; then THEME_COLOR_RYUJINXLDN="$DARKRED"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "DARKBLUE" ]; then THEME_COLOR_RYUJINXLDN="$DARKBLUE"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "DARKGREEN" ]; then THEME_COLOR_RYUJINXLDN="$DARKGREEN"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "DARKYELLOW" ]; then THEME_COLOR_RYUJINXLDN="$DARKYELLOW"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "DARKPURPLE" ]; then THEME_COLOR_RYUJINXLDN="$DARKPURPLE"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "DARKCYAN" ]; then THEME_COLOR_RYUJINXLDN="$DARKCYAN"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "WHITE" ]; then THEME_COLOR_RYUJINXLDN="$WHITE"; fi
if [ "$THEME_COLOR_RYUJINXLDN" = "BLACK" ]; then THEME_COLOR_RYUJINXLDN="$BLACK"; fi
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
# REPLACE COLORS FOR CONSOLE MODE: 
   if [[ -e "/tmp/updater-mode" ]]; then 
      MODE=$(cat /tmp/updater-mode | grep MODE | cut -d "=" -f2)
   fi
      if [[ "$MODE" = "CONSOLE" ]]; then 
         TEXT_COLOR=$X 
         THEME_COLOR=$X
         THEME_COLOR_OK=$X
         THEME_COLOR_YUZU=$X
         THEME_COLOR_YUZUEA=$X
         THEME_COLOR_RYUJINX=$X
         THEME_COLOR_RYUJINXLDN=$X
         THEME_COLOR_RYUJINXAVALONIA=$X
      fi
# PREPARE COOKIE FOR FUNCTIONS: 
rm -rf /userdata/system/switch/extra/batocera-switch-updatersettings
echo "TEXT_SIZE=$TEXT_SIZE" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "TEXT_COLOR=$TEXT_COLOR" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR=$THEME_COLOR" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR_YUZU=$THEME_COLOR_YUZU" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR_YUZUEA=$THEME_COLOR_YUZUEA" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR_RYUJINX=$THEME_COLOR_RYUJINX" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR_RYUJINXAVALONIA=$THEME_COLOR_RYUJINXAVALONIA" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR_RYUJINXLDN=$THEME_COLOR_RYUJINXLDN" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "THEME_COLOR_OK=$THEME_COLOR_OK" >> /userdata/system/switch/extra/batocera-switch-updatersettings
echo "EMULATORS=$EMULATORS" >> /userdata/system/switch/extra/batocera-switch-updatersettings
####################################################################################
function update_emulator {
E=$1 && N=$2
link_yuzu="$4"
link_yuzuea="$5"
link_ryujinx="$6"
link_ryujinxldn="$7"
link_ryujinxavalonia="$8"
# ---------------------------------------------------------------------------------- 
# TEMPORARILY FREEZING UPDATES FOR RYUJINX: 
#link_ryujinx=https://github.com/uureel/batocera.pro/raw/main/switch/extra/ryujinx-1.1.382-linux_x64.tar.gz
#link_ryujinxavalonia=https://github.com/uureel/batocera.pro/raw/main/switch/extra/test-ava-ryujinx-1.1.382-linux_x64.tar.gz
##
updates=$(cat /tmp/updater-settings | grep "updates=locked" | cut -d "=" -f2)
   if [[ "$updates" = "locked" ]]; then 
      link_ryujinx=https://github.com/uureel/batocera.pro/raw/main/switch/extra/ryujinx-1.1.382-linux_x64.tar.gz
      link_ryujinxavalonia=https://github.com/uureel/batocera.pro/raw/main/switch/extra/test-ava-ryujinx-1.1.382-linux_x64.tar.gz
      locked=1
   fi 
##
# ---------------------------------------------------------------------------------- 
# DEPRECATED :: TEMPORARILY FREEZING UPDATES FOR YUZU: 
#link_yuzu=https://github.com/uureel/batocera.pro/raw/main/switch/extra/yuzu-mainline-20221204-9af678822.AppImage
#link_yuzuea=https://github.com/uureel/batocera.pro/raw/main/switch/extra/Linux-Yuzu-EA-3180.AppImage
# ----------------------------------------------------------------------------------
# PATHS: 
path_yuzu=/userdata/system/switch/yuzu.AppImage
path_yuzuea=/userdata/system/switch/yuzuEA.AppImage
path_ryujinx=/userdata/system/switch/Ryujinx.AppImage
path_ryujinxldn=/userdata/system/switch/Ryujinx-LDN.AppImage
path_ryujinxavalonia=/userdata/system/switch/Ryujinx-Avalonia.AppImage
# ---------------------------------------------------------------------------------- 
# READ SETTINGS FROM COOKIE: 
cookie=/userdata/system/switch/extra/batocera-switch-updatersettings
TEXT_SIZE=$(cat $cookie | grep "TEXT_SIZE=" | cut -d "=" -f 2)
TEXT_COLOR=$(cat $cookie | grep "TEXT_COLOR=" | cut -d "=" -f 2)
THEME_COLOR=$(cat $cookie | grep "THEME_COLOR=" | cut -d "=" -f 2)
THEME_COLOR_YUZU=$(cat $cookie | grep "THEME_COLOR_YUZU=" | cut -d "=" -f 2)
THEME_COLOR_YUZUEA=$(cat $cookie | grep "THEME_COLOR_YUZUEA=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINX=$(cat $cookie | grep "THEME_COLOR_RYUJINX=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXLDN=$(cat $cookie | grep "THEME_COLOR_RYUJINXLDN=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXAVALONIA=$(cat $cookie | grep "THEME_COLOR_RYUJINXAVALONIA=" | cut -d "=" -f 2)
THEME_COLOR_OK=$(cat $cookie | grep "THEME_COLOR_OK=" | cut -d "=" -f 2)
EMULATORS=$(cat $cookie | grep "EMULATORS=" | cut -d "=" -f 2)
# ---------------------------------------------------------------------------------- 
# OVERRIDE COLORS FOR SSH/XTERM: 
X='\033[0m' # / resetcolor
   if [[ -e "/tmp/updater-mode" ]]; then 
      MODE=$(cat /tmp/updater-mode | grep MODE | cut -d "=" -f2)
   fi
      if [[ "$MODE" = "CONSOLE" ]]; then 
         TEXT_COLOR=$X 
         THEME_COLOR=$X
         THEME_COLOR_OK=$X
         THEME_COLOR_YUZU=$X
         THEME_COLOR_YUZUEA=$X
         THEME_COLOR_RYUJINX=$X
         THEME_COLOR_RYUJINXLDN=$X
         THEME_COLOR_RYUJINXAVALONIA=$X
      fi
# ---------------------------------------------------------------------------------- 
# RUN UPDATER FOR SELECTED EMULATOR:
# ----------------------------------------------------------------------------------
extra=/userdata/system/switch/extra
temp=/userdata/system/switch/extra/downloads
mkdir /userdata/system/switch 2>/dev/null
mkdir /userdata/system/switch/extra 2>/dev/null
mkdir /userdata/system/switch/extra/downloads 2>/dev/null
# 
#
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
# EMULATORS UPDATERS:·
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
#
#
if [ "$3" = "YUZU" ]; then
T=$THEME_COLOR_YUZU
version=$(echo "$link_yuzu" | sed 's,^.*/download/,,g' | cut -d "/" -f1 | cut -d "-" -f3)
if [ "$N" = "1" ]; then C=""; else C="$E/$N"; fi
echo -e "${T}██ $C   ${F}YUZU   ${T}❯❯   ${T}$version"
rm -rf $temp/yuzu 2>/dev/null
mkdir $temp/yuzu 2>/dev/null
cd $temp/yuzu
curl --progress-bar --remote-name --location $link_yuzu
mv $temp/yuzu/* $temp/yuzu/yuzu.AppImage 2>/dev/null
chmod a+x "$temp/yuzu/yuzu.AppImage" 2>/dev/null
$temp/yuzu/yuzu.AppImage --appimage-extract 1>/dev/null 2>/dev/null 
mkdir /userdata/system/switch 2>/dev/null
mkdir /userdata/system/switch/extra 2>/dev/null
mkdir /userdata/system/switch/extra/yuzu 2>/dev/null
#cp $temp/yuzu/squashfs-root/usr/lib/libQt5* /userdata/system/switch/extra/yuzu/ 2>/dev/null 
rm /userdata/system/switch/extra/yuzu/libQ* 2>/dev/null
cp $temp/yuzu/squashfs-root/usr/lib/libicu* /userdata/system/switch/extra/yuzu/ 2>/dev/null 
cp $temp/yuzu/squashfs-root/usr/bin/yuzu /userdata/system/switch/extra/yuzu/yuzu 2>/dev/null
cp $temp/yuzu/squashfs-root/usr/bin/yuzu-room /userdata/system/switch/extra/yuzu/yuzu-room 2>/dev/null
cd $temp
# make launcher
ai=/userdata/system/switch/yuzu.AppImage; rm $ai 2>/dev/null
echo '#!/bin/bash' >> $ai
echo 'cp /userdata/system/switch/extra/yuzu/lib* /lib64/ 2>/dev/null' >> $ai 
echo 'if [ ! -L /userdata/system/configs/Ryujinx/bis/user/save ]; then mkdir /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null; rsync -au /userdata/saves/Ryujinx/ /userdata/system/configs/Ryujinx/bis/user/save/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/nand/user/save ]; then mkdir /userdata/system/configs/yuzu/nand/user/save 2>/dev/null; rsync -au /userdata/saves/yuzu/ /userdata/system/configs/yuzu/nand/user/save/ 2>/dev/null; fi' >> $ai
echo 'ff=/userdata/bios/switch/firmware' >> $ai
echo 'fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered' >> $ai
echo 'fy=/userdata/system/configs/yuzu/nand/system/Contents/registered' >> $ai
echo 'rsync -au $ff/ $fr/ ; rsync -au $ff/ $fy/' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/keys ]; then mkdir /userdata/system/configs/yuzu/keys 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/yuzu/keys/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/system ]; then mkdir /userdata/system/configs/Ryujinx/system 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/Ryujinx/system/ 2>/dev/null; fi' >> $ai
echo 'rm /usr/bin/yuzu 2>/dev/null; rm /usr/bin/yuzu-room 2>/dev/null' >> $ai
echo 'ln -s /userdata/system/switch/yuzu.AppImage /usr/bin/yuzu 2>/dev/null' >> $ai
echo 'cp /userdata/system/switch/extra/yuzu/yuzu-room /usr/bin/yuzu-room 2>/dev/null' >> $ai
echo 'QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata QT_FONT_DPI=128 QT_SCALE_FACTOR=1 /userdata/system/switch/extra/yuzu/yuzu "$1" "$2" "$3"' >> $ai
dos2unix "$ai" 2>/dev/null; chmod a+x "$ai" 2>/dev/null
chmod a+x "/userdata/system/switch/extra/yuzu/yuzu" 2>/dev/null
chmod a+x "/userdata/system/switch/extra/yuzu/yuzu-room" 2>/dev/null
size_yuzu=$(($(wc -c $temp/yuzu/yuzu.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
#echo -e "${T}■ ~/switch/yuzu.AppImage · ${T}$size_yuzu( )MB   ${T}" | sed 's/( )//g'
echo
cd ~/
fi
#
#
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
#
#
if [ "$3" = "YUZUEA" ]; then
T=$THEME_COLOR_YUZUEA
version=$(echo "$link_yuzuea" | sed 's,^.*Linux-Yuzu-EA-,,g' | sed 's,.AppImage,,g')
if [ "$N" = "1" ]; then C=""; else C="$E/$N"; fi
echo -e "${T}██ $C   ${F}YUZU-EA   ${T}❯❯   ${T}$version"
rm -rf $temp/yuzuea 2>/dev/null
mkdir $temp/yuzuea 2>/dev/null
cd $temp/yuzuea
curl --progress-bar --remote-name --location $link_yuzuea
mv $temp/yuzuea/* $temp/yuzuea/yuzuEA.AppImage 2>/dev/null
chmod a+x "$temp/yuzuea/yuzuEA.AppImage" 2>/dev/null
$temp/yuzuea/yuzuEA.AppImage --appimage-extract 1>/dev/null 2>/dev/null 
mkdir /userdata/system/switch 2>/dev/null
mkdir /userdata/system/switch/extra 2>/dev/null
mkdir /userdata/system/switch/extra/yuzuea 2>/dev/null
#cp $temp/yuzuea/squashfs-root/usr/lib/libQt5* /userdata/system/switch/extra/yuzuea/ 2>/dev/null
rm /userdata/system/switch/extra/yuzuea/libQ* 2>/dev/null 
cp $temp/yuzuea/squashfs-root/usr/lib/libicu* /userdata/system/switch/extra/yuzuea/ 2>/dev/null 
cp $temp/yuzuea/squashfs-root/usr/bin/yuzu /userdata/system/switch/extra/yuzuea/yuzu 2>/dev/null
cp $temp/yuzuea/squashfs-root/usr/bin/yuzu-room /userdata/system/switch/extra/yuzuea/yuzu-room 2>/dev/null
cd $temp
# make launcher
ai=/userdata/system/switch/yuzuEA.AppImage; rm $ai 2>/dev/null
echo '#!/bin/bash' >> $ai
echo 'cp /userdata/system/switch/extra/yuzuea/lib* /lib64/ 2>/dev/null' >> $ai 
echo 'if [ ! -L /userdata/system/configs/Ryujinx/bis/user/save ]; then mkdir /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null; rsync -au /userdata/saves/Ryujinx/ /userdata/system/configs/Ryujinx/bis/user/save/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/nand/user/save ]; then mkdir /userdata/system/configs/yuzu/nand/user/save 2>/dev/null; rsync -au /userdata/saves/yuzu/ /userdata/system/configs/yuzu/nand/user/save/ 2>/dev/null; fi' >> $ai
echo 'ff=/userdata/bios/switch/firmware' >> $ai
echo 'fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered' >> $ai
echo 'fy=/userdata/system/configs/yuzu/nand/system/Contents/registered' >> $ai
echo 'rsync -au $ff/ $fr/ ; rsync -au $ff/ $fy/' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/keys ]; then mkdir /userdata/system/configs/yuzu/keys 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/yuzu/keys/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/system ]; then mkdir /userdata/system/configs/Ryujinx/system 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/Ryujinx/system/ 2>/dev/null; fi' >> $ai
echo 'rm /usr/bin/yuzu 2>/dev/null; rm /usr/bin/yuzu-room 2>/dev/null' >> $ai
echo 'ln -s /userdata/system/switch/yuzuEA.AppImage /usr/bin/yuzu 2>/dev/null' >> $ai
echo 'cp /userdata/system/switch/extra/yuzuea/yuzu-room /usr/bin/yuzu-room 2>/dev/null' >> $ai
echo 'QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/yuzuea/yuzu "$1" "$2" "$3"' >> $ai
dos2unix "$ai" 2>/dev/null; chmod a+x "$ai" 2>/dev/null
chmod a+x "/userdata/system/switch/extra/yuzuea/yuzu" 2>/dev/null
chmod a+x "/userdata/system/switch/extra/yuzuea/yuzu-room" 2>/dev/null
size_yuzuea=$(($(wc -c $temp/yuzuea/yuzuEA.AppImage | awk '{print $1}')/1048576)) 2>/dev/null
#echo -e "${T}■ ~/switch/yuzuEA.AppImage · ${T}$size_yuzuea( )MB   ${T}" | sed 's/( )//g'
echo
cd ~/
fi
#
#
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
#
#
if [ "$3" = "RYUJINX" ]; then
T=$THEME_COLOR_RYUJINX
   if [[ "$locked" = "1" ]]; then 
      version="1.1.382 (locked)"
      else 
      version=$(echo "$link_ryujinx" | sed 's,^.*/download/,,g' | cut -d "/" -f1)
   fi 
# --------------------------------------------------------
if [ "$N" = "1" ]; then C=""; else C="$E/$N"; fi
echo -e "${T}██ $C   ${F}RYUJINX   ${T}❯❯   ${T}$version"
# --------------------------------------------------------
# \\ get dependencies for handling ryujinx
link_tar=https://github.com/ordovice/batocera-switch/blob/main/system/switch/extra/batocera-switch-tar
if [[ -e "$extra/batocera-switch-tar" ]]; then 
chmod a+x "$extra/batocera-switch-tar"
else 
wget -q -O "$extra/batocera-switch-tar" "$link_tar"
chmod a+x "$extra/batocera-switch-tar"
fi
cp "$extra/batocera-switch-libselinux.so.1" "/lib/libselinux.so.1" 2>/dev/null
# //
# /userdata/system/switch/extra/ryujinx/ will keep all ryujinx related dependencies
emu=ryujinx
mkdir $extra/$emu 2>/dev/null
rm -rf $temp/$emu 2>/dev/null
mkdir $temp/$emu 2>/dev/null
cd $temp/$emu
wget -q -O "$extra/$emu/xdg-mime" "https://github.com/uureel/batocera.pro/raw/main/switch/extra/xdg-mime"
chmod a+x "$extra/$emu/xdg-mime"
curl --progress-bar --remote-name --location $link_ryujinx
$extra/batocera-switch-tar -xf $temp/$emu/*.tar.gz
cp $temp/$emu/publish/lib* $extra/$emu/
mkdir $extra/$emu/mime 2>/dev/null; 
cp -rL $temp/$emu/publish/mime/* $extra/$emu/mime/ 2>/dev/null;
cp -rL $temp/$emu/publish/*.config $extra/$emu/ 2>/dev/null;
cd $extra/$emu
rm -rf $extra/$emu/dependencies 2>/dev/null
ls -l ./lib* | awk '{print $9}' | cut -d "/" -f2 >> $extra/$emu/dependencies
cd ~/
startup=$extra/$emu/startup
rm -rf $startup 2>/dev/null
echo '#!/bin/bash' >> $startup
echo 'cp /userdata/system/switch/extra/'$emu'/lib* /lib/ 2>/dev/null' >> $startup
dos2unix "$startup"
chmod a+x "$startup"
$extra/$emu/startup 2>/dev/null
# / 
path_ryujinx=$extra/$emu/Ryujinx.AppImage
cp $temp/$emu/publish/Ryujinx $path_ryujinx 2>/dev/null
chmod a+x "$path_ryujinx" 2>/dev/null
# make launcher 
ai=/userdata/system/switch/Ryujinx.AppImage; rm $ai 2>/dev/null
echo '#!/bin/bash' >> $ai
echo 'cp /userdata/system/switch/extra/'$emu'/lib* /lib/ 2>/dev/null' >> $ai
echo 'cp /userdata/system/switch/extra/'$emu'/xdg-mime /usr/bin/ 2>/dev/null' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/bis/user/save ]; then mkdir /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null; rsync -au /userdata/saves/Ryujinx/ /userdata/system/configs/Ryujinx/bis/user/save/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/nand/user/save ]; then mkdir /userdata/system/configs/yuzu/nand/user/save 2>/dev/null; rsync -au /userdata/saves/yuzu/ /userdata/system/configs/yuzu/nand/user/save/ 2>/dev/null; fi' >> $ai
echo 'ff=/userdata/bios/switch/firmware' >> $ai
echo 'fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered' >> $ai
echo 'fy=/userdata/system/configs/yuzu/nand/system/Contents/registered' >> $ai
echo 'rsync -au $ff/ $fr/; rsync -au $ff/ $fy/' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/keys ]; then mkdir /userdata/system/configs/yuzu/keys 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/yuzu/keys/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/system ]; then mkdir /userdata/system/configs/Ryujinx/system 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/Ryujinx/system/ 2>/dev/null; fi' >> $ai
echo 'rm /usr/bin/ryujinx 2>/dev/null; ln -s /userdata/system/switch/Ryujinx.AppImage /usr/bin/ryujinx 2>/dev/null' >> $ai
echo 'if [[ "$1" = "" ]]; then QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 SCRIPT_DIR=/userdata/system/switch/extra/ryujinx DOTNET_EnableAlternateStackCheck=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/ryujinx/Ryujinx.AppImage' >> $ai
echo 'else QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 SCRIPT_DIR=/userdata/system/switch/extra/ryujinx DOTNET_EnableAlternateStackCheck=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/ryujinx/Ryujinx.AppImage "$1"; fi' >> $ai
dos2unix "$ai" 2>/dev/null; chmod a+x "$ai" 2>/dev/null
# --------------------------------------------------------
# --------------------------------------------------------
size_ryujinx=$(($(wc -c $path_ryujinx | awk '{print $1}')/1048576)) 2>/dev/null
#echo -e "${T}■ ~/switch/Ryujinx.AppImage · ${T}$size_ryujinx( )MB   ${T}" | sed 's/( )//g'
echo
cd ~/
fi
#
#
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
#
#
if [ "$3" = "RYUJINXLDN" ]; then
T=$THEME_COLOR_RYUJINXLDN
version="3.0.1 / 1.1.368"
# --------------------------------------------------------
if [ "$N" = "1" ]; then C=""; else C="$E/$N"; fi
echo -e "${T}██ $C   ${F}RYUJINX-LDN   ${T}❯❯   ${T}$version"
# --------------------------------------------------------
# \\ get dependencies for handling ryujinxavalonia
link_tar=https://github.com/ordovice/batocera-switch/blob/main/system/switch/extra/batocera-switch-tar
if [[ -e "$extra/batocera-switch-tar" ]]; then 
   chmod a+x "$extra/batocera-switch-tar"
else 
   wget -q -O "$extra/batocera-switch-tar" "$link_tar"
   chmod a+x "$extra/batocera-switch-tar"
fi
cp "$extra/batocera-switch-libselinux.so.1" "/lib/libselinux.so.1" 2>/dev/null
# //
# /userdata/system/switch/extra/ryujinxavalonia/ will keep all ryujinxavalonia related dependencies
emu=ryujinxldn
mkdir $extra/$emu 2>/dev/null  
rm -rf $temp/$emu 2>/dev/null
mkdir $temp/$emu 2>/dev/null
cd $temp/$emu
wget -q -O "$extra/$emu/xdg-mime" "https://github.com/uureel/batocera.pro/raw/main/switch/extra/xdg-mime"
chmod a+x "$extra/$emu/xdg-mime"
curl --progress-bar --remote-name --location $link_ryujinxldn
$extra/batocera-switch-tar -xf $temp/$emu/*.tar.gz 2>/dev/null
cp $temp/$emu/publish/lib* $extra/$emu/ 2>/dev/null
mkdir $extra/$emu/mime 2>/dev/null; 
cp -rL $temp/$emu/publish/mime/* $extra/$emu/mime/ 2>/dev/null;
cp -rL $temp/$emu/publish/*.config $extra/$emu/ 2>/dev/null;
rm -rf $extra/$emu/startup 2>/dev/null
cd $extra/$emu
rm -rf $extra/$emu/dependencies 2>/dev/null
ls -l ./lib* | awk '{print $9}' | cut -d "/" -f2 >> $extra/$emu/dependencies
cd ~/
startup=$extra/$emu/startup
rm -rf $startup 2>/dev/null
echo '#!/bin/bash' >> $startup
echo 'cp /userdata/system/switch/extra/'$emu'/lib* /lib/ 2>/dev/null' >> $startup
dos2unix "$startup"
chmod a+x "$startup"
$extra/$emu/startup 2>/dev/null
# /
# --------------------------------------------------------
path_ryujinx=$extra/$emu/Ryujinx-LDN.AppImage
cp $temp/$emu/publish/Ryujinx.Ava $path_ryujinx 2>/dev/null
chmod a+x "$path_ryujinx" 2>/dev/null
# make launcher 
ai=/userdata/system/switch/Ryujinx-LDN.AppImage; rm $ai 2>/dev/null
echo '#!/bin/bash' >> $ai
echo 'cp /userdata/system/switch/extra/'$emu'/lib* /lib/ 2>/dev/null' >> $ai
echo 'cp /userdata/system/switch/extra/'$emu'/xdg-mime /usr/bin/ 2>/dev/null' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/bis/user/save ]; then mkdir /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null; rsync -au /userdata/saves/Ryujinx/ /userdata/system/configs/Ryujinx/bis/user/save/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/nand/user/save ]; then mkdir /userdata/system/configs/yuzu/nand/user/save 2>/dev/null; rsync -au /userdata/saves/yuzu/ /userdata/system/configs/yuzu/nand/user/save/ 2>/dev/null; fi' >> $ai
echo 'ff=/userdata/bios/switch/firmware' >> $ai
echo 'fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered' >> $ai
echo 'fy=/userdata/system/configs/yuzu/nand/system/Contents/registered' >> $ai
echo 'rsync -au $ff/ $fr/; rsync -au $ff/ $fy/' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/keys ]; then mkdir /userdata/system/configs/yuzu/keys 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/yuzu/keys/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/system ]; then mkdir /userdata/system/configs/Ryujinx/system 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/Ryujinx/system/ 2>/dev/null; fi' >> $ai
echo 'rm /usr/bin/ryujinx 2>/dev/null; ln -s /userdata/system/switch/Ryujinx-Avalonia.AppImage /usr/bin/ryujinx 2>/dev/null' >> $ai
echo 'if [[ "$1" = "" ]]; then QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 SCRIPT_DIR=/userdata/system/switch/extra/ryujinxldn DOTNET_EnableAlternateStackCheck=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/ryujinxldn/Ryujinx-LDN.AppImage' >> $ai
echo 'else QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 SCRIPT_DIR=/userdata/system/switch/extra/ryujinxldn DOTNET_EnableAlternateStackCheck=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/ryujinxldn/Ryujinx-LDN.AppImage "$1"; fi' >> $ai
dos2unix "$ai" 2>/dev/null; chmod a+x "$ai" 2>/dev/null
# --------------------------------------------------------
# --------------------------------------------------------
size_ryujinx=$(($(wc -c $path_ryujinx | awk '{print $1}')/1048576)) 2>/dev/null
#echo -e "${T}■ ~/switch/Ryujinx-LDN.AppImage · ${T}$size_ryujinx( )MB   ${T}" | sed 's/( )//g'
echo
cd ~/
fi
#
#
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
#
#
if [ "$3" = "RYUJINXAVALONIA" ]; then
T=$THEME_COLOR_RYUJINXAVALONIA
   if [[ "$locked" = "1" ]]; then 
      version="1.1.382 (locked)"
      else 
      version=$(echo "$link_ryujinxavalonia" | sed 's,^.*/download/,,g' | cut -d "/" -f1)
   fi
# --------------------------------------------------------
if [ "$N" = "1" ]; then C=""; else C="$E/$N"; fi
echo -e "${T}██ $C   ${F}RYUJINX-AVALONIA   ${T}❯❯   ${T}$version"
# --------------------------------------------------------
# \\ get dependencies for handling ryujinxavalonia
link_tar=https://github.com/ordovice/batocera-switch/blob/main/system/switch/extra/batocera-switch-tar
if [[ -e "$extra/batocera-switch-tar" ]]; then 
   chmod a+x "$extra/batocera-switch-tar"
else 
   wget -q -O "$extra/batocera-switch-tar" "$link_tar"
   chmod a+x "$extra/batocera-switch-tar"
fi
cp "$extra/batocera-switch-libselinux.so.1" "/lib/libselinux.so.1" 2>/dev/null
# //
# /userdata/system/switch/extra/ryujinxavalonia/ will keep all ryujinxavalonia related dependencies
emu=ryujinxavalonia
mkdir $extra/$emu 2>/dev/null  
rm -rf $temp/$emu 2>/dev/null
mkdir $temp/$emu 2>/dev/null
cd $temp/$emu
wget -q -O "$extra/$emu/xdg-mime" "https://github.com/uureel/batocera.pro/raw/main/switch/extra/xdg-mime"
chmod a+x "$extra/$emu/xdg-mime"
curl --progress-bar --remote-name --location $link_ryujinxavalonia
$extra/batocera-switch-tar -xf $temp/$emu/*.tar.gz 2>/dev/null
cp $temp/$emu/publish/lib* $extra/$emu/ 2>/dev/null
mkdir $extra/$emu/mime 2>/dev/null; 
cp -rL $temp/$emu/publish/mime/* $extra/$emu/mime/ 2>/dev/null;
cp -rL $temp/$emu/publish/*.config $extra/$emu/ 2>/dev/null;
rm -rf $extra/$emu/startup 2>/dev/null
cd $extra/$emu
rm -rf $extra/$emu/dependencies 2>/dev/null
ls -l ./lib* | awk '{print $9}' | cut -d "/" -f2 >> $extra/$emu/dependencies
cd ~/
startup=$extra/$emu/startup
rm -rf $startup 2>/dev/null
echo '#!/bin/bash' >> $startup
echo 'cp /userdata/system/switch/extra/'$emu'/lib* /lib/ 2>/dev/null' >> $startup
dos2unix "$startup"
chmod a+x "$startup"
$extra/$emu/startup 2>/dev/null
# /
# --------------------------------------------------------
path_ryujinx=$extra/$emu/Ryujinx-Avalonia.AppImage
cp $temp/$emu/publish/Ryujinx.Ava $path_ryujinx 2>/dev/null
chmod a+x "$path_ryujinx" 2>/dev/null
# make launcher 
ai=/userdata/system/switch/Ryujinx-Avalonia.AppImage; rm $ai 2>/dev/null
echo '#!/bin/bash' >> $ai
echo 'cp /userdata/system/switch/extra/'$emu'/lib* /lib/ 2>/dev/null' >> $ai
echo 'cp /userdata/system/switch/extra/'$emu'/xdg-mime /usr/bin/ 2>/dev/null' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/bis/user/save ]; then mkdir /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null; rsync -au /userdata/saves/Ryujinx/ /userdata/system/configs/Ryujinx/bis/user/save/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/nand/user/save ]; then mkdir /userdata/system/configs/yuzu/nand/user/save 2>/dev/null; rsync -au /userdata/saves/yuzu/ /userdata/system/configs/yuzu/nand/user/save/ 2>/dev/null; fi' >> $ai
echo 'ff=/userdata/bios/switch/firmware' >> $ai
echo 'fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered' >> $ai
echo 'fy=/userdata/system/configs/yuzu/nand/system/Contents/registered' >> $ai
echo 'rsync -au $ff/ $fr/; rsync -au $ff/ $fy/' >> $ai
echo 'if [ ! -L /userdata/system/configs/yuzu/keys ]; then mkdir /userdata/system/configs/yuzu/keys 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/yuzu/keys/ 2>/dev/null; fi' >> $ai
echo 'if [ ! -L /userdata/system/configs/Ryujinx/system ]; then mkdir /userdata/system/configs/Ryujinx/system 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/Ryujinx/system/ 2>/dev/null; fi' >> $ai
echo 'rm /usr/bin/ryujinx 2>/dev/null; ln -s /userdata/system/switch/Ryujinx-Avalonia.AppImage /usr/bin/ryujinx 2>/dev/null' >> $ai
echo 'if [[ "$1" = "" ]]; then QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 SCRIPT_DIR=/userdata/system/switch/extra/ryujinxavalonia DOTNET_EnableAlternateStackCheck=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/ryujinxavalonia/Ryujinx-Avalonia.AppImage' >> $ai
echo 'else QT_FONT_DPI=128 QT_SCALE_FACTOR=1 GDK_SCALE=1 SCRIPT_DIR=/userdata/system/switch/extra/ryujinxavalonia DOTNET_EnableAlternateStackCheck=1 QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins QT_PLUGIN_PATH=/usr/lib/qt/plugins XDG_CONFIG_HOME=/userdata/system/configs XDG_CACHE_HOME=/userdata/saves QT_QPA_PLATFORM=xcb XDG_RUNTIME_DIR=/userdata /userdata/system/switch/extra/ryujinxavalonia/Ryujinx-Avalonia.AppImage "$1"; fi' >> $ai
dos2unix "$ai" 2>/dev/null; chmod a+x "$ai" 2>/dev/null
# --------------------------------------------------------
# --------------------------------------------------------
size_ryujinx=$(($(wc -c $path_ryujinx | awk '{print $1}')/1048576)) 2>/dev/null
#echo -e "${T}■ ~/switch/Ryujinx-Avalonia.AppImage · ${T}$size_ryujinx( )MB   ${T}" | sed 's/( )//g'
echo
cd ~/
fi
#
#
# ---------------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------------- 
#
#
}
export -f update_emulator
#
#
#
function batocera_update_switch {
######################################################################
if [[ -e "/tmp/updater-mode" ]]; then 
   MODE=$(cat /tmp/updater-mode | grep MODE | cut -d "=" -f2)
fi
cd ~/
# -------------------------------------------------------------------
# -------------------------------------------------------------------
spinner()
{
    local pid=$1
    local delay=0.2
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf "LOADING EMULATORS  %c   " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
    done
    printf "   \b\b\b\b"
}
# -------------------------------------------------------------------
# -------------------------------------------------------------------
resolvelinks()
{
# LINKS & RESOLVERS:
# -------------------------------------------------------------------
links=/userdata/system/switch/extra/links
rm -rf $links 2>/dev/null
# YUZU:
release_yuzu=$(curl -s https://github.com/yuzu-emu/yuzu-mainline/ | grep "yuzu-emu/yuzu-mainline/releases/tag/" | sed 's/^.*href=/href=/g' | cut -d "/" -f 6 | cut -d \" -f 1)
date_yuzu=$(curl -s https://github.com/yuzu-emu/yuzu-mainline/releases/tag/$release_yuzu | grep "datetime=" | sed 's/^.*datetime/datetime/g' | cut -d \" -f 2 | cut -c 1-10 | sed 's/-//g')
subrelease_yuzu=$(curl -s https://github.com/yuzu-emu/yuzu-mainline/releases/tag/$release_yuzu | grep data-hovercard-url | grep commit-link | head -n 1 | cut -d "=" -f 4 | cut -d "/" -f 7 | cut -c 1-9)
link_yuzu=https://github.com/yuzu-emu/yuzu-mainline/releases/download/$release_yuzu/yuzu-mainline-$date_yuzu-$subrelease_yuzu.AppImage
# -------------------------------------------------------------------
# YUZUEA: 
release_yuzuea=$(curl -s https://github.com/pineappleEA/pineapple-src | grep /releases/ | cut -d "=" -f 5 | cut -d / -f 6 | cut -d '"' -f 1)
link_yuzuea=https://github.com/pineappleEA/pineapple-src/releases/download/$release_yuzuea/Linux-Yuzu-$release_yuzuea.AppImage
# -------------------------------------------------------------------
# RYUJINX:
release_ryujinx=$(curl -s https://github.com/Ryujinx/release-channel-master | grep "/release-channel-master/releases/tag/" | sed 's,^.*/release-channel-master/releases/tag/,,g' | cut -d \" -f1)
link_ryujinx=https://github.com/Ryujinx/release-channel-master/releases/download/$release_ryujinx/ryujinx-$release_ryujinx-linux_x64.tar.gz
# -------------------------------------------------------------------
# RYUJINXLDN:
link_ryujinxldn=https://github.com/uureel/batocera.pro/raw/main/switch/extra/ava-ryujinx-1.1.0-ldn3.0.1-linux_x64.tar.gz
## -------------------------------------------------------------------
# RYUJINXAVALONIA:
link_ryujinxavalonia=https://github.com/Ryujinx/release-channel-master/releases/download/$release_ryujinx/test-ava-ryujinx-$release_ryujinx-linux_x64.tar.gz
#
echo "link_yuzu@$link_yuzu" >> $links
echo "link_yuzuea@$link_yuzuea" >> $links
echo "link_ryujinx@$link_ryujinx" >> $links
echo "link_ryujinxldn@$link_ryujinxldn" >> $links
echo "link_ryujinxavalonia@$link_ryujinxavalonia" >> $links
}
######################################################################
# READ SETTINGS FROM COOKIE: -----------------------------------------
cookie=/userdata/system/switch/extra/batocera-switch-updatersettings
TEXT_SIZE=$(cat $cookie | grep "TEXT_SIZE=" | cut -d "=" -f 2)
TEXT_COLOR=$(cat $cookie | grep "TEXT_COLOR=" | cut -d "=" -f 2)
THEME_COLOR=$(cat $cookie | grep "THEME_COLOR=" | cut -d "=" -f 2)
THEME_COLOR_YUZU=$(cat $cookie | grep "THEME_COLOR_YUZU=" | cut -d "=" -f 2)
THEME_COLOR_YUZUEA=$(cat $cookie | grep "THEME_COLOR_YUZUEA=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINX=$(cat $cookie | grep "THEME_COLOR_RYUJINX=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXLDN=$(cat $cookie | grep "THEME_COLOR_RYUJINXLDN=" | cut -d "=" -f 2)
THEME_COLOR_RYUJINXAVALONIA=$(cat $cookie | grep "THEME_COLOR_RYUJINXAVALONIA=" | cut -d "=" -f 2)
THEME_COLOR_OK=$(cat $cookie | grep "THEME_COLOR_OK=" | cut -d "=" -f 2)
EMULATORS=$(cat $cookie | grep "EMULATORS=" | cut -d "=" -f 2)
# -------------------------
F=$TEXT_COLOR
T=$THEME_COLOR
# REREAD TEXT/THEME COLORS:
###########################
X='\033[0m'               # / resetcolor
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
R=$RED
W=$WHITE
B=$BLACK
F=$WHITE
# -------------------------
#  override colors: 
if [[ "$MODE" = "CONSOLE" ]]; then 
   RED=$X
   R=$X
   F=$X
   W=$X
fi
# -------------------------
clear
echo -e "${R}---------------------------"
echo -e "${F}SWITCH UPDATER FOR BATOCERA${R}"
echo
echo
resolvelinks & spinner $!
# -------------------------
clear
echo -e "${W}${R}>--------------------------"
echo -e "${R}.${W}/iTCH UPDATER FOR BATOCERA"
echo
echo
echo -e "${R}LOADING EMULATORS"
sleep 0.1111
# -------------------------
clear
echo -e "${W}\^${R}/>-----------------------"
echo -e "${F}${R}:${W}-iTCH UPDATER FOR BATOCERA"
echo
echo
echo -e "${R} /OADING/EMULATOR/"
sleep 0.1111
# -------------------------
clear
echo -e "${W}─<|v${R}x>---------------------"
echo -e "${F}s/${R}:${W}\\\cH UPDATER FOR BATOCERA"
echo
echo
echo -e "${R} LOAD/NGEMU/A/ORS"
sleep 0.1111
# -------------------------
clear
echo -e "${W}───</^${R}\>-------------------"
echo -e "${F}SWi-${R}:${W}| UPDATER FOR BATOCERA"
echo
echo
echo -e "${R}  LOA//N/EMU/AT/RS"
sleep 0.1111
# -------------------------
clear
echo -e "${W}──────<xv${R}|>----------------"
echo -e "${F}SWITCH 4${R}.${W}/aTER FOR BATOCERA"
echo
echo
echo -e "${R}  LOAD//EMUL//S"
sleep 0.1111
# -------------------------
clear
echo -e "${W}─────────<\^${R}/>-------------"
echo -e "${F}SWITCH Up|${R}:${W}-eR FOR BATOCERA"
echo
echo
echo -e "${R}   LOA///EMU///S"
sleep 0.1111
# -------------------------
clear
echo -e "${W}────────────<|v${R}x>----------"
echo -e "${F}SWITCH UPDAt/${R}. ${W}\oR BATOCERA"
echo
echo
echo -e "${R}   /OADNEM/TRS"
sleep 0.1111
# -------------------------
clear
echo -e "${W}───────────────</^${R}\>-------"
echo -e "${F}SWITCH UPDATER -${R}:${W}| BATOCERA"
echo
echo
echo -e "${R}   /OA/NEM//RS"
sleep 0.1111
# -------------------------
clear
echo -e "${W}──────────────────<xv${R}|>----"
echo -e "${F}SWITCH UPDATER FOR 4${R}.${W}/oCERA"
echo
echo
echo -e "${R}   ///A/N${W}EM/${R}//S"
sleep 0.1111
# -------------------------
clear
echo -e "${W}─────────────────────<\^${R}/>-"
echo -e "${F}SWITCH UPDATER FOR BAt|${R}:${W}-rA"
echo
echo
echo -e "${R}    ///${W}A/N/${R}/${W}/${R}//S"
sleep 0.1111
# -------------------------
clear
echo -e "${W}───────────────────────<|v${R}x"
echo -e "${W}SWITCH UPDATER FOR BATOc/${R}.${W}\\"
echo
echo
echo -e "${R}     //${W}A${R}//${W}\/${R}/// "
sleep 0.1111
# -------------------------
clear
echo -e "${W}──────────────────────────<\\"
echo -e "${W}SWITCH UPDATER FOR BATOCe-${R}:"
echo
echo
echo -e "${R}       /${W}\/${R}/${W}//      "
sleep 0.1111
# -------------------------
clear
echo -e "${W}────────────────────────────<"
echo -e "${W}SWITCH UPDATER FOR BATOCER\\"
echo
echo
echo -e "${R}       ${W}/${R}/${W}\\\\${R}/      "
sleep 0.1111
# -------------------------
clear
echo -e "${W}─────────────────────────────┐"
echo -e "${W}SWITCH UPDATER FOR BATOCERA  │"
echo
echo
# -------------------------
links=/userdata/system/switch/extra/links
link_yuzu=$(cat "$links" | grep "link_yuzu@" | cut -d "@" -f2 )
link_yuzuea=$(cat "$links" | grep "link_yuzuea@" | cut -d "@" -f2 )
link_ryujinx=$(cat "$links" | grep "link_ryujinx@" | cut -d "@" -f2 )
link_ryujinxldn=$(cat "$links" | grep "link_ryujinxldn@" | cut -d "@" -f2 )
link_ryujinxavalonia=$(cat "$links" | grep "link_ryujinxavalonia@" | cut -d "@" -f2 )
#
# UPDATE 5 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 5)" != "" ]]; then
update_emulator 1 5 $(echo "$EMULATORS" | cut -d "-" -f 1) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 2 5 $(echo "$EMULATORS" | cut -d "-" -f 2) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 3 5 $(echo "$EMULATORS" | cut -d "-" -f 3) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 4 5 $(echo "$EMULATORS" | cut -d "-" -f 4) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 5 5 $(echo "$EMULATORS" | cut -d "-" -f 5) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
echo
echo -e "${TEXT_COLOR}       ${TEXT_COLOR}5/5${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W} │"
echo -e "${THEME_COLOR}────────────────────────────────────────┘${X}"
fi
# UPDATE 4 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 5)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" != "" ]]; then
update_emulator 1 4 $(echo "$EMULATORS" | cut -d "-" -f 1) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 2 4 $(echo "$EMULATORS" | cut -d "-" -f 2) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 3 4 $(echo "$EMULATORS" | cut -d "-" -f 3) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 4 4 $(echo "$EMULATORS" | cut -d "-" -f 4) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
echo
echo -e "${TEXT_COLOR}       ${TEXT_COLOR}4/4${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W} │"
echo -e "${THEME_COLOR}───────────────────────────────────────┘${X}"
fi
# UPDATE 3 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 5)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" != "" ]]; then
update_emulator 1 3 $(echo "$EMULATORS" | cut -d "-" -f 1) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 2 3 $(echo "$EMULATORS" | cut -d "-" -f 2) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 3 3 $(echo "$EMULATORS" | cut -d "-" -f 3) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
echo
echo -e "${TEXT_COLOR}       ${TEXT_COLOR}3/3${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W} │"
echo -e "${THEME_COLOR}───────────────────────────────────────┘${X}"
fi
# UPDATE 2 EMULATORS -------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 5)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 2)" != "" ]]; then
update_emulator 1 2 $(echo "$EMULATORS" | cut -d "-" -f 1) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
update_emulator 2 2 $(echo "$EMULATORS" | cut -d "-" -f 2) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
echo
echo -e "${TEXT_COLOR}       ${TEXT_COLOR}2/2${TEXT_COLOR} SWITCH EMULATORS UPDATED ${THEME_COLOR_OK}OK ${W} │"
echo -e "${THEME_COLOR}───────────────────────────────────────┘${X}"
fi
# UPDATE 1 EMULATOR ---------------------------------------
if [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 5)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 4)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 3)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 2)" = "" ]] && [[ "$(echo $EMULATORS | cut -d "=" -f 2 | cut -d "-" -f 1)" != "" ]]; then
update_emulator 1 1 $(echo "$EMULATORS" | cut -d "-" -f 1) "$link_yuzu" "$link_yuzuea" "$link_ryujinx" "$link_ryujinxldn" "$link_ryujinxavalonia"
echo
echo -e "${TEXT_COLOR}                   EMULATOR UPDATED ${THEME_COLOR_OK}OK ${W} │"
echo -e "${THEME_COLOR}───────────────────────────────────────┘${X}"
fi
#
sleep 1.1
#
}
export -f batocera_update_switch
#
######################################################################
#
function post-install() {
# -------------------------------------------------------------------
# PREPARE BATOCERA-SWITCH-STARTUP FILE
# -------------------------------------------------------------------
# prepare patcher 
url_patcher="https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-patcher.sh"
wget -q -O "/userdata/system/switch/extra/batocera-switch-patcher.sh" "$url_patcher"
dos2unix ~/switch/extra/batocera-switch-patcher.sh 2>/dev/null
chmod a+x ~/switch/extra/batocera-switch-patcher.sh 2>/dev/null
# -------------------------------------------------------------------
startup=/userdata/system/switch/extra/batocera-switch-startup
rm "$startup" 2>/dev/null
#
echo '#!/bin/bash' >> $startup 
#\ prepare system
echo '#\ prepare system ' >> $startup
echo 'sysctl -w vm.max_map_count=262144 1>/dev/null' >> $startup
echo 'extra=/userdata/system/switch/extra' >> $startup
echo 'cp $extra/lib* /lib/ 2>/dev/null' >> $startup
echo 'cp $extra/*.desktop /usr/share/applications/ 2>/dev/null' >> $startup
echo 'cp /userdata/system/switch/extra/libthai.so.0.3.1 /lib/libthai.so.0.3.1 2>/dev/null' >> $startup
echo 'cp /userdata/system/switch/extra/batocera-switch-libthai.so.0.3 /lib/libthai.so.0.3 2>/dev/null' >> $startup
echo 'cp /userdata/system/switch/extra/batocera-switch-libselinux.so.1 /lib/libselinux.so.1 2>/dev/null' >> $startup
echo 'cp /userdata/system/switch/extra/batocera-switch-libtinfo.so.6 /lib/libtinfo.so.6 2>/dev/null' >> $startup
#\ link ryujinx config folders 
echo '#\ link ryujinx config folders ' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx 2>/dev/null' >> $startup
echo 'mv /userdata/system/configs/Ryujinx /userdata/system/configs/Ryujinx_tmp 2>/dev/null' >> $startup
echo 'cp -rL /userdata/system/.config/Ryujinx/* /userdata/configs/Ryujinx_tmp 2>/dev/null' >> $startup
echo 'rm -rf /userdata/system/.config/Ryujinx' >> $startup
echo 'mv /userdata/system/configs/Ryujinx_tmp /userdata/system/configs/Ryujinx 2>/dev/null' >> $startup
echo 'ln -s /userdata/system/configs/Ryujinx /userdata/system/.config/Ryujinx 2>/dev/null' >> $startup
echo 'rm /userdata/system/configs/Ryujinx/Ryujinx 2>/dev/null' >> $startup
#
#\ link ryujinx saves folders 
echo '#\ link ryujinx saves folders ' >> $startup
echo 'mkdir /userdata/saves 2>/dev/null' >> $startup
echo 'mkdir /userdata/saves/Ryujinx 2>/dev/null' >> $startup
echo 'mv /userdata/saves/Ryujinx /userdata/saves/Ryujinx_tmp 2>/dev/null' >> $startup
echo 'cp -rL /userdata/system/configs/Ryujinx/bis/user/save/* /userdata/saves/Ryujinx_tmp/ 2>/dev/null' >> $startup
echo 'rm -rf /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null' >> $startup
echo 'mv /userdata/saves/Ryujinx_tmp /userdata/saves/Ryujinx 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx/bis 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx/bis/user 2>/dev/null' >> $startup
echo 'ln -s /userdata/saves/Ryujinx /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null' >> $startup
echo 'rm /userdata/saves/Ryujinx/Ryujinx 2>/dev/null' >> $startup
echo 'if [ ! -L /userdata/system/configs/Ryujinx/bis/user/save ]; then mkdir /userdata/system/configs/Ryujinx/bis/user/save 2>/dev/null; rsync -au /userdata/saves/Ryujinx/ /userdata/system/configs/Ryujinx/bis/user/save/ 2>/dev/null; fi' >> $startup
#
#\ link yuzu config folders 
echo '#\ link yuzu config folders ' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu 2>/dev/null' >> $startup
echo 'mv /userdata/system/configs/yuzu /userdata/system/configs/yuzu_tmp 2>/dev/null' >> $startup
echo 'cp -rL /userdata/system/.config/yuzu/* /userdata/configs/yuzu_tmp 2>/dev/null' >> $startup
echo 'cp -rL /userdata/system/.local/share/yuzu/* /userdata/configs/yuzu_tmp 2>/dev/null' >> $startup
echo 'rm -rf /userdata/system/.config/yuzu' >> $startup
echo 'rm -rf /userdata/system/.local/share/yuzu' >> $startup
echo 'mv /userdata/system/configs/yuzu_tmp /userdata/system/configs/yuzu 2>/dev/null' >> $startup
echo 'ln -s /userdata/system/configs/yuzu /userdata/system/.config/yuzu 2>/dev/null' >> $startup
echo 'ln -s /userdata/system/configs/yuzu /userdata/system/.local/share/yuzu 2>/dev/null' >> $startup
echo 'rm /userdata/system/configs/yuzu/yuzu 2>/dev/null' >> $startup
#
#\ link yuzu saves folders
echo '#\ link yuzu saves folders' >> $startup
echo 'mkdir /userdata/saves 2>/dev/null' >> $startup
echo 'mkdir /userdata/saves/yuzu 2>/dev/null' >> $startup
echo 'mv /userdata/saves/yuzu /userdata/saves/yuzu_tmp 2>/dev/null' >> $startup
echo 'cp -rL /userdata/system/configs/yuzu/nand/user/save/* /userdata/saves/yuzu_tmp/ 2>/dev/null' >> $startup
echo 'rm -rf /userdata/system/configs/yuzu/nand/user/save 2>/dev/null' >> $startup
echo 'mv /userdata/saves/yuzu_tmp /userdata/saves/yuzu 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu/nand 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu/nand/user 2>/dev/null' >> $startup
echo 'ln -s /userdata/saves/yuzu /userdata/system/configs/yuzu/nand/user/save 2>/dev/null' >> $startup
echo 'rm /userdata/saves/yuzu/yuzu 2>/dev/null' >> $startup
echo 'if [ ! -L /userdata/system/configs/yuzu/nand/user/save ]; then mkdir /userdata/system/configs/yuzu/nand/user/save 2>/dev/null; rsync -au /userdata/saves/yuzu/ /userdata/system/configs/yuzu/nand/user/save/ 2>/dev/null; fi' >> $startup
#
#\ link yuzu and ryujinx keys folders to bios/switch 
echo '#\ link yuzu and ryujinx keys folders to bios/switch ' >> $startup
echo 'cp -rL /userdata/system/configs/yuzu/keys/* /userdata/bios/switch/ 2>/dev/null' >> $startup
echo 'cp -rL /userdata/system/configs/Ryujinx/system/* /userdata/bios/switch/ 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx 2>/dev/null' >> $startup
echo 'mv /userdata/bios/switch /userdata/bios/switch_tmp 2>/dev/null' >> $startup
echo 'rm -rf /userdata/system/configs/yuzu/keys 2>/dev/null' >> $startup
echo 'rm -rf /userdata/system/configs/Ryujinx/system 2>/dev/null' >> $startup
echo 'mv /userdata/bios/switch_tmp /userdata/bios/switch 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx 2>/dev/null' >> $startup
echo 'ln -s /userdata/bios/switch /userdata/system/configs/yuzu/keys 2>/dev/null' >> $startup
echo 'ln -s /userdata/bios/switch /userdata/system/configs/Ryujinx/system 2>/dev/null' >> $startup
echo 'if [ ! -L /userdata/system/configs/yuzu/keys ]; then mkdir /userdata/system/configs/yuzu/keys 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/yuzu/keys/ 2>/dev/null; fi' >> $startup
echo 'if [ ! -L /userdata/system/configs/Ryujinx/system ]; then mkdir /userdata/system/configs/Ryujinx/system 2>/dev/null; cp -rL /userdata/bios/switch/*.keys /userdata/system/configs/Ryujinx/system/ 2>/dev/null; fi' >> $startup
#
#\ rsync ryujinx+yuzu firmware folders with bios/switch/firmware
echo '#\ rsync ryujinx+yuzu firmware folders with bios/switch/firmware' >> $startup
echo 'rm -rf /userdata/bios/switch/.firmware 2>/dev/null' >> $startup
echo 'rm -rf /userdata/bios/switch/_firmware_ 2>/dev/null' >> $startup
echo 'ff=/userdata/bios/switch/firmware' >> $startup
echo 'ft=/userdata/bios/switch/firmware_backup' >> $startup
echo 'fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered' >> $startup
echo 'fy=/userdata/system/configs/yuzu/nand/system/Contents/registered' >> $startup
echo 'rm $fr 2>/dev/null' >> $startup
echo 'rm $fy 2>/dev/null' >> $startup
echo 'mkdir /userdata/bios 2>/dev/null' >> $startup
echo 'mkdir /userdata/bios/switch 2>/dev/null' >> $startup
echo 'mkdir /userdata/bios/switch/firmware 2>/dev/null' >> $startup
echo 'mkdir /userdata/bios/switch/firmware_backup 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx/bis 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx/bis/system 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx/bis/system/Contents 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/Ryujinx/bis/system/Contents/registered 2>/dev/null' >> $startup
#
echo 'mkdir /userdata/system/configs 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu/nand 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu/nand/system 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu/nand/system/Contents 2>/dev/null' >> $startup
echo 'mkdir /userdata/system/configs/yuzu/nand/system/Contents/registered 2>/dev/null' >> $startup
#
echo 'rsync -au $ff/ $fr/' >> $startup
echo 'rsync -au $fr/ $ff/' >> $startup
echo 'rsync -au $ff/ $fy/' >> $startup
echo 'rsync -au $fy/ $ff/' >> $startup
echo 'rm -rf $ft 2>/dev/null' >> $startup
#
# run batocera-switch-patcher.sh 
#echo '/userdata/system/switch/extra/batocera-switch-patcher.sh 2>/dev/null' >> $startup
echo ' ' >> $startup
dos2unix ~/switch/extra/batocera-switch-startup 
chmod a+x ~/switch/extra/batocera-switch-startup 
# & run startup immediatelly: 
/userdata/system/switch/extra/batocera-switch-startup 
# -------------------------------------------------------------------
# ADD TO BATOCERA AUTOSTART > /USERDATA/SYSTEM/CUSTOM.SH 
# -------------------------------------------------------------------
csh=/userdata/system/custom.sh; dos2unix $csh
startup="/userdata/system/switch/extra/batocera-switch-startup"
if [[ -f $csh ]];
   then
      tmp1=/tmp/tcsh1
      tmp2=/tmp/tcsh2
      remove="$startup"
      rm $tmp1 2>/dev/null; rm $tmp2 2>/dev/null
      nl=$(cat "$csh" | wc -l); nl1=$(($nl + 1))
         l=1; 
         for l in $(seq 1 $nl1); do
            ln=$(cat "$csh" | sed ""$l"q;d" );
               if [[ "$(echo "$ln" | grep "$remove")" != "" ]]; then :; 
                else 
                  if [[ "$l" = "1" ]]; then
                        if [[ "$(echo "$ln" | grep "#" | grep "/bin/" | grep "bash" )" != "" ]]; then :; else echo "$ln" >> "$tmp1"; fi
                     else 
                        echo "$ln" >> $tmp1;
                  fi
               fi            
            ((l++))
         done
         # 
         rm $tmp2
       echo -e '#!/bin/bash' >> $tmp2
       echo -e "\n$startup \n" >> $tmp2          
       cat "$tmp1" | sed -e '/./b' -e :n -e 'N;s/\n$//;tn' >> "$tmp2"
       cp $tmp2 $csh; dos2unix $csh; chmod a+x $csh  
   else  #(!f csh)   
       echo -e '#!/bin/bash' >> $csh
       echo -e "\n$startup\n" >> $csh  
       dos2unix $csh; chmod a+x $csh  
fi 
dos2unix ~/custom.sh
chmod a+x ~/custom.sh 
# --------------------------------------------------------------------
# CLEAR THE OLD V34- CUSTOM.SH LINE IF FOUND AND THE SYSTEM IS NOW VERSION V35+:
# THIS SHOULD HELP WITH UPGRADED VERSIONS AND 'OTHER INSTALLS' 
   if [[ "$(uname -a | grep "x86_64")" != "" ]] && [[ "$(uname -a | awk '{print $3}')" > "5.18.00" ]]; then
      remove="cat /userdata/system/configs/emulationstation/add_feat_os.cfg /userdata/system/configs/emulationstation/add_feat_switch.cfg"
      csh=/userdata/system/custom.sh
        if [[ -e "$csh" ]]; then
         tmp=/userdata/system/customsh.tmp
         rm $tmp 2>/dev/null
         nl=$(cat "$csh" | wc -l)
         l=1; while [[ "$l" -le "$nl" ]]; 
         do
            ln=$(cat "$csh" | sed ""$l"q;d")
               if [[ "$(echo "$ln" | grep "$remove")" != "" ]]; then :; else echo "$ln" >> "$tmp"; fi
            ((l++))
         done
         cp "$tmp" "$csh" 2>/dev/null
         rm "$tmp" 2>/dev/null
        fi
      es=/userdata/system/configs/emulationstation
      backup=/userdata/system/switch/extra/backup
      mkdir /userdata/system/switch 2>/dev/null
      mkdir /userdata/system/switch/extra 2>/dev/null
      mkdir /userdata/system/switch/extra/backup 2>/dev/null
      # REMOVE OLD ~/CONFIGS/EMULATIONSTATION/files if found & system is now upgraded: 
      rm "$es/add_feat_switch.cfg" 2>/dev/null
   fi
# -------------------------------------------------------------------- 
# REMOVE OLD UPDATERS 
rm /userdata/roms/ports/updateyuzu.sh 2>/dev/null 
rm /userdata/roms/ports/updateyuzuea.sh 2>/dev/null
rm /userdata/roms/ports/updateyuzuEA.sh 2>/dev/null 
rm /userdata/roms/ports/updateryujinx.sh 2>/dev/null
rm /userdata/roms/ports/updateryujinxavalonia.sh 2>/dev/null
# --------------------------------------------------------------------
# AUTOMATICALLY PULL THE LATEST EMULATORS FEATURES UPDATES / ALSO UPDATE THESE FILES: 
url_switchkeys=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/configs/evmapy/switch.keys
url_es_features_switch=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/configs/emulationstation/es_features_switch.cfg
url_es_systems_switch=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/configs/emulationstation/es_systems_switch.cfg
url_switchlauncher=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/switchlauncher.py
url_GeneratorImporter=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/GeneratorImporter.py
url_ryujinxMainlineGenerator=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py
url_yuzuMainlineGenerator=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py
url_sshupdater=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-sshupdater.sh
url_updater=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-updater.sh
url_portsupdater="https://raw.githubusercontent.com/ordovice/batocera-switch/main/roms/ports/Switch%20Updater.sh"
url_portsupdaterkeys="https://raw.githubusercontent.com/ordovice/batocera-switch/main/roms/ports/Switch%20Updater.sh.keys"   
   wget -q -O "/userdata/system/configs/evmapy/switch.keys" "$url_switchkeys"
   wget -q -O "/userdata/system/configs/emulationstation/es_features_switch.cfg" "$url_es_features_switch"
   wget -q -O "/userdata/system/configs/emulationstation/es_systems_switch.cfg" "$url_es_systems_switch"
   wget -q -O "/userdata/system/switch/configgen/switchlauncher.py" "$url_switchlauncher"
   wget -q -O "/userdata/system/switch/configgen/GeneratorImporter.py" "$url_GeneratorImporter"
   wget -q -O "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py" "$url_ryujinxMainlineGenerator"
   wget -q -O "/userdata/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py" "$url_yuzuMainlineGenerator"
      dos2unix "/userdata/system/configs/evmapy/switch.keys" 
      dos2unix "/userdata/system/configs/emulationstation/es_features_switch.cfg" 
      dos2unix "/userdata/system/configs/emulationstation/es_systems_switch.cfg" 
      dos2unix "/userdata/system/switch/configgen/switchlauncher.py" 
      dos2unix "/userdata/system/switch/configgen/GeneratorImporter.py" 
      dos2unix "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py" 
      dos2unix "/userdata/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py" 
      dos2unix "/userdata/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py"
   # update batocera-switch-sshupdater.sh
   wget -q -O "/userdata/system/switch/extra/batocera-switch-sshupdater.sh" "$url_sshupdater"
   dos2unix "/userdata/system/switch/extra/batocera-switch-sshupdater.sh"
   chmod a+x "/userdata/system/switch/extra/batocera-switch-sshupdater.sh"
   # update batocera-switch-updater.sh
   wget -q -O "/userdata/system/switch/extra/batocera-switch-updater.sh" "$url_updater"
   dos2unix "/userdata/system/switch/extra/batocera-switch-updater.sh"
   chmod a+x "/userdata/system/switch/extra/batocera-switch-updater.sh"
   # update ports Switch Updater.sh
   wget -q -O "/userdata/system/roms/ports/Switch Updater.sh" "$url_portsupdater"
   dos2unix "/userdata/system/roms/ports/Switch Updater.sh"
   chmod a+x "/userdata/system/roms/ports/Switch Updater.sh"
   # update ports Switch Updater.sh.keys
   wget -q -O "/userdata/system/roms/ports/Switch Updater.sh.keys" "$url_portsupdaterkeys"
   dos2unix "/userdata/system/roms/ports/Switch Updater.sh.keys"
   # get batocera-switch-patcher.sh 
   wget -q -O "/userdata/system/switch/extra/batocera-switch-patcher.sh" "$url_patcher"
   dos2unix "/userdata/system/switch/extra/batocera-switch-patcher.sh"
   chmod a+x "/userdata/system/switch/extra/batocera-switch-patcher.sh"
# --------------------------------------------------------------------
# --------------------------------------------------------------------
#\
# \ download ryujinx generator only if custom ryujinx controller patch is not being used
ryugenpatch=/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator_patched.py
ryugen=/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py
ryu382=$(echo "$link_ryujinx" | grep "1.1.382")
ava382=$(echo "$link_ryujinxavalonia" | grep "1.1.382")
origen=$(cat /userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py | grep "cvalue\['id" | grep "convuuid")
   
   #backup patch gen
   if [[ "$origen" = "" ]]; then
      cp "$ryugen" "$ryugenpatch" 2>/dev/null
   fi
   
   #if frozen   
      if [[ "$ryu382" != "" ]] || [[ "$ava382" != "" ]]; then
         #frozen and ori gen
         if [[ "$origen" != "" ]]; then
            wget -q -O "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py" "$url_ryujinxMainlineGenerator"
            dos2unix "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py"
         fi
         #frozen and patch gen found, backup
         if [[ "$origen" = "" ]]; then
            cp "$ryugen" "$ryugenpatch" 2>/dev/null
            wget -q -O "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py" "$url_ryujinxMainlineGenerator"
            dos2unix "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py"
         fi
      fi 
      
   #if unfrozen   
      if [[ "$ryu382" = "" ]] || [[ "$ava382" = "" ]]; then
         #found patch gen found, restore
         if [[ -e "$ryugenpatch" ]]; then
            cp "$ryugenpatch" "$ryugen"
         else 
            wget -q -O "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py" "$url_ryujinxMainlineGenerator"
            dos2unix "/userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py"
         fi
      fi 
# / 
#/
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# CLEAR TEMP & COOKIE:
rm -rf /userdata/system/switch/extra/downloads 2>/dev/null
rm /userdata/system/switch/extra/display.settings 2>/dev/null
rm /userdata/system/switch/extra/updater.settings 2>/dev/null
killall -9 vlc 2>/dev/null & killall -9 xterm 2>/dev/null & curl http://127.0.0.1:1234/reloadgames && exit 0
}
export -f post-install
#
######################################################################
#
# include display output: 
   tput=/userdata/system/switch/extra/batocera-switch-tput
   libtinfo=/userdata/system/switch/extra/batocera-switch-libtinfo.so.6
   mkdir /userdata/system/switch 2>/dev/null; mkdir /userdata/system/switch/extra 2>/dev/null
      if [[ ( -e "$tput" && "$(wc -c "$tput" | awk '{print $1}')" < "444" ) || ( ! -e "$tput" ) ]]; then
         rm "$tput" 2>/dev/null
         wget -q -O /userdata/system/switch/extra/batocera-switch-tput https://github.com/uureel/batocera-switch/raw/main/system/switch/extra/batocera-switch-tput
      fi
      if [[ ( -e "$libtinfo" && "$(wc -c "$libtinfo" | awk '{print $1}')" < "444" ) || ( ! -e "$libtinfo" ) ]]; then
         rm "$libtinfo" 2>/dev/null
         wget -q -O /userdata/system/switch/extra/batocera-switch-libtinfo.so.6 https://github.com/uureel/batocera-switch/raw/main/system/switch/extra/batocera-switch-libtinfo.so.6
      fi
   chmod a+x "$tput" 2>/dev/null
   cp "$libtinfo" "/lib/libtinfo.so.6" 2>/dev/null
#
      function get-xterm-fontsize {
         cfg=/userdata/system/switch/extra/display.cfg
            rm /tmp/cols 2>/dev/null
            killall -9 xterm 2>/dev/null
            DISPLAY=:0.0 xterm -fullscreen -fg black -bg black -fa Monospace -en UTF-8 -e bash -c "unset COLUMNS & /userdata/system/switch/extra/batocera-switch-tput cols >> /tmp/cols" 2>/dev/null
            killall -9 xterm 2>/dev/null
         res=$(xrandr | grep " connected " | awk '{print $3}' | cut -d x -f1)
         columns=$(cat /tmp/cols); echo "$res=$columns" >> "$cfg"
         cols=$(cat "$cfg" | tail -n 1 | cut -d "=" -f2 2>/dev/null) 2>/dev/null
         TEXT_SIZE=$(bc <<<"scale=0;$cols/10" 2>/dev/null) 2>/dev/null
      }
      export -f get-xterm-fontsize
##################################
get-xterm-fontsize 2>/dev/null
#
# ensure fontsize: 
cfg=/userdata/system/switch/extra/display.cfg
cols=$(cat "$cfg" | tail -n 1 | cut -d "=" -f2 2>/dev/null) 2>/dev/null
colres=$(cat "$cfg" | tail -n 1 | cut -d "=" -f1 2>/dev/null) 2>/dev/null
res=$(xrandr | grep " connected " | awk '{print $3}' | cut -d x -f1)
fallback=10 
#
#####
   if [[ -e "$cfg" ]] && [[ "$cols" != "80" ]]; then 
      if [[ "$colres" = "$res" ]]; then
         TEXT_SIZE=$(bc <<<"scale=0;$cols/10" 2>/dev/null) 2>/dev/null
      fi
      #|
      if [[ "$colres" != "$res" ]]; then
         rm "$cfg" 2>/dev/null
            try=1
            until [[ "$cols" != "80" ]] 
            do
            get-xterm-fontsize 2>/dev/null
            cols=$(cat "$cfg" | tail -n 1 | cut -d "=" -f2 2>/dev/null) 2>/dev/null
            try=$(($try+1)); if [[ "$try" -ge "10" ]]; then TEXT_SIZE=$fallback; cols=1; fi
            done 
            if [[ "$cols" != "1" ]]; then TEXT_SIZE=$(bc <<<"scale=0;$cols/10" 2>/dev/null) 2>/dev/null; fi
      fi
   # 
   else
   # 
      get-xterm-fontsize 2>/dev/null
      cols=$(cat "$cfg" | tail -n 1 | cut -d "=" -f2 2>/dev/null) 2>/dev/null
         try=1
         until [[ "$cols" != "80" ]] 
         do
            get-xterm-fontsize 2>/dev/null
            cols=$(cat "$cfg" | tail -n 1 | cut -d "=" -f2 2>/dev/null) 2>/dev/null
            try=$(($try+1)); if [[ "$try" -ge "10" ]]; then TEXT_SIZE=$fallback; cols=1; fi
         done 
         if [[ "$cols" != "1" ]]; then TEXT_SIZE=$(bc <<<"scale=0;$cols/10" 2>/dev/null) 2>/dev/null; fi
         if [ "$TEXT_SIZE" = "" ]; then TEXT_SIZE=$fallback; fi
   fi    #
   ##### #
         if [[ ( -e "/tmp/updater-textsize" && "$(cat "/tmp/updater-textsize" | grep "AUTO")" != "") || ( -e "/tmp/updater-textsize" && "$(cat "/tmp/updater-textsize" | grep "auto")" != "" ) ]]; then 
            TEXT_SIZE=$TEXT_SIZE
         else 
            TEXT_SIZE=$(cat "/tmp/updater-textsize")
         fi
         TEXT_SIZE=$(bc <<<"scale=0;$TEXT_SIZE/1")
         # ###################################################################
         # 
         ## RUN THE UPDATER: ------------------------------------------------- 
            if [[ "$MODE" = "DISPLAY" ]]; then 
            if [[ "$ANIMATION" = "YES" ]]; then sleep 0.1111; 
            DISPLAY=:0.0 unclutter-remote -h & cvlc -f --no-audio --no-video-title-show --no-mouse-events --no-keyboard-events --no-repeat "/userdata/system/switch/extra/loader.mp4" 2>/dev/null & sleep 3.333 && killall -9 vlc; fi 
            DISPLAY=:0.0 unclutter-remote -h & xterm -fs $TEXT_SIZE -fullscreen -fg black -bg black -fa Monospace -en UTF-8 -e bash -c "batocera_update_switch" 2>/dev/null 
            fi
            if [[ "$MODE" = "CONSOLE" ]]; then 
            batocera_update_switch console
            fi
############################################################################################################
# additional: 
su -c "post-install 2>/dev/null &" &
############################################################################################################
# exit: 
killall -9 vlc 2>/dev/null & killall -9 xterm 2>/dev/null & curl http://127.0.0.1:1234/reloadgames && exit 0
############################################################################################################
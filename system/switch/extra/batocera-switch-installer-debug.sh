#!/usr/bin/env bash 
# BATOCERA.PRO INSTALLER
######################################################################
#--------------------------------------------------------------------- 
APPNAME="SWITCH-EMULATION" 
ORIGIN="github.com/ordovice/batocera-switch" 
#---------------------------------------------------------------------
######################################################################
ORIGIN="${ORIGIN^^}"
extra=/userdata/system/switch/extra 
mkdir /userdata/system/switch  
mkdir /userdata/system/switch/extra  
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# --------------------------------------------------------------------
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\   
function batocera-pro-installer {
APPNAME=$1
ORIGIN=$2
# --------------------------------------------------------------------
# -- colors: 
###########################
X='\033[0m'               # / resetcolor
W='\033[0;37m'            # white
#-------------------------#
RED='\033[1;31m'          # red
BLUE='\033[1;34m'         # blue
GREEN='\033[1;32m'        # green
PURPLE='\033[1;35m'       # purple
DARKRED='\033[0;31m'      # darkred
DARKBLUE='\033[0;34m'     # darkblue
DARKGREEN='\033[0;32m'    # darkgreen
DARKPURPLE='\033[0;35m'   # darkpurple
###########################
# -- display theme:
L=$W
T=$W
R=$RED
B=$BLUE
G=$GREEN
P=$PURPLE
W=$X
# --------------------------------------------------------------------
echo
echo
echo 
echo -e "${X}${X}$APPNAME${X} INSTALLER ${X}"
echo 
echo 
echo
sleep 0.33

echo -e "${X}INSTALLING $APPNAME FOR BATOCERA IN DEBUGGING MODE"
echo -e "${X}USING $ORIGIN"
echo 
echo
echo
sleep 1
# --------------------------------------------------------------------
# -- check system before proceeding
if [[ "$(uname -a | grep "x86_64")" != "" ]]; then 
:
else
echo
echo -e "${X}ERROR: SYSTEM NOT SUPPORTED"
echo -e "${X}YOU NEED BATOCERA X86_64${X}"
echo
sleep 5
exit 0
# quit
exit 0
fi
# --------------------------------------------------------------------
# -------------------------------------------------------------------- 
# -------------------------------------------------------------------- 
echo -e "${X}PLEASE WAIT${X} . . ." 
#echo -e "${X}${X}" 
# -------------------------------------------------------------------- 
# -------------------------------------------------------------------- 
# -------------------------------------------------------------------- 
# PRESERVE CONFIG FILE 
cfg=/userdata/system/switch/CONFIG.txt 
if [[ -f "$cfg" ]]; then 
      # check config file version & update ---------------------------
      link_defaultconfig=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-config.txt
      wget -q --no-check-certificate --no-cache --no-cookies -O "/tmp/.CONFIG.txt" "$link_defaultconfig"
         currentver=$(cat "$cfg" | grep "(ver " | head -n1 | sed 's,^.*(ver ,,g' | cut -d ")" -f1)
            if [[ "$currentver" = "" ]]; then currentver=1.0.0; fi
         latestver=$(cat "/tmp/.CONFIG.txt" | grep "(ver " | head -n1 | sed 's,^.*(ver ,,g' | cut -d ")" -f1)
            if [[ "$latestver" > "$currentver" ]]; then 
               cp /tmp/.CONFIG.txt $cfg 
               echo -e "\n~/switch/CONFIG.txt FILE HAS BEEN UPDATED!\n"
            fi
      # check config file version & update ---------------------------
   cp $cfg /tmp/.userconfigfile 
fi
# -------------------------------------------------------------------- 
# PURGE OLD INSTALLS 
rm -rf /userdata/system/switch 
rm /userdata/system/configs/emulationstation/add_feat_switch.cfg 
rm /userdata/system/configs/emulationstation/es_features.cfg 
# -------------------------------------------------------------------- 
# FILL PATHS
#mkdir -p /userdata/roms/ports/images 
#mkdir -p /userdata/roms/switch 
#mkdir -p /userdata/bios/switch 
#mkdir -p /userdata/bios/switch/firmware 
#mkdir -p /userdata/system/configs/emulationstation 
#mkdir -p /userdata/system/configs/evmapy 
#mkdir -p /userdata/system/switch/configgen/generators/yuzu 
#mkdir -p /userdata/system/switch/configgen/generators/ryujinx 
#mkdir -p /userdata/system/switch/extra 

mkdir /userdata/roms/switch 
mkdir /userdata/roms/ports 
mkdir /userdata/roms/ports/images 

mkdir /userdata/bios/switch 
mkdir /userdata/bios/switch/firmware 

mkdir /userdata/system/switch 
mkdir /userdata/system/switch/extra 
mkdir /userdata/system/switch/configgen 
mkdir /userdata/system/switch/configgen/generators 
mkdir /userdata/system/switch/configgen/generators/yuzu 
mkdir /userdata/system/switch/configgen/generators/ryujinx 

mkdir /userdata/system/configs 
mkdir /userdata/system/configs/evmapy 
mkdir /userdata/system/configs/emulationstation 

# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/SWITCH/EXTRA
path=/userdata/system/switch/extra
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra
wget -O "$path/batocera-config-ryujinx" "$url/batocera-config-ryujinx"
wget -O "$path/batocera-config-ryujinx-avalonia" "$url/batocera-config-ryujinx-avalonia"
wget -O "$path/batocera-config-yuzu" "$url/batocera-config-yuzu"
wget -O "$path/batocera-config-yuzuEA" "$url/batocera-config-yuzuEA"
wget -O "$path/batocera-switch-libselinux.so.1" "$url/batocera-switch-libselinux.so.1"
wget -O "$path/batocera-switch-libthai.so.0.3" "$url/batocera-switch-libthai.so.0.3"
wget -O "$path/batocera-switch-libtinfo.so.6" "$url/batocera-switch-libtinfo.so.6"
wget -O "$path/batocera-switch-sshupdater.sh" "$url/batocera-switch-sshupdater.sh"
wget -O "$path/batocera-switch-tar" "$url/batocera-switch-tar"
wget -O "$path/batocera-switch-tput" "$url/batocera-switch-tput"
wget -O "$path/batocera-switch-updater.sh" "$url/batocera-switch-updater.sh"
wget -O "$path/icon_ryujinx.png" "$url/icon_ryujinx.png"
wget -O "$path/icon_yuzu.png" "$url/icon_yuzu.png"
wget -O "$path/libthai.so.0.3.1" "$url/libthai.so.0.3.1"
wget -O "$path/ryujinx-avalonia.png" "$url/ryujinx-avalonia.png"
wget -O "$path/ryujinx.png" "$url/ryujinx.png"
wget -O "$path/yuzu.png" "$url/yuzu.png"
wget -O "$path/yuzuEA.png" "$url/yuzuEA.png"
# -------------------------------------------------------------------- 
# + get default config file: 
wget -O "/userdata/system/switch/CONFIG.txt" "https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-config.txt"
# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/SWITCH/CONFIGGEN/GENERATORS/RYUJINX
path=/userdata/system/switch/configgen/generators/ryujinx
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/generators/ryujinx
wget -O "$path/__init__.py" "$url/__init__.py"
wget -O "$path/ryujinxMainlineGenerator.py" "$url/ryujinxMainlineGenerator.py"
# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/SWITCH/CONFIGGEN/GENERATORS/YUZU
path=/userdata/system/switch/configgen/generators/yuzu
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/generators/yuzu
wget -O "$path/__init__.py" "$url/__init__.py"
wget -O "$path/yuzuMainlineGenerator.py" "$url/yuzuMainlineGenerator.py"
# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/SWITCH/CONFIGGEN/GENERATORS
path=/userdata/system/switch/configgen/generators
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen/generators
wget -O "$path/__init__.py" "$url/__init__.py"
wget -O "$path/Generator.py" "$url/Generator.py"
# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/SWITCH/CONFIGGEN
path=/userdata/system/switch/configgen
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/configgen
wget -O "$path/GeneratorImporter.py" "$url/GeneratorImporter.py"
wget -O "$path/switchlauncher.py" "$url/switchlauncher.py"
wget -O "$path/switchlauncher2.py" "$url/switchlauncher2.py"
# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/CONFIGS/EMULATIONSTATION
path=/userdata/system/configs/emulationstation
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/configs/emulationstation
wget -O "$path/es_features_switch.cfg" "$url/es_features_switch.cfg"
wget -O "$path/es_systems_switch.cfg" "$url/es_systems_switch.cfg"
# -------------------------------------------------------------------- 
# FILL /USERDATA/SYSTEM/CONFIGS/EMULATIONSTATION 
path=/userdata/system/configs/evmapy
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/configs/evmapy
wget -O "$path/switch.keys" "$url/switch.keys"
# -------------------------------------------------------------------- 
# FILL /USERDATA/ROMS/PORTS 
path=/userdata/roms/ports 
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/roms/ports
wget -O "$path/Switch Updater.sh" "$url/Switch Updater.sh"
# -------------------------------------------------------------------- 
# FILL /USERDATA/ROMS/PORTS/IMAGES 
path=/userdata/roms/ports/images
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/roms/ports/images
wget -O "$path/Switch Updater-boxart.png" "$url/Switch Updater-boxart.png"
wget -O "$path/Switch Updater-cartridge.png" "$url/Switch Updater-cartridge.png"
wget -O "$path/Switch Updater-mix.png" "$url/Switch Updater-mix.png"
wget -O "$path/Switch Updater-screenshot.png" "$url/Switch Updater-screenshot.png"
wget -O "$path/Switch Updater-wheel.png" "$url/Switch Updater-wheel.png"
# -------------------------------------------------------------------- 
# FILL /USERDATA/ROMS/SWITCH
path=/userdata/roms/switch
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/roms/switch
wget -O "$path/_info.txt" "$url/_info.txt"
# -------------------------------------------------------------------- 
# FILL /USERDATA/BIOS/SWITCH 
path=/userdata/bios/switch
url=https://raw.githubusercontent.com/ordovice/batocera-switch/main/bios/switch
wget -O "$path/_info.txt" "$url/_info.txt"
# -------------------------------------------------------------------- 
# REMOVE OLD UPDATERS 
rm /userdata/roms/ports/updateyuzu.sh  
rm /userdata/roms/ports/updateyuzuea.sh 
rm /userdata/roms/ports/updateyuzuEA.sh  
rm /userdata/roms/ports/updateryujinx.sh 
rm /userdata/roms/ports/updateryujinxavalonia.sh 
# --------------------------------------------------------------------
dos2unix /userdata/system/switch/extra/*.sh 
dos2unix /userdata/system/switch/extra/batocera-config* 
chmod a+x /userdata/system/switch/extra/*.sh 
chmod a+x /userdata/system/switch/extra/batocera-config* 
chmod a+x /userdata/system/switch/extra/batocera-switch-lib* 
chmod a+x /userdata/system/switch/extra/*.desktop 
# --------------------------------------------------------------------
echo -e "${X} > INSTALLED OK${X}" 
sleep 1
echo
echo
echo
# restore xterm font
X='\033[0m' # / resetcolor
echo -e "${X}LOADING ${X}SWITCH UPDATER${X} . . ." 
echo -e "${X} "
rm -rf /userdata/system/switch/extra/installation 
rm /tmp/batocera-switch-updater.sh  
mkdir -p /tmp 
wget -O "/tmp/batocera-switch-updater.sh" "https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-updater.sh" 
sed -i 's,MODE=DISPLAY,MODE=CONSOLE,g' /tmp/batocera-switch-updater.sh 
dos2unix /tmp/batocera-switch-updater.sh  
chmod a+x /tmp/batocera-switch-updater.sh  
sed -i 's,clear,,g' /tmp/batocera-switch-updater.sh 
/tmp/batocera-switch-updater.sh CONSOLE 
sleep 0.1 
echo "OK" >> /userdata/system/switch/extra/installation
sleep 0.1
   # --- \ restore user config file for the updater if running clean install/update from the switch installer 
   if [[ -e /tmp/.userconfigfile ]]; then 
      cp /tmp/.userconfigfile /userdata/system/switch/CONFIG.txt 
   fi 
   # --- /
} 
export -f batocera-pro-installer  
# --------------------------------------------------------------------
batocera-pro-installer "$APPNAME" "$ORIGIN" 
# --------------------------------------------------------------------
X='\033[0m' # / resetcolor
if [[ -e /userdata/system/switch/extra/installation ]]; then
rm /userdata/system/switch/extra/installation 
echo
echo 
echo 
echo -e "   ${X}$APPNAME INSTALLED${X}" 
echo 
echo 
echo
echo -e "   ${X}-----------------------------------------------------${X}"
echo -e "   ${X}Place your keys into /userdata/bios/switch/${X}" 
echo -e "   ${X}Firmware *.nca into /userdata/bios/switch/firmware/${X}" 
echo
echo -e "   ${X}Use Switch Updater in Ports to update emulators${X}" 
echo -e "   ${X}For Switch Updater settings, check:${X}"
echo -e "   ${X}/userdata/system/switch/CONFIG.txt${X}" 
echo -e "   ${X}-----------------------------------------------------${X}"
echo
echo
echo -e "   ${X}-----------------------------------------------------${X}"
echo -e "   ${X}IN CASE OF ISSUES: ${X}"
echo 
echo -e "   ${X}1) try using opengl instead of vulkan ${X}"
echo -e "   ${X}2) use [autocontroller = off] in advanced settings & ${X}"
echo -e "   ${X}   configure controller manually in f1-applications ${X}"
echo
echo -e "   ${X}CHECK LOGS: ${X}"
echo -e "   ${X}> emulators logs are in /userdata/system/switch/logs/${X}" 
echo -e "   ${X}> emulationstation logs are in /userdata/system/logs/${X}" 
echo -e "   ${X}-----------------------------------------------------${X}"
echo 
echo 
else
echo 
echo 
echo 
echo -e "   ${X}Looks like the installation failed :(${X}" 
echo
echo -e "   ${X}Try running the script again,${X}" 
echo
echo -e "   ${X}If it still fails, try installing manually${X}" 
echo 
echo
echo 
sleep 1
exit 0
fi
# done. 

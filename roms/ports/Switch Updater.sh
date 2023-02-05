#!/usr/bin/env bash
#####################################################################
#                      PORTS: SWITCH UPDATER                        #
#                  -----------------------------                    #
#                  > https://discord.gg/hH5AfThG                    #
#              > github.com/ordovice/batocera-switch                #
#####################################################################
ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && net=on || net=off
if [ "$net" = "off" ]; then 
	DISPLAY=:0.0 xterm -fs 10 -fullscreen -fg black -bg black -fa Monospace -en UTF-8 -e bash -c "echo -e \"\n \033[0;37m NO INTERNET CONNECTION :( \033[0;30m \" & sleep 3" 2>/dev/null && exit 0 & exit 1 & exit 2
else
	updater=/userdata/system/switch/extra/batocera-switch-updater.sh; rm "$updater" 2>/dev/null; 
	wget -q --no-check-certificate --no-cache --no-cookies -O "$updater" "https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-updater.sh"
	dos2unix "$updater"; chmod a+x "$updater"
	/userdata/system/switch/extra/batocera-switch-updater.sh
fi
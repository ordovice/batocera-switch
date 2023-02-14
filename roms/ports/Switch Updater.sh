#!/usr/bin/env bash
#####################################################################
#                      PORTS: SWITCH UPDATER                        #
#                  -----------------------------                    #
#                 > https://discord.gg/SWBvBkmn9P                   #
#              > github.com/ordovice/batocera-switch                #
#####################################################################
updater=/userdata/system/switch/extra/batocera-switch-updater.sh
rm "$updater" 2>/dev/null 
wget -q --no-check-certificate --no-cache --no-cookies -O "$updater" "https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-updater.sh"
dos2unix "$updater"
chmod a+x "$updater"
bash /userdata/system/switch/extra/batocera-switch-updater.sh

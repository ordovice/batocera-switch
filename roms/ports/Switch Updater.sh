#!/usr/bin/env bash
#####################################################################
#                      PORTS: SWITCH UPDATER                        #
#                  -----------------------------                    #
#                  > https://discord.gg/hH5AfThG                    #
#              > github.com/ordovice/batocera-switch                #
#####################################################################
updater=/userdata/system/switch/extra/batocera-switch-updater.sh; rm "$updater" 2>/dev/null; 
wget -q -O "$updater" "https://raw.githubusercontent.com/ordovice/batocera-switch/main/system/switch/extra/batocera-switch-updater.sh"
dos2unix "$updater"; chmod a+x "$updater"
/userdata/system/switch/extra/batocera-switch-updater.sh

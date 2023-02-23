#!/usr/bin/env bash 
# ryujinx controller patcher for batocera-switch 
################################################
clear 

G='\033[1;32m'
R='\033[1;31m'
X='\033[0m'


echo -e "${R}---------${R}--------------------------------------------------"
echo -e "${R}RYUJINX CONTROLLER PATCHER FOR BATOCERA-SWITCH:"
echo -e "${X}/userdata/system/switch/extra/ryujinx-controller-patcher.sh"
echo -e "${R}---------${R}--------------------------------------------------"
echo -e "${R}HOW TO USE: ${X}" 
echo -e "${X}1  ${R}\ ${X}  OPEN [RYUJINX/AVALONIA] FROM [F1-APPS]"
echo -e "${X}2  ${R}/ ${X}  SELECT YOUR CONTROLLER & CONFIGURE"
echo -e "${X}3  ${R}\ ${X}  APPLY AND SAVE"
echo -e "${X}4   ${R}>>${X}  ${X}RUN THIS SCRIPT"
echo -e "${R}---------${R}--------------------------------------------------"
echo
echo
echo

getavaid="$(cat /userdata/system/configs/Ryujinx/Config.json | grep '"id":' | cut -d \" -f4 | head -n 1 | cut -d " " -f1)"

if [[ "$getavaid" = "" ]] || [[ "$getavaid" = "0" ]]; then 
	echo -e "${R} COULDN'T FIND CONTROLLER ID, YOU NEED TO FIRST CONFIGURE "
	echo -e "${R} THE CONTROLLER IN F1 -> APPS -> RYUJINX/AVALONIA "
	echo 
	echo -e "${R} THEN RUN THIS SCRIPT AGAIN "
	echo
	echo -e "${X} "
	echo
	exit 0
fi

if [[ "$getavaid" != "" ]] && [[ "$getavaid" != "0" ]]; then

	avaid=""$(echo $getavaid)""
	genline=$(cat /userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py | grep "cvalue\['id")
	replace="$genline"
	replaced=$(echo "$genline" | sed 's,^.*= ,,g')
	old=$(cat /userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py | grep "cvalue\['id" | sed 's,^.* = ,,g')
	new=\"$avaid\"
	with="                cvalue\['id'] = \"$getavaid\""
    line="            cvalue['id'] = controllernumber + '-' + str(convuuid)"

	if [[ "$old" = "$new" ]]; then 
		echo -e "${G}---------${G}--------------------------------------------------"
		echo -e "${X}ALREADY PATCHED TO USE THIS CONTROLLER ${G}/"
		echo
		echo -e "${G}"$replaced""
		echo -e "${G}---------${G}--------------------------------------------------"
		echo
		echo -e "${X} "
		echo
		exit 0
	fi

	if [[ "$replace" != "$with" ]]; then 

		sed -i "s/^.*cvalue\['id'\] =.*$/                cvalue['id'] = \"$getavaid\"/g" /userdata/system/switch/configgen/generators/ryujinx/ryujinxMainlineGenerator.py

		echo -e "${G}REPLACED ${X}--------------------------------------------------"
		echo -e "$replaced"
		echo
		echo -e "${G}WITH ${X}"
		echo -e "\"$avaid\""
		echo -e "${X}---------${X}--------------------------------------------------"
		echo
		echo -e "${X} "
		echo
		exit 0
	fi

fi


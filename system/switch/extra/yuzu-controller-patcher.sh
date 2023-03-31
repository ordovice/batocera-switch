#!/usr/bin/env bash 
# yuzu controller patcher for batocera-switch 
#############################################
clear 

G='\033[1;32m'
R='\033[1;31m'
X='\033[0m'


echo -e "${R}---------${R}--------------------------------------------------"
echo -e "${R}YUZU CONTROLLER PATCHER FOR BATOCERA-SWITCH:"
echo -e "${X}/userdata/system/switch/extra/yuzu-controller-patcher.sh"
echo -e "${R}---------${R}--------------------------------------------------"
echo -e "${R}HOW TO USE: ${X}" 
echo -e "${X}1  ${R}\ ${X}  OPEN YUZU FROM [F1-APPS]"
echo -e "${X}2  ${R}/ ${X}  SELECT YOUR CONTROLLER FROM THE INPUT DEVICES"
echo -e "${X}3  ${R}\ ${X}  APPLY / SAVE"
echo -e "${X}4   ${R}>>${X}  ${X}RUN THIS SCRIPT" 
echo -e "${R}---------${R}--------------------------------------------------"
echo
echo
echo
# proper id: 030000005e0400008e02000010010000
# auto   id: 030081b85e0400008e02000010010000

id="$(cat /userdata/system/configs/yuzu/qt-config.ini | grep 'guid:' | head -n1 | sed 's,^.*guid:,,g' | cut -d "," -f1)"

if [[ "$id" = "" ]] || [[ "$id" = "0" ]]; then 
	echo -e "${R} COULDN'T FIND CONTROLLER ID, YOU NEED TO FIRST CONFIGURE "
	echo -e "${R} THE CONTROLLER IN F1 -> APPS -> YUZU "
	echo 
	echo -e "${R} SELECT YOUR CONTROLLER FROM THE INPUT DEVICES, SAVE "
	echo
	echo -e "${R} THEN RUN THIS SCRIPT AGAIN "
	echo
	echo
	exit 0
fi

if [[ "$id" != "" ]] && [[ "$id" != "0" ]]; then

	id=""$(echo $id)""
	
	genline=$(cat /userdata/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py | grep 'inputguid = controller.guid')
	replace="$genline"
	replaced=$(echo "$genline" | sed 's,^.*= ,,g')
	old=$(cat /userdata/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py | grep 'inputguid = "' | head -n1 | sed 's,^.* = ,,g')
	new=\"$id\"
	with="                inputguid = \"$id\""
    line="                inputguid = controller.guid"

	if [[ "$old" = "$new" ]]; then 
		echo -e "${G}---------${G}--------------------------------------------------"
		echo -e "${X}OK! YUZU GENERATOR IS PATCHED TO USE THIS CONTROLLER "
		echo -e "${G}"$id""
		echo -e "${G}---------${G}--------------------------------------------------"
		echo
		echo -e "${X} "
		echo
		exit 0
	fi

	if [[ "$replace" != "$with" ]]; then 

		sed -i "s/^.*inputguid = controller.guid/                inputguid = \"$id\"/g" /userdata/system/switch/configgen/generators/yuzu/yuzuMainlineGenerator.py

		echo -e "${X}---------${X}--------------------------------------------------"
		echo -e "${X}---------${X}--------------------------------------------------"
		echo
		echo -e "${G}OK! YUZU GENERATOR IS PATCHED ${X}"
		echo 
		echo -e "${X}REPLACED ${X}"
		echo -e "inputguid = $replaced"
		echo
		echo -e "${X}WITH ${X}"
		echo -e "inputguid = \"$id\""
		echo
		echo -e "${X}---------${X}--------------------------------------------------"
		echo -e "${X}---------${X}--------------------------------------------------"
		echo
		echo -e "${X} "
		echo
		exit 0
	fi

fi


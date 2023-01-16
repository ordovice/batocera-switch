#!/bin/bash
#
# patch dolphinGenerator.py and batocera-config-dolphin to use QT_PLUGIN_PATH=/usr/lib/qt/plugins 
cd /usr/lib/python*/site-packages/configgen/generators/dolphin
path=$(echo ${PWD})
cd ~/
file="$path/dolphinGenerator.py"
ispatched=$(cat "$file" | grep "QT_PLUGIN_PATH")
if [[ "$ispatched" != "" ]]; then 
: 
else 
pfile=/tmp/dolphinGenerator.py
rm "$pfile" 2>/dev/null
nrlines=$(cat "$file" | wc -l)
L=1; while [[ "$L" -le "$nrlines" ]]; 
	 do 
	 	thisline=$(cat $file | sed ''$L'q;d')
	 		if [[ "$(echo "$thisline" | grep "QT_QPA_PLATFORM")" != "" ]]; then 
		 	echo '            "QT_PLUGIN_PATH":"/usr/lib/qt/plugins", \' >> "$pfile"
		 	echo "$thisline" >> "$pfile"
		 	else
		 	echo "$thisline" >> "$pfile"
		 	fi
	 L=$(($L+1))
	 done 
  cp "$pfile" "$file"
  sed -i 's,QT_QPA_PLATFORM=xcb,QT_PLUGIN_PATH=/usr/lib/qt/plugins QT_QPA_PLATFORM=xcb,g' /usr/bin/batocera-config-dolphin
fi
# / patch dolphinGenerator.py and batocera-config-dolphin to use QT_PLUGIN_PATH=/usr/lib/qt/plugins 

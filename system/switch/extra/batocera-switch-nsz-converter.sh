#!/bin/bash
# batocera-switch nsz-converter 
#########################################################################################################################
#
# get rom
rom="$(cat /tmp/switchromname)"
#
# set rev 
cp /userdata/system/pro/ps3plus/extras/batocera-switch-rev /usr/bin/rev 2>/dev/null && chmod a+x /usr/bin/rev 2>/dev/null
#
##### (b 1)
	# 
	if [[ "$(echo "$rom" | rev | cut -c 1-4 | rev)" = ".nsz" ]]; then 
	#
	# check nsz converter --------------
	#-----------------------------------
	###### (b 2) 
		if [[ $(which nsz) = "" ]]; then 

			function installinfo() { 
				echo -e "\033[0;37mPREPARING NSZ CONVERTER ... \033[0;30m \n"
			} 
			export -f installinfo

			function install() {
				cp /userdata/bios/switch/prod.keys /usr/bin/keys.txt 2>/dev/null
				cp -r /userdata/system/switch/extra/nsz/curses /usr/lib/python3.10/site-packages/ 2>/dev/null
				cp -r /userdata/system/switch/extra/nsz/lib-dynload /usr/lib/python3.10/ 2>/dev/null
				python -m ensurepip --default-pip 1>/dev/null 2>/dev/null
				#python -m pip install --upgrade pip 1>/dev/null 2>/dev/null
				python -m pip install pycryptodome 1>/dev/null 2>/dev/null
				python -m pip install zstandard 1>/dev/null 2>/dev/null
				python -m pip install enlighten 1>/dev/null 2>/dev/null
				python -m pip install nsz 1>/dev/null 2>/dev/null
			}
			export -f install  

			cp /usr/bin/xterm /usr/bin/nszinstall 2>/dev/null
			DISPLAY=:0.0 /usr/bin/nszinstall -fs 8 -fullscreen -fg white -bg black -fa Monospace -en UTF-8 -e bash -c "clear && installinfo & install && sleep 0.5 && clear && clear" 2>/dev/null 
			killall -9 nszinstall 
			rm -rf /usr/bin/nszinstall 2>/dev/null

		fi # (e 2)
	######## 
	#
	# f/info-------------
	#--------------------
		function info() { 
			echo -e "\033[0;37mCONVERTING ROM FROM NSZ TO NSP ... \033[0;30m \n"
		} 
		export -f info

	# f/convert-------------
	#-----------------------
		function convert() {
			# get rom 	
			rom="$(cat /tmp/switchromname)"

			# convert 
			nsz -D -w -t 4 -P "$rom" 
			sleep 0.1 

				# get filenames 
				pathdepth=$(tr -dc '/' <<<"$rom" | wc -c)
				romfield=$(($pathdepth+1))
				romname="$(echo "$rom" | cut -d "/" -f$(echo $romfield))"
				romnamensp="$(echo "$romname" | sed 's,.nsz,.nsp,g')"
			
					# remove nsz file 
					rm -rf "$rom" 2>/dev/null 
					# reload games 
					curl http://127.0.0.1:1234/reloadgames 
		} 
		export -f convert

	# run in xterm -------------------------------------
	#---------------------------------------------------
			cp /usr/bin/xterm /usr/bin/nszconvert 2>/dev/null
			DISPLAY=:0.0 xterm -fs 8 -fullscreen -fg white -bg black -fa Monospace -en UTF-8 -e bash -c "clear && info && convert && sleep 1 && clear && clear" 2>/dev/null 
			killall -9 nszconvert 2>/dev/null 
			rm -rf /usr/bin/nszconvert 2>/dev/null

			# pass cookie ------------------------------
			#-------------------------------------------
				rom=$(echo "$rom" | sed 's,.nsz,.nsp,g')
				rm /tmp/switchromname 2>/dev/null
				echo "$rom" >> /tmp/switchromname 
	fi # (e 1)
	   #
########
#
#########################################################################################################################

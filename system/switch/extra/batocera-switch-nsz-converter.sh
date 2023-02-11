#!/bin/bash
# batocera-switch nsz-converter 
#########################################################################################################################
#
# get rom
rom="$(cat /tmp/switchromname)"
#
# set rev 
cp /userdata/system/switch/extra/batocera-switch-rev /usr/bin/rev 2>/dev/null && chmod a+x /usr/bin/rev 2>/dev/null
#
##### (b 1)
	# 
	if [[ "$(echo "$rom" | rev | cut -c 1-4 | rev)" = ".nsz" ]]; then 
	#
	# check nsz converter --------------
	#-----------------------------------
	###### (b 2) 

		if [[ "$(which nsz | head -n 1 | grep "not found")" != "" ]] || [[ "$(which nsz | head -n 1)" = "" ]]; then 

			function nsz-install() {
				echo -e "\033[0;37mPREPARING NSZ CONVERTER ... \033[0;30m \n"
				python -m ensurepip --default-pip 1>/dev/null 2>/dev/null 
				python -m pip install --upgrade pip 1>/dev/null 2>/dev/null 
				python -m pip install --upgrade --force-reinstall pycryptodome 1>/dev/null 2>/dev/null 
				python -m pip install --upgrade --force-reinstall nsz 1>/dev/null 2>/dev/null 
				wait
				sleep 0.1
			}
			export -f nsz-install

			cp /usr/bin/xterm /usr/bin/nszinstall 2>/dev/null
			DISPLAY=:0.0 /usr/bin/nszinstall -fs 8 -fullscreen -fg white -bg black -fa Monospace -en UTF-8 -e bash -c "nsz-install" 2>/dev/null 
			wait
			killall -9 nszinstall && rm /usr/bin/nszinstall 2>/dev/null
			 

		fi # (e 2)
	######## 
	# f/convert-------------
	#-----------------------
		function convert-nsz() {
			echo -e "\033[0;37mCONVERTING ROM FROM NSZ TO NSP ... \033[0;30m \n"
			# get rom 	
			rom="$(cat /tmp/switchromname)"

			# fill dependencies 
			cp -r /userdata/system/switch/extra/nsz/curses /usr/lib/python3.10/site-packages/ 2>/dev/null
			chmod a+x /userdata/system/switch/extra/nsz/lib-dynload/*.so 2>/dev/null
			cp -r /userdata/system/switch/extra/nsz/lib-dynload/_curses* /usr/lib/python3.10/lib-dynload/ 2>/dev/null
			cp /userdata/bios/switch/prod.keys /usr/bin/keys.txt 2>/dev/null

			# convert 
			sleep 0.5 && nsz -D -w -t 4 -P "$rom" 
			wait
			echo -e "\n\n\033[0;37mROM CONVERTED TO NSP \033[0;30m \n\n"
			sleep 0.5 
			
					# remove nsz file 
					rm -rf "$rom" 2>/dev/null 
					# reload games 
					curl http://127.0.0.1:1234/reloadgames 
		} 
		export -f convert-nsz

	# run in xterm -------------------------------------
	#---------------------------------------------------
			DISPLAY=:0.0 xterm -fs 8 -fullscreen -fg white -bg black -fa Monospace -en UTF-8 -e bash -c "clear && convert-nsz && sleep 1 && clear" 2>/dev/null 

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

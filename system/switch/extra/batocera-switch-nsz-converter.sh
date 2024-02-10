#!/bin/bash
# batocera-switch nsz-converter 
#########################################################################################################################
#-------------------------------------------
# get rom
	rom="$(cat /tmp/switchromname)"
#-------------------------------------------
# set rev 
	cp /userdata/system/switch/extra/batocera-switch-rev /usr/bin/rev 2>/dev/null 
		chmod a+x /usr/bin/rev 2>/dev/null 
#-------------------------------------------
# NSZ
#####  
	# 
	if [[ "$(echo "$rom" | rev | cut -c 1-4 | rev)" = ".nsz" ]]; then 
		echo "nsz!"
	#
	##### \
		# ------------------------------------------------------ 
		# check if nsz converter is available, if not install it  
		if [[ "$(which nsz | head -n 1 | grep "not found")" != "" ]] || [[ "$(which nsz | head -n 1)" = "" ]]; then 
			function nsz-install() 
			{
				echo -e "╔═════════════════════════════════════════════╗ "
				echo -e "║ PREPARING NSZ & XCZ CONVERTER . . .         ║ "
				echo -e "╚═════════════════════════════════════════════╝ "
					echo
					echo
						python -m ensurepip --default-pip 1>/dev/null 2>/dev/null 
						python -m pip install --upgrade pip 1>/dev/null 2>/dev/null 
						python -m pip install --upgrade --force-reinstall pycryptodome 1>/dev/null 2>/dev/null 
						python -m pip install --upgrade --force-reinstall nsz 1>/dev/null 2>/dev/null 
						wait
							sleep 0.1
			}
			export -f nsz-install
			# run the nsz installer 
			cp /usr/bin/xterm /usr/bin/nszinstall 2>/dev/null
			chmod a+x /usr/bin/nszinstall
				DISPLAY=:0.0 /usr/bin/nszinstall -fs 8 -fullscreen -fg black -bg gray -fa Monospace -en UTF-8 -e bash -c "nsz-install" 2>/dev/null 
				wait
					killall -9 nszinstall && rm /usr/bin/nszinstall 2>/dev/null
		fi
		# ------------------------------------------------------ 
		# /
		# 
		##### \\
			# ==================================================
			# run nsz converter 
			function convert-nsz() 
			{
				echo -e "╔═════════════════════════════════════════════╗ "
				echo -e "║ CONVERTING NSZ TO NSP . . .                 ║ "
				echo -e "╚═════════════════════════════════════════════╝ "
					echo
					echo
					#-------------------------------------------
					# get rom from launcher cookie 
					rom="$(cat /tmp/switchromname)"
					#-------------------------------------------
					# fill dependencies 
					chmod a+x /userdata/system/switch/extra/nsz/lib-dynload/*.so 2>/dev/null
						# for python 3.11
						if [[ -d "/usr/lib/python3.11" ]]; then 
							cp -r /userdata/system/switch/extra/nsz/curses /usr/lib/python3.11/site-packages/ 2>/dev/null
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.11/lib-dynload/_curses.cpython-311-x86_64-linux-gnu.so
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses_panel.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.11/lib-dynload/_curses_panel.cpython-311-x86_64-linux-gnu.so
							fi
						# for python 3.10
						if [[ -d "/usr/lib/python3.10" ]]; then 
							cp -r /userdata/system/switch/extra/nsz/curses /usr/lib/python3.10/site-packages/ 2>/dev/null
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.10/lib-dynload/_curses.cpython-310-x86_64-linux-gnu.so
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses_panel.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.10/lib-dynload/_curses_panel.cpython-310-x86_64-linux-gnu.so
							fi
					#-------------------------------------------
					# fill user keys 
					cp /userdata/bios/switch/prod.keys /usr/bin/keys.txt 2>/dev/null
					#-------------------------------------------
					# run conversion  
					sleep 0.5 && nsz -D -w -t 4 -P "$rom" 
					wait
						echo -e "╔═════════════════════════════════════════════╗ "
						echo -e "║ FINISHED CONVERTING TO NSP                  ║ "
						echo -e "╚═════════════════════════════════════════════╝ "
						sleep 0.5 					
					#-------------------------------------------
					# remove the nsz file 
					# rm -rf "$rom" 2>/dev/null
					#-------------------------------------------
					# & reload games to remove the nsz entry  
					curl http://127.0.0.1:1234/reloadgames 
			} 
			export -f convert-nsz
			#-------------------------------------------
			# run in xterm 
				cp /usr/bin/xterm /usr/bin/nszconvert 2>/dev/null
				chmod a+x /usr/bin/nszconvert 
					DISPLAY=:0.0 /usr/bin/nszconvert -fs 8 -fullscreen -fg black -bg gray -fa Monospace -en UTF-8 -e bash -c "clear && convert-nsz && sleep 1 && clear" 2>/dev/null 
					wait
				killall -9 nszconvert && rm /usr/bin/nszconvert 2>/dev/null
			#-------------------------------------------
			# pass the rom cookie for launcher&emulator 
				rompath="$(dirname "$rom")"
				romname="$(basename "$rom" ".nsz")"
					rom="$rompath/$romname.nsp"
						rm /tmp/switchromname 2>/dev/null
							echo "$rom" >> /tmp/switchromname 
	######### ==================================================
	#
	fi 
#####
#
# XCZ
#####  
	# 
	if [[ "$(echo "$rom" | rev | cut -c 1-4 | rev)" = ".xcz" ]]; then 
		echo "xcz!"
	#
	##### \
		#  ------------------------------------------------------ 
		#  check if nsz converter is available, if not install it  
		if [[ "$(which nsz | head -n 1 | grep "not found")" != "" ]] || [[ "$(which nsz | head -n 1)" = "" ]]; then 
			function nsz-install() 
			{
				echo -e "╔═════════════════════════════════════════════╗ "
				echo -e "║ PREPARING NSZ & XCZ CONVERTER . . .         ║ "
				echo -e "╚═════════════════════════════════════════════╝ "
					echo
					echo
						python -m ensurepip --default-pip 1>/dev/null 2>/dev/null 
						python -m pip install --upgrade pip 1>/dev/null 2>/dev/null 
						python -m pip install --upgrade --force-reinstall pycryptodome 1>/dev/null 2>/dev/null 
						python -m pip install --upgrade --force-reinstall nsz 1>/dev/null 2>/dev/null 
						wait
							sleep 0.1
			}
			export -f nsz-install
			# run the nsz installer 
			cp /usr/bin/xterm /usr/bin/nszinstall 2>/dev/null
			chmod a+x /usr/bin/nszinstall
				DISPLAY=:0.0 /usr/bin/nszinstall -fs 8 -fullscreen -fg black -bg gray -fa Monospace -en UTF-8 -e bash -c "nsz-install" 2>/dev/null 
				wait
					killall -9 nszinstall && rm /usr/bin/nszinstall 2>/dev/null
		fi
		#  ------------------------------------------------------ 
		# /
		# 
		##### \\
			#  run xcz converter 
			function convert-xcz() 
			{
				echo -e "╔═════════════════════════════════════════════╗ "
				echo -e "║ CONVERTING XCZ TO XCI . . .                 ║ "
				echo -e "╚═════════════════════════════════════════════╝ "
					echo
					echo
					#-------------------------------------------
					# get rom from launcher cookie 
					rom="$(cat /tmp/switchromname)"
					#-------------------------------------------
					# fill dependencies 
					chmod a+x /userdata/system/switch/extra/nsz/lib-dynload/*.so 2>/dev/null
						# for python 3.11
						if [[ -d "/usr/lib/python3.11" ]]; then 
							cp -r /userdata/system/switch/extra/nsz/curses /usr/lib/python3.11/site-packages/ 2>/dev/null
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.11/lib-dynload/_curses.cpython-311-x86_64-linux-gnu.so
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses_panel.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.11/lib-dynload/_curses_panel.cpython-311-x86_64-linux-gnu.so
							fi
						# for python 3.10
						if [[ -d "/usr/lib/python3.10" ]]; then 
							cp -r /userdata/system/switch/extra/nsz/curses /usr/lib/python3.10/site-packages/ 2>/dev/null
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.10/lib-dynload/_curses.cpython-310-x86_64-linux-gnu.so
							cp /userdata/system/switch/extra/nsz/lib-dynload/_curses_panel.cpython-310-x86_64-linux-gnu.so /usr/lib/python3.10/lib-dynload/_curses_panel.cpython-310-x86_64-linux-gnu.so
							fi
					#-------------------------------------------
					# fill user keys 
					cp /userdata/bios/switch/prod.keys /usr/bin/keys.txt 2>/dev/null
					#-------------------------------------------
					# run conversion  
					sleep 0.5 && nsz -D -w -t 4 -P "$rom" 
					wait
						echo -e "╔═════════════════════════════════════════════╗ "
						echo -e "║ FINISHED CONVERTING TO XCZ                  ║ "
						echo -e "╚═════════════════════════════════════════════╝ "
						sleep 0.5 					
					#-------------------------------------------
					# remove the xcz file 
					# rm -rf "$rom" 2>/dev/null
					#-------------------------------------------
					# & reload games to remove the xcz entry  
					curl http://127.0.0.1:1234/reloadgames 
			} 
			export -f convert-xcz
			#-------------------------------------------
			# run in xterm 
				cp /usr/bin/xterm /usr/bin/nszconvert 2>/dev/null
				chmod a+x /usr/bin/nszconvert 
					DISPLAY=:0.0 /usr/bin/nszconvert -fs 8 -fullscreen -fg black -bg gray -fa Monospace -en UTF-8 -e bash -c "clear && convert-xcz && sleep 1 && clear" 2>/dev/null 
					wait
				killall -9 nszconvert && rm /usr/bin/nszconvert 2>/dev/null
			#-------------------------------------------
			# pass the rom cookie for launcher&emulator 
				rompath="$(dirname "$rom")"
				romname="$(basename "$rom" ".xcz")"
					rom="$rompath/$romname.xci"
						rm /tmp/switchromname 2>/dev/null
							echo "$rom" >> /tmp/switchromname 
	#########  ==================================================
	#
	fi 
######
exit 0
######

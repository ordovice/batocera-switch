#!/bin/bash
# batocera-desktop-xdg.sh
#########################---------------------------------------------------------------------------------------------

xdg=/userdata/system/switch/extra/xdg 

# --------------------------------------------------------------------------------------------------------------------
# check filesystem
fs=$(blkid | grep "$(df -h /userdata | awk 'END {print $1}')" | sed 's,^.*TYPE=,,g' | sed 's,",,g' | tr 'a-z' 'A-Z')
  if [[ "$(echo "$fs" | grep "EXT")" != "" ]] || [[ "$(echo "$fs" | grep "BTR")" != "" ]]; then
  	:
  else
  	exit 1
  fi

# --------------------------------------------------------------------------------------------------------------------
# usr/bin
cd $xdg/usr/bin
	for file in *; do
	    # Check if file is not a directory
	    if [ -f "$file" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -e "/usr/bin/$file" ]]; then
	        	ln -sf "$(pwd)/$file" "/usr/bin/$file" 2>/dev/null
	    	fi
	    fi
	done

# --------------------------------------------------------------------------------------------------------------------
# usr/libexec
cd $xdg/usr/libexec
	for file in *; do
	    # Check if file is not a directory
	    if [ -f "$file" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -e "/usr/libexec/$file" ]]; then
		        ln -sf "$(pwd)/$file" "/usr/libexec/$file" 2>/dev/null
			fi
			if [[ ! -e "/usr/bin/$file" ]]; then
	        	ln -sf "$(pwd)/$file" "/usr/bin/$file" 2>/dev/null
	        fi
	    fi
	done

# --------------------------------------------------------------------------------------------------------------------
# libs 

	# x86_64-linux-gnu 
		if [[ ! -d "/usr/lib/x86_64-linux-gnu" ]]; then
			mkdir -p /usr/lib/x86_64-linux-gnu 2>/dev/null 
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl /usr/lib/x86_64-linux-gnu/perl 2>/dev/null
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl5 /usr/lib/x86_64-linux-gnu/perl5 2>/dev/null
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl-base 2>/dev/null
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/xfce4 /usr/lib/x86_64-linux-gnu/xfce4 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl /usr/lib/perl 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl5 /usr/lib/perl5 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl-base /usr/lib/perl-base 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/xfce4 /usr/lib/xfce4 2>/dev/null
		fi 
		if [[ -d "/usr/lib/x86_64-linux-gnu" ]]; then
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl /usr/lib/x86_64-linux-gnu/perl 2>/dev/null
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl5 /usr/lib/x86_64-linux-gnu/perl5 2>/dev/null
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl-base 2>/dev/null
				ln -sf $xdg/usr/lib/x86_64-linux-gnu/xfce4 /usr/lib/x86_64-linux-gnu/xfce4 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl /usr/lib/perl 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl5 /usr/lib/perl5 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/perl-base /usr/lib/perl-base 2>/dev/null
					ln -sf $xdg/usr/lib/x86_64-linux-gnu/xfce4 /usr/lib/xfce4 2>/dev/null
		fi 

	# python (350kB)
		if [[ -d "/usr/lib/python3.11" ]]; then 
			cp -r $xdg/usr/lib/python3/dist-packages/xdg /usr/lib/python3.11/site-packages
				#cd /usr/lib/python3.11/site-packages/xdg/__pycache__
				#for file in *-38.*; do mv -- "$file" "${file/-38./-311.}"; done
				#cd ~/ 
		fi
		if [[ -d "/usr/lib/python3.10" ]]; then 
			cp -r $xdg/usr/lib/python3/dist-packages/xdg /usr/lib/python3.10/site-packages
				cd /usr/lib/python3.10/site-packages/xdg/__pycache__
				for file in *-311.*; do mv -- "$file" "${file/-311./-310.}"; done
				cd ~/ 
		fi

	## systemd (11MB)
	#  cp -r $xdg/usr/lib/systemd /usr/lib/ 2>/dev/null
	cd $xdg/usr/lib/systemd
	for item in *; do
	    # Check if file is not a directory
	    if [ -f "$item" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -e "/usr/lib/$item" ]]; then
		        ln -sf "$(pwd)/$item" "/usr/lib/$item" 2>/dev/null
			fi
	    fi
	    if [ -d "$item" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -d "/usr/lib/$item" ]]; then
		        ln -sf "$(pwd)/$item" "/usr/lib/$item" 2>/dev/null
			fi
	    fi
	done

	## extra libs (1.7MB)
	#  cp -r $xdg/usr/lib/x86_64-linux-gnu/lib* /usr/lib/ 2>/dev/null
	cd $xdg/usr/lib/x86_64-linux-gnu
	for item in *; do
	    # Check if file is not a directory
	    if [ -f "$item" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -e "/usr/lib/$item" ]]; then
		        ln -sf "$(pwd)/$item" "/usr/lib/$item" 2>/dev/null
			fi
	    fi
	    if [ -d "$item" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -d "/usr/lib/$item" ]]; then
		        ln -sf "$(pwd)/$item" "/usr/lib/$item" 2>/dev/null
			fi
	    fi
	done

	## extra libcrypt (0.5MB)
	#  cp -r $xdg/lib64/lib* /usr/lib/ 2>/dev/null
	cd $xdg/lib64
	for item in *; do
	    # Check if file is not a directory
	    if [ -f "$item" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -e "/usr/lib/$item" ]]; then
		        ln -sf "$(pwd)/$item" "/usr/lib/$item" 2>/dev/null
			fi
	    fi
	    if [ -d "$item" ]; then
	        # Create symlink in /usr/bin/
	        if [[ ! -d "/usr/lib/$item" ]]; then
		        ln -sf "$(pwd)/$item" "/usr/lib/$item" 2>/dev/null
			fi
	    fi
	done

# --------------------------------------------------------------------------------------------------------------------
# usr/share folders (7MB)
	cp -r $xdg/usr/share/* /usr/share 2>/dev/null 

# --------------------------------------------------------------------------------------------------------------------
# mime files
	
	# filemanager/desktop  
	cp -r $xdg/config/filemanager /usr/bin/ 2>/dev/null
	cp -r $xdg/config/filemanager.desktop /usr/share/applications/ 2>/dev/null

	# mimeapps.list 
	# cp -r $xdg/config/mimeapps.list /userdata/system/.config/mimeapps.list 2>/dev/null
	[[ ! -e /userdata/system/.config/mimeapps.list ]] && cp $xdg/config/mimeapps.list /userdata/system/.config/mimeapps.list 2>/dev/null


	# xfce4 helpers 
	mkdir -p /userdata/system/.local/share/xfce4/helpers 2>/dev/null
	# cp -r $xdg/local/share/xfce4/helpers/* /userdata/system/.local/share/xfce4/helpers/ 2>/dev/null
	for file in $xdg/local/share/xfce4/helpers/*; do filename=$(basename "$file"); [ ! -e "/userdata/system/.local/share/xfce4/helpers/$filename" ] && cp "$file" "/userdata/system/.local/share/xfce4/helpers/"; done 2>/dev/null

	mkdir -p /userdata/system/.config/xfce4 2>/dev/null
	# cp -r $xdg/config/helpers.rc /userdata/system/.config/xfce4/ 2>/dev/null
	[[ ! -e /userdata/system/.config/xfce4/helpers.rc ]] && cp $xdg/config/helpers.rc /userdata/system/.config/xfce4/ 2>/dev/null

# --------------------------------------------------------------------------------------------------------------------
# export flags
	export PATH=/usr/libexec:${PATH}
	export PATH=/usr/share/applications:${PATH}
	export XDG_DATA_DIRS=/usr/share/applications:${XDG_DATA_DIRS}
	
# this is still needed per each app: 
# XDG_CURRENT_DESKTOP=XFCE DESKTOP_SESSION=XFCE
export XDG_CURRENT_DESKTOP=XFCE
export DESKTOP_SESSION=XFCE

# end;
exit 0


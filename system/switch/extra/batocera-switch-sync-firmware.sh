#!/bin/bash
#   //=================================//
#  //  batocera-switch sync firmware  //
# //=================================//
# 
# set paths 
fr=/userdata/system/configs/Ryujinx/bis/system/Contents/registered
fy=/userdata/system/configs/yuzu/nand/system/Contents/registered
fs=/userdata/bios/switch/firmware
mkdir -p $fr 2>/dev/null
mkdir -p $fy 2>/dev/null
mkdir -p $fs 2>/dev/null
diag=0
#
#\------------\ 
# \------------\ 
#  prepare checks 
cr=1; cy=1; cs=1
#
#  prepare stat
if [[ ! -e /userdata/system/switch/extra/batocera-switch-stat ]]; then 
url_stat=https://github.com/uureel/batocera-switch/raw/main/system/switch/extra/batocera-switch-stat
wget -q --no-check-certificate --no-cache --no-cookies -O /userdata/system/switch/extra/batocera-switch-stat $url_stat
elif [[ "$(wc -c /userdata/system/switch/extra/batocera-switch-stat | awk '{print $1}')" < "90000" ]]; then 
url_stat=https://github.com/uureel/batocera-switch/raw/main/system/switch/extra/batocera-switch-stat
wget -q --no-check-certificate --no-cache --no-cookies -O /userdata/system/switch/extra/batocera-switch-stat $url_stat
fi 
chmod a+x /userdata/system/switch/extra/batocera-switch-stat 2>/dev/null
#
#  check = latest modified files 
rf=$(ls $fr -Art | grep ".nca" | tail -n 1)
yf=$(ls $fy -Art | grep ".nca" | tail -n 1)
sf=$(ls $fs -Art | grep ".nca" | tail -n 1)
if [[ "$rf" = "" ]]; then cr=0; else dr=$(/userdata/system/switch/extra/batocera-switch-stat -c "%Y" $fr/$rf 2>/dev/null); fi
if [[ "$yf" = "" ]]; then cy=0; else dy=$(/userdata/system/switch/extra/batocera-switch-stat -c "%Y" $fy/$yf 2>/dev/null); fi
if [[ "$sf" = "" ]]; then cs=0; else ds=$(/userdata/system/switch/extra/batocera-switch-stat -c "%Y" $fs/$sf 2>/dev/null); fi
#
#  check = directory size
sr=$(du -Hs $fr | awk '{print $1}')
sy=$(du -Hs $fy | awk '{print $1}')
ss=$(du -Hs $fs | awk '{print $1}')
if [[ "$sr" -le "200000" ]]; then cr=0; fi
if [[ "$sy" -le "200000" ]]; then cy=0; fi
if [[ "$ss" -le "200000" ]]; then cs=0; fi
#
#  check = number of files
nr=$(find $fr -type f | wc -l)
ny=$(find $fy -type f | wc -l)
ns=$(find $fs -type f | wc -l)
if [[ "$nr" -le "200" ]]; then cr=0; fi
if [[ "$ny" -le "200" ]]; then cy=0; fi
if [[ "$ns" -le "200" ]]; then cs=0; fi
# /------------/ 
#/------------/ 
# 
# ---
#
# find optimal firmware 
if [[ "$dr" != "" ]] && [[ "$dr" -ge "$dy" ]] && [[ "$dr" -ge "$ds" ]]; then f=r; fi
if [[ "$dy" != "" ]] && [[ "$dy" -ge "$dr" ]] && [[ "$dy" -ge "$ds" ]]; then f=y; fi
if [[ "$ds" != "" ]] && [[ "$ds" -ge "$dr" ]] && [[ "$ds" -ge "$dy" ]]; then f=s; fi
#
# ---
#
# & 
# >> populate using /userdata/bios/switch/firmware  
if [[ "$f" = "s" ]]; then
	if [[ "$ds" > "$dr" ]]; then  
	rm -rf "$fr/"* 2>/dev/null
		#cp -rL $fs/* $fr/ 2>/dev/null & 
		rsync -au --delete $fs/ $fr/ 2>/dev/null & 
			wait 
	fi
	if [[ "$ds" > "$dy" ]]; then  
	rm -rf "$fy/"* 2>/dev/null
		#cp -rL $fs/* $fy/ 2>/dev/null & 
		rsync -au --delete $fs/ $fy/ 2>/dev/null & 
			wait 
	fi
			# additional filenumber check
				if [[ "$nr" > "$ns" ]]; then  
				rm -rf $fr/* 2>/dev/null
					#cp -rL $fs/* $fr/ 2>/dev/null & 
					cp -r $fs/* $fr/ 2>/dev/null
				fi
				if [[ "$ny" > "$ns" ]]; then  
				rm -rf $fy/* 2>/dev/null
					#cp -rL $fs/* $fy/ 2>/dev/null & 
					cp -r $fs/* $fy/ 2>/dev/null
				fi
fi
#
# or 
# >> populate using fryujinx 
if [[ "$f" = "r" ]]; then
	if [[ "$dr" > "$dy" ]]; then  
	rm -rf "$fy/"* 2>/dev/null
		#cp -rL $fr/* $fy/ 2>/dev/null & 
		rsync -au --delete $fr/ $fy/ 2>/dev/null & 
			wait 
	fi
	if [[ "$dr" > "$ds" ]]; then  
	rm -rf "$fs/"* 2>/dev/null
		#cp -rL $fr/* $fs/ 2>/dev/null & 
		rsync -au --delete $fr/ $fs/ 2>/dev/null & 
			wait 
	fi
			# additional filenumber check
				if [[ "$ny" > "$nr" ]]; then  
				rm -rf $fy/* 2>/dev/null
					#cp -rL $fs/* $fr/ 2>/dev/null & 
					cp -r $fr/* $fy/ 2>/dev/null
				fi
				if [[ "$ns" > "$nr" ]]; then  
				rm -rf $fs/* 2>/dev/null
					#cp -rL $fs/* $fy/ 2>/dev/null & 
					cp -r $fr/* $fs/ 2>/dev/null
				fi
fi
#
# or 
# >> populate using yuzu  
if [[ "$f" = "y" ]]; then
	if [[ "$dy" > "$dr" ]]; then  
	rm -rf "$fr/"* 2>/dev/null
		#cp -rL $fy/* $fr/ 2>/dev/null & 
		rsync -au --delete $fy/ $fr/ 2>/dev/null & 
			wait 
	fi
	if [[ "$dy" > "$ds" ]]; then  
	rm -rf "$fs/"* 2>/dev/null
		#cp -rL $fy/* $fs/ 2>/dev/null & 
		rsync -au --delete $fy/ $fs/ 2>/dev/null & 
			wait 
	fi
			# additional filenumber check
				if [[ "$nr" > "$ny" ]]; then  
				rm -rf $fr/* 2>/dev/null
					#cp -rL $fs/* $fr/ 2>/dev/null & 
					cp -r $fy/* $fr/ 2>/dev/null
				fi 
				if [[ "$ns" > "$ny" ]]; then  
				rm -rf $fs/* 2>/dev/null
					#cp -rL $fs/* $fy/ 2>/dev/null & 
					cp -r $fy/* $fs/ 2>/dev/null
				fi
fi
#
# ---
# end 
#############################
if [[ "$diag" != "0" ]]; then 
echo "rf=$rf"
echo "yf=$yf"
echo "sf=$sf"
echo "dr=$dr"
echo "dy=$dy"
echo "ds=$ds"
echo "sr=$sr"
echo "sy=$sy"
echo "ss=$ss"
echo "nr=$nr"
echo "ny=$ny"
echo "ns=$ns"
echo "fw=$f"
fi
exit 0; exit 1
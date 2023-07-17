#!/bin/bash
# batocera-switch-mousemove.sh 
##################################################

# get screen resolution 
  r=$(xrandr | grep " connected" | awk '{print $3}')
  w=$(echo $r | cut -dx -f1 | cut -d+ -f2)
  h=$(echo $r | cut -d+ -f1 | cut -dx -f2)

# prepare dependencies 
  ln -sf /userdata/system/switch/extra/batocera-switch-libxdo.so.3 /lib/libxdo.so.3
  ln -sf /userdata/system/switch/extra/batocera-switch-xdotool /usr/lib/xdotool
 
# move mouse cursor to bottom right corner 
  xdotool mousemove $w $h

#!/bin/bash
# batocera-switch-mousemove.sh 
##################################################

# get screen resolution 
  r=$(xrandr | grep "+" | awk '{print $1}' | tail -n1)
  w=$(echo "$r" | cut -d "x" -f1)
  h=$(echo "$r" | cut -d "x" -f2)

# prepare dependencies 
  ln -sf /userdata/system/switch/extra/batocera-switch-libxdo.so.3 /lib/libxdo.so.3
  ln -sf /userdata/system/switch/extra/batocera-switch-xdotool /usr/bin/xdotool
 
# move mouse cursor to bottom right corner
if [[ "$w" =~ ^[1-9][0-9]{2,}$ ]] && [[ "$h" =~ ^[1-9][0-9]{2,}$ ]]; then
  xdotool mousemove --sync $w $h 2>/dev/null
else 
  xdotool mousemove --sync 0 0 2>/dev/null
fi
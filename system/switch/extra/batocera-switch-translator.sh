#!/bin/bash

################################################################################
# don't run unless translations are provided 
  exit 0
################################################################################

#-------------------------------------------------------------------------------
t=/userdata/system/switch/extra/translations
e=/userdata/system/configs/emulationstation
f=es_features_switch.cfg
reload=maybe
if [[ -s /usr/bin/batocera-settings-get ]]; then
lang=$(/usr/bin/batocera-settings-get system.language)
  if [[ "$lang" != "not found" ]] && [[ "$lang" != "" ]]; then
  	if [[ -s $t/$lang/$f ]]; then
  	  if [[ "$(diff $t/$lang/$f $e/$f)" != "" ]]; then reload=yes; fi
      cp $t/$lang/$f $e/$f
    else
  	  if [[ "$(diff $t/en_US/$f $e/$f)" != "" ]]; then reload=yes; fi
      cp $t/en_US/$f $e/$f
    fi
  else
  	  if [[ "$(diff $t/en_US/$f $e/$f)" != "" ]]; then reload=yes; fi
      cp $t/en_US/$f $e/$f
  fi
fi
if [[ "$reload" = "yes" ]]; then curl http://127.0.0.1:1234/reloadgames; fi
exit 0
#-------------------------------------------------------------------------------

#!/usr/bin/env python

import generators
from configgen.generators.Generator import Generator
import Command as Command
import os
import stat
from os import path
import batoceraFiles as batoceraFiles
from xml.dom import minidom
import codecs
import controllersConfig as controllersConfig
import configparser
from shutil import copyfile

class RyujinxGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download Ryujinx.AppImage
        st = os.stat("/userdata/system/switch/Ryujinx.AppImage")
        os.chmod("/userdata/system/switch/Ryujinx.AppImage", st.st_mode | stat.S_IEXEC)
            
        if not path.isdir(batoceraFiles.CONF + "/Ryujinx"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx")
        
        RyujinxHome = batoceraFiles.CONF
        
        commandArray = ["/userdata/system/switch/Ryujinx.AppImage", rom ]
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxHome, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb", "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)}
            )

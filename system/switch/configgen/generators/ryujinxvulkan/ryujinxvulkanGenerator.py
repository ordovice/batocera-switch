#!/usr/bin/env python

from configgen.generators.Generator import Generator
import configgen.Command as Command
import os
import stat
from os import path
import configgen.batoceraFiles as batoceraFiles
from xml.dom import minidom
import codecs
import configgen.controllersConfig as controllersConfig
import configparser
from shutil import copyfile

class RyujinxVulkanGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download Ryujinx.AppImage
        st = os.stat("/userdata/system/switch/RyujinxVulkan.AppImage")
        os.chmod("/userdata/system/switch/RyujinxVulkan.AppImage", st.st_mode | stat.S_IEXEC)
            
        if not path.isdir(batoceraFiles.CONF + "/RyujinxVulkan"):
            os.mkdir(batoceraFiles.CONF + "/RyujinxVulkan")
        
        RyujinxVulkanHome = batoceraFiles.CONF + '/RyujinxVulkan'
        
        commandArray = ["/userdata/system/switch/RyujinxVulkan.AppImage", rom ]
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxVulkanHome, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb", "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)}
            )

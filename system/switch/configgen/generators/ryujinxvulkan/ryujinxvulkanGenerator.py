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

class RyujinxVulkanGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download Ryujinx.AppImage
        st = os.stat("/userdata/system/switch/RyujinxVulkan.AppImage")
        os.chmod("/userdata/system/switch/RyujinxVulkan.AppImage", st.st_mode | stat.S_IEXEC)
            
        if not path.isdir(batoceraFiles.CONF + "/RyujinxVulkan"):
            os.mkdir(batoceraFiles.CONF + "/RyujinxVulkan")
        
        copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/RyujinxVulkan/Ryujinx/system/prod.keys")
        copyfile(batoceraFiles.BIOS + "/switch/title.keys", batoceraFiles.CONF + "/RyujinxVulkan/Ryujinx/system/title.keys")

        RyujinxVulkanHome = batoceraFiles.CONF + '/RyujinxVulkan'
        
        if path.exists(batoceraFiles.CONF + "/RyujinxVulkan/Ryujinx/qt-config.ini"):
            commandArray = ["/userdata/system/switch/RyujinxVulkan.AppImage", rom ]
        else:
            commandArray = ["/userdata/system/switch/RyujinxVulkan.AppImage"]
            

        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxVulkanHome, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb", "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)}
            )

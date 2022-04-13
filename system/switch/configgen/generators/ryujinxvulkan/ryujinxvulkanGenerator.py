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

        RyujinxVulkanConfig = batoceraFiles.CONF + '/RyujinxVulkan/qt-config.ini'
        RyujinxVulkanHome = batoceraFiles.CONF + '/RyujinxVulkan'
        

        commandArray = ["/userdata/system/switch/RyujinxVulkan.AppImage", rom ]
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxVulkanHome, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb"}
            )


    @staticmethod
    def writeRyujinxConfig(RyujinxVulkanConfigFile, system, playersControllers):
        # pads
        RyujinxVulkanButtons = {
            "button_a":      "a",
            "button_b":      "b",
            "button_x":      "x",
            "button_y":      "y",
            "button_dup":     "up",
            "button_ddown":   "down",
            "button_dleft":   "left",
            "button_dright":  "right",
            "button_l":      "pageup",
            "button_r":      "pagedown",
            "button_plus":  "start",
            "button_minus": "select",
            "button_zl":     "l2",
            "button_zr":     "r2",
            "button_sl":     "l3",
            "button_sr":     "r3",
            "button_home":   "hotkey"
        }

        RyujinxVulkanAxis = {
            "lstick":    "joystick1",
            "rstick":    "joystick2"
        }

        # ini file
        RyujinxVulkanConfig = configparser.RawConfigParser()
        RyujinxVulkanConfig.optionxform=str
        if os.path.exists(RyujinxConfigFile):
            RyujinxVulkanConfig.read(RyujinxVulkanConfigFile)

        
        # UI section
        if not RyujinxVulkanConfig.has_section("UI"):
            RyujinxVulkanConfig.add_section("UI")
        
        RyujinxVulkanConfig.set("UI", "fullscreen", "true")
        RyujinxVulkanConfig.set("UI", "fullscreen\\default", "true")
        RyujinxVulkanConfig.set("UI", "confirmClose", "false")
        RyujinxVulkanConfig.set("UI", "confirmClose\\default", "false")
        RyujinxVulkanConfig.set("UI", "firstStart", "false")
        RyujinxVulkanConfig.set("UI", "firstStart\\default", "false")
        RyujinxVulkanConfig.set("UI", "displayTitleBars", "false")
        RyujinxVulkanConfig.set("UI", "displayTitleBars\\default", "false")        
        RyujinxVulkanConfig.set("UI", "enable_discord_presence", "false")
        RyujinxVulkanConfig.set("UI", "enable_discord_presence\\default", "false")    
        RyujinxVulkanConfig.set("UI", "calloutFlags", "1")
        RyujinxVulkanConfig.set("UI", "calloutFlags\\default", "false")     
        RyujinxVulkanConfig.set("UI", "singleWindowMode", "true")
        RyujinxVulkanConfig.set("UI", "singleWindowMode\\default", "true")            


        # controls section
        if not RyujinxVulkanConfig.has_section("Controls"):
            RyujinxVulkanConfig.add_section("Controls")


        # Options required to load the functions when the configuration file is created
        if not RyujinxVulkanConfig.has_option("Controls", "vibration_enabled"):
            RyujinxVulkanConfig.set("Controls", "vibration_enabled", "false")
            RyujinxVulkanConfig.set("Controls", "vibration_enabled\\default", "false")    
            RyujinxVulkanConfig.set("Controls", "use_docked_mode", "true")
            RRyujinxVulkanConfig.set("Controls", "use_docked_mode\\default", "true")
            #RyujinxConfig.set("Controls", "profiles\\size", 1)

        for index in playersControllers :
            controller = playersControllers[index]
            controllernumber = str(int(controller.player) - 1)
            for x in RyujinxVulkanButtons:
                RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(RyujinxVulkanGenerator.setButton(RyujinxVulkanButtons[x], controller.guid, controller.inputs,controllernumber)))
            for x in RyujinxVulkanAxis:
                RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(RyujinxVulkanGenerator.setAxis(RyujinxVulkanAxis[x], controller.guid, controller.inputs,controllernumber)))
            RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
            RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_type", "0")
            RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_type\\default", "0")
            RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "false")
            RyujinxVulkanConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "false")
        
            
        # telemetry section
        if not RyujinxVulkanConfig.has_section("WebService"):
            RyujinxVulkanConfig.add_section("WebService") 
        RyujinxVulkanConfig.set("WebService", "enable_telemetry", "false")
        RyujinxVulkanConfig.set("WebService", "enable_telemetry\\default", "false") 
        
        
        # controls section
        if not RyujinxVulkanConfig.has_section("Services"):
            RyujinxVulkanConfig.add_section("Services")
        RyujinxVulkanConfig.set("Services", "bcat_backend", "none")
        RyujinxVulkanConfig.set("Services", "bcat_backend\\default", "none") 

        ### update the configuration file
        if not os.path.exists(os.path.dirname(RyujinxVulkanConfigFile)):
            os.makedirs(os.path.dirname(RyujinxVulkanConfigFile))
        with open(RyujinxVulkanConfigFile, 'w') as configfile:
            RyujinxVulkanConfig.write(configfile)

    @staticmethod
    def setButton(key, padGuid, padInputs,controllernumber):
        # it would be better to pass the joystick num instead of the guid because 2 joysticks may have the same guid
        if key in padInputs:
            input = padInputs[key]

            if input.type == "button":
                return ("button:{},guid:{},engine:sdl,port:{}").format(input.id, padGuid,controllernumber)
            elif input.type == "hat":
                return ("engine:sdl,guid:{},hat:{},direction:{},port:{}").format(padGuid, input.id, RyujinxVulkanGenerator.hatdirectionvalue(input.value),controllernumber)
            elif input.type == "axis":
                # untested, need to configure an axis as button / triggers buttons to be tested too
                return ("engine:sdl,guid:{},axis:{},direction:{},threshold:{},port:{}").format(padGuid, input.id, "+", 0.5,controllernumber)

    @staticmethod
    def setAxis(key, padGuid, padInputs,controllernumber):
        inputx = -1
        inputy = -1

        if key == "joystick1":
            try:
                 inputx = padInputs["joystick1left"]
            except:
                 inputx = ["0"]
        elif key == "joystick2":
            try:
                 inputx = padInputs["joystick2left"]
            except:
                 inputx = ["0"]

        if key == "joystick1":
            try:
                 inputy = padInputs["joystick1up"]
            except:
                 inputy = ["0"]
        elif key == "joystick2":
            try:
                 inputy = padInputs["joystick2up"]
            except:
                 inputy = ["0"]

        try:
            return ("axis_x:{},guid:{},axis_y:{},engine:sdl,,port:{}").format(inputx.id, padGuid, inputy.id,controllernumber)
        except:
            return ("0")

    @staticmethod
    def hatdirectionvalue(value):
        if int(value) == 1:
            return "up"
        if int(value) == 4:
            return "down"
        if int(value) == 2:
            return "right"
        if int(value) == 8:
            return "left"
        return "unknown"
    
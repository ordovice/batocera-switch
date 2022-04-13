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

class RyujinxGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download Ryujinx.AppImage
        st = os.stat("/userdata/system/switch/Ryujinx.AppImage")
        os.chmod("/userdata/system/switch/Ryujinx.AppImage", st.st_mode | stat.S_IEXEC)
        if not path.isdir(batoceraFiles.SAVES + "/Ryujinx"):
            os.mkdir(batoceraFiles.SAVES + "/Ryujinx")
            
        if not path.isdir(batoceraFiles.CONF + "/Ryujinx"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx")
        
        if not path.isdir(batoceraFiles.CONF + "/Ryujinx/system"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx/system")

        copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/Ryujinx/system/prod.keys")


        RyujinxConfig = batoceraFiles.CONF + '/Ryujinx/qt-config.ini'
        RyujinxHome = batoceraFiles.CONF
        RyujinxSaves = batoceraFiles.CONF
        
        RyujinxGenerator.writeRyujinxConfig(RyujinxConfig, system, playersControllers)

        commandArray = ["/userdata/system/switch/Ryujinx.AppImage", rom ]
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxHome, "XDG_DATA_HOME":RyujinxSaves, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb"}
            )


    @staticmethod
    def writeRyujinxConfig(RyujinxConfigFile, system, playersControllers):
        # pads
        RyujinxButtons = {
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

        RyujinxAxis = {
            "lstick":    "joystick1",
            "rstick":    "joystick2"
        }

        # ini file
        RyujinxConfig = configparser.RawConfigParser()
        RyujinxConfig.optionxform=str
        if os.path.exists(RyujinxConfigFile):
            RyujinxConfig.read(RyujinxConfigFile)

        
        # UI section
        if not RyujinxConfig.has_section("UI"):
            RyujinxConfig.add_section("UI")
        
        RyujinxConfig.set("UI", "fullscreen", "true")
        RyujinxConfig.set("UI", "fullscreen\\default", "true")
        RyujinxConfig.set("UI", "confirmClose", "false")
        RyujinxConfig.set("UI", "confirmClose\\default", "false")
        RyujinxConfig.set("UI", "firstStart", "false")
        RyujinxConfig.set("UI", "firstStart\\default", "false")
        RyujinxConfig.set("UI", "displayTitleBars", "false")
        RyujinxConfig.set("UI", "displayTitleBars\\default", "false")        
        RyujinxConfig.set("UI", "enable_discord_presence", "false")
        RyujinxConfig.set("UI", "enable_discord_presence\\default", "false")    
        RyujinxConfig.set("UI", "calloutFlags", "1")
        RyujinxConfig.set("UI", "calloutFlags\\default", "false")     
        RyujinxConfig.set("UI", "singleWindowMode", "true")
        RyujinxConfig.set("UI", "singleWindowMode\\default", "true")            


        # controls section
        if not RyujinxConfig.has_section("Controls"):
            RyujinxConfig.add_section("Controls")


        # Options required to load the functions when the configuration file is created
        if not RyujinxConfig.has_option("Controls", "vibration_enabled"):
            RyujinxConfig.set("Controls", "vibration_enabled", "false")
            RyujinxConfig.set("Controls", "vibration_enabled\\default", "false")    
            RyujinxConfig.set("Controls", "use_docked_mode", "true")
            RyujinxConfig.set("Controls", "use_docked_mode\\default", "true")
            #RyujinxConfig.set("Controls", "profiles\\size", 1)

        for index in playersControllers :
            controller = playersControllers[index]
            controllernumber = str(int(controller.player) - 1)
            for x in RyujinxButtons:
                RyujinxConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(RyujinxGenerator.setButton(RyujinxButtons[x], controller.guid, controller.inputs,controllernumber)))
            for x in RyujinxAxis:
                RyujinxConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(RyujinxGenerator.setAxis(RyujinxAxis[x], controller.guid, controller.inputs,controllernumber)))
            RyujinxConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
            RyujinxConfig.set("Controls", "player_" + controllernumber + "_type", "0")
            RyujinxConfig.set("Controls", "player_" + controllernumber + "_type\\default", "0")
            RyujinxConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "false")
            RyujinxConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "false")
        
            
        # telemetry section
        if not RyujinxConfig.has_section("WebService"):
            RyujinxConfig.add_section("WebService") 
        RyujinxConfig.set("WebService", "enable_telemetry", "false")
        RyujinxConfig.set("WebService", "enable_telemetry\\default", "false") 
        
        
        # controls section
        if not RyujinxConfig.has_section("Services"):
            RyujinxConfig.add_section("Services")
        RyujinxConfig.set("Services", "bcat_backend", "none")
        RyujinxConfig.set("Services", "bcat_backend\\default", "none") 

        ### update the configuration file
        if not os.path.exists(os.path.dirname(RyujinxConfigFile)):
            os.makedirs(os.path.dirname(RyujinxConfigFile))
        with open(RyujinxConfigFile, 'w') as configfile:
            RyujinxConfig.write(configfile)

    @staticmethod
    def setButton(key, padGuid, padInputs,controllernumber):
        # it would be better to pass the joystick num instead of the guid because 2 joysticks may have the same guid
        if key in padInputs:
            input = padInputs[key]

            if input.type == "button":
                return ("button:{},guid:{},engine:sdl,port:{}").format(input.id, padGuid,controllernumber)
            elif input.type == "hat":
                return ("engine:sdl,guid:{},hat:{},direction:{},port:{}").format(padGuid, input.id, RyujinxGenerator.hatdirectionvalue(input.value),controllernumber)
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
    
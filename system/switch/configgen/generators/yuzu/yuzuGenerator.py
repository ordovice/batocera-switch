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

class YuzuGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download yuzu.AppImage
        st = os.stat("/userdata/system/switch/yuzu.AppImage")
        os.chmod("/userdata/system/switch/yuzu.AppImage", st.st_mode | stat.S_IEXEC)
        if not path.isdir(batoceraFiles.SAVES + "/yuzu"):
            os.mkdir(batoceraFiles.SAVES + "/yuzu")
            
        if not path.isdir(batoceraFiles.CONF + "/yuzu"):
            os.mkdir(batoceraFiles.CONF + "/yuzu")
        
        if not path.isdir(batoceraFiles.CONF + "/yuzu/keys"):
            os.mkdir(batoceraFiles.CONF + "/yuzu/keys")

        copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/yuzu/keys/prod.keys")


        yuzuConfig = batoceraFiles.CONF + '/yuzu/qt-config.ini'
        yuzuHome = batoceraFiles.CONF
        yuzuSaves = batoceraFiles.CONF
        
        YuzuGenerator.writeYuzuConfig(yuzuConfig, system, playersControllers)

        commandArray = ["/userdata/system/switch/yuzu.AppImage", "-f", "-g", rom ]
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":yuzuHome, "XDG_DATA_HOME":yuzuSaves, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb"}
            )


    @staticmethod
    def writeYuzuConfig(yuzuConfigFile, system, playersControllers):
        # pads
        yuzuButtons = {
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

        yuzuAxis = {
            "lstick":    "joystick1",
            "rstick":    "joystick2"
        }

        # ini file
        yuzuConfig = configparser.RawConfigParser()
        yuzuConfig.optionxform=str
        if os.path.exists(yuzuConfigFile):
            yuzuConfig.read(yuzuConfigFile)

        
        # UI section
        if not yuzuConfig.has_section("UI"):
            yuzuConfig.add_section("UI")
        
        yuzuConfig.set("UI", "fullscreen", "true")
        yuzuConfig.set("UI", "fullscreen\\default", "true")
        yuzuConfig.set("UI", "confirmClose", "false")
        yuzuConfig.set("UI", "confirmClose\\default", "false")
        yuzuConfig.set("UI", "firstStart", "false")
        yuzuConfig.set("UI", "firstStart\\default", "false")
        yuzuConfig.set("UI", "displayTitleBars", "false")
        yuzuConfig.set("UI", "displayTitleBars\\default", "false")        
        yuzuConfig.set("UI", "enable_discord_presence", "false")
        yuzuConfig.set("UI", "enable_discord_presence\\default", "false")    
        yuzuConfig.set("UI", "calloutFlags", "1")
        yuzuConfig.set("UI", "calloutFlags\\default", "false")     
        yuzuConfig.set("UI", "singleWindowMode", "true")
        yuzuConfig.set("UI", "singleWindowMode\\default", "true")            


        # controls section
        if not yuzuConfig.has_section("Controls"):
            yuzuConfig.add_section("Controls")


        # Options required to load the functions when the configuration file is created
        if not yuzuConfig.has_option("Controls", "vibration_enabled"):
            yuzuConfig.set("Controls", "vibration_enabled", "false")
            yuzuConfig.set("Controls", "vibration_enabled\\default", "false")    
            yuzuConfig.set("Controls", "use_docked_mode", "true")
            yuzuConfig.set("Controls", "use_docked_mode\\default", "true")
            #yuzuConfig.set("Controls", "profiles\\size", 1)

        for index in playersControllers :
            controller = playersControllers[index]
            controllernumber = str(int(controller.player) - 1)
            for x in yuzuButtons:
                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuGenerator.setButton(yuzuButtons[x], controller.guid, controller.inputs,controllernumber)))
            for x in yuzuAxis:
                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuGenerator.setAxis(yuzuAxis[x], controller.guid, controller.inputs,controllernumber)))
            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "0")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "0")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "false")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "false")
        
            
        # telemetry section
        if not yuzuConfig.has_section("WebService"):
            yuzuConfig.add_section("WebService") 
        yuzuConfig.set("WebService", "enable_telemetry", "false")
        yuzuConfig.set("WebService", "enable_telemetry\\default", "false") 
        
        
        # controls section
        if not yuzuConfig.has_section("Services"):
            yuzuConfig.add_section("Services")
        yuzuConfig.set("Services", "bcat_backend", "none")
        yuzuConfig.set("Services", "bcat_backend\\default", "none") 

        ### update the configuration file
        if not os.path.exists(os.path.dirname(yuzuConfigFile)):
            os.makedirs(os.path.dirname(yuzuConfigFile))
        with open(yuzuConfigFile, 'w') as configfile:
            yuzuConfig.write(configfile)

    @staticmethod
    def setButton(key, padGuid, padInputs,controllernumber):
        # it would be better to pass the joystick num instead of the guid because 2 joysticks may have the same guid
        if key in padInputs:
            input = padInputs[key]

            if input.type == "button":
                return ("button:{},guid:{},engine:sdl,port:{}").format(input.id, padGuid,controllernumber)
            elif input.type == "hat":
                return ("engine:sdl,guid:{},hat:{},direction:{},port:{}").format(padGuid, input.id, YuzuGenerator.hatdirectionvalue(input.value),controllernumber)
            elif input.type == "axis":
                # untested, need to configure an axis as button / triggers buttons to be tested too
                return ("engine:sdl,guid:{},axis:{},direction:{},threshold:{},port:{}").format(padGuid, input.id, "+", 0.5,controllernumber)

    @staticmethod
    def setAxis(key, padGuid, padInputs,controllernumber):
        inputx = -1
        inputy = -1

        if key == "joystick1":
            inputx = padInputs["joystick1left"]
        elif key == "joystick2":
            inputx = padInputs["joystick2left"]

        if key == "joystick1":
            inputy = padInputs["joystick1up"]
        elif key == "joystick2":
            inputy = padInputs["joystick2up"]

        return ("axis_x:{},guid:{},axis_y:{},engine:sdl,,port:{}").format(inputx.id, padGuid, inputy.id,controllernumber)

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
    
#!/usr/bin/env python

from configgen.generators.Generator import Generator
import configgen.Command as Command
import os
from os import path
import configgen.batoceraFiles as batoceraFiles
from xml.dom import minidom
import codecs
import configgen.controllersConfig as controllersConfig
import ConfigParser
from shutil import copyfile

class YuzuGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        if not path.isdir(batoceraFiles.SAVES + "/yuzu"):
            os.mkdir(batoceraFiles.SAVES + "/yuzu")
            
        if not path.isdir(batoceraFiles.CONF + "/yuzu"):
            os.mkdir(batoceraFiles.CONF + "/yuzu")
        
        if not path.isdir(batoceraFiles.CONF + "/yuzu/keys"):
            os.mkdir(batoceraFiles.CONF + "/yuzu/keys")

        copyfile(batoceraFiles.BIOS + "/yuzu/prod.keys", batoceraFiles.CONF + "/yuzu/keys/prod.keys")


        yuzuConfig = batoceraFiles.CONF + '/yuzu/qt-config.ini'
        yuzuHome = batoceraFiles.CONF
        yuzuSaves = batoceraFiles.CONF
        
        YuzuGenerator.writeYuzuConfig(yuzuConfig, system, playersControllers)

        commandArray = ["/userdata/system/switch/yuzu.AppImage", rom]
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
        yuzuConfig = ConfigParser.RawConfigParser()
        if os.path.exists(yuzuConfigFile):
            yuzuConfig.read(yuzuConfigFile)

        
        # UI section
        if not yuzuConfig.has_section("UI"):
            yuzuConfig.add_section("UI")
        
        yuzuConfig.set("UI", "fullscreen", "true")
        yuzuConfig.set("UI", "fullscreen\\default", "true")
        yuzuConfig.set("UI", "confirmclose", "false")
        yuzuConfig.set("UI", "confirmclose\\default", "false")
        yuzuConfig.set("UI", "firstStart", "false")
        yuzuConfig.set("UI", "firstStart\\default", "false")
        yuzuConfig.set("UI", "displayTitleBars", "false")
        yuzuConfig.set("UI", "displayTitleBars\\default", "false")        
        yuzuConfig.set("UI", "enable_discord_presence", "false")
        yuzuConfig.set("UI", "enable_discord_presence\\default", "false")       


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
            for x in yuzuButtons:
                yuzuConfig.set("Controls", "player_" + controller.player + "_" + x, '"{}"'.format(YuzuGenerator.setButton(yuzuButtons[x], controller.guid, controller.inputs)))
            for x in yuzuAxis:
                yuzuConfig.set("Controls", "player_" + controller.player + "_" + x, '"{}"'.format(YuzuGenerator.setAxis(yuzuAxis[x], controller.guid, controller.inputs)))
            break
            
            yuzuConfig.set("Controls", "player_" + controller.player + "_connected", "true")
            
        # telemetry section
        if not yuzuConfig.has_section("WebService"):
            yuzuConfig.add_section("WebService") 
        yuzuConfig.set("WebService", "enable_telemetry", "false")
        yuzuConfig.set("WebService", "enable_telemetry\\default", "false") 


        ### update the configuration file
        if not os.path.exists(os.path.dirname(yuzuConfigFile)):
            os.makedirs(os.path.dirname(yuzuConfigFile))
        with open(yuzuConfigFile, 'w') as configfile:
            yuzuConfig.write(configfile)

    @staticmethod
    def setButton(key, padGuid, padInputs):
        # it would be better to pass the joystick num instead of the guid because 2 joysticks may have the same guid
        if key in padInputs:
            input = padInputs[key]

            if input.type == "button":
                return ("button:{},guid:{},engine:sdl").format(input.id, padGuid)
            elif input.type == "hat":
                return ("engine:sdl,guid:{},hat:{},direction:{}").format(padGuid, input.id, YuzuGenerator.hatdirectionvalue(input.value))
            elif input.type == "axis":
                # untested, need to configure an axis as button / triggers buttons to be tested too
                return ("engine:sdl,guid:{},axis:{},direction:{},threshold:{}").format(padGuid, input.id, "+", 0.5)

    @staticmethod
    def setAxis(key, padGuid, padInputs):
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

        return ("axis_x:{},guid:{},axis_y:{},engine:sdl").format(inputx.id, padGuid, inputy.id)

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
    
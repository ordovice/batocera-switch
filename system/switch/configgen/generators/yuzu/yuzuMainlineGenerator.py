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
from utils.logger import get_logger

eslog = get_logger(__name__)

class YuzuMainlineGenerator(Generator):

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
        copyfile(batoceraFiles.BIOS + "/switch/title.keys", batoceraFiles.CONF + "/yuzu/keys/title.keys")

        yuzuConfig = batoceraFiles.CONF + '/yuzu/qt-config.ini'
        yuzuHome = batoceraFiles.CONF
        yuzuSaves = batoceraFiles.CONF
        
        YuzuMainlineGenerator.writeYuzuConfig(yuzuConfig, system, playersControllers)

        commandArray = ["/userdata/system/switch/yuzu.AppImage", "-f", "-g", rom ]
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":yuzuHome, "XDG_DATA_HOME":yuzuSaves, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb", "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)}
            )


    # @staticmethod
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
            "button_sl":     "l",
            "button_sr":     "r",
            "button_zl":     "l2",
            "button_zr":     "r2",
            "button_lstick":     "l3",
            "button_rstick":     "r3",
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
        
        yuzuConfig.set("UI", "fullscreen", "false")
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
        yuzuConfig.set("UI", "hideInactiveMouse", "true")
        yuzuConfig.set("UI", "hideInactiveMouse\\default", "false")

        # Roms path (need for load update/dlc)
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\deep_scan", "false")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\deep_scan\\default", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\expanded", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\expanded\\default", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\path", "/userdata/roms/switch")
        yuzuConfig.set("UI", "Paths\\gamedirs\\size", "1")

    # Core section
        if not yuzuConfig.has_section("Core"):
            yuzuConfig.add_section("Core")

        # Multicore
        if system.isOptSet('multicore'):
            yuzuConfig.set("Core", "use_multi_core", system.config["multicore"])
        else:
            yuzuConfig.set("Core", "use_multi_core", "true")
        yuzuConfig.set("Core", "use_multi_core\\default", "false")

    # Renderer section
        if not yuzuConfig.has_section("Renderer"):
            yuzuConfig.add_section("Renderer")

        # Aspect ratio
        if system.isOptSet('yuzu_ratio'):
            yuzuConfig.set("Renderer", "aspect_ratio", system.config["yuzu_ratio"])
        else:
            yuzuConfig.set("Renderer", "aspect_ratio", "0")
        yuzuConfig.set("Renderer", "aspect_ratio\\default", "false")

        # Graphical backend
        if system.isOptSet('yuzu_backend'):
            yuzuConfig.set("Renderer", "backend", system.config["yuzu_backend"])
        else:
            yuzuConfig.set("Renderer", "backend", "0")
        yuzuConfig.set("Renderer", "backend\\default", "false")

        # Async Shader compilation
        if system.isOptSet('async_shaders'):
            yuzuConfig.set("Renderer", "use_asynchronous_shaders", system.config["async_shaders"])
        else:
            yuzuConfig.set("Renderer", "use_asynchronous_shaders", "true")
        yuzuConfig.set("Renderer", "use_asynchronous_shaders\\default", "false")

        # Assembly shaders
        if system.isOptSet('shaderbackend'):
            yuzuConfig.set("Renderer", "shader_backend", system.config["shaderbackend"])
        else:
            yuzuConfig.set("Renderer", "shader_backend", "0")
        yuzuConfig.set("Renderer", "shader_backend\\default", "false")

        # Async Gpu Emulation
        if system.isOptSet('async_gpu'):
            yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation", system.config["async_gpu"])
        else:
            yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation", "true")
        yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation\\default", "false")

        # Use NVDEC Emulation
        if system.isOptSet('nvdec_emu'):
            yuzuConfig.set("Renderer", "use_nvdec_emulation", system.config["nvdec_emu"])
        else:
            yuzuConfig.set("Renderer", "use_nvdec_emulation", "true")
        yuzuConfig.set("Renderer", "use_nvdec_emulation\\default", "false")

        # Gpu Accuracy
        if system.isOptSet('gpuaccuracy'):
            yuzuConfig.set("Renderer", "gpu_accuracy", system.config["gpuaccuracy"])
        else:
            yuzuConfig.set("Renderer", "gpu_accuracy", "0")
        yuzuConfig.set("Renderer", "gpu_accuracy\\default", "false")

        # Vsync
        if system.isOptSet('vsync'):
            yuzuConfig.set("Renderer", "use_vsync", system.config["vsync"])
        else:
            yuzuConfig.set("Renderer", "use_vsync", "false")
        yuzuConfig.set("Renderer", "use_vsync\\default", "false")

        # Gpu cache garbage collection
        if system.isOptSet('gpu_cache_gc'):
            yuzuConfig.set("Renderer", "use_caches_gc", system.config["gpu_cache_gc"])
        else:
            yuzuConfig.set("Renderer", "use_caches_gc", "false")
        yuzuConfig.set("Renderer", "use_caches_gc\\default", "false")

        # Max anisotropy
        if system.isOptSet('anisotropy'):
            yuzuConfig.set("Renderer", "max_anisotropy", system.config["anisotropy"])
        else:
            yuzuConfig.set("Renderer", "max_anisotropy", "0")
        yuzuConfig.set("Renderer", "max_anisotropy\\default", "false")

        # Resolution scaler
        if system.isOptSet('resolution_scale'):
            yuzuConfig.set("Renderer", "resolution_setup", system.config["resolution_scale"])
        else:
            yuzuConfig.set("Renderer", "resolution_setup", "2")
        yuzuConfig.set("Renderer", "resolution_setup\\default", "false")

        # Scaling filter
        if system.isOptSet('scale_filter'):
            yuzuConfig.set("Renderer", "scaling_filter", system.config["scale_filter"])
        else:
            yuzuConfig.set("Renderer", "scaling_filter", "1")
        yuzuConfig.set("Renderer", "scaling_filter\\default", "false")

        # Anti aliasing method
        if system.isOptSet('aliasing_method'):
            yuzuConfig.set("Renderer", "anti_aliasing", system.config["aliasing_method"])
        else:
            yuzuConfig.set("Renderer", "anti_aliasing", "0")
        yuzuConfig.set("Renderer", "anti_aliasing\\default", "false")

    # Cpu Section
        if not yuzuConfig.has_section("Cpu"):
            yuzuConfig.add_section("Cpu")

        # Cpu Accuracy
        if system.isOptSet('cpuaccuracy'):
            yuzuConfig.set("Cpu", "cpu_accuracy", system.config["cpuaccuracy"])
        else:
            yuzuConfig.set("Cpu", "cpu_accuracy", "0")
        yuzuConfig.set("Cpu", "cpu_accuracy\\default", "false")

    # System section
        if not yuzuConfig.has_section("System"):
            yuzuConfig.add_section("System")

        # Language
        if system.isOptSet('language'):
            yuzuConfig.set("System", "language_index", system.config["language"])
        else:
            yuzuConfig.set("System", "language_index", "2")
        yuzuConfig.set("System", "language_index\\default", "false")

        # Region
        if system.isOptSet('region'):
            yuzuConfig.set("System", "region_index", system.config["region"])
        else:
            yuzuConfig.set("System", "region_index", "2")
        yuzuConfig.set("System", "region_index\\default", "false")

    # controls section
        if not yuzuConfig.has_section("Controls"):
            yuzuConfig.add_section("Controls")

        # Dock Mode
        if system.isOptSet('dock_mode'):
            yuzuConfig.set("Controls", "use_docked_mode", system.config["dock_mode"])
        else:
            yuzuConfig.set("Controls", "use_docked_mode", "true")
        yuzuConfig.set("Controls", "use_docked_mode\\default", "false")

        # Player 1 Pad Type
        if system.isOptSet('p1_pad'):
            yuzuConfig.set("Controls", "player_0_type", system.config["p1_pad"])
        else:
            yuzuConfig.set("Controls", "player_0_type", "0")
        yuzuConfig.set("Controls", "player_0_type\default", "false")

        # Player 2 Pad Type
        if system.isOptSet('p2_pad'):
            yuzuConfig.set("Controls", "player_1_type", system.config["p2_pad"])
        else:
            yuzuConfig.set("Controls", "player_1_type", "0")
        yuzuConfig.set("Controls", "player_1_type\default", "false")

        yuzuConfig.set("Controls", "vibration_enabled", "true")
        yuzuConfig.set("Controls", "vibration_enabled\\default", "false")
        yuzuConfig.set("Controls", "player_0_connected", "true")
        yuzuConfig.set("Controls", "player_0_connected\\default", "false")
        yuzuConfig.set("Controls", "player_0_vibration_enabled", "true")
        yuzuConfig.set("Controls", "player_0_vibration_enabled\\default", "false")
        yuzuConfig.set("Controls", "player_1_connected", "true")
        yuzuConfig.set("Controls", "player_1_connected\\default", "false")
        yuzuConfig.set("Controls", "player_1_vibration_enabled", "true")
        yuzuConfig.set("Controls", "player_1_vibration_enabled\\default", "false")
        #yuzuConfig.set("Controls", "profiles\\size", 1)
        
        
        #lastcontrollerguid = ""
        #lastcontrollernumber = 0
        cguid = [0 for x in range(10)]

        for index in playersControllers :
            controller = playersControllers[index]
            portnumber = cguid.count(controller.guid)
            controllernumber = str(int(controller.player) - 1)
            cguid[int(controllernumber)] = controller.guid
            inputguid = controller.guid
            guidstoreplace = ["050000004c050000cc09000000810000","050000004c050000c405000000810000"]
            if controller.guid in guidstoreplace:
                inputguid = "030000004c050000cc09000000006800"

            for x in yuzuButtons:
                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setButton(yuzuButtons[x], inputguid, controller.inputs,portnumber)))
            for x in yuzuAxis:
                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setAxis(yuzuAxis[x], inputguid, controller.inputs, portnumber)))
            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\default", "false")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "0")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "false")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")

    # telemetry section
        if not yuzuConfig.has_section("WebService"):
            yuzuConfig.add_section("WebService") 
        yuzuConfig.set("WebService", "enable_telemetry", "false")
        yuzuConfig.set("WebService", "enable_telemetry\\default", "false") 
        
        
    # Services section
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
                return ("button:{},guid:{},port:{},engine:sdl").format(input.id, padGuid, controllernumber)
            elif input.type == "hat":
                return ("hat:{},direction:{},guid:{},port:{},engine:sdl").format(input.id, YuzuMainlineGenerator.hatdirectionvalue(input.value), padGuid, controllernumber)
            elif input.type == "axis":
                # untested, need to configure an axis as button / triggers buttons to be tested too
                return ("threshold:{},axis:{},guid:{},port:{},invert:{},engine:sdl").format(0.5, input.id, padGuid, controllernumber, "+")

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
            return ("range:1.000000,deadzone:0.100000,invert_y:+,invert_x:+,offset_y:-0.000000,axis_y:{},offset_x:-0.000000,axis_x:{},guid:{},port:{},engine:sdl").format(inputy.id, inputx.id, padGuid, controllernumber)
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
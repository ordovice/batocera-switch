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
        if os.path.exists("/userdata/system/switch/yuzu.AppImage"):
            st = os.stat("/userdata/system/switch/yuzu.AppImage")
            os.chmod("/userdata/system/switch/yuzu.AppImage", st.st_mode | stat.S_IEXEC)

        if os.path.exists("/userdata/system/switch/yuzuEA.AppImage"):
            st = os.stat("/userdata/system/switch/yuzuEA.AppImage")
            os.chmod("/userdata/system/switch/yuzuEA.AppImage", st.st_mode | stat.S_IEXEC)

        if not os.path.exists("/lib/libthai.so.0.3.1"):
            copyfile("/userdata/system/switch/extra/libthai.so.0.3.1", "/lib/libthai.so.0.3.1")
        if not os.path.exists("/lib/libthai.so.0"):
            st = os.symlink("/lib/libthai.so.0.3.1","/lib/libthai.so.0")

        #Create Keys Folder
        if not os.path.exists(batoceraFiles.CONF + "/yuzu"):
            os.mkdir(batoceraFiles.CONF + "/yuzu")

        if not os.path.exists(batoceraFiles.CONF + "/yuzu/keys"):
            os.mkdir(batoceraFiles.CONF + "/yuzu/keys")

        #Link Yuzu App Directory to /system/configs/yuzu
        if not os.path.exists("/userdata/system/.local"):
            os.mkdir("/userdata/system/.local")

        if not os.path.exists("/userdata/system/.local/share"):
            os.mkdir("/userdata/system/.local/share")

        if not os.path.exists("/userdata/system/.local/share/yuzu"):
            st = os.symlink("/userdata/system/configs/yuzu","/userdata/system/.local/share/yuzu")

        #Link Yuzu Config Directory to /system/configs/yuzu
        if not os.path.exists("/userdata/system/.config"):
            os.mkdir("/userdata/system/.config")

        if not os.path.exists("/userdata/system/.config/yuzu"):
            st = os.symlink("/userdata/system/configs/yuzu","/userdata/system/.config/yuzu")

        #Link Yuzu Saves Directory to /userdata/saves/yuzu
        if not os.path.exists("/userdata/system/.cache"):
            os.mkdir("/userdata/system/.cache")

        if not os.path.exists("/userdata/system/.cache/yuzu"):
            os.mkdir("/userdata/system/.cache/yuzu")

        if not os.path.exists("/userdata/system/.cache/yuzu/game_list"):
            st = os.symlink("/userdata/saves/yuzu","/userdata/system/.cache/yuzu/game_list")

        copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/yuzu/keys/prod.keys")
        copyfile(batoceraFiles.BIOS + "/switch/title.keys", batoceraFiles.CONF + "/yuzu/keys/title.keys")

        yuzuConfig = batoceraFiles.CONF + '/yuzu/qt-config.ini'
        
        YuzuMainlineGenerator.writeYuzuConfig(yuzuConfig, system, playersControllers)
        if system.config['emulator'] == 'yuzu-early-access':
            commandArray = ["/userdata/system/switch/yuzuEA.AppImage", "-f", "-g", rom ]
        else:
            commandArray = ["/userdata/system/switch/yuzu.AppImage", "-f", "-g", rom ]
                      # "XDG_DATA_HOME":yuzuSaves, , "XDG_CACHE_HOME":batoceraFiles.CACHE, "XDG_CONFIG_HOME":yuzuHome,
        return Command.Command(
            array=commandArray,
            env={"QT_QPA_PLATFORM":"xcb","SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers) }
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


        yuzuDSButtons = {
            "button_a":      1,
            "button_b":      0,
            "button_x":      3,
            "button_y":      2,
            "button_dup":     11,
            "button_ddown":   12,
            "button_dleft":   13,
            "button_dright":  14,
            "button_l":      9,
            "button_r":      10,
            "button_plus":  6,
            "button_minus": 4,
            "button_sl":     9,
            "button_sr":     10,
            "button_lstick":     7,
            "button_rstick":     8,
            "button_home":   5
        }

        yuzuDSAxis = {
            "lstick":    0,
            "rstick":    2,
            "button_zl":     4,
            "button_zr":     5
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
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\deep_scan", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\deep_scan\\default", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\expanded", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\expanded\\default", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\path", "/userdata/roms/switch")
        yuzuConfig.set("UI", "Paths\\gamedirs\\size", "1")

        yuzuConfig.set("UI", "Screenshots\\enable_screenshot_save_as", "true")
        yuzuConfig.set("UI", "Screenshots\\enable_screenshot_save_as\\default", "true")
        yuzuConfig.set("UI", "Screenshots\\screenshot_path", "/userdata/screenshots")
        yuzuConfig.set("UI", "Screenshots\\screenshot_path\\default", "true")

    # Data Storage section
        if not yuzuConfig.has_section("Data%20Storage"):
            yuzuConfig.add_section("Data%20Storage")
        yuzuConfig.set("Data%20Storage", "dump_directory", "/userdata/system/configs/yuzu/dump")
        yuzuConfig.set("Data%20Storage", "dump_directory\\default", "true")

        yuzuConfig.set("Data%20Storage", "load_directory", "/userdata/system/configs/yuzu/load")
        yuzuConfig.set("Data%20Storage", "load_directory\\default", "true")

        yuzuConfig.set("Data%20Storage", "nand_directory", "/userdata/system/configs/yuzu/nand")
        yuzuConfig.set("Data%20Storage", "nand_directory\\default", "true")

        yuzuConfig.set("Data%20Storage", "sdmc_directory", "/userdata/system/configs/yuzu/sdmc")
        yuzuConfig.set("Data%20Storage", "sdmc_directory\\default", "true")

        yuzuConfig.set("Data%20Storage", "tas_directory", "/userdata/system/configs/yuzu/tas")
        yuzuConfig.set("Data%20Storage", "tas_directory\\default", "true")

        yuzuConfig.set("Data%20Storage", "use_virtual_sd", "true")
        yuzuConfig.set("Data%20Storage", "use_virtual_sd\\default", "true")

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
            guidstoreplace_ds4 = ["050000004c050000cc09000000810000","050000004c050000c405000000810000"]
            if controller.guid in guidstoreplace_ds4:
                inputguid = "030000004c050000cc09000000006800"
            
            guidstoreplace_ds5 = ["050000004c050000e60c000000810000"]
            if controller.guid in guidstoreplace_ds5:
                inputguid = "030000004c050000e60c000000006800"

            #DS5 corrections
            if ((controller.guid in guidstoreplace_ds5) or (controller.guid in guidstoreplace_ds4)) :
                #button_a="engine:sdl,port:0,guid:030000004c050000e60c000000006800,button:1"
                for x in yuzuDSButtons:
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},button:{}"'.format(portnumber,inputguid,yuzuDSButtons[x]))
                for x in yuzuDSAxis:
                    if(x == "button_zl" or x == "button_zr"):
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuDSAxis[x]))
                    else:
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:+,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuDSAxis[x],yuzuDSAxis[x]+1))
                yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
            else:
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
                return ("engine:sdl,button:{},guid:{},port:{}").format(input.id, padGuid, controllernumber)
            elif input.type == "hat":
                return ("engine:sdl,hat:{},direction:{},guid:{},port:{}").format(input.id, YuzuMainlineGenerator.hatdirectionvalue(input.value), padGuid, controllernumber)
            elif input.type == "axis":
                # untested, need to configure an axis as button / triggers buttons to be tested too
                return ("engine:sdl,threshold:{},axis:{},guid:{},port:{},invert:{}").format(0.5, input.id, padGuid, controllernumber, "+")
                

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
            return ("engine:sdl,range:1.000000,deadzone:0.100000,invert_y:+,invert_x:+,offset_y:-0.000000,axis_y:{},offset_x:-0.000000,axis_x:{},guid:{},port:{}").format(inputy.id, inputx.id, padGuid, controllernumber)
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
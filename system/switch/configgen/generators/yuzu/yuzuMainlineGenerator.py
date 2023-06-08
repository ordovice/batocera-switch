#!/usr/bin/env python

import generators
from configgen.generators.Generator import Generator
import Command as Command
import os
import shutil
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

        #Create OS Saves folder
        if not os.path.exists(batoceraFiles.SAVES + "/yuzu"):
            os.mkdir(batoceraFiles.SAVES + "/yuzu")        

        #Link Yuzu App Directory to /system/configs/yuzu
        if not os.path.exists("/userdata/system/.local"):
            os.mkdir("/userdata/system/.local")

        if not os.path.exists("/userdata/system/.local/share"):
            os.mkdir("/userdata/system/.local/share")
        
        #Remove .local/share/yuzu if it exists and isnt' a link
        if os.path.exists("/userdata/system/.local/share/yuzu"):
            if not os.path.islink("/userdata/system/.local/share/yuzu"):
                shutil.rmtree("/userdata/system/.local/share/yuzu")
        
        if not os.path.exists("/userdata/system/.local/share/yuzu"):
            st = os.symlink("/userdata/system/configs/yuzu","/userdata/system/.local/share/yuzu")

        #Link Yuzu Config Directory to /system/configs/yuzu
        if not os.path.exists("/userdata/system/.config"):
            os.mkdir("/userdata/system/.config")

        #Remove .config/yuzu if it exists and isnt' a link
        if os.path.exists("/userdata/system/.config/yuzu"):            
            if not os.path.islink("/userdata/system/.config/yuzu"):
                shutil.rmtree("/userdata/system/.config/yuzu")

        if not os.path.exists("/userdata/system/.config/yuzu"):
            st = os.symlink("/userdata/system/configs/yuzu","/userdata/system/.config/yuzu")

        #Link Yuzu Saves Directory to /userdata/saves/yuzu
        if not os.path.exists("/userdata/system/.cache"):
            os.mkdir("/userdata/system/.cache")

        if not os.path.exists("/userdata/system/.cache/yuzu"):
            os.mkdir("/userdata/system/.cache/yuzu")

        #remove game_list if it exists and isn't a link
        if os.path.exists("/userdata/system/.cache/yuzu/game_list"):            
            if not os.path.islink("/userdata/system/.cache/yuzu/game_list"):
                shutil.rmtree("/userdata/system/.cache/yuzu/game_list")

        if not os.path.exists("/userdata/system/.cache/yuzu/game_list"):
            st = os.symlink("/userdata/saves/yuzu","/userdata/system/.cache/yuzu/game_list")

        #copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/yuzu/keys/prod.keys")
        #copyfile(batoceraFiles.BIOS + "/switch/title.keys", batoceraFiles.CONF + "/yuzu/keys/title.keys")

        yuzuConfig = batoceraFiles.CONF + '/yuzu/qt-config.ini'
        beforeyuzuConfig = batoceraFiles.CONF + '/yuzu/before-qt-config.ini'
        
        YuzuMainlineGenerator.writeYuzuConfig(yuzuConfig,beforeyuzuConfig, system, playersControllers)
        if system.config['emulator'] == 'yuzu-early-access':
            commandArray = ["/userdata/system/switch/yuzuEA.AppImage", "-f", "-g", rom ]
        else:
            commandArray = ["/userdata/system/switch/yuzu.AppImage", "-f",  "-g", rom ]
                      # "XDG_DATA_HOME":yuzuSaves, , "XDG_CACHE_HOME":batoceraFiles.CACHE, "XDG_CONFIG_HOME":yuzuHome,
        return Command.Command(
            array=commandArray,
            env={"QT_QPA_PLATFORM":"xcb","SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers) }
            )


    # @staticmethod
    def writeYuzuConfig(yuzuConfigFile, beforeyuzuConfigFile, system, playersControllers):
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
            "button_sl":     "pageup",
            "button_sr":     "pagedown",
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

        yuzuSCButtons = {
            "button_a":      6,
            "button_b":     5,
            "button_x":      8,
            "button_y":      7,
            "button_dup":     20,
            "button_ddown":   21,
            "button_dleft":   22,
            "button_dright":  23,
            "button_l":      9,
            "button_r":      10,
            "button_plus":  14,
            "button_minus": 13,
            #"button_zl":     18,
            #"button_zr":     10,
            "button_lstick":     16,
            "button_rstick":     17,
            "button_home":   13
        }

        yuzuSCAxis = {
            "lstick":    1,
            "rstick":    4,
            "button_zl":     2,
            "button_zr":     5
        }

        yuzuSCButtons2 = {
            "button_a":      4,
            "button_b":     5,
            "button_x":      6,
            "button_y":      7,
            "button_dup":     19,
            "button_ddown":   20,
            "button_dleft":   21,
            "button_dright":  22,
            "button_l":      8,
            "button_r":      10,
            "button_plus":  13,
            "button_minus": 12,
            #"button_zl":     18,
            #"button_zr":     10,
            "button_lstick":     15,
            "button_rstick":     16,
            "button_home":   23
        }

        yuzuSCAxis2 = {
            "lstick":    1,
            "rstick":    4,
            "button_zl":     2,
            "button_zr":     5
        }

        yuzuSwitchButtons = {
            "button_a":      0,
            "button_b":      1,
            "button_x":      2,
            "button_y":      3,
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

        yuzuSwitchAxis = {
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
        
        yuzuConfig.set("UI", "fullscreen", "true")
        yuzuConfig.set("UI", "fullscreen\\default", "false")
        yuzuConfig.set("UI", "confirmClose", "false")
        yuzuConfig.set("UI", "confirmClose\\default", "false")
        yuzuConfig.set("UI", "firstStart", "false")
        yuzuConfig.set("UI", "firstStart\\default", "false")
        yuzuConfig.set("UI", "displayTitleBars", "false")
        yuzuConfig.set("UI", "displayTitleBars\\default", "false")

        if system.isOptSet('yuzu_enable_discord_presence'):
            yuzuConfig.set("UI", "enable_discord_presence", system.config["yuzu_enable_discord_presence"])
        else:
            yuzuConfig.set("UI", "enable_discord_presence", "false")

        yuzuConfig.set("UI", "enable_discord_presence\\default", "false")



        yuzuConfig.set("UI", "calloutFlags", "1")
        yuzuConfig.set("UI", "calloutFlags\\default", "false")

        # Single Window Mode
        if system.isOptSet('single_window'):
            yuzuConfig.set("UI", "singleWindowMode", system.config["single_window"])
            yuzuConfig.set("UI", "singleWindowMode\\default", "false")
        else:
            yuzuConfig.set("UI", "singleWindowMode", "true")
            yuzuConfig.set("UI", "singleWindowMode\\default", "true")

        # User Profile select on boot
        if system.isOptSet('user_profile'):
            yuzuConfig.set("UI", "select_user_on_boot", system.config["user_profile"])
            yuzuConfig.set("UI", "select_user_on_boot\\default", "false")
        else:
            yuzuConfig.set("UI", "select_user_on_boot", "true")
            yuzuConfig.set("UI", "select_user_on_boot\\default", "true")

        yuzuConfig.set("UI", "hideInactiveMouse", "true")
        yuzuConfig.set("UI", "hideInactiveMouse\\default", "true")

        # Roms path (need for load update/dlc)
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\deep_scan", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\deep_scan\\default", "false")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\expanded", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\expanded\\default", "true")
        yuzuConfig.set("UI", "Paths\\gamedirs\\1\\path", "/userdata/roms/switch")
        yuzuConfig.set("UI", "Paths\\gamedirs\\size", "1")

        yuzuConfig.set("UI", "Screenshots\\enable_screenshot_save_as", "true")
        yuzuConfig.set("UI", "Screenshots\\enable_screenshot_save_as\\default", "true")
        yuzuConfig.set("UI", "Screenshots\\screenshot_path", "/userdata/screenshots")
        yuzuConfig.set("UI", "Screenshots\\screenshot_path\\default", "false")

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
            yuzuConfig.set("Core", "use_multi_core\\default", "false")
        else:
            yuzuConfig.set("Core", "use_multi_core", "true")
            yuzuConfig.set("Core", "use_multi_core\\default", "true")

    # Renderer section
        if not yuzuConfig.has_section("Renderer"):
            yuzuConfig.add_section("Renderer")

        # Aspect ratio
        if system.isOptSet('yuzu_ratio'):
            yuzuConfig.set("Renderer", "aspect_ratio", system.config["yuzu_ratio"])
            yuzuConfig.set("Renderer", "aspect_ratio\\default", "false")
        else:
            yuzuConfig.set("Renderer", "aspect_ratio", "0")
            yuzuConfig.set("Renderer", "aspect_ratio\\default", "true")

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
            yuzuConfig.set("Renderer", "shader_backend\\default", "false")
        else:
            yuzuConfig.set("Renderer", "shader_backend", "0")
            yuzuConfig.set("Renderer", "shader_backend\\default", "true")

        # Async Gpu Emulation
        if system.isOptSet('async_gpu'):
            yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation", system.config["async_gpu"])
            yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation\\default", "false")
        else:
            yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation", "true")
            yuzuConfig.set("Renderer", "use_asynchronous_gpu_emulation\\default", "true")

        # NVDEC Emulation
        if system.isOptSet('nvdec_emu'):
            yuzuConfig.set("Renderer", "nvdec_emulation", system.config["nvdec_emu"])
            yuzuConfig.set("Renderer", "nvdec_emulation\\default", "false")
        else:
            yuzuConfig.set("Renderer", "nvdec_emulation", "2")
            yuzuConfig.set("Renderer", "nvdec_emulation\\default", "true")

        # Gpu Accuracy
        if system.isOptSet('gpuaccuracy'):
            yuzuConfig.set("Renderer", "gpu_accuracy", system.config["gpuaccuracy"])
        else:
            yuzuConfig.set("Renderer", "gpu_accuracy", "0")
        yuzuConfig.set("Renderer", "gpu_accuracy\\default", "false")

        # Vsync
        if system.isOptSet('vsync'):
            yuzuConfig.set("Renderer", "use_vsync", system.config["vsync"])
            yuzuConfig.set("Renderer", "use_vsync\\default", "false")
            if system.config["vsync"] == "2":
                yuzuConfig.set("Renderer", "use_vsync\\default", "true")
        else:
            yuzuConfig.set("Renderer", "use_vsync", "1")
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
            yuzuConfig.set("Renderer", "max_anisotropy\\default", "false")
        else:
            yuzuConfig.set("Renderer", "max_anisotropy", "0")
            yuzuConfig.set("Renderer", "max_anisotropy\\default", "true")

        # Resolution scaler
        if system.isOptSet('resolution_scale'):
            yuzuConfig.set("Renderer", "resolution_setup", system.config["resolution_scale"])
            yuzuConfig.set("Renderer", "resolution_setup\\default", "false")
        else:
            yuzuConfig.set("Renderer", "resolution_setup", "2")
            yuzuConfig.set("Renderer", "resolution_setup\\default", "true")

        # Scaling filter
        if system.isOptSet('scale_filter'):
            yuzuConfig.set("Renderer", "scaling_filter", system.config["scale_filter"])
            yuzuConfig.set("Renderer", "scaling_filter\\default", "false")
        else:
            yuzuConfig.set("Renderer", "scaling_filter", "1")
            yuzuConfig.set("Renderer", "scaling_filter\\default", "true")

        # Anti aliasing method
        if system.isOptSet('aliasing_method'):
            yuzuConfig.set("Renderer", "anti_aliasing", system.config["aliasing_method"])
            yuzuConfig.set("Renderer", "anti_aliasing\\default", "false")
        else:
            yuzuConfig.set("Renderer", "anti_aliasing", "0")
            yuzuConfig.set("Renderer", "anti_aliasing\\default", "true")

    # Cpu Section
        if not yuzuConfig.has_section("Cpu"):
            yuzuConfig.add_section("Cpu")

        # Cpu Accuracy
        if system.isOptSet('cpuaccuracy'):
            yuzuConfig.set("Cpu", "cpu_accuracy", system.config["cpuaccuracy"])
            yuzuConfig.set("Cpu", "cpu_accuracy\\default", "false")
        else:
            yuzuConfig.set("Cpu", "cpu_accuracy", "0")
            yuzuConfig.set("Cpu", "cpu_accuracy\\default", "true")

    # System section
        if not yuzuConfig.has_section("System"):
            yuzuConfig.add_section("System")

        # Language
        if system.isOptSet('language'):
            yuzuConfig.set("System", "language_index", system.config["language"])
            yuzuConfig.set("System", "language_index\\default", "false")
        else:
            yuzuConfig.set("System", "language_index", "1")
            yuzuConfig.set("System", "language_index\\default", "true")

        # Audio Mode
        if system.isOptSet('audio_mode'):
            yuzuConfig.set("System", "sound_index", system.config["audio_mode"])
            yuzuConfig.set("System", "sound_index\\default", "false")
        else:
            yuzuConfig.set("System", "sound_index", "1")
            yuzuConfig.set("System", "sound_index\\default", "true")

        # Region
        if system.isOptSet('region'):
            yuzuConfig.set("System", "region_index", system.config["region"])
            yuzuConfig.set("System", "region_index\\default", "false")
        else:
            yuzuConfig.set("System", "region_index", "1")
            yuzuConfig.set("System", "region_index\\default", "true")

    # controls section
        if not yuzuConfig.has_section("Controls"):
            yuzuConfig.add_section("Controls")

        # Dock Mode
        if system.isOptSet('dock_mode'):
            yuzuConfig.set("Controls", "use_docked_mode", system.config["dock_mode"])
            yuzuConfig.set("Controls", "use_docked_mode\\default", "false")
        else:
            yuzuConfig.set("Controls", "use_docked_mode", "true")
            yuzuConfig.set("Controls", "use_docked_mode\\default", "true")


        if ((system.isOptSet('yuzu_auto_controller_config') and not (system.config["yuzu_auto_controller_config"] == "0")) or not system.isOptSet('yuzu_auto_controller_config')):
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
            
            # Player 3 Pad Type
            if system.isOptSet('p3_pad'):
                yuzuConfig.set("Controls", "player_2_type", system.config["p3_pad"])
            else:
                yuzuConfig.set("Controls", "player_2_type", "0")

            # Player 4 Pad Type
            if system.isOptSet('p4_pad'):
                yuzuConfig.set("Controls", "player_3_type", system.config["p4_pad"])
            else:
                yuzuConfig.set("Controls", "player_3_type", "0")

            
            yuzuConfig.set("Controls", "player_1_type\default", "false")

            yuzuConfig.set("Controls", "vibration_enabled", "true")
            yuzuConfig.set("Controls", "vibration_enabled\\default", "true")

            guidstoreplace_ds4 = ["050000004c050000c405000000783f00","050000004c050000c4050000fffe3f00","050000004c050000c4050000ffff3f00","050000004c050000cc090000fffe3f00","050000004c050000cc090000ffff3f00","30303839663330346632363232623138","31326235383662333266633463653332","34613139376634626133336530386430","37626233336235343937333961353732","38393161636261653636653532386639","63313733393535663339656564343962","63393662363836383439353064663939","65366465656364636137653363376531","66613532303965383534396638613230","050000004c050000cc090000df070000","050000004c050000cc090000df870001","050000004c050000cc090000ff070000","030000004c050000a00b000011010000","030000004c050000a00b000011810000","030000004c050000c405000011010000","030000004c050000c405000011810000","030000004c050000cc09000000010000","030000004c050000cc09000011010000","030000004c050000cc09000011810000","03000000c01100000140000011010000","050000004c050000c405000000010000","050000004c050000c405000000810000","050000004c050000c405000001800000","050000004c050000cc09000000010000","050000004c050000cc09000000810000","050000004c050000cc09000001800000","030000004c050000a00b000000010000","030000004c050000c405000000000000","030000004c050000c405000000010000","03000000120c00000807000000000000","03000000120c0000111e000000000000","03000000120c0000121e000000000000","03000000120c0000130e000000000000","03000000120c0000150e000000000000","03000000120c0000180e000000000000","03000000120c0000181e000000000000","03000000120c0000191e000000000000","03000000120c00001e0e000000000000","03000000120c0000a957000000000000","03000000120c0000aa57000000000000","03000000120c0000f21c000000000000","03000000120c0000f31c000000000000","03000000120c0000f41c000000000000","03000000120c0000f51c000000000000","03000000120c0000f70e000000000000","03000000120e0000120c000000000000","03000000160e0000120c000000000000","030000001a1e0000120c000000000000","030000004c050000a00b000000000000","030000004c050000cc09000000000000","35643031303033326130316330353564","31373231336561636235613666323035","536f6e7920496e746572616374697665","576972656c65737320436f6e74726f6c","050000004c050000cc090000ff870001","050000004c050000cc090000ff876d01","31663838336334393132303338353963"]
            guidstoreplace_ds5_wireless = ["32633532643734376632656664383733","37363764353731323963323639666565","61303162353165316365336436343139","050000004c050000e60c0000df870000","050000004c050000e60c000000810000","030000004c050000e60c000000010000","050000004c050000e60c0000fffe3f00","030000004c050000e60c000000000000","050000004c050000e60c000000010000","030000004c050000e60c000011010000","32346465346533616263386539323932","050000004c050000e60c0000ff870000"]
            guidstoreplace_ds5_wired = ["030000004c050000e60c000011810000"]
            guidstoreplace_xbox = ["050000005e040000fd02000030110000"]
            guidstoreplace_steam = ["03000000de2800000512000010010000"]
            guidstoreplace_steam2 = ["03000000de2800000512000011010000"]
            guidstoreplace_switch = ["030000007e0500000920000011810000"]

            cguid = [0 for x in range(10)]
            lastplayer = 0
            for index in playersControllers :
                controller = playersControllers[index]
                portnumber = cguid.count(controller.guid)
                controllernumber = str(int(controller.player) - 1)
                cguid[int(controllernumber)] = controller.guid
                inputguid = controller.guid
                #DS4 GUIDs from https://github.com/gabomdq/SDL_GameControllerDB/blob/master/gamecontrollerdb.txt
                if controller.guid in guidstoreplace_ds4:
                    inputguid = "030000004c050000cc09000000006800"
                #DS5 GUIDs from https://github.com/gabomdq/SDL_GameControllerDB/blob/master/gamecontrollerdb.txt
                if controller.guid in guidstoreplace_ds5_wireless:
                    inputguid = "030000004c050000e60c000000006800"
                if controller.guid in guidstoreplace_ds5_wired:
                    inputguid = "030000004c050000e60c000000016800"
                if controller.guid in guidstoreplace_xbox:
                    inputguid = "050000005e040000fd02000030110000"
                if controller.guid in guidstoreplace_switch:
                    inputguid = "030000007e0500000920000000026803"
                #DS5 corrections
                if ((controller.guid in guidstoreplace_ds5_wireless) or (controller.guid in guidstoreplace_ds4) or (controller.guid in guidstoreplace_ds5_wired)) :
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
                elif ((controller.guid in guidstoreplace_switch)) :
                    #button_a="engine:sdl,port:0,guid:030000004c050000e60c000000006800,button:1"
                    for x in yuzuSwitchButtons:
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},button:{}"'.format(portnumber,inputguid,yuzuSwitchButtons[x]))
                    for x in yuzuSwitchAxis:
                        if(x == "button_zl" or x == "button_zr"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuSwitchAxis[x]))
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:+,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuDSAxis[x],yuzuDSAxis[x]+1))
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                elif (controller.guid in guidstoreplace_steam) :
                    #button_a="engine:sdl,port:0,guid:030000004c050000e60c000000006800,button:1"
                    for x in yuzuSCButtons:
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},button:{}"'.format(portnumber,inputguid,yuzuSCButtons[x]))
                    for x in yuzuSCAxis:
                        if(x == "button_zl" or x == "button_zr"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuSCAxis[x]))
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:+,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuSCAxis[x],yuzuSCAxis[x]+1))
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"[empty]"')
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"[empty]"')
                    #yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                    #yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                elif (controller.guid in guidstoreplace_steam2) :
                    #button_a="engine:sdl,port:0,guid:030000004c050000e60c000000006800,button:1"
                    for x in yuzuSCButtons2:
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},button:{}"'.format(portnumber,inputguid,yuzuSCButtons2[x]))
                    for x in yuzuSCAxis2:
                        if(x == "button_zl" or x == "button_zr"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuSCAxis2[x]))
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:+,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuSCAxis2[x],yuzuSCAxis2[x]+1))
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"[empty]"')
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"[empty]"')
                    #yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                    #yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                else:
                    for x in yuzuButtons:
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setButton(yuzuButtons[x], inputguid, controller.inputs,portnumber)))
                    for x in yuzuAxis:
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setAxis(yuzuAxis[x], inputguid, controller.inputs, portnumber)))
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '[empty]')
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '[empty]')

                
                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                if (controllernumber == "0"):
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\default", "true")
                else:
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\default", "false")                    
                yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "0")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")
                lastplayer = int(controllernumber)
            lastplayer = lastplayer + 1
            eslog.debug("Last Player {}".format(lastplayer))
            for y in range(lastplayer, 9):
                controllernumber = str(y)
                eslog.debug("Setting Controller: {}".format(controllernumber))
                for x in yuzuButtons:
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '""')
                for x in yuzuDSAxis:
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '""')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_a", '"toggle:0,code:67,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_a\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_b", '"toggle:0,code:88,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_b\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_ddown", '"toggle:0,code:16777237,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_ddown\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_dleft", '"toggle:0,code:16777234,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_dleft\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_dright", '"toggle:0,code:16777236,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_dright\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_dup", '"toggle:0,code:16777235,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_dup\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_home", '"toggle:0,code:0,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_home\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_l", '"toggle:0,code:81,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_l\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_lstick", '"toggle:0,code:70,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_lstick\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_minus", '"toggle:0,code:78,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_minus\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_plus", '"toggle:0,code:77,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_plus\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_r", '"toggle:0,code:69,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_r\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_rstick", '"toggle:0,code:71,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_rstick\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_screenshot", '"toggle:0,code:0,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_screenshot\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sl", '"toggle:0,code:81,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sl\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sr", '"toggle:0,code:69,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sr\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_x", '"toggle:0,code:86,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_x\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_y", '"toggle:0,code:90,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_y\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_zl", '"toggle:0,code:82,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_zl\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_zr", '"toggle:0,code:84,engine:keyboard"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_button_zr\\default", "true")

                yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick", '"modifier_scale:0.500000,modifier:toggle$00$1code$016777248$1engine$0keyboard,right:toggle$00$1code$068$1engine$0keyboard,left:toggle$00$1code$065$1engine$0keyboard,down:toggle$00$1code$083$1engine$0keyboard,up:toggle$00$1code$087$1engine$0keyboard,engine:analog_from_button"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick\\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick", '"modifier_scale:0.500000,modifier:toggle$00$1code$00$1engine$0keyboard,right:toggle$00$1code$076$1engine$0keyboard,left:toggle$00$1code$074$1engine$0keyboard,down:toggle$00$1code$075$1engine$0keyboard,up:toggle$00$1code$073$1engine$0keyboard,engine:analog_from_button"')
                yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick\\default", "true")


                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "false")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\default", "true")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "0")
                yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "true")
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

        with open(beforeyuzuConfigFile, 'w') as configfile:
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
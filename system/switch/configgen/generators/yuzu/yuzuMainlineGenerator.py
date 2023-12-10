#!/usr/bin/env python

import generators
from configgen.generators.Generator import Generator
import Command as Command
import os
import shutil
import stat
import batoceraFiles as batoceraFiles
import controllersConfig as controllersConfig
import configparser
from shutil import copyfile
from utils.logger import get_logger
import subprocess

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
        
        os.environ["PYSDL2_DLL_PATH"] = "/userdata/system/switch/extra/sdl/"
        
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

        yuzuConfig.set("UI", "Shortcuts\Main%20Window\Exit%20yuzu\Controller_KeySeq", "Home+Plus")
        yuzuConfig.set("UI", "Shortcuts\Main%20Window\Exit%20yuzu\Controller_KeySeq\\default", "false")

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

        #ASTC Decoding Method
        if system.isOptSet('accelerate_astc'):
            yuzuConfig.set("Renderer", "accelerate_astc", system.config["accelerate_astc"])
            yuzuConfig.set("Renderer", "accelerate_astc\\default", "false")
        else:
            yuzuConfig.set("Renderer", "accelerate_astc", "1")
            yuzuConfig.set("Renderer", "accelerate_astc\\default", "true")            

        # ASTC Texture Recompression
        if system.isOptSet('astc_recompression'):


            yuzuConfig.set("Renderer", "astc_recompression", system.config["astc_recompression"])
            yuzuConfig.set("Renderer", "astc_recompression\\default", "false")
            if system.config["astc_recompression"] == "0":
                yuzuConfig.set("Renderer", "use_vsync\\default", "true")
            yuzuConfig.set("Renderer", "async_astc", "false")
            yuzuConfig.set("Renderer", "async_astc\\default", "true")
        else:
            yuzuConfig.set("Renderer", "astc_recompression", "0")
            yuzuConfig.set("Renderer", "astc_recompression\\default", "true")
            yuzuConfig.set("Renderer", "async_astc", "false")
            yuzuConfig.set("Renderer", "async_astc\\default", "true")

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
            
        # Dock Mode
        if system.isOptSet('dock_mode'):
            if system.config["dock_mode"] == "1":
                yuzuConfig.set("System", "use_docked_mode", "1")
                yuzuConfig.set("System", "use_docked_mode\\default", "true")
            elif system.config["dock_mode"] == "0":
                yuzuConfig.set("System", "use_docked_mode", "0")
                yuzuConfig.set("System", "use_docked_mode\\default", "false")
        else:
            yuzuConfig.set("System", "use_docked_mode", "1")
            yuzuConfig.set("System", "use_docked_mode\\default", "true")

    # controls section
        if not yuzuConfig.has_section("Controls"):
            yuzuConfig.add_section("Controls")
            
        if ((system.isOptSet('yuzu_auto_controller_config') and not (system.config["yuzu_auto_controller_config"] == "0")) or not system.isOptSet('yuzu_auto_controller_config')):

            known_reversed_guids = ["03000000c82d00000631000014010000"]
            #These are controllers that use Batocera mappings for some reason
            use_batocera_guids = ["050000005e0400008e02000030110000","030000005e0400008e02000014010000","0000000053696e64656e206c69676800"]
            filename = "/userdata/system/switch/configgen/debugcontrollers.txt"
            if os.path.exists(filename):
                file = open(filename, 'r')
                debugcontrollers = bool(file.readline())
                file.close()
            else:
                debugcontrollers = False
            
            if debugcontrollers:
                eslog.debug("=====================================================Start Bato Controller Debug Info=========================================================")
                for index in playersControllers :
                    controller = playersControllers[index]
                    eslog.debug("Controller configName: {}".format(controller.configName))
                    eslog.debug("Controller index: {}".format(controller.index))
                    eslog.debug("Controller realName: {}".format(controller.realName))                
                    eslog.debug("Controller dev: {}".format(controller.dev))
                    eslog.debug("Controller player: {}".format(controller.player))
                    eslog.debug("Controller GUID: {}".format(controller.guid))
                    eslog.debug("")
                eslog.debug("=====================================================End Bato Controller Debug Info===========================================================")
                eslog.debug("")

            import sdl2
            from sdl2 import (
                SDL_TRUE
            )
            from sdl2 import joystick
            from ctypes import create_string_buffer
            sdl2.SDL_ClearError()
            sdl2.SDL_SetHint(b"SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", b"1")
            ret = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_GAMECONTROLLER)
            assert ret == 0, _check_error_msg()

            sdl_devices = []
            count = joystick.SDL_NumJoysticks()

            if debugcontrollers:
                eslog.debug("=====================================================Start SDL Controller Debug Info==========================================================")
                for i in range(count):
                    if sdl2.SDL_IsGameController(i) == SDL_TRUE:
                        pad = sdl2.SDL_JoystickOpen(i)
                        cont = sdl2.SDL_GameControllerOpen(i)
                        joy_guid = joystick.SDL_JoystickGetDeviceGUID(i)
                        buff = create_string_buffer(33)
                        joystick.SDL_JoystickGetGUIDString(joy_guid,buff,33)
                        buff[2] = b'0'
                        buff[3] = b'0'
                        buff[4] = b'0'
                        buff[5] = b'0'
                        buff[6] = b'0'
                        buff[7] = b'0'
                        guidstring = ((bytes(buff)).decode()).split('\x00',1)[0]
                        eslog.debug("Joystick GUID: {}".format(guidstring))                 
                        joy_path = joystick.SDL_JoystickPathForIndex(i)
                        eslog.debug("Joystick Path: {}".format(joy_path.decode()))
                        eslog.debug("Joystick Type: {}".format(sdl2.SDL_JoystickGetDeviceType(i))) 
                        pad_type = sdl2.SDL_GameControllerTypeForIndex(i)
                        eslog.debug("Joystick Pad Type: {}".format(pad_type))                    
                        controllername = (sdl2.SDL_GameControllerNameForIndex(i)).decode()
                        eslog.debug("Joystick Name: {}".format(controllername))     

                        eslog.debug("Joystick Vendor: {}".format(joystick.SDL_JoystickGetDeviceVendor(i)))
                        eslog.debug("Joystick Product: {}".format(joystick.SDL_JoystickGetDeviceProduct(i)))
                        eslog.debug("Joystick Product Version: {}".format(joystick.SDL_JoystickGetDeviceProductVersion(i)))

                        sdl2.SDL_GameControllerClose(cont)
                        sdl2.SDL_JoystickClose(pad)
                        eslog.debug("")
                eslog.debug("=====================================================End SDL Controller Debug Info============================================================")
                eslog.debug("")

            for i in range(count):
                    if sdl2.SDL_IsGameController(i) == SDL_TRUE:
                        pad = sdl2.SDL_JoystickOpen(i)
                        cont = sdl2.SDL_GameControllerOpen(i)
                        #iid = sdl2.SDL_JoystickInstanceID(pad)
                        #gc = sdl2.SDL_GameControllerMappingForDeviceIndex(i)

                        gc_a = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_A)
                        if(gc_a.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_b = "hat:" + str(gc_a.value.hat.hat)
                        else:
                            button_b = gc_a.value.button

                        gc_b = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_B)
                        if(gc_b.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_a = "hat:" + str(gc_b.value.hat.hat)
                        else:
                            button_a = gc_b.value.button

                        gc_x = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_X)
                        if(gc_x.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_y = "hat:" + str(gc_x.value.hat.hat)
                        else:
                            button_y = gc_x.value.button

                        gc_y = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_Y)
                        if(gc_y.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_x = "hat:" + str(gc_y.value.hat.hat)
                        else:
                            button_x = gc_y.value.button

                        gc_dup = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP)
                        if(gc_dup.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_dup = "hat:" + str(gc_dup.value.hat.hat)
                        else:
                            button_dup = gc_dup.value.button

                        gc_ddown = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN)
                        if(gc_ddown.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_ddown = "hat:" + str(gc_ddown.value.hat.hat)
                        else:
                            button_ddown = gc_ddown.value.button    

                        gc_dleft = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT)
                        if(gc_dleft.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_dleft = "hat:" + str(gc_ddown.value.hat.hat)
                        else:
                            button_dleft = gc_dleft.value.button                     

                        gc_dright = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT)
                        if(gc_dright.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_dright = "hat:" + str(gc_ddown.value.hat.hat)
                        else:
                            button_dright = gc_dright.value.button 

                        gc_l = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER)
                        if(gc_l.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_l = "hat:" + str(gc_l.value.hat.hat)
                        else:
                            button_l = gc_l.value.button

                        gc_r = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER)
                        if(gc_r.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_HAT):
                            button_r = "hat:" + str(gc_r.value.hat.hat)
                        else:
                            button_r = gc_r.value.button

                        gc_lstick = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_LEFTSTICK)
                        button_lstick = gc_lstick.value.button

                        gc_rstick = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_RIGHTSTICK)
                        button_rstick = gc_rstick.value.button

                        gc_home = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_GUIDE)
                        button_home = gc_home.value.button

                        gc_minus = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_BACK)
                        button_minus = gc_minus.value.button

                        gc_plus = sdl2.SDL_GameControllerGetBindForButton(cont,sdl2.SDL_CONTROLLER_BUTTON_START)
                        button_plus = gc_plus.value.button

                        gc_zl = sdl2.SDL_GameControllerGetBindForAxis(cont,sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT)
                        if(gc_zl.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_AXIS):
                            button_zl = "axis"
                            axis_button_zl = gc_zl.value.axis
                        else:
                            button_zl = gc_zl.value.button
                            axis_button_zl = "noaxis"
                        
                        gc_zr = sdl2.SDL_GameControllerGetBindForAxis(cont,sdl2.SDL_CONTROLLER_AXIS_TRIGGERRIGHT)
                        if(gc_zr.bindType == sdl2.SDL_CONTROLLER_BINDTYPE_AXIS):
                            button_zr = "axis"
                            axis_button_zr = gc_zr.value.axis
                        else:
                            button_zr = gc_zr.value.button
                            axis_button_zr = "noaxis"

                        gc_axis_lstick_x = sdl2.SDL_GameControllerGetBindForAxis(cont,sdl2.SDL_CONTROLLER_AXIS_LEFTX)
                        axis_lstick_x = gc_axis_lstick_x.value.axis

                        gc_axis_rstick_x = sdl2.SDL_GameControllerGetBindForAxis(cont,sdl2.SDL_CONTROLLER_AXIS_RIGHTX)
                        axis_rstick_x = gc_axis_rstick_x.value.axis

                        joy_guid = joystick.SDL_JoystickGetDeviceGUID(i)
                        buff = create_string_buffer(33)
                        joystick.SDL_JoystickGetGUIDString(joy_guid,buff,33)                    
                        joy_path = joystick.SDL_JoystickPathForIndex(i)
                        buff[2] = b'0'
                        buff[3] = b'0'
                        buff[4] = b'0'
                        buff[5] = b'0'
                        buff[6] = b'0'
                        buff[7] = b'0'
                        guidstring = ((bytes(buff)).decode()).split('\x00',1)[0]
                        if(joy_path.decode() == 'nintendo_joycons_combined' ):
                            outputpath = 'nintendo_joycons_combined'
                        else:    
                            command = "udevadm info --query=path --name=" + joy_path.decode()
                            outputpath = (((subprocess.check_output(command, shell=True)).decode()).partition('/input/')[0]).partition('/hidraw')[0]
                        pad_type = sdl2.SDL_GameControllerTypeForIndex(i)
                        controllername = (sdl2.SDL_GameControllerNameForIndex(i)).decode()

                        if( "Steam" in controllername):
                            pad_type = 1
                        if("Xin-Mo Xin-Mo Dual Arcade" in controllername):
                            pad_type = 1
                        #Fix for Steam controller assignment
                        controller_value = {
                            "index" : i , 
                            'path' : outputpath, 
                            "guid" : guidstring, 
                            #"instance" : iid,  
                            "type" : pad_type, 
                            "button_a" : button_a, 
                            "button_b" : button_b, 
                            "button_x" : button_x, 
                            "button_y" : button_y,                                             
                            "button_dup" : button_dup, 
                            "button_ddown" : button_ddown,
                            "button_dleft" : button_dleft,
                            "button_dright" : button_dright,    
                            "button_l" : button_l,
                            "button_r" : button_r,
                            "button_sl" : button_l,
                            "button_sr" : button_r,
                            "button_lstick" : button_lstick,
                            "button_rstick" : button_rstick,
                            "button_minus" : button_minus,
                            "button_plus" : button_plus,
                            "button_home" : button_home,
                            "button_zl" : button_zl,
                            "button_zr" : button_zr,
                            "axis_button_zl" : axis_button_zl,
                            "axis_button_zr" : axis_button_zr,
                            "axis_lstick_x" : axis_lstick_x,
                            "axis_rstick_x" : axis_rstick_x                                                      
                            }
                        sdl_devices.append(controller_value)
                        sdl2.SDL_GameControllerClose(cont)
                        sdl2.SDL_JoystickClose(pad)
            sdl2.SDL_Quit()

            eslog.debug("Joysticks: {}".format(sdl_devices))


            if system.isOptSet("yuzu_enable_rumble"):
                yuzuConfig.set("Controls", "vibration_enabled", system.config["yuzu_enable_rumble"])
                yuzuConfig.set("Controls", "vibration_enabled\\default", system.config["yuzu_enable_rumble"])
            else:
                yuzuConfig.set("Controls", "vibration_enabled", "true")
                yuzuConfig.set("Controls", "vibration_enabled\\default", "true")


            cguid = [0 for x in range(10)]
            lastplayer = 0
            for index in playersControllers :
                controller = playersControllers[index]


                if(controller.guid != "050000007e0500000620000001800000" and controller.guid != "050000007e0500000720000001800000"):
                    #don't run the code for Joy-Con (L) or Joy-Con (R) - Batocera adds these and only works with a pair
                    which_pad = "p" + str(lastplayer+1) + "_pad"

                    if debugcontrollers:
                        eslog.debug("Controller configName: {}".format(controller.configName))
                        eslog.debug("Controller index: {}".format(controller.index))
                        eslog.debug("Controller realName: {}".format(controller.realName))                
                        eslog.debug("Controller dev: {}".format(controller.dev))
                        eslog.debug("Controller player: {}".format(controller.player))
                        eslog.debug("Controller GUID: {}".format(controller.guid))
                        eslog.debug("Which Pad: {}".format(which_pad))


                    if(playersControllers[index].realName == 'Nintendo Switch Combined Joy-Cons'):  #works in Batocera v37
                        outputpath = "nintendo_joycons_combined"
                        sdl_mapping = next((item for item in sdl_devices if (item["path"] == outputpath or item["path"] == '/devices/virtual')),None)
                    else:
                        command = "udevadm info --query=path --name=" + playersControllers[index].dev
                        outputpath = ((subprocess.check_output(command, shell=True)).decode()).partition('/input/')[0]
                        sdl_mapping = next((item for item in sdl_devices if item["path"] == outputpath),None)

                    if(controller.guid in known_reversed_guids):
                        eslog.debug("Swapping type for GUID")
                        if(sdl_mapping['type'] == 0):
                            sdl_mapping['type'] = 1
                        else:
                            sdl_mapping['type'] = 0          
                    
                    eslog.debug("Mapping: {}".format(sdl_mapping))

                    if(controller.guid in use_batocera_guids):
                        inputguid = controller.guid
                        sdl_mapping = None
                        #Force the non-SDL controller branch
                    else:
                        inputguid = sdl_mapping['guid']

                    controllernumber = str(lastplayer)
                    portnumber = cguid.count(inputguid)
                    cguid[int(controllernumber)] = inputguid

                    if debugcontrollers:
                        eslog.debug("Controller number: {}".format(controllernumber))
                        eslog.debug("Controller port: {}".format(portnumber))
                        eslog.debug("Controller cguid: {}".format(cguid[int(controllernumber)]))                


                    if(sdl_mapping == None):
                        eslog.debug("Batocera controller Branch")
                        if (system.isOptSet(which_pad) and (system.config[which_pad] == "2")):
                            eslog.debug("Controller Type: Left Joycon")
                            #2 = Left Joycon
                            #Switch and generic controllers aren't swapping ABXY
                            yuzuButtons = {
                                "button_a":      "a", #notused on left joycon
                                "button_b":      "b", #notused on left joycon
                                "button_x":      "x", #notused on left joycon
                                "button_y":      "y", #notused on left joycon
                                "button_dup":     "y",
                                "button_ddown":   "a",
                                "button_dleft":   "b",
                                "button_dright":  "x",
                                "button_l":      "pageup",
                                "button_r":      "pagedown", #notused on left joycon
                                "button_plus":  "start", #notused on left joycon
                                "button_minus": "select",
                                "button_sl":     "pageup",
                                "button_sr":     "pagedown",
                                "button_lstick":     "l3",
                                "button_rstick":     "r3", #notused on left joycon
                                "button_home":   "hotkey", #notused on left joycon
								"button_screenshot": "hotkey", #Added to left joycon to act as "home"
								"button_zl": "l2",
                                "button_zr": "r2" #notused on left joycon
                            }

                            yuzuAxis = {
                                "lstick":    "joystick1",
                                "rstick":    "joystick1"
                            }

                            #Configure buttons and triggers
                            for x in yuzuButtons:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setButton(yuzuButtons[x], inputguid, controller.inputs,portnumber)))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                            for x in yuzuAxis:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setAxis(yuzuAxis[x], inputguid, controller.inputs, portnumber, 1)))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")


                        elif (system.isOptSet(which_pad) and (system.config[which_pad] == "3")):
                            eslog.debug("Controller Type: Right Joycon")
                            #3 = Right Joycon
                            #Switch and generic controllers aren't swapping ABXY
                            yuzuButtons = {
                                "button_a":      "b", 
                                "button_b":      "y", 
                                "button_x":      "a", 
                                "button_y":      "x", 
                                "button_dup":     "y", #notused on right joycon
                                "button_ddown":   "a", #notused on right joycon
                                "button_dleft":   "b", #notused on right joycon
                                "button_dright":  "x", #notused on right joycon
                                "button_l":      "pageup", #notused on right joycon
                                "button_r":      "pagedown",
                                "button_plus":  "start", #notused on left joycon
                                "button_minus": "select",
                                "button_sl":     "pageup",
                                "button_sr":     "pagedown",
                                "button_lstick":     "l3", #notused on right joycon
                                "button_rstick":     "r3", 
                                "button_home":   "hotkey", 
								"button_screenshot": "hotkey", #Added to left joycon to act as "home"
								"button_zl": "l2",
                                "button_zr": "r2"
                            }

                            yuzuAxis = {
                                "lstick":    "joystick1",
                                "rstick":    "joystick1"
                            }

                            #Configure buttons and triggers
                            for x in yuzuButtons:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setButton(yuzuButtons[x], inputguid, controller.inputs,portnumber)))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                            for x in yuzuAxis:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setAxis(yuzuAxis[x], inputguid, controller.inputs, portnumber,2)))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                        else:
                            eslog.debug("Controller Type: Non-Joycon")
                            #0 = Pro Controller, 1 = Dual Joycons, 4 = Handheld Mode,  (and other cases not yet defined)
                            #Switch and generic controllers aren't swapping ABXY
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
                                "button_lstick":     "l3",
                                "button_rstick":     "r3",
                                "button_home":   "hotkey",
                                "button_zl": "l2",
                                "button_zr": "r2"
                            }

                            yuzuAxis = {
                                "lstick":    "joystick1",
                                "rstick":    "joystick2"
                            }

                            #Configure buttons and triggers
                            for x in yuzuButtons:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setButton(yuzuButtons[x], inputguid, controller.inputs,portnumber)))
                        
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")                           

                            for x in yuzuAxis:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{}"'.format(YuzuMainlineGenerator.setAxis(yuzuAxis[x], inputguid, controller.inputs, portnumber,0)))     
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                        #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))

                        yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                        if (controllernumber == "0"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                        if system.isOptSet(which_pad):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", system.config["p1_pad"])
                            #yuzuConfig.set("Controls", "player_0_type", system.config["p1_pad"])
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "0")

                        yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "true")

                        if system.isOptSet("yuzu_enable_rumble"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")

                        lastplayer = int(controllernumber) + 1

                    elif (sdl_mapping['type'] == 13):
                        #we have real joycons
                        eslog.debug("Joycon Branch")
                        yuzuPad1Buttons = {
                                "button_l":      64, 
                                "button_minus":  65536,
                                "button_lstick": 524288,
                                "button_screenshot": 2097152,
                                "button_dup":    2, 
                                "button_ddown":  1,
                                "button_dleft":  8,
                                "button_dright": 4,
                                "button_zl": 128
                            }
                        
                        yuzuPad2Buttons = {
                                "button_a":      2048, #notused on left joycon
                                "button_b":      1024, #notused on left joycon
                                "button_x":      512, #notused on left joycon
                                "button_y":      256, #notused on left joycon
                                "button_r":      16384, #notused on left joycon
                                "button_plus":   131072, #notused on left joycon
                                "button_rstick": 262144, #notused on left joycon
                                "button_home":   1048576,  #notused on left joycon
                                "button_zr": 32768 #notused on left joycon
                            }

                        if (system.isOptSet(which_pad) and (system.config[which_pad] == "2")):
                            eslog.debug("Controller Type: Left Joycon")
                            pad1 = 1
                            pad2 = 1
                            lastplayer = int(controllernumber)+1
                            
                            #Configure buttons and triggers
                            for x in yuzuPad1Buttons:
                                eslog.debug("Left Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,yuzuPad1Buttons[x],portnumber,pad1))
                            for x in yuzuPad2Buttons:
                                eslog.debug("Left Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,yuzuPad2Buttons[x],portnumber,pad2))

                            #sl and sr of left pad
                            eslog.debug("Left Joycon SL")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sl", '"pad:{},button:32,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sr", '"pad:{},button:16,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))

                            #set joysticks
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick", '"axis_y:1,axis_x:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick", '"axis_y:3,axis_x:2,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            
                            #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"motion:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"motion:1,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                            
                            if (controllernumber == "0"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                            #Forcing to left joycon
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "2")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "false")
                            if system.isOptSet("yuzu_enable_rumble"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")

                            eslog.debug("Controller Type: Right Joycon after Left")
                            pad1 = 2
                            pad2 = 2
                            controllernumber = str(lastplayer)
                            lastplayer = int(controllernumber)+1

                            #Configure buttons and triggers
                            for x in yuzuPad1Buttons:
                                eslog.debug("Right Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,yuzuPad1Buttons[x],portnumber,pad1))
                            for x in yuzuPad2Buttons:
                                eslog.debug("Right Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,yuzuPad2Buttons[x],portnumber,pad2))

                            #sl and sr of right pad
                            eslog.debug("Right Joycon SL")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sl", '"pad:{},button:8192,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sr", '"pad:{},button:4096,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))

                            #set joysticks
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick", '"axis_y:1,axis_x:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick", '"axis_y:3,axis_x:2,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            
                            #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"motion:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"motion:1,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))



                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                            if (controllernumber == "0"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                            #Forcing to right joycons
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "3")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "false")
                            if system.isOptSet("yuzu_enable_rumble"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")



                        
                        elif (system.isOptSet(which_pad) and (system.config[which_pad] == "3")):
                            eslog.debug("Controller Type: Right Joycon")
                            pad1 = 2
                            pad2 = 2

                            lastplayer = int(controllernumber)+1

                            #Configure buttons and triggers
                            for x in yuzuPad1Buttons:
                                eslog.debug("Right Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,yuzuPad1Buttons[x],portnumber,pad1))
                            for x in yuzuPad2Buttons:
                                eslog.debug("Right Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,yuzuPad2Buttons[x],portnumber,pad2))

                            #sl and sr of right pad
                            eslog.debug("Right Joycon SL")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sl", '"pad:{},button:8192,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sr", '"pad:{},button:4096,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))

                            #set joysticks
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick", '"axis_y:1,axis_x:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick", '"axis_y:3,axis_x:2,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            
                            #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"motion:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"motion:1,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))



                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                            if (controllernumber == "0"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                            #Forcing to right joycons
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "3")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "false")
                            if system.isOptSet("yuzu_enable_rumble"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")


                            eslog.debug("Controller Type: Left Joycon After Right")
                            pad1 = 1
                            pad2 = 1
                            controllernumber = str(lastplayer)
                            lastplayer = int(controllernumber)+1
                            
                            #Configure buttons and triggers
                            for x in yuzuPad1Buttons:
                                eslog.debug("Left Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,yuzuPad1Buttons[x],portnumber,pad1))
                            for x in yuzuPad2Buttons:
                                eslog.debug("Left Joycon {}".format(x))
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,yuzuPad2Buttons[x],portnumber,pad2))

                            #sl and sr of left pad
                            eslog.debug("Left Joycon SL")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sl", '"pad:{},button:32,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_button_sr", '"pad:{},button:16,port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))

                            #set joysticks
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick", '"axis_y:1,axis_x:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick", '"axis_y:3,axis_x:2,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            
                            #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"motion:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"motion:1,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                            
                            if (controllernumber == "0"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                            #Forcing to left joycon
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "2")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "false")
                            if system.isOptSet("yuzu_enable_rumble"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")

                        else:
                            eslog.debug("Controller Type: Dual Joycons")
                            pad1 = 1
                            pad2 = 2
                            lastplayer = int(controllernumber)+1

                            #Configure buttons and triggers
                            for x in yuzuPad1Buttons:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,yuzuPad1Buttons[x],portnumber,pad1))
                            for x in yuzuPad2Buttons:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"pad:{},button:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,yuzuPad2Buttons[x],portnumber,pad2))

                            #sl and sr not connected for dual joycon mode
                            yuzuConfig.set("Controls", "player_" + controllernumber + "button_sl", '[empty]')
                            yuzuConfig.set("Controls", "player_" + controllernumber + "button_sr", '[empty]')

                            #set joysticks
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_lstick", '"axis_y:1,axis_x:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_rstick", '"axis_y:3,axis_x:2,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))
                            
                            #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"motion:0,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad1,portnumber,pad1))
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"motion:1,pad:{},port:{},guid:0000000000000000000000000000000{},engine:joycon"'.format(pad2,portnumber,pad2))

                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                            if (controllernumber == "0"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                            #Forcing to dual joycons
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "1")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "false")
                            if system.isOptSet("yuzu_enable_rumble"):
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                            else:
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                                yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")
                            
                    else:
                        eslog.debug("SDL controller Branch")
                        if (system.isOptSet(which_pad) and (system.config[which_pad] == "2")):
                            eslog.debug("Controller Type: Left Joycon")
                            #2 = Left Joycon
                            #Switch and generic controllers aren't swapping ABXY
                            if (sdl_mapping['type'] == 0):
                                yuzuButtons = {
                                    "button_a":      sdl_mapping['button_b'], #notused on left joycon
                                    "button_b":      sdl_mapping['button_a'], #notused on left joycon
                                    "button_x":      sdl_mapping['button_y'], #notused on left joycon
                                    "button_y":      sdl_mapping['button_x'], #notused on left joycon
                                    "button_l":      sdl_mapping['button_l'], 
                                    "button_r":      sdl_mapping['button_r'], #notused on left joycon
                                    "button_plus":   sdl_mapping['button_plus'], #notused on left joycon
                                    "button_minus":  sdl_mapping['button_minus'],
                                    "button_sl":     sdl_mapping['button_sl'], 
                                    "button_sr":     sdl_mapping['button_sr'],
                                    "button_lstick": sdl_mapping['button_lstick'],
                                    "button_rstick": sdl_mapping['button_rstick'], #notused on left joycon
                                    "button_home":   sdl_mapping['button_home'],  #notused on left joycon
                                    "button_screenshot": sdl_mapping['button_home'], #Added to left joycon to act as "home"
                                    "button_dup":    sdl_mapping['button_x'], 
                                    "button_ddown":  sdl_mapping['button_b'],
                                    "button_dleft":  sdl_mapping['button_a'],
                                    "button_dright": sdl_mapping['button_y'],
                                    "button_zl": sdl_mapping['button_zl'],
                                    "button_zr": sdl_mapping['button_zr'] #notused on left joycon
                                }
                            else:
                                yuzuButtons = {
                                    "button_a":      sdl_mapping['button_a'], #notused on left joycon
                                    "button_b":      sdl_mapping['button_b'], #notused on left joycon
                                    "button_x":      sdl_mapping['button_x'], #notused on left joycon
                                    "button_y":      sdl_mapping['button_y'], #notused on left joycon
                                    "button_l":      sdl_mapping['button_l'], 
                                    "button_r":      sdl_mapping['button_r'], #notused on left joycon
                                    "button_plus":   sdl_mapping['button_plus'], #notused on left joycon
                                    "button_minus":  sdl_mapping['button_minus'],
                                    "button_sl":     sdl_mapping['button_sl'], 
                                    "button_sr":     sdl_mapping['button_sr'],
                                    "button_lstick": sdl_mapping['button_lstick'],
                                    "button_rstick": sdl_mapping['button_rstick'], #notused on left joycon
                                    "button_home":   sdl_mapping['button_home'],  #notused on left joycon
                                    "button_screenshot": sdl_mapping['button_home'], #Added to left joycon to act as "home"
                                    "button_dup":    sdl_mapping['button_y'], 
                                    "button_ddown":  sdl_mapping['button_a'],
                                    "button_dleft":  sdl_mapping['button_b'],
                                    "button_dright": sdl_mapping['button_x'],
                                    "button_zl": sdl_mapping['button_zl'],
                                    "button_zr": sdl_mapping['button_zr'] #notused on left joycon
                                }

                            yuzuAxis = {
                                "lstick":    int(sdl_mapping['axis_lstick_x']),
                                "rstick":    int(sdl_mapping['axis_rstick_x'])
                            }

                            yuzuAxisButtons = {
                                "button_zl": sdl_mapping['axis_button_zl'],
                                "button_zr": sdl_mapping['axis_button_zr']
                            }

                            yuzuHat = {
                                "button_dup":     'up',
                                "button_ddown":   'down',
                                "button_dleft":   'left',
                                "button_dright":  'right'
                            }

                            #Configure buttons and triggers
                            for x in yuzuButtons:
                                if("hat" in str(yuzuButtons[x])):
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{},direction:{},guid:{},port:{},engine:sdl"'.format(yuzuButtons[x],yuzuHat[x],inputguid,portnumber))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                                elif("axis" in str(yuzuButtons[x])):
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuAxisButtons[x]))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                                else:
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"button:{},guid:{},port:{},engine:sdl"'.format(yuzuButtons[x],inputguid,portnumber))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                            #set joysticks
                            for x in yuzuAxis:
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:-,invert_y:+,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuAxis[x]+1,yuzuAxis[x]))
                        elif (system.isOptSet(which_pad) and (system.config[which_pad] == "3")):
                            eslog.debug("Controller Type: Right Joycon")
                            #2 = Left Joycon
                            #Switch and generic controllers aren't swapping ABXY
                            if (sdl_mapping['type'] == 0):
                                yuzuButtons = {
                                    "button_a":      sdl_mapping['button_a'], #was b
                                    "button_b":      sdl_mapping['button_x'], #was a
                                    "button_x":      sdl_mapping['button_b'], #was y
                                    "button_y":      sdl_mapping['button_y'], #was x
                                    "button_l":      sdl_mapping['button_l'], #notused on right joycon
                                    "button_r":      sdl_mapping['button_r'],
                                    "button_plus":   sdl_mapping['button_plus'],
                                    "button_minus":  sdl_mapping['button_minus'], #notused on right joycon
                                    "button_sl":     sdl_mapping['button_sl'], 
                                    "button_sr":     sdl_mapping['button_sr'],
                                    "button_lstick": sdl_mapping['button_lstick'], #notused on right joycon
                                    "button_rstick": sdl_mapping['button_lstick'], #mapping to left stick
                                    "button_home":   sdl_mapping['button_home'], 
                                    #"button_screenshot": sdl_mapping['button_home'],
                                    "button_dup":    sdl_mapping['button_x'],  #notused on right joycon
                                    "button_ddown":  sdl_mapping['button_b'], #notused on right joycon
                                    "button_dleft":  sdl_mapping['button_a'], #notused on right joycon
                                    "button_dright": sdl_mapping['button_y'], #notused on right joycon
                                    "button_zl": sdl_mapping['button_zl'], #notused on right joycon
                                    "button_zr": sdl_mapping['button_zr'] 
                                }
                            else:
                                yuzuButtons = {
                                    "button_a":      sdl_mapping['button_b'], 
                                    "button_b":      sdl_mapping['button_y'],
                                    "button_x":      sdl_mapping['button_a'],
                                    "button_y":      sdl_mapping['button_x'],
                                    "button_l":      sdl_mapping['button_l'], #notused on right joycon
                                    "button_r":      sdl_mapping['button_r'],
                                    "button_plus":   sdl_mapping['button_plus'],
                                    "button_minus":  sdl_mapping['button_minus'], #notused on right joycon
                                    "button_sl":     sdl_mapping['button_sl'], 
                                    "button_sr":     sdl_mapping['button_sr'],
                                    "button_lstick": sdl_mapping['button_lstick'], #notused on right joycon
                                    "button_rstick": sdl_mapping['button_lstick'], #mapping to left stick
                                    "button_home":   sdl_mapping['button_home'], 
                                    #"button_screenshot": sdl_mapping['button_home'],
                                    "button_dup":    sdl_mapping['button_x'],  #notused on right joycon
                                    "button_ddown":  sdl_mapping['button_b'], #notused on right joycon
                                    "button_dleft":  sdl_mapping['button_a'], #notused on right joycon
                                    "button_dright": sdl_mapping['button_y'], #notused on right joycon
                                    "button_zl": sdl_mapping['button_zl'], #notused on right joycon
                                    "button_zr": sdl_mapping['button_zr'] 
                                }

                            yuzuAxis = {
                                "lstick":    int(sdl_mapping['axis_lstick_x']), #notused on right joycon
                                "rstick":    int(sdl_mapping['axis_lstick_x']) #mapping to left stick
                            }

                            yuzuAxisButtons = {
                                "button_zl": sdl_mapping['axis_button_zl'],
                                "button_zr": sdl_mapping['axis_button_zr']
                            }

                            yuzuHat = {
                                "button_dup":     'up',
                                "button_ddown":   'down',
                                "button_dleft":   'left',
                                "button_dright":  'right'
                            }

                            #Configure buttons and triggers
                            for x in yuzuButtons:
                                if("hat" in str(yuzuButtons[x])):
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{},direction:{},guid:{},port:{},engine:sdl"'.format(yuzuButtons[x],yuzuHat[x],inputguid,portnumber))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")
                                elif("axis" in str(yuzuButtons[x])):
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuAxisButtons[x]))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")
                                else:
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"button:{},guid:{},port:{},engine:sdl"'.format(yuzuButtons[x],inputguid,portnumber))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                            #set joysticks
                            for x in yuzuAxis:
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:-,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuAxis[x]+1,yuzuAxis[x]))
                                
                        else:
                            #0 = Pro Controller, 1 = Dual Joycons, 4 = Handheld Mode,  (and other cases not yet defined)
                            #Switch and generic controllers aren't swapping ABXY
                            if (sdl_mapping['type'] == 0):
                                yuzuButtons = {
                                    "button_a":      sdl_mapping['button_b'],
                                    "button_b":      sdl_mapping['button_a'],
                                    "button_x":      sdl_mapping['button_y'],
                                    "button_y":      sdl_mapping['button_x'],
                                    "button_l":      sdl_mapping['button_l'],
                                    "button_r":      sdl_mapping['button_r'],
                                    "button_plus":   sdl_mapping['button_plus'],
                                    "button_minus":  sdl_mapping['button_minus'],
                                    "button_sl":     sdl_mapping['button_sl'],
                                    "button_sr":     sdl_mapping['button_sr'],
                                    "button_lstick": sdl_mapping['button_lstick'],
                                    "button_rstick": sdl_mapping['button_rstick'],
                                    "button_home":   sdl_mapping['button_home'],
                                    "button_dup":    sdl_mapping['button_dup'],
                                    "button_ddown":  sdl_mapping['button_ddown'],
                                    "button_dleft":  sdl_mapping['button_dleft'],
                                    "button_dright": sdl_mapping['button_dright'],
                                    "button_zl": sdl_mapping['button_zl'],
                                    "button_zr": sdl_mapping['button_zr']
                                }
                            else:
                                yuzuButtons = {
                                    "button_a":      sdl_mapping['button_a'],
                                    "button_b":      sdl_mapping['button_b'],
                                    "button_x":      sdl_mapping['button_x'],
                                    "button_y":      sdl_mapping['button_y'],
                                    "button_l":      sdl_mapping['button_l'],
                                    "button_r":      sdl_mapping['button_r'],
                                    "button_plus":   sdl_mapping['button_plus'],
                                    "button_minus":  sdl_mapping['button_minus'],
                                    "button_sl":     sdl_mapping['button_sl'],
                                    "button_sr":     sdl_mapping['button_sr'],
                                    "button_lstick": sdl_mapping['button_lstick'],
                                    "button_rstick": sdl_mapping['button_rstick'],
                                    "button_home":   sdl_mapping['button_home'],
                                    "button_dup":    sdl_mapping['button_dup'],
                                    "button_ddown":  sdl_mapping['button_ddown'],
                                    "button_dleft":  sdl_mapping['button_dleft'],
                                    "button_dright": sdl_mapping['button_dright'],
                                    "button_zl": sdl_mapping['button_zl'],
                                    "button_zr": sdl_mapping['button_zr']
                                }

                            yuzuAxis = {
                                "lstick":    int(sdl_mapping['axis_lstick_x']),
                                "rstick":    int(sdl_mapping['axis_rstick_x'])
                            }

                            yuzuAxisButtons = {
                                "button_zl": sdl_mapping['axis_button_zl'],
                                "button_zr": sdl_mapping['axis_button_zr']
                            }

                            yuzuHat = {
                                "button_dup":     'up',
                                "button_ddown":   'down',
                                "button_dleft":   'left',
                                "button_dright":  'right'
                            }

                            #Configure buttons and triggers
                            for x in yuzuButtons:
                                if("hat" in str(yuzuButtons[x])):
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"{},direction:{},guid:{},port:{},engine:sdl"'.format(yuzuButtons[x],yuzuHat[x],inputguid,portnumber))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")
                                elif("axis" in str(yuzuButtons[x])):
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,invert:+,port:{},guid:{},axis:{},threshold:0.500000"'.format(portnumber,inputguid,yuzuAxisButtons[x]))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")
                                else:
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"button:{},guid:{},port:{},engine:sdl"'.format(yuzuButtons[x],inputguid,portnumber))
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x + "\\default", "false")

                            #set joysticks
                            for x in yuzuAxis:
                                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '"engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:+,deadzone:0.150000,range:0.950000"'.format(portnumber,inputguid,yuzuAxis[x],yuzuAxis[x]+1))
                                        


                        #Enable motion no matter what, as enabling won't hurt things if it doesn't exist
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_motionleft", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_motionright", '"engine:sdl,motion:0,port:{},guid:{}"'.format(portnumber,inputguid))

                        yuzuConfig.set("Controls", "player_" + controllernumber + "_connected", "true")
                        if (controllernumber == "0"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "true")
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_connected\\default", "false")

                        if system.isOptSet(which_pad):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", system.config["p1_pad"])
                            #yuzuConfig.set("Controls", "player_0_type", system.config["p1_pad"])
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_type", "0")


                        yuzuConfig.set("Controls", "player_" + controllernumber + "_button_screenshot", "[empty]")
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_button_screenshot\\default", "false")
                        yuzuConfig.set("Controls", "player_" + controllernumber + "_type\\default", "true")


                        if system.isOptSet("yuzu_enable_rumble"):
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", system.config["yuzu_enable_rumble"])
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", system.config["yuzu_enable_rumble"])
                        else:
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled", "true")
                            yuzuConfig.set("Controls", "player_" + controllernumber + "_vibration_enabled\\default", "true")

                        lastplayer = int(controllernumber) + 1

            
            
            #lastplayer = lastplayer + 1
            eslog.debug("Last Player {}".format(lastplayer))
            for y in range(lastplayer, 9):
                controllernumber = str(y)
                eslog.debug("Setting Controller: {}".format(controllernumber))
                for x in yuzuButtons:
                    yuzuConfig.set("Controls", "player_" + controllernumber + "_" + x, '""')
                for x in yuzuAxis:
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
            #eslog.debug("Mapping: {}".format(input))

            if input.type == "button":
                return ("button:{},guid:{},port:{},engine:sdl").format(input.id, padGuid, controllernumber)
            elif input.type == "hat":
                return ("hat:{},direction:{},guid:{},port:{},engine:sdl").format(input.id, YuzuMainlineGenerator.hatdirectionvalue(input.value), padGuid, controllernumber)
            elif input.type == 'axis':
                return ("threshold:0.500000,axis:{},pad:0,port:{},guid:{},engine:sdl").format(input.id, controllernumber, padGuid)

    @staticmethod
    def setAxis(key, padGuid, padInputs,controllernumber, axisReversed):
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

        if(axisReversed == 1):
            #Left Joycon
            try:
                return ("engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:-,invert_y:+,deadzone:0.150000,range:0.950000").format(controllernumber, padGuid, inputy.id, inputx.id)
            except:
                return ("0")
        if(axisReversed == 2):
            #Right Joycon
            try:
                return ("engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:1,deadzone:0.150000,range:0.950000").format(controllernumber, padGuid, inputy.id, inputx.id)
            except:
                return ("0")
        else:
            try:
                return ("engine:sdl,port:{},guid:{},axis_x:{},offset_x:-0.011750,axis_y:{},offset_y:-0.027467,invert_x:+,invert_y:+,deadzone:0.150000,range:0.950000").format(controllernumber, padGuid, inputx.id, inputy.id)
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

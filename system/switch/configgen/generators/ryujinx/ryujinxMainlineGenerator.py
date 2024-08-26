#!/usr/bin/env python

import generators
from configgen.generators.Generator import Generator
import Command as Command
import os
import stat
import json
import uuid
from os import path
from os import environ
import batoceraFiles as batoceraFiles
import controllersConfig as controllersConfig
from shutil import copyfile
from utils.logger import get_logger
import subprocess


eslog = get_logger(__name__)

class RyujinxMainlineGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download Ryujinx.AppImage
        if os.path.exists("/userdata/system/switch/Ryujinx.AppImage"):
            st = os.stat("/userdata/system/switch/Ryujinx.AppImage")
            os.chmod("/userdata/system/switch/Ryujinx.AppImage", st.st_mode | stat.S_IEXEC)
        if os.path.exists("/userdata/system/switch/Ryujinx-Avalonia.AppImage"):
            st = os.stat("/userdata/system/switch/Ryujinx-Avalonia.AppImage")
            os.chmod("/userdata/system/switch/Ryujinx-Avalonia.AppImage", st.st_mode | stat.S_IEXEC)
        if os.path.exists("/userdata/system/switch/Ryujinx-LDN.AppImage"):
            st = os.stat("/userdata/system/switch/Ryujinx-LDN.AppImage")
            os.chmod("/userdata/system/switch/Ryujinx-LDN.AppImage", st.st_mode | stat.S_IEXEC)  

        if not path.isdir(batoceraFiles.CONF + "/Ryujinx"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx")
        if not path.isdir(batoceraFiles.CONF + "/Ryujinx/system"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx/system")

        RyujinxConfig = batoceraFiles.CONF + '/Ryujinx/Config.json'
        RyujinxHome = batoceraFiles.CONF

        firstrun = True
        if path.exists(RyujinxConfig):
            firstrun = False
        #First Run - Open Ryujinx for firmware install if it's never existed before

        #Configuration update
        RyujinxMainlineGenerator.writeRyujinxConfig(RyujinxConfig, system, playersControllers)

        if firstrun:  #Run Ryujinx with no rom so users can install firmware
            if system.config['emulator'] == 'ryujinx-avalonia':
                commandArray = ["/userdata/system/switch/Ryujinx-Avalonia.AppImage"]
            elif system.config['emulator'] == 'ryujinx-ldn':
                commandArray = ["/userdata/system/switch/Ryujinx-LDN.AppImage"]
            else:
                commandArray = ["/userdata/system/switch/Ryujinx.AppImage"]
        else:
            if system.config['emulator'] == 'ryujinx-avalonia':
                commandArray = ["/userdata/system/switch/Ryujinx-Avalonia.AppImage" , rom]
            elif system.config['emulator'] == 'ryujinx-ldn':
                commandArray = ["/userdata/system/switch/Ryujinx-LDN.AppImage" , rom]
            else:
                commandArray = ["/userdata/system/switch/Ryujinx.AppImage" , rom]
        eslog.debug("Controller Config before Playing: {}".format(controllersConfig.generateSdlGameControllerConfig(playersControllers)))
        #, "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxHome, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb", "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)}
            )

    def writeRyujinxConfig(RyujinxConfigFile, system, playersControllers):

        #Get ryujinx version
        if system.config['emulator'] == 'ryujinx-avalonia':
            filename = "/userdata/system/switch/extra/ryujinxavalonia/version.txt"
            os.environ["PYSDL2_DLL_PATH"] = "/userdata/system/switch/extra/ryujinxavalonia/"
        elif system.config['emulator'] == 'ryujinx-ldn':
            filename = "/userdata/system/switch/extra/ryujinxldn/version.txt"
            os.environ["PYSDL2_DLL_PATH"] = "/userdata/system/switch/extra/ryujinxldn/"
        else:
            filename = "/userdata/system/switch/extra/ryujinx/version.txt"
            os.environ["PYSDL2_DLL_PATH"] = "/userdata/system/switch/extra/ryujinx/"
            
        if os.path.exists(filename):
            file = open(filename, 'r')
            ryu_version = int(file.readline())
            file.close()
        else:
            ryu_version = 382
        #import SDL to try and guess controller order

        eslog.debug("Ryujinx Version: {}".format(ryu_version))

        #with open('/userdata/system/switch/configgen/mapping.csv', mode='r', encoding='utf-8-sig') as csv_file:
        #    reader = csv.DictReader(csv_file)
        #    controller_data = list(reader)

        if os.path.exists(RyujinxConfigFile):
            with open(RyujinxConfigFile, "r") as read_file:
                data = json.load(read_file)
        else:
                data = {}

        if system.config['emulator'] == 'ryujinx-avalonia':
            if ryu_version >= 1215:
                data['version'] = 49
            elif ryu_version >= 924:
                data['version'] = 47
            else:
                data['version'] = 42
        else:
            if ryu_version >= 1215:
                data['version'] = 49
            elif ryu_version >= 924:
                data['version'] = 47
            elif ryu_version > 382:
                data['version'] = 42
            else:
                data['version'] = 40
                
        data['enable_file_log'] = bool('true')
        data['backend_threading'] = 'Auto'

        if system.isOptSet('res_scale'):
            data['res_scale'] = int(system.config["res_scale"])
        else:
            data['res_scale'] = 1

        data['res_scale_custom'] = 1

        if system.isOptSet('max_anisotropy'):
            data['max_anisotropy'] = int(system.config["max_anisotropy"])
        else:
            data['max_anisotropy'] = -1 

        if system.isOptSet('aspect_ratio'):
            data['aspect_ratio'] = system.config["aspect_ratio"]
        else:
            data['aspect_ratio'] = 'Fixed16x9'

        data['logging_enable_debug'] = bool(0)
        data['logging_enable_stub'] = bool(0)
        data['logging_enable_info'] = bool(0)
        data['logging_enable_warn'] = bool(0)
        data['logging_enable_error'] = bool(0)
        data['logging_enable_trace'] = bool(0)
        data['logging_enable_guest'] = bool(0)
        data['logging_enable_fs_access_log'] = bool(0)
        data['logging_filtered_classes'] = []
        data['logging_graphics_debug_level'] = 'None'

        if system.isOptSet('system_language'):
            data['system_language'] = system.config["system_language"]
        else:
            data['system_language'] = 'AmericanEnglish'

        if system.isOptSet('system_region'):
            data['system_region'] = system.config["system_region"]
        else:
            data['system_region'] = 'USA'

        data['system_time_zone'] = 'UTC'
        data['system_time_offset'] = 0

        if system.isOptSet('ryu_docked_mode'):
            data['docked_mode'] = bool(int(system.config["ryu_docked_mode"]))
        else:
            data['docked_mode'] = bool('true')

        if system.isOptSet('ryu_enable_discord_integration'):
            data['enable_discord_integration'] = bool(int(system.config["ryu_enable_discord_integration"]))
        else:
            data['enable_discord_integration'] = bool('true')    

        data['check_updates_on_start'] = bool('false')
        data['show_confirm_exit'] = bool(0)
        data['hide_cursor_on_idle'] = bool('true')

        #V-Sync
        if system.isOptSet('ryu_vsync'):
            data['enable_vsync'] = bool(int(system.config["ryu_vsync"]))
        else:
            data['enable_vsync'] = bool('true')    

        #Shader Cache
        if system.isOptSet('ryu_shadercache'):
            data['enable_shader_cache'] = bool(int(system.config["ryu_shadercache"]))
        else:
            data['enable_shader_cache'] = bool('true')    

        #data['enable_texture_recompression'] = bool(0)

        if system.isOptSet('enable_ptc'):
            data['enable_ptc'] = bool(int(system.config["enable_ptc"]))
        else:
            data['enable_ptc'] = bool('true')    


        data['enable_internet_access'] = bool(0)

        #File System Integrity Checks
        if system.isOptSet('enable_fs_integrity_checks'):
            data['enable_fs_integrity_checks'] = bool(int(system.config["enable_fs_integrity_checks"]))
        else:
            data['enable_fs_integrity_checks'] = bool('true')    

        data['fs_global_access_log_mode'] = 0
        data['audio_backend'] = 'SDL2'
        data['audio_volume'] = 1

        if system.isOptSet('memory_manager_mode'):
            data['memory_manager_mode'] = system.config["memory_manager_mode"]
        else:
            data['memory_manager_mode'] = 'HostMappedUnsafe'   

        if system.isOptSet('expand_ram'):
            data['expand_ram'] = bool(int(system.config["expand_ram"]))
        else:
            data['expand_ram'] = bool(0)  

        if system.isOptSet('ignore_missing_services'):
            data['ignore_missing_services'] = bool(int(system.config["ignore_missing_services"]))
        else:
            data['ignore_missing_services'] = bool(0) 

        data['language_code'] = str(getLangFromEnvironment())

        data['enable_custom_theme'] = bool(0)
        data['custom_theme_path'] = ''
        data['base_style'] = 'Dark'
        data['game_list_view_mode'] = 0
        data['show_names'] = bool('true')
        data['grid_size'] = 2
        data['application_sort'] = 0
        data['is_ascending_order'] = bool('true')
        data['start_fullscreen'] = bool('true')
        data['show_console'] = bool('true')
        data['enable_keyboard'] = bool(0)
        data['enable_mouse'] = bool(0)
        data['game_dirs'] = ["/userdata/roms/switch"]
        data['keyboard_config'] = []
        data['controller_config'] = []
        hotkeys = {}
        hotkeys['toggle_vsync'] = "Tab"
        hotkeys['screenshot'] = "F8"
        hotkeys['show_ui'] = "F4" 
        hotkeys['pause'] = "F5"
        hotkeys['toggle_mute'] = "F2"
        hotkeys['res_scale_up'] = "Unbound" 
        hotkeys['res_scale_down'] = "Unbound" 
        data['hotkeys'] = hotkeys  
        gui_columns = {}
        gui_columns['fav_column'] = bool('true')
        gui_columns['icon_column'] = bool('true')
        gui_columns['app_column'] = bool('true')
        gui_columns['dev_column'] = bool('true')
        gui_columns['version_column'] = bool('true')
        gui_columns['time_played_column'] = bool('true')
        gui_columns['last_played_column'] = bool('true')
        gui_columns['file_ext_column'] = bool('true')
        gui_columns['file_size_column'] = bool('true')
        gui_columns['path_column'] = bool('true')
        data['gui_columns'] = gui_columns 
        column_sort = {}
        column_sort['sort_column_id'] = 0
        column_sort['sort_ascending'] = bool(0)         
        data['column_sort'] = column_sort

        if ((system.isOptSet('ryu_auto_controller_config') and not (system.config["ryu_auto_controller_config"] == "0")) or not system.isOptSet('ryu_auto_controller_config')):
            
            # make sure that libSDL2.so is restored (because when using Xbox series X, it has to be renamed in libSDL2.so-configgen
            filename_sdl2 = os.environ["PYSDL2_DLL_PATH"] + "libSDL2.so"
            filename_sdl2_configgen = filename_sdl2 + "-configgen"
            if not os.path.exists(filename_sdl2):
                os.replace(filename_sdl2_configgen, filename_sdl2)

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

            input_config = []

              

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
                        pad = sdl2.SDL_GameControllerOpen(i)
                        joy_guid = joystick.SDL_JoystickGetDeviceGUID(i)
                        buff = create_string_buffer(33)
                        joystick.SDL_JoystickGetGUIDString(joy_guid,buff,33)                    
                        joy_path = joystick.SDL_JoystickPathForIndex(i)
                        guidstring = ((bytes(buff)).decode()).split('\x00',1)[0]

                        if(joy_path.decode() == 'nintendo_joycons_combined' ):
                            outputpath = 'nintendo_joycons_combined'
                        else:    
                            command = "udevadm info --query=path --name=" + joy_path.decode()
                            outputpath = (((subprocess.check_output(command, shell=True)).decode()).partition('/input/')[0]).partition('/hidraw')[0]
                            
                        pad_type = sdl2.SDL_GameControllerTypeForIndex(i)
                        #Fix for Steam controller assignment
                        controllername = (sdl2.SDL_GameControllerNameForIndex(i)).decode()
                        if( "Steam" in controllername):
                            pad_type = 1
                        if("Xin-Mo Xin-Mo Dual Arcade" in controllername):
                            pad_type = 1
                        controller_value = {"index" : i , 'path' : outputpath, "guid" : guidstring, "type" : pad_type }
                        sdl_devices.append(controller_value)
                        sdl2.SDL_GameControllerClose(pad)
            sdl2.SDL_Quit()

            eslog.debug("Joysticks: {}".format(sdl_devices))
            #New Logic
            for index in playersControllers :
                controller = playersControllers[index]
                #inputguid = controller.guid
                if(controller.guid != "050000007e0500000620000001800000" and controller.guid != "050000007e0500000720000001800000"):
                    #don't run the code for Joy-Con (L) or Joy-Con (R) - Batocera adds these and only works with a pair
                    if debugcontrollers:
                        eslog.debug("Controller configName: {}".format(controller.configName))
                        eslog.debug("Controller index: {}".format(controller.index))
                        eslog.debug("Controller realName: {}".format(controller.realName))                
                        eslog.debug("Controller dev: {}".format(controller.dev))
                        eslog.debug("Controller player: {}".format(controller.player))
                        eslog.debug("Controller GUID: {}".format(controller.guid))



                    if(playersControllers[index].realName == 'Nintendo Switch Combined Joy-Cons'):  #works in Batocera v37
                        outputpath = "nintendo_joycons_combined"
                        sdl_mapping = next((item for item in sdl_devices if (item["path"] == outputpath or item["path"] == '/devices/virtual')),None)
                    else:
                        command = "udevadm info --query=path --name=" + playersControllers[index].dev
                        outputpath = ((subprocess.check_output(command, shell=True)).decode()).partition('/input/')[0]
                        sdl_mapping = next((item for item in sdl_devices if item["path"] == outputpath),None)

                    eslog.debug("Mapping: {}".format(sdl_mapping))
                    
                    myid = uuid.UUID(sdl_mapping['guid'])
                    myid.bytes_le
                    convuuid = uuid.UUID(bytes=myid.bytes_le)
                    controllernumber = str(sdl_mapping['index'])
                    #Map Keys and GUIDs
                    cvalue = {}
    

                    motion = {}
                    motion['motion_backend'] = "GamepadDriver"
                    motion['sensitivity'] = 100
                    motion['gyro_deadzone'] = 1

                    motion['enable_motion'] = bool('true')

                    rumble = {}
                    rumble['strong_rumble'] = 1
                    rumble['weak_rumble'] = 1
                    if system.isOptSet("ryu_enable_rumble"):
                        rumble['enable_rumble'] = bool(int(system.config["ryu_enable_rumble"]))
                    else:
                        rumble['enable_rumble'] = bool('true')
                    
                    which_pad = "p" + str(int(controller.player)) + "_pad"

                    if ((system.isOptSet(which_pad) and ((system.config[which_pad] == "ProController") or (system.config[which_pad] == "JoyconPair")) ) or not system.isOptSet(which_pad)):
                        left_joycon_stick = {}
                        left_joycon_stick['joystick'] = "Left"
                        left_joycon_stick['rotate90_cw'] = bool(0)
                        left_joycon_stick['invert_stick_x'] = bool(0)
                        left_joycon_stick['invert_stick_y'] = bool(0)
                        left_joycon_stick['stick_button'] = "LeftStick"            

                        right_joycon_stick = {}
                        right_joycon_stick['joystick'] = "Right"
                        right_joycon_stick['rotate90_cw'] = bool(0)
                        right_joycon_stick['invert_stick_x'] = bool(0)
                        right_joycon_stick['invert_stick_y'] = bool(0)
                        right_joycon_stick['stick_button'] = "RightStick" 



                        left_joycon = {}
                        left_joycon['button_minus'] = "Minus"
                        left_joycon['button_l'] = "LeftShoulder"
                        left_joycon['button_zl'] = "LeftTrigger"
                        left_joycon['button_sl'] = "Unbound"
                        left_joycon['button_sr'] = "Unbound"
                        left_joycon['dpad_up'] = "DpadUp"
                        left_joycon['dpad_down'] = "DpadDown"
                        left_joycon['dpad_left'] = "DpadLeft"
                        left_joycon['dpad_right'] = "DpadRight"


                        right_joycon = {}
                        right_joycon['button_plus'] = "Plus"
                        right_joycon['button_r'] = "RightShoulder"
                        right_joycon['button_zr'] = "RightTrigger"
                        right_joycon['button_sl'] = "Unbound"
                        right_joycon['button_sr'] = "Unbound"

                        if (sdl_mapping['type'] == 0) or (sdl_mapping['type'] == 5) or (sdl_mapping['type'] >= 11):
                            right_joycon['button_x'] = "X"
                            right_joycon['button_b'] = "B"
                            right_joycon['button_y'] = "Y"
                            right_joycon['button_a'] = "A" 
                        else:
                            right_joycon['button_x'] = "Y"
                            right_joycon['button_b'] = "A"
                            right_joycon['button_y'] = "X"
                            right_joycon['button_a'] = "B" 

                        if system.isOptSet(which_pad):
                            cvalue['controller_type'] = system.config["p1_pad"]
                        else: 
                            cvalue['controller_type'] = "ProController"

                    elif (system.isOptSet(which_pad) and (system.config[which_pad] == "JoyconLeft")):
                        left_joycon_stick = {}
                        left_joycon_stick['joystick'] = "Left"
                        left_joycon_stick['rotate90_cw'] = bool(0)
                        left_joycon_stick['invert_stick_x'] = bool(0)
                        left_joycon_stick['invert_stick_y'] = bool(0)
                        left_joycon_stick['stick_button'] = "LeftStick"            

                        right_joycon_stick = {}
                        right_joycon_stick['joystick'] = "Unbound"
                        right_joycon_stick['rotate90_cw'] = bool(0)
                        right_joycon_stick['invert_stick_x'] = bool(0)
                        right_joycon_stick['invert_stick_y'] = bool(0)
                        right_joycon_stick['stick_button'] = "Unbound"

                        left_joycon = {}
                        left_joycon['button_minus'] = "Minus"
                        left_joycon['button_l'] = "LeftShoulder"
                        left_joycon['button_zl'] = "LeftTrigger"
                        left_joycon['button_sl'] = "LeftShoulder"
                        left_joycon['button_sr'] = "RightShoulder"

                        if (sdl_mapping['type'] == 0) or (sdl_mapping['type'] == 5) or (sdl_mapping['type'] >= 11):
                            left_joycon['dpad_up'] = "Y"
                            left_joycon['dpad_down'] = "A"
                            left_joycon['dpad_left'] = "X"
                            left_joycon['dpad_right'] = "B"
                        else:
                            left_joycon['dpad_up'] = "Y"
                            left_joycon['dpad_down'] = "A"
                            left_joycon['dpad_left'] = "X"
                            left_joycon['dpad_right'] = "B"                        

                        right_joycon = {}
                        right_joycon['button_plus'] = "Plus"
                        right_joycon['button_r'] = "RightShoulder"
                        right_joycon['button_zr'] = "RightTrigger"
                        right_joycon['button_sl'] = "Unbound"
                        right_joycon['button_sr'] = "Unbound"

                        if (sdl_mapping['type'] == 0) or (sdl_mapping['type'] == 5) or (sdl_mapping['type'] >= 11):
                            right_joycon['button_x'] = "X"
                            right_joycon['button_b'] = "B"
                            right_joycon['button_y'] = "Y"
                            right_joycon['button_a'] = "A"                         
                        else:
                            right_joycon['button_x'] = "Y"
                            right_joycon['button_b'] = "A"
                            right_joycon['button_y'] = "X"
                            right_joycon['button_a'] = "B" 

                        cvalue['controller_type'] = "JoyconLeft"
                        
                    elif (system.isOptSet(which_pad) and (system.config[which_pad] == "JoyconRight")):
                        left_joycon_stick = {}
                        left_joycon_stick['joystick'] = "Unbound"
                        left_joycon_stick['rotate90_cw'] = bool(1)
                        left_joycon_stick['invert_stick_x'] = bool(1)
                        left_joycon_stick['invert_stick_y'] = bool(1)
                        left_joycon_stick['stick_button'] = "Unbound"           

                        right_joycon_stick = {}
                        right_joycon_stick['joystick'] = "Left"
                        right_joycon_stick['rotate90_cw'] = bool(0)
                        right_joycon_stick['invert_stick_x'] = bool(0)
                        right_joycon_stick['invert_stick_y'] = bool(0)
                        right_joycon_stick['stick_button'] = "LeftStick" 

                        left_joycon = {}
                        left_joycon['button_minus'] = "Minus"
                        left_joycon['button_l'] = "LeftShoulder"
                        left_joycon['button_zl'] = "LeftTrigger"
                        left_joycon['button_sl'] = "Unbound"
                        left_joycon['button_sr'] = "Unbound"

                        left_joycon['dpad_up'] = "DpadUp"
                        left_joycon['dpad_down'] = "DpadDown"
                        left_joycon['dpad_left'] = "DpadLeft"
                        left_joycon['dpad_right'] = "DpadRight"

                        right_joycon = {}
                        right_joycon['button_plus'] = "Plus"
                        right_joycon['button_r'] = "RightShoulder"
                        right_joycon['button_zr'] = "RightTrigger"
                        right_joycon['button_sl'] = "LeftShoulder"
                        right_joycon['button_sr'] = "RightShoulder"

                        if (sdl_mapping['type'] == 0) or (sdl_mapping['type'] == 5) or (sdl_mapping['type'] >= 11):
                            right_joycon['button_x'] = "A"
                            right_joycon['button_b'] = "Y"
                            right_joycon['button_y'] = "X"
                            right_joycon['button_a'] = "B" 
                        else:
                            right_joycon['button_x'] = "B"
                            right_joycon['button_b'] = "X"
                            right_joycon['button_y'] = "Y"
                            right_joycon['button_a'] = "A"                         
                        cvalue['controller_type'] = "JoyconRight"
                    else:
                        #Handle old settings that don't match above
                        left_joycon_stick = {}
                        left_joycon_stick['joystick'] = "Left"
                        left_joycon_stick['rotate90_cw'] = bool(0)
                        left_joycon_stick['invert_stick_x'] = bool(0)
                        left_joycon_stick['invert_stick_y'] = bool(0)
                        left_joycon_stick['stick_button'] = "LeftStick"            

                        right_joycon_stick = {}
                        right_joycon_stick['joystick'] = "Right"
                        right_joycon_stick['rotate90_cw'] = bool(0)
                        right_joycon_stick['invert_stick_x'] = bool(0)
                        right_joycon_stick['invert_stick_y'] = bool(0)
                        right_joycon_stick['stick_button'] = "RightStick" 



                        left_joycon = {}
                        left_joycon['button_minus'] = "Minus"
                        left_joycon['button_l'] = "LeftShoulder"
                        left_joycon['button_zl'] = "LeftTrigger"
                        left_joycon['button_sl'] = "Unbound"
                        left_joycon['button_sr'] = "Unbound"
                        left_joycon['dpad_up'] = "DpadUp"
                        left_joycon['dpad_down'] = "DpadDown"
                        left_joycon['dpad_left'] = "DpadLeft"
                        left_joycon['dpad_right'] = "DpadRight"


                        right_joycon = {}
                        right_joycon['button_plus'] = "Plus"
                        right_joycon['button_r'] = "RightShoulder"
                        right_joycon['button_zr'] = "RightTrigger"
                        right_joycon['button_sl'] = "Unbound"
                        right_joycon['button_sr'] = "Unbound"

                        if (sdl_mapping['type'] == 0) or (sdl_mapping['type'] == 5) or (sdl_mapping['type'] >= 11):
                            right_joycon['button_x'] = "X"
                            right_joycon['button_b'] = "B"
                            right_joycon['button_y'] = "Y"
                            right_joycon['button_a'] = "A" 
                        else:
                            right_joycon['button_x'] = "Y"
                            right_joycon['button_b'] = "A"
                            right_joycon['button_y'] = "X"
                            right_joycon['button_a'] = "B" 

                        cvalue['controller_type'] = "ProController"

                    cvalue['left_joycon_stick'] = left_joycon_stick          
                    cvalue['right_joycon_stick'] = right_joycon_stick
                    cvalue['deadzone_left'] = 0.1           
                    cvalue['deadzone_right'] = 0.1 
                    cvalue['range_left'] = 1          
                    cvalue['range_right'] = 1 
                    cvalue['trigger_threshold'] = 0.5  
                    cvalue['motion'] = motion
                    cvalue['rumble'] = rumble
                    cvalue['left_joycon'] = left_joycon
                    cvalue['right_joycon'] = right_joycon

                    cvalue['version'] = 1
                    cvalue['backend'] = "GamepadSDL2"
                    cvalue['id'] = controllernumber + '-' + str(convuuid)
                    
                    cvalue['player_index'] = "Player" +  str(int(controller.player))
                    input_config.append(cvalue)
            
            data['input_config'] = input_config

        # if we turn the auto_control_config off, then it's better to avoid conflicts with the sdl2 coming from ryujinx (which completely messes up xbox series x controllers with both bluetooth and dongle
        try:
            if system.config["ryu_auto_controller_config"] == "0":
                filename_sdl2 = os.environ["PYSDL2_DLL_PATH"] + "libSDL2.so"
                filename_sdl2_configgen = filename_sdl2 + "-configgen"
                if os.path.exists(filename_sdl2):
                    os.replace(filename_sdl2, filename_sdl2_configgen)
        except:
            pass
        
        #Resolution Scale
        if system.isOptSet('ryu_resolution_scale'):
            if system.config["ryu_resolution_scale"] in {'1.0', '2.0', '3.0', '4.0', 1.0, 2.0, 3.0, 4.0}:
                data['res_scale_custom'] = 1
                if system.config["ryu_resolution_scale"] in {'1.0', 1.0}:
                    data['res_scale'] = 1
                if system.config["ryu_resolution_scale"] in {'2.0', 2.0}:
                    data['res_scale'] = 2
                if system.config["ryu_resolution_scale"] in {'3.0', 3.0}:
                    data['res_scale'] = 3
                if system.config["ryu_resolution_scale"] in {'4.0', 4.0}:
                    data['res_scale'] = 4
            else:
                data['res_scale_custom'] = float(system.config["ryu_resolution_scale"])
                data['res_scale'] = -1
        else:
            data['res_scale_custom'] = 1
            data['res_scale'] = 1

        #Texture Recompression
        if system.isOptSet('ryu_texture_recompression'):
            if system.config["ryu_texture_recompression"] in {"true", "1", 1}:
                data['enable_texture_recompression'] = True
            elif system.config["ryu_texture_recompression"] in {"false", "0", 0}:
                data['enable_texture_recompression'] = False
        else:
            data['enable_texture_recompression'] = False

        #Vulkan or OpenGl
        if system.isOptSet('ryu_backend'):
            data['graphics_backend'] = system.config["ryu_backend"]
        else:
            data['graphics_backend'] = 'Vulkan'

        #Audio backend: SDL2 or OpenAL
        if system.isOptSet('ryu_audio_backend'):
            data['audio_backend'] = system.config["ryu_audio_backend"]
        else:
            data['audio_backend'] = 'SDL2'

        # this erases the user manual configuration.
        # It's problematic in case of hybrid laptop as it may always default to the igpu instead of the dgpu
        # data['preferred_gpu'] = ""

        with open(batoceraFiles.CONF + '/Ryujinx/BeforeRyu.json', "w") as outfile:
            outfile.write(json.dumps(data, indent=2))

        with open(RyujinxConfigFile, "w") as outfile:
            outfile.write(json.dumps(data, indent=2))


def getLangFromEnvironment():
    lang = environ['LANG'][:5]
    availableLanguages = [ "en_US", "pt_BR", "es_ES", "fr_FR", "de_DE","it_IT", "el_GR", "tr_TR", "zh_CN"]
    if lang in availableLanguages:
        return lang
    else:
        return "en_US"

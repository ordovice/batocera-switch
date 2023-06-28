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
from xml.dom import minidom
import codecs
import controllersConfig as controllersConfig
import configparser
from shutil import copyfile
from utils.logger import get_logger
import csv
import sys
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

        #copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/Ryujinx/system/prod.keys")
        #copyfile(batoceraFiles.BIOS + "/switch/title.keys", batoceraFiles.CONF + "/Ryujinx/system/title.keys")

        RyujinxConfig = batoceraFiles.CONF + '/Ryujinx/Config.json'
        RyujinxHome = batoceraFiles.CONF
        RyujinxSaves = batoceraFiles.CONF
        eslog.debug("System Path: {}".format(sys.path))
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
            ryu_version = file.readline()
            file.close()
        else:
            ryu_version = "1.1.382"
        #import SDL to try and guess controller order
        from ..ryujinx import sdl2
        from ..ryujinx.sdl2 import (
            SDL_TRUE
        )
        from ..ryujinx.sdl2 import joystick
        from ctypes import create_string_buffer
        #ret = SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)



        sdl2.SDL_ClearError()
        sdl2.SDL_SetHint(b"SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", b"1")
        ret = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_GAMECONTROLLER)
        assert ret == 0, _check_error_msg()
            # Also initialize a virtual joystick (if supported)
        if sdl2.dll.version >= 2014:
            virt_type = joystick.SDL_JOYSTICK_TYPE_GAMECONTROLLER
            #virt_index = joystick.SDL_JoystickAttachVirtual(virt_type, 2, 4, 1)
        
        sdl_devices = []
        count = joystick.SDL_NumJoysticks()
        for i in range(count):
                if sdl2.SDL_IsGameController(i) == SDL_TRUE:
                    pad = sdl2.SDL_GameControllerOpen(i)
                    joy_guid = joystick.SDL_JoystickGetDeviceGUID(i)
                    buff = create_string_buffer(33)
                    joystick.SDL_JoystickGetGUIDString(joy_guid,buff,33)                    
                    joy_path = joystick.SDL_JoystickPathForIndex(i)

                    guidstring = ((bytes(buff)).decode()).split('\x00',1)[0]
                    command = "udevadm info --query=path --name=" + joy_path.decode()
                    outputpath = (((subprocess.check_output(command, shell=True)).decode()).partition('/input/')[0]).partition('/hidraw')[0]
                    controller_value = {"index" : i , 'path' : outputpath, "guid" : guidstring }
                    sdl_devices.append(controller_value)
                    sdl2.SDL_GameControllerClose(pad)
        sdl2.SDL_Quit()

        eslog.debug("Joystick Path: {}".format(sdl_devices))


        with open('/userdata/system/switch/configgen/mapping.csv', mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            controller_data = list(reader)

        if os.path.exists(RyujinxConfigFile):
            with open(RyujinxConfigFile, "r") as read_file:
                data = json.load(read_file)
        else:
                data = {}
        if system.config['emulator'] == 'ryujinx-avalonia':
            data['version'] = 42  #Avalonia Version needs to see 38
        else:
            if(ryu_version == '1.1.382'):
                data['version'] = 40  #1.1.382 version
            else:
                data['version'] = 47 #1.1.924 version
        
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

        data['check_updates_on_start'] = bool(0)
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

        data['enable_texture_recompression'] = bool(0)

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

        guidstoreplace_ds4a = ["050000004c050000cc09000000810000","050000004c050000c405000000783f00","050000004c050000c4050000fffe3f00","050000004c050000c4050000ffff3f00","050000004c050000cc090000fffe3f00","050000004c050000cc090000ffff3f00","30303839663330346632363232623138","31326235383662333266633463653332","34613139376634626133336530386430","37626233336235343937333961353732","38393161636261653636653532386639","63313733393535663339656564343962","63393662363836383439353064663939","65366465656364636137653363376531","66613532303965383534396638613230","050000004c050000cc090000df070000","050000004c050000cc090000df870001","050000004c050000cc090000ff070000","030000004c050000a00b000011010000","030000004c050000a00b000011810000","030000004c050000c405000011010000","030000004c050000c405000011810000","030000004c050000cc09000000010000","030000004c050000cc09000011010000","030000004c050000cc09000011810000","03000000c01100000140000011010000","050000004c050000c405000000010000","050000004c050000c405000001800000","050000004c050000cc09000000010000","050000004c050000cc09000001800000","030000004c050000a00b000000010000","030000004c050000c405000000000000","030000004c050000c405000000010000","03000000120c00000807000000000000","03000000120c0000111e000000000000","03000000120c0000121e000000000000","03000000120c0000130e000000000000","03000000120c0000150e000000000000","03000000120c0000180e000000000000","03000000120c0000181e000000000000","03000000120c0000191e000000000000","03000000120c00001e0e000000000000","03000000120c0000a957000000000000","03000000120c0000aa57000000000000","03000000120c0000f21c000000000000","03000000120c0000f31c000000000000","03000000120c0000f41c000000000000","03000000120c0000f51c000000000000","03000000120c0000f70e000000000000","03000000120e0000120c000000000000","03000000160e0000120c000000000000","030000001a1e0000120c000000000000","030000004c050000a00b000000000000","030000004c050000cc09000000000000","35643031303033326130316330353564","31373231336561636235613666323035","536f6e7920496e746572616374697665","576972656c65737320436f6e74726f6c","050000004c050000cc090000ff870001","050000004c050000cc090000ff876d01","31663838336334393132303338353963"]
        guidstoreplace_ds4b = ["050000004c050000c405000000810000"]

        guidstoreplace_ds5_wireless = ["32633532643734376632656664383733","37363764353731323963323639666565","61303162353165316365336436343139","050000004c050000e60c0000df870000","050000004c050000e60c000000810000","030000004c050000e60c000000010000","050000004c050000e60c0000fffe3f00","030000004c050000e60c000000000000","050000004c050000e60c000000010000","030000004c050000e60c000011010000","32346465346533616263386539323932","050000004c050000e60c0000ff870000"]
        guidstoreplace_ds5_wired = ["030000004c050000e60c000011810000"]
        guidstoreplace_xbox = ["050000005e040000fd02000030110000"]
        guidstochangebuttons_xbox = ["030000005e0400008e02000014010000"]

        xbox_count = 0
        switch_count = 0
        ds4_count = 0
        ds5_count = 0
        if(ryu_version == "1.1.382"):
            for index in playersControllers :
                controller = playersControllers[index]

                controller_mapping = next((item for item in controller_data if item["old_guid"] == controller.guid),None)

                if(controller_mapping == None):
                    if controller.guid in guidstoreplace_xbox:
                        xbox_count = xbox_count + 1
                    if controller.guid in guidstoreplace_ds4a:
                        ds4_count = ds4_count + 1
                    if controller.guid in guidstoreplace_ds4b:
                        ds4_count = ds4_count + 1
                    if controller.guid in guidstoreplace_ds5_wireless:
                        ds5_count = ds5_count + 1
                    if controller.guid in guidstoreplace_ds5_wired:
                        ds5_count = ds5_count + 1
                else:
                    if controller_mapping['ryu_type'] == 'xbox':
                        xbox_count = xbox_count + 1
                    if controller_mapping['ryu_type'] == 'sony_ds4':
                        ds4_count = ds4_count + 1
                    if controller_mapping['ryu_type'] == 'sony_ds5':
                        ds5_count = ds5_count + 1
                    if controller_mapping['ryu_type'] == 'switch':
                        switch_count = switch_count + 1

            ds4_index = 0
            switch_index = ds4_count + ds5_count
            xbox_index = ds4_count + ds5_count + switch_count
            reg_index = ds4_count + ds5_count + xbox_count + switch_count

            eslog.debug("Counts: Sony DS4: {}".format(ds4_count))
            eslog.debug("Counts: Sony DS5: {}".format(ds5_count))
            eslog.debug("Counts: Switch: {}".format(switch_count))
            eslog.debug("Counts: XBox: {}".format(xbox_count))

            eslog.debug("Index: Sony DS4: {}".format(ds4_index))
            eslog.debug("Index: Switch: {}".format(switch_index))
            eslog.debug("Index: XBox: {}".format(xbox_index))

        if ((system.isOptSet('ryu_auto_controller_config') and not (system.config["ryu_auto_controller_config"] == "0")) or not system.isOptSet('ryu_auto_controller_config')):
            



            input_config = []

            if(ryu_version != "1.1.382"):
                #New Logic
                for index in playersControllers :
                    controller = playersControllers[index]
                    inputguid = controller.guid
                    command = "udevadm info --query=path --name=" + playersControllers[index].dev
                    outputpath = ((subprocess.check_output(command, shell=True)).decode()).partition('/input/')[0]

                    controller_mapping = next((item for item in controller_data if item["old_guid"] == inputguid),None)
                    sdl_mapping = next((item for item in sdl_devices if item["path"] == outputpath),None)

                    myid = uuid.UUID(sdl_mapping['guid'])
                    myid.bytes_le
                    convuuid = uuid.UUID(bytes=myid.bytes_le)
                    controllernumber = str(sdl_mapping['index'])
                    #Map Keys and GUIDs
                    cvalue = {}
                    left_joycon_stick = {}
                    left_joycon_stick['joystick'] = "Left"
                    left_joycon_stick['invert_stick_x'] = bool(0)
                    left_joycon_stick['invert_stick_y'] = bool(0)
                    left_joycon_stick['rotate90_cw'] = bool(0)
                    left_joycon_stick['stick_button'] = "LeftStick"            
                    cvalue['left_joycon_stick'] = left_joycon_stick
                    right_joycon_stick = {}
                    right_joycon_stick['joystick'] = "Right"
                    right_joycon_stick['invert_stick_x'] = bool(0)
                    right_joycon_stick['invert_stick_y'] = bool(0)
                    right_joycon_stick['rotate90_cw'] = bool(0)
                    right_joycon_stick['stick_button'] = "RightStick"            
                    cvalue['right_joycon_stick'] = right_joycon_stick
                    cvalue['deadzone_left'] = 0.1           
                    cvalue['deadzone_right'] = 0.1 
                    cvalue['range_left'] = 1          
                    cvalue['range_right'] = 1 
                    cvalue['trigger_threshold'] = 0.5  

                    motion = {}
                    motion['motion_backend'] = "GamepadDriver"
                    motion['sensitivity'] = 100
                    motion['gyro_deadzone'] = 1
                    motion['enable_motion'] = bool('true')
                    cvalue['motion'] = motion

                    rumble = {}
                    rumble['strong_rumble'] = 1
                    rumble['weak_rumble'] = 1
                    rumble['enable_rumble'] = bool('true')
                    cvalue['rumble'] = rumble

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

                    cvalue['left_joycon'] = left_joycon
                    right_joycon = {}
                    right_joycon['button_plus'] = "Plus"
                    right_joycon['button_r'] = "RightShoulder"
                    right_joycon['button_zr'] = "RightTrigger"
                    right_joycon['button_sl'] = "Unbound"
                    right_joycon['button_sr'] = "Unbound"

                    if (controller_mapping == None):
                        #Follow Default
                        right_joycon['button_x'] = "X"
                        right_joycon['button_b'] = "B"
                        right_joycon['button_y'] = "Y"
                        right_joycon['button_a'] = "A" 
                    else:
                        right_joycon['button_x'] = controller_mapping['ryu_x']
                        right_joycon['button_b'] = controller_mapping['ryu_b']
                        right_joycon['button_y'] = controller_mapping['ryu_y']
                        right_joycon['button_a'] = controller_mapping['ryu_a']
                    cvalue['right_joycon'] = right_joycon

                    cvalue['version'] = 1
                    cvalue['backend'] = "GamepadSDL2"
                    cvalue['id'] = controllernumber + '-' + str(convuuid)
                    cvalue['controller_type'] = "ProController"
                    cvalue['player_index'] = "Player" +  str(int(controller.player))
                    input_config.append(cvalue)
            else:
                #Old Logic
                eslog.debug("Following old 1.1.382 logic")
                
                for index in playersControllers :
                    controller = playersControllers[index]
                    if controller.guid in guidstoreplace_xbox:
                        controllernumber = str(int(ds4_index))
                        ds4_index = ds4_index + 1
                        inputguid = "030000005e040000fd02000000006800"
                    elif controller.guid in guidstoreplace_ds4a:
                        controllernumber = str(int(ds4_index))
                        ds4_index = ds4_index + 1
                        inputguid = "030000004c050000cc09000000006800"
                    elif controller.guid in guidstoreplace_ds4b:
                        controllernumber = str(int(ds4_index))
                        ds4_index = ds4_index + 1
                        inputguid = "030000004c050000c405000000006800"
                    elif controller.guid in guidstoreplace_ds5_wireless:
                        controllernumber = str(int(ds4_index))
                        ds4_index = ds4_index + 1
                        inputguid = "030000004c050000e60c000000006800"
                        #inputguid = "030072264c050000e60c000000006800"  #Ryujinx > 1.1.383
                    elif controller.guid in guidstoreplace_ds5_wired:
                        controllernumber = str(int(ds4_index))
                        ds4_index = ds4_index + 1
                        inputguid = "030000004c050000e60c000000016800"
                    else:
                        controllernumber = str(int(reg_index))
                        reg_index = reg_index + 1
                        inputguid = controller.guid
                    myid = uuid.UUID(inputguid)
                    myid.bytes_le
                    convuuid = uuid.UUID(bytes=myid.bytes_le)
                    cvalue = {}
                    left_joycon_stick = {}
                    left_joycon_stick['joystick'] = "Left"
                    left_joycon_stick['invert_stick_x'] = bool(0)
                    left_joycon_stick['invert_stick_y'] = bool(0)
                    left_joycon_stick['rotate90_cw'] = bool(0)
                    left_joycon_stick['stick_button'] = "LeftStick"            
                    cvalue['left_joycon_stick'] = left_joycon_stick
                    right_joycon_stick = {}
                    right_joycon_stick['joystick'] = "Right"
                    right_joycon_stick['invert_stick_x'] = bool(0)
                    right_joycon_stick['invert_stick_y'] = bool(0)
                    right_joycon_stick['rotate90_cw'] = bool(0)
                    right_joycon_stick['stick_button'] = "RightStick"            
                    cvalue['right_joycon_stick'] = right_joycon_stick
                    cvalue['deadzone_left'] = 0.1           
                    cvalue['deadzone_right'] = 0.1 
                    cvalue['range_left'] = 1          
                    cvalue['range_right'] = 1 
                    cvalue['trigger_threshold'] = 0.5  

                    motion = {}
                    motion['motion_backend'] = "GamepadDriver"
                    motion['sensitivity'] = 100
                    motion['gyro_deadzone'] = 1
                    motion['enable_motion'] = bool('true')
                    cvalue['motion'] = motion

                    rumble = {}
                    rumble['strong_rumble'] = 1
                    rumble['weak_rumble'] = 1
                    rumble['enable_rumble'] = bool('true')
                    cvalue['rumble'] = rumble

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

                    cvalue['left_joycon'] = left_joycon
                    right_joycon = {}
                    right_joycon['button_plus'] = "Plus"
                    right_joycon['button_r'] = "RightShoulder"
                    right_joycon['button_zr'] = "RightTrigger"
                    right_joycon['button_sl'] = "Unbound"
                    right_joycon['button_sr'] = "Unbound"
                    if controller.guid in guidstoreplace_ds4a or controller.guid in guidstoreplace_ds4b or controller.guid in guidstoreplace_ds5_wireless or controller.guid in guidstoreplace_ds5_wired or controller.guid in guidstoreplace_ds5_wired or controller.guid in guidstochangebuttons_xbox:
                        right_joycon['button_x'] = "Y"
                        right_joycon['button_b'] = "A"
                        right_joycon['button_y'] = "X"
                        right_joycon['button_a'] = "B"
                    else:
                        right_joycon['button_x'] = "X"
                        right_joycon['button_b'] = "B"
                        right_joycon['button_y'] = "Y"
                        right_joycon['button_a'] = "A"               
                    cvalue['right_joycon'] = right_joycon

                    cvalue['version'] = 1
                    cvalue['backend'] = "GamepadSDL2"
                    cvalue['id'] = controllernumber + '-' + str(convuuid)
                    cvalue['controller_type'] = "ProController"
                    cvalue['player_index'] = "Player" +  str(int(controller.player))
                    input_config.append(cvalue)
            
            data['input_config'] = input_config

        #Vulkan or OpenGl
        if system.isOptSet('ryu_backend'):
            data['graphics_backend'] = system.config["ryu_backend"]
        else:
            data['graphics_backend'] = 'Vulkan'

        data['preferred_gpu'] = ""

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

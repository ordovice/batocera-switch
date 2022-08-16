#!/usr/bin/env python

import generators
from configgen.generators.Generator import Generator
import Command as Command
import os
import stat
import json
import uuid
from os import path
import batoceraFiles as batoceraFiles
from xml.dom import minidom
import codecs
import controllersConfig as controllersConfig
import configparser
from shutil import copyfile
from utils.logger import get_logger

eslog = get_logger(__name__)

class RyujinxGenerator(Generator):

    def generate(self, system, rom, playersControllers, gameResolution):
        #handles chmod so you just need to download Ryujinx.AppImage
        st = os.stat("/userdata/system/switch/Ryujinx.AppImage")
        os.chmod("/userdata/system/switch/Ryujinx.AppImage", st.st_mode | stat.S_IEXEC)
            
        if not path.isdir(batoceraFiles.CONF + "/Ryujinx"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx")
        if not path.isdir(batoceraFiles.CONF + "/Ryujinx/system"):
            os.mkdir(batoceraFiles.CONF + "/Ryujinx/system")

        copyfile(batoceraFiles.BIOS + "/switch/prod.keys", batoceraFiles.CONF + "/Ryujinx/system/prod.keys")
        copyfile(batoceraFiles.BIOS + "/switch/title.keys", batoceraFiles.CONF + "/Ryujinx/system/title.keys")

        RyujinxConfig = batoceraFiles.CONF + '/Ryujinx/Config.json'
        RyujinxHome = batoceraFiles.CONF
        RyujinxSaves = batoceraFiles.CONF

        firstrun = True
        if path.exists(RyujinxConfig):
            firstrun = False
        #First Run - Open Ryujinx for firmware install if it's never existed before

        #Configuration update
        RyujinxGenerator.writeRyujinxConfig(RyujinxConfig, system, playersControllers)

        if firstrun:  #Run Ryujinx with no rom so users can install firmware
            if system.config['emulator'] == 'ryujinx-avalonia':
                commandArray = ["/userdata/system/switch/Ryujinx-Avalonia.AppImage"]
            else:
                commandArray = ["/userdata/system/switch/Ryujinx.AppImage"]
        else:
            if system.config['emulator'] == 'ryujinx-avalonia':
                commandArray = ["/userdata/system/switch/Ryujinx-Avalonia.AppImage" , rom]
            else:
                commandArray = ["/userdata/system/switch/Ryujinx.AppImage" , rom]
            
        return Command.Command(
            array=commandArray,
            env={"XDG_CONFIG_HOME":RyujinxHome, "XDG_CACHE_HOME":batoceraFiles.CACHE, "QT_QPA_PLATFORM":"xcb", "SDL_GAMECONTROLLERCONFIG": controllersConfig.generateSdlGameControllerConfig(playersControllers)}
            )

    def writeRyujinxConfig(RyujinxConfigFile, system, playersControllers):

        if os.path.exists(RyujinxConfigFile):
            with open(RyujinxConfigFile, "r") as read_file:
                data = json.load(read_file)
        else:
                data = {}
        if system.config['emulator'] == 'ryujinx-avalonia':
            data['version'] = 38  #Avalonia Version needs to see 38
        else:
            data['version'] = 40  #Continuous version needs at least this version
        #Graphics Backend
        data['enable_file_log'] = bool('true')
        data['backend_threading'] = 'Auto'
        data['res_scale'] = 1
        data['res_scale_custom'] = 1
        data['max_anisotropy'] = -1
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
        data['system_language'] = 'AmericanEnglish'
        data['system_region'] = 'USA'
        data['system_time_zone'] = 'UTC'
        data['system_time_offset'] = 0
        data['docked_mode'] = bool('true')
        data['enable_discord_integration'] = bool(0)
        data['check_updates_on_start'] = bool(0)
        data['show_confirm_exit'] = bool(0)
        data['hide_cursor_on_idle'] = bool('true')
        data['enable_vsync'] = bool('true')
        data['enable_shader_cache'] = bool('true')
        data['enable_texture_recompression'] = bool(0)
        data['enable_ptc'] = bool('true')
        data['enable_internet_access'] = bool(0)
        data['enable_fs_integrity_checks'] = bool('true')
        data['fs_global_access_log_mode'] = 0
        data['audio_backend'] = 'SDL2'
        data['audio_volume'] = 1
        data['memory_manager_mode'] = 'HostMappedUnsafe'
        data['expand_ram'] = bool(0)
        data['ignore_missing_services'] = bool(0)
        data['language_code'] = 'en_US'
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
        data['game_dirs'] = []
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

        input_config = []
        for index in playersControllers :
            controller = playersControllers[index]
            controllernumber = str(int(controller.player) - 1)
            myid = uuid.UUID(controller.guid)
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
            right_joycon['button_x'] = "Y"
            right_joycon['button_b'] = "A"
            right_joycon['button_y'] = "X"
            right_joycon['button_a'] = "B"
            cvalue['right_joycon'] = right_joycon

            cvalue['version'] = 1
            cvalue['backend'] = "GamepadSDL2"
            cvalue['id'] = controllernumber + '-' + str(convuuid)
            cvalue['controller_type'] = "ProController"
            cvalue['player_index'] = "Player" +  str(int(controller.player))    
            input_config.append(cvalue)
        data['input_config'] = input_config
        data['graphics_backend'] = 'Vulkan'
        data['preferred_gpu'] = ""

        with open(batoceraFiles.CONF + '/Ryujinx/BeforeRyu.json', "w") as outfile:
            outfile.write(json.dumps(data, indent=2))

        with open(RyujinxConfigFile, "w") as outfile:
            outfile.write(json.dumps(data, indent=2))
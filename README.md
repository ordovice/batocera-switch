# batocera-switch
Extends Batocera and adds switch emulation as an UNSUPPORTED ADD-ON to BATOCERA.  

Master branch is currently working on Batocera 35-37. If you have v34, please upgrade Batocera as we are no longer supporting v34.

This version of the code requires a file system for userdata that supports symlinking (EXT4, BTRFS).  

This version integrates work from foclabroc, Batocera Nation, and uureel.  It does not include the bios keys.  

Controller automapping is a constant work in progress.  You can turn off automapping, but you can help improve the project by submitting your controller configs for inclusion in the mapping files.  Not all controllers work with the modern Ryujinx.  

## GET Support Here
https://discord.gg/cuw5Xt7M7d

## EASY INSTALL
From a terminal window, run the following:
curl -L switch.batocera.pro | bash

After installing, copy your prod.keys and title.keys to /share/bios/switch.  If you wish to use Ryujinx you will also need to supply the firmware zip file.

Thanks to uureel for simplifying the install/update of Switch components for the Batocera Add-On.  

## UPGRADING OLDER VERSIONS OF THIS ADD-ON NOT INSTALLED WITH THE EASY INSTALL METHOD
Delete the \system\switch folder and install this repo as normal.  There are folders in the old install that will break this version.  

## V34 Users
The Switch Add-On is no longer being supported or maintained for v34 of Batocera

## Reporting Issues
Please use the controller issue templates for reporting controller issues.  For other issues, provide as much information as possible, and if it's a launch issue, please be sure to include the es_launch_stdout.log and es_launch_stderr.log log files from \system\logs

## SPECIAL THANKS
Special thanks for foclabroc, Rion, and Darknior for testing things out as I change things, [RGS] for a controller donation, and anyone else who contributes and helps me make this better. 

## UPDATE 2023-06-26
Controller auto configuration was finally improved with a mapping table for yuzu, and ryujinx is next up!

## UPDATE 2023-03-13
The Controller autoconfiguration is in process of being updated as more of a controller table.  Additionally, Ryujinx is still locked due to incompatibilities with the SDL within Batocera and Ryujinx  

## UPDATE 2022-09-07
Because controller auto configuration for apps that don't pull SDL directly is a challenge and I'm not actually doing any app compilation, I've added a feature to the system that allows you to turn off auto configuration.  This is useful for people with single controllers that never change (for example) so you can configure it once and just leave it.

What I've found for Ryujinx
- XBox One Controllers (or those that pretend to be them) are prioritized first and have their GUID changed to a XB1 General GUID
- DS4/DS are prioritized second and have their GUID changed.  Additionally wired/wireless matters
- Generic controllers are mapped after

## UPDATE 2022-09-05
DS4/DS5 auto configuration has been added to Ryujinx at this time.  I've also corrected a reversal of buttons that some people noticed in Ryujinx with 8bitdo controllers (because I was so focused on DS4/DS5 I had reversed them)

## UPDATE 2022-08-31
Yuzu Configuration now REMOVES the folders listed in the 2022-08-30 update if they existas non-links, so back up any save states/shaders/etc from this folder before executing this code (in theory, regular batocera-switch users should not be impacted).

It appears yuzu EA will crash the first time you use it after downloading an update.  The second time you run it should be ok.  This is an issue with zenity in the auto update image.  

## UPDATE 2022-08-30
DS4 and DS5 controller support in Yuzu is now working.  Ryujinx still has not been updated  In order to accomplish this, some folders had to change, so if you have the following folders from running yuzu manually (for example), you will need to remove them or the symlink process will not work.  You only need to do this once.  As I find GUIDs for DS4/DS5 controllers I will update the code here:
- /userdata/system/.local/share/yuzu (\share\system\.local\share\yuzu)
- /userdata/system/.config/yuzu (\share\system\.config\yuzu)
- /userdata/system/.cache/yuzu/game_list (\share\system\.cache\yuzu\game_list)

Additionally, you will need to move files from /userdata/save/yuzu/game_list (\share\saves\yuzu\game_list) into /userdata/save/yuzu (\share\saves\yuzu) as this folder is now symlinked to the path yuzu is expecting

## CONTROLLER REQUESTS
- 8bitDo SN30 Pro 2
- 8Bitdo Ultimate Bluetooth Controller with Charging Dock, Bluetooth Controller for Switch and Windows is supposed to have gyro support.  I could use one for testing at some point, or a contact who has purchased one.  I would like to create a "has_motion" class with all the GUIDS of non-Sony controllers that have Gyro's.

## TESTING REQUESTS
Controllers that are not 8bitdo SN30's, DS4, or DS5 controllers

## TO-DO
- hulk smash bugs
- update guids for xbox as reported

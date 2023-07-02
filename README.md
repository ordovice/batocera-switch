# batocera-switch
Extends Batocera and adds switch emulation as an UNSUPPORTED ADD-ON to BATOCERA.  

Master branch is currently working on Batocera 35-37. If you have v34, please upgrade Batocera as we are no longer supporting v34.

This version of the code requires a file system for userdata that supports symlinking (EXT4, BTRFS).  

This version integrates work from foclabroc, Batocera Nation, and [uureel].  It does not include the bios keys.  

Controller automapping is a constant work in progress.  Autoconfiguration of controllers is now handled via [pySDL](https://github.com/py-sdl/py-sdl2) and some python magic.

## GET Support Here
https://discord.gg/cuw5Xt7M7d

## TODO
Continue building out mapping file for Yuzu and Ryujinx
Actual Joycon support
Proper controller type selection (currently everything is forced to Pro Controller)
Confirm if Motion can just be enabled for all controllers whether they have it or not

## EASY INSTALL
From a terminal window, run the following:
curl -L switch.batocera.pro | bash

After installing, copy your prod.keys and title.keys to /share/bios/switch.  If you wish to use Ryujinx you will also need to supply the firmware zip file.

Thanks to [uureel] for simplifying the install/update of Switch components for the Batocera Add-On.  

## UPGRADING OLDER VERSIONS OF THIS ADD-ON NOT INSTALLED WITH THE EASY INSTALL METHOD
Delete the \system\switch folder and install this repo as normal.  There are folders in the old install that will break this version.  

## Reporting Issues
Please use the controller issue templates for reporting controller issues.  For other issues, provide as much information as possible, and if it's a launch issue, please be sure to include the es_launch_stdout.log and es_launch_stderr.log log files from \system\logs

## SPECIAL THANKS
Special thanks for foclabroc, Rion, and Darknior and multiple members of the [Batocera Nation Discord](https://discord.gg/cuw5Xt7M7d) for testing things especially with the migration to SDL, [RGS] for a controller donation, and anyone else who contributes and helps me make this better. 

## UPDATE 2023-06-28
Controller auto configuration has been migrated to the same versions of SDL that yuzu and ryujinx are using, utilizing the [pySDL project](https://github.com/py-sdl/py-sdl2).



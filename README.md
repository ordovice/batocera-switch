# batocera-switch
Extends Batocera and adds switch emulation

Master branch is currently working on Batocera 34 and the latest Batocera 35 beta.

This version of the code requires a file system for userdata that supports symlinking (EXT4, BTRFS).  

Copy the folders and files in this repo into the appropriate folders of Batocera.  This repo setup has all the folders you should need to add.  Add your own title.keys and prod.keys to the switch bios folder.  If you plan on using Ryujinx when it's supported, place the switch firmware in this folder as well (you will need to manually install it in Ryujinx on first start or when prompted)

You will need to provide Yuzu and Ryujinx installs.  There are update scripts that you can run via Ports to download the appropriate AppImages to the system\switch directory.  You do not need to chmod +x them before running as the configgen script takes care of this.  

This version integrates work from foclabroc and Batocera Nation but does not include the appimages or the bios keys that their download does.  Additionally, controllers in Yuzu and Ryujinx are auto mapped now as of v34, but any DS4/DS5 controllers will not work or will impact the others working.  

## V34 Users
V34 users, you need to rename the renameme_custom.sh file to custom.sh to add the options for the emulators to Batocera.  This has been changed in V35 and there will be cleanup needed if you are not upgraded currently.

## V35+ Users
V35 users (beta2 and newer), please remove/rename the custom.sh file originally provided in older versions and delete the es_features.cfg file from \system\configs\emulationstation as the switch specific addons file now works properly.

## Reporting Issues
Please use the controller issue templates for reporting controller issues.  For other issues, provide as much information as possible, and if it's a launch issue, please be sure to include the es_launch_stdout.log and es_launch_stderr.log log files from \system\logs

## SPECIAL THANKS
Special thanks for foclabroc, Rion, and Darknior for testing things out as I change things, [RGS] for a controller donation, and anyone else who contributes and helps me make this better. 

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
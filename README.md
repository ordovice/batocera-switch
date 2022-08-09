# batocera-switch
Extends Batocera and adds switch emulation

The Batocera 30 release is needed for Batocera 30, and the master branch is currently working on Batocera 34 (and has not been tested on any other versions as of August 9, 2022)

Copy the folders and files in this repo into the appropriate folders of Batocera.  This repo setup has all the folders you should need to add.  Add your own title.keys and prod.keys to the switch bios folder.  If you plan on using Ryujinx when it's supported, place the switch firmware in this folder as well (you will need to manually install it in Ryujinx)

You will need to provide Yuzu and Ryujinx installs.  There are update scripts that you can run via SSH to download the appropriate AppImages to the system\switch directory.  You need to chmod +x them before running.  

This version integrates work from foclabroc and Batocera Nation but does not include the appimages or the bios keys that their download does.  Additionally, controllers in Yuzu are auto mapped now as of v34.  

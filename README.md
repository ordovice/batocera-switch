# batocera-switch
Extends Batocera and adds switch emulation

The Batocera 30 release is needed for Batocera 30, and the master branch is currently working on Batocera 34 and the latest Batocera 35 beta

Copy the folders and files in this repo into the appropriate folders of Batocera.  This repo setup has all the folders you should need to add.  Add your own title.keys and prod.keys to the switch bios folder.  If you plan on using Ryujinx when it's supported, place the switch firmware in this folder as well (you will need to manually install it in Ryujinx on first start or when prompted)

You will need to provide Yuzu and Ryujinx installs.  There are update scripts that you can run via Ports to download the appropriate AppImages to the system\switch directory.  You do not need to chmod +x them before running as the configgen script takes care of this.  

This version integrates work from foclabroc and Batocera Nation but does not include the appimages or the bios keys that their download does.  Additionally, controllers in Yuzu and Ryujinx are auto mapped now as of v34, but any DS4/DS5 controllers will not work or will impact the others working.  

A special note about DS4 and DS5 controllers: They are not supported properly inside yuzu's Linux environment for autoconfiguration at this time.  This appears to be a concern with both Yuzu and Ryujinx.  Yuzu doesn't map certain buttons correctly and Ryujinx changes the auto order based on these controllers.  I have questions in to both development teams, but they will remain unsupported and will be assumed to break your running configuration if connected. 

PLEASE DELETE THE FOLLOWING FILES FROM /system/configs/emulationstation
- es_features_os.cfg
This is in preparation for improvements coming down the road for batocera to include natural expansion of the es_features functionality.  I have renamed the add-on file and temp file to add_feat_os and add_feat_switch.  The es_features_switch is already set for the future now.  When that happens, you will not need to copy the custom.sh file anymore.  

Special thanks for foclabroc for testing and [RGS] for controller support. 
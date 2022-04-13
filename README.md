# batocera-switch
Extends Batocera and adds switch emulation

The Batocera 30 release is needed for Batocera 30, and the master branch is currently working on Batocera 33

Copy the folders and files in this repo into the appropriate folders of Batocera.  You will need to create a folder under the bios folder called 'switch' and put the prod.keys and title.keys under.  

Provide Yuzu and Ryujinx installs from official Yuzu/Ryujinx sites.  There are update scripts that you can run via SSH to download the files to the directory.  You need to chmod +x them before running.  

This version integrates work from foclabroc and Batocera Nation but does not include the appimages or the bios keys that their download does.  Additionally, controllers in Yuzu are auto mapped now.  

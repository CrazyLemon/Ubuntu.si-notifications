##### Author: Drazen M. <drazen@ubuntu.si>

For this script to work you should receive 3 files in archive. Well 4 if i'm counting this README.
The script has been tested on Ubuntu 12.04 LTS and on 12.10.

## Python script
First one is 'obvestila.py'. This is a python script containing probably the most important part.
Script handles and shows latest posts via OSD notifications on Ubuntu.si.

## BASH script
The second one is 'UbuntuSiObvestila.sh'. This is a BASH script. This script checks for
directories and creates them if they do not exist. Script also moves 'obvestila.py' and
'ubuntusi.png' file to a newly created directory.
After that it creates a .desktop file for autostart purposes. With .desktop file
the python script gets started automatically on user login.

### Icon
The least important part is Ubuntu.si icon. This icon takes care that notification looks nice and funky.

## What to do
Launch your Terminal. Move to location where you either have .zip file or you have unpacked the archive.
If you haven't unpacked the files yet, run

	 `unzip *.zip`

now that we all have unpacked content we should start our bash script.

	`chmod +x UbuntuSiObvestila.sh`
	`./UbuntuSiObvestila.sh`

And thats its.. ICON and Python script are no longer in that directory - they were moved into a newly created directory which you can enter with

	`cd ~/.UbuntuSi/`

Now you can delete UbuntuSiObvestila.sh if you don't need it anymore.

### Disabling autostart
In Ubuntu, you should open Startup applications (Začetni programi in slovenian) and disable by unchecking or by removing the correct entry and deleting ~/.UbuntuSi directory.

### Modifications
Currently 'obvestila.py' will check every 7200 seconds if there are new articles on Ubuntu.si. If you wish to modify that, open 'obvestila.py' with gedit or your favorite text editor and change 7200 in timer.setInterval(7200) to your favorite refresh speed, save and exit.
DO NOT set it to check posts every 60 seconds or less - the server might start rejecting your requests.

### Help / bugs
Join us at <www.ubuntu.si/forum> for help and/or bug reports.

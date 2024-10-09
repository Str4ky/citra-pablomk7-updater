# Citra PabloMK7 Fork Updater
Lets you update the Citra fork of PabloMK7

## Installation:
Download `cput.exe` and put it in a folder where it's in the PATH (for example `C:\Windows`)

## Usage:
To use it you need to use Windows's command prompt<br><br>
To set Citra's folder<br>
`cput set <citra folder>`<br>
`C:\Users\<user>\AppData\Local\Citra\nightly/canary` is Citra's default path so set the folder where `citra-qt.exe` is inside<br><br>
To create a shortcut in the start menu to the script's verify function<br>
`cput shortcut desktop/startmenu`<br>
To update Citra<br>
`cput update`
To either launch Citra or update it if it's not up to date<br>
`cput verify`

## ATTENTION!!!
### DO NOT SET THE FOLDER `C:\Users\<user>\AppData\Roaming\Citra` (or any folder with datas you don't want to lose) OR YOU WILL LOSE ANY DATAS AFTER UPDATING
Theoretically you cannot as I made it so the program checks if it's a valid Citra folder but don't try to nypass this to put a folder that can erase datas

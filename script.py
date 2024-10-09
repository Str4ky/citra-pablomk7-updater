from pathlib import Path
from PIL import Image
import requests
import zipfile
import shutil
import json
import sys
import os


def update():
    #Get the version value from the JSON file
    date = release_info['published_at'][:10]
    date = date.replace("-", "")
    #Set the download url to what we got from the JSON
    file = "https://github.com/PabloMK7/citra/releases/download/r" + name + "/citra-windows-msvc-" + date + "-" + name + ".zip"
    print(f"Updating Citra to r{name}...\n")
    #Download the file
    os.system(f"curl -L -o citra.zip {file}")
    #Remove Citra's previous version
    shutil.rmtree(citra_dir, ignore_errors=True)
    #Extract Citra's newest version
    with zipfile.ZipFile("citra.zip", 'r') as zip_ref:
        zip_ref.extractall(parent_dir)
    os.rename(parent_dir / f"citra-windows-msvc-{date}-{name}", citra_dir)
    #Clean up the downloaded zip
    os.remove("citra.zip")
    print(f"\nCitra has been updated to r{name}!")


#Reset the variable if no argument hasn't been set
if len(sys.argv) > 1:
    argument = sys.argv[1]
else:
    argument = ""

#Set the directory to the user's directory
user_dir = str(Path.home())

#Set the JSON path
json_path = f"{user_dir}/cput.json"

#Create the JSON file if it doesn't exist
if not os.path.exists(json_path):
    with open(json_path, "w") as json_file:
        data = {}
        json.dump(data, json_file)

# Set a variable in a JSON file based on the folder passed by the user
if argument == "set":
    # If there's a second argument
    if len(sys.argv) > 2:
        folder = sys.argv[2]
        # If the folder exists and citra-qt.exe is in it
        if Path(folder + "/citra-qt.exe").exists():
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
            data["path"] = f"{folder}"
            with open(json_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print("Citra folder has been set")
            sys.exit(0)
        else:
            print("The folder you provided isn't one where Citra is installed")
            sys.exit(1)
    else:
        print("You did not provide a folder")
        print("\nUse: cput set <citra_folder>")
        sys.exit(1)
#Create a shortcut to the verify action on the start menu
elif argument == "shortcut":
        if getattr(sys, 'frozen', False):
            exe_file = sys.executable
            #Set shortcut attributes
            start_menu_path = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Citra (PabloMK7 fork).lnk'
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
                if "path" in data:
                    if  data["path"] == "":
                        print("Citra folder is not set not set")
                        print("\nUse: cput set <citra_folder>")
                        sys.exit(1)
                    elif data["path"] != "":
                        #Create the icon
                        image = Image.open(Path(data["path"]) / "dist/citra.png")
                        image = image.convert('RGBA')
                        image.save(user_dir + "/citra.ico", format='ICO', sizes=[(64, 64), (128, 128), (256, 256)])
                        icon_path = user_dir + "/citra.ico"
                        #Create the shortcut
                        os.system(f"powershell.exe -Command \"$s=(New-Object -COM WScript.Shell).CreateShortcut('{start_menu_path}');$s.TargetPath='{exe_file}';$s.Arguments='verify';$s.IconLocation='{icon_path}';$s.Save()\"")
                        print("Shortcut has been created")
                        sys.exit(0)
                else:
                    print("Citra folder is not set not set")
                    print("\nUse: cput set <citra_folder>")
                    sys.exit(1)
                json_file.close()
#Update Citra to it's latest version
elif argument == "update":
    with open(json_path, "r") as json_file:
        #Load the JSON file
        data = json.load(json_file)
        #If the path value is empty
        if "path" in data:
            if  data["path"] == "":
                print("Citra folder is not set not set")
                print("\nUse: cput set <citra_folder>")
                sys.exit(1)
        else:
            print("Citra folder is not set not set")
            print("\nUse: cput set <citra_folder>")
            sys.exit(1)
        #Get Citra's folder and it's parent
        citra_dir = Path(data["path"])
        parent_dir = Path(citra_dir).parent
        #URL to the PabloMK7 citra fork's repo from Github's api
        url = "https://api.github.com/repos/PabloMK7/citra/releases/latest"
        #Parse the returnd JSON
        response = requests.get(url)
        if response.status_code == 200:
            #Get the infos from the JSON
            release_info = json.loads(response.text)
            name = release_info['name'][1:]
            #Put the version in the JSON file
            data["version"] = f"{name}"
            with open(json_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            #Update Citra
            update()
        json_file.close()
        sys.exit(0)
elif argument == "verify":
    #read the version value from the json file
    with open(json_path, "r") as json_file:
        #Load the JSON file
        data = json.load(json_file)
        #If the path value is empty
        if "path" in data:
            if  data["path"] == "":
                print("Citra folder is not set not set")
                print("\nUse: cput set <citra_folder>")
                sys.exit(1)
        else:
            print("Citra folder is not set not set")
            print("\nUse: cput set <citra_folder>")
            sys.exit(1)
        citra_dir = Path(data["path"])
        parent_dir = Path(citra_dir).parent
        citra_ver = data["version"]
        json_file.close()
        #Check for updates
        print(f"Checking for updates...\n")
        url = "https://api.github.com/repos/PabloMK7/citra/releases/latest"
        #Parse the returnd JSON
        response = requests.get(url)
        if response.status_code == 200:
            #Get the infos from the JSON
            release_info = json.loads(response.text)
            name = release_info['name'][1:]
            #If the version value is different from the latest version
            if citra_ver != name and citra_ver != "":
                #Put the version in the JSON file
                with open(json_path, "r") as json_file:
                    data = json.load(json_file)
                    data["version"] = f"{name}"
                    with open(json_path, "w") as json_file:
                        json.dump(data, json_file, indent=4)
                    json_file.close()
                #Update Citra
                update()
                #Run Citra's executable
                print("\nLaunching Citra...\n")
                os.system(f"start {citra_dir}/citra-qt.exe")
                sys.exit(0)
            elif citra_ver == name or citra_ver == "":
                #Run Citra's executable
                print("Launching Citra...\n")
                os.system(f"start {citra_dir}/citra-qt.exe")
                sys.exit(0) 
else:
    #Show help
    print("Citra MK7's fork updater")
    print("\ncput set <citra_folder>              Set Citra folder")
    print("cput shortcut                        Create a shortcut to the verify function in the start menu")
    print("cput update                          Update Citra to it's latest version")
    print("cput verify                          Verify if Citra is up to date and run it")
    sys.exit(1)
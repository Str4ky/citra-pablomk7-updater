from pathlib import Path
import requests
import zipfile
import shutil
import json
import sys
import os

#Reset the variable if no argument hasn't been set
if len(sys.argv) > 1:
    argument = sys.argv[1]
else:
    argument = ""

#Set the directory to the user's directory
user_dir = str(Path.home())

#Set an environment variable based on the folder passed by the user
if argument == "set":
    #If there's a second argument
    if len(sys.argv) > 2:
        folder = sys.argv[2]
        #If the folder exists and citra-qt.exe is in it
        if Path(folder + "/citra-qt.exe").exists():
            data = {
                "path": folder
            }
            with open(f"{user_dir}/cput.json", "w") as json_file:
                json.dump(data, json_file)
                json_file.close()
            print(f"Citra folder has been set")
            sys.exit(0)
        else:
            print("The folder you provided isn't one where Citra is installed")
            sys.exit(1)
    else:
        print("You did not provide a folder")
        print("\nUse: cput set <citra_folder>")
        sys.exit(1)
#Update Citra to it's latest version
elif argument == "update":
    #If the json file exist
    if Path(f"{user_dir}/cput.json").exists():
        #If the content of the path value of the json is empty
        with open("cput.json", "r") as json_file:
            content = json.load(json_file)
            json_file.close()
            if content["path"] == "":
                print("Citra folder is not set not set")
                print("\nUse: cput set <citra_folder>")
                sys.exit(1)
    else:
        print("Citra folder is not set not set")
        print("\nUse: cput set <citra_folder>")
        sys.exit(1)
    #Get Citra's folder and it's parent
    citra_dir = Path(content["path"])
    parent_dir = Path(citra_dir).parent
    #URL to the PabloMK7 citra fork's repo from Github's api
    url = "https://api.github.com/repos/PabloMK7/citra/releases/latest"
    #Parse the returnd JSON
    response = requests.get(url)
    if response.status_code == 200:
        #Get the infos from the JSON
        release_info = json.loads(response.text)
        name = release_info['name'][1:]
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
else:
    #Show help
    print("Citra MK7's fork updater")
    print("\ncput set <citra_folder>              Set Citra folder")
    print("cput update                          Update Citra to it's latest version")
    sys.exit(1)
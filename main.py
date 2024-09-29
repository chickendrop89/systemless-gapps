import os
import sys
import json
import shutil
import zipfile
import tarfile
import time
import fnmatch

from termcolor import cprint

# Resize window to fit banner
sys.stdout.write("\x1b[8;35;110t")

BANNER = r"""
       _____           _                 _                  _____                          
      / ____|         | |               | |                / ____|   /\                    
     | (___  _   _ ___| |_ ___ _ __ ___ | | ___  ___ ___  | |  __   /  \   _ __  _ __  ___ 
      \___ \| | | / __| __/ _ \ '_ ` _ \| |/ _ \/ __/ __| | | |_ | / /\ \ | '_ \| '_ \/ __|
      ____) | |_| \__ \ ||  __/ | | | | | |  __/\__ \__ \ | |__| |/ ____ \| |_) | |_) \__ \
     |_____/ \__, |___/\__\___|_| |_| |_|_|\___||___/___/  \_____/_/    \_\ .__/| .__/|___/
              __/ |                                                       | |   | |        
             |___/                                                        |_|   |_|        

    * Systemless GApps by @chickendrop89, @Wacko1805       
    * NOTE: Make sure to edit preferences.json                        
    * USAGE: python3 main.py <input: nikgapps package> <output directory>            
"""


def printbanner():
    """Prints Systemless GApps banner"""
    cprint(BANNER, "black", "on_green", attrs=["bold"])


# I/O Parameters
if len(sys.argv) != 3:
    printbanner()
    sys.exit(1)
else:
    inputFilename = os.path.abspath(sys.argv[1])
    outputDirectory = os.path.abspath(sys.argv[2])


def cleanenvironment():
    """Cleans environment of build-related folders"""
    cprint("Cleaning environment", "black", "on_green", attrs=["bold"])

    try:
        # Sets correct permissions for deletion
        os.chmod("gapps", 0o777)
        os.chmod("builds", 0o777)
        os.chmod("appset", 0o777)

        # Deletes build-related folders and files
        shutil.rmtree("gapps", ignore_errors=True)
        shutil.rmtree("builds", ignore_errors=True)
        shutil.rmtree("appset", ignore_errors=True)

        os.remove("template/module.prop")
    except OSError:
        pass


with open("preferences.json", encoding="utf-8") as preferences:
    contents = json.load(preferences)

    # Module properties
    moduleId = contents["magisk"]["id"]
    moduleName = contents["magisk"]["name"]
    moduleVersion = contents["magisk"]["version"]
    moduleVersionCode = contents["magisk"]["versionCode"]
    moduleAuthor = contents["magisk"]["author"]
    moduleDescription = contents["magisk"]["description"]


def createmoduleprop():
    """Creates module.prop from strings included in preferences.json"""
    with open("template/module.prop", "w", encoding="utf-8") as module:
        module.write(
            "id="
            + moduleId
            + "\n"
            + "name="
            + moduleName
            + "\n"
            + "version="
            + moduleVersion
            + "\n"
            + "versionCode="
            + moduleVersionCode
            + "\n"
            + "author="
            + moduleAuthor
            + "\n"
            + "description="
            + moduleDescription
        )


def extractgapps():
    """Extracts specified NikGApps package"""
    if os.path.exists(inputFilename):
        with zipfile.ZipFile(os.path.join(".", inputFilename), "r") as zip_ref:
            zip_ref.extractall("gapps")
    else:
        cprint(f"{inputFilename} is not present in parent directory", "white", "on_red", attrs=["bold"])
        sys.exit(1)

    # Define the appsetPath variable to point to the 'appset' directory
    appsetpath = os.path.join(".", "appset")

    # Check if the 'appset' directory exists before proceeding
    if not os.path.exists(appsetpath):
        os.makedirs(appsetpath)

    rootpath = os.path.join("gapps", "AppSet")

    for root, __dest, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, "*.zip"):
            cprint(f"Extracting {os.path.join(root, filename)}", "black", "on_magenta", attrs=["bold"])
            zipfile.ZipFile(os.path.join(root, filename)).extractall(appsetpath)

        for filename in fnmatch.filter(files, "*.tar.xz"):
            cprint(f"Extracting {os.path.join(root, filename)}", "black", "on_magenta", attrs=["bold"])
            with tarfile.open(os.path.join(root, filename), "r:xz") as tar:
                for member in tar:
                    member.mtime = time.time()  # Set mtime to current time
                    tar.extract(member, path=appsetpath, filter="tar")

    os.remove("appset/installer.sh")
    os.remove("appset/uninstaller.sh")

    # Renames Files from ___ to /
    for filename in os.listdir(appsetpath):
        src_file = os.path.join(appsetpath, filename)
        dst_file = os.path.join(appsetpath, filename.replace("___", os.sep).lstrip(os.sep))

        # Check if the destination directory exists, if not create it
        dst_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        if os.path.exists(dst_file):
            if os.path.isdir(dst_file):
                shutil.rmtree(dst_file)
            else:
                os.remove(dst_file)

        shutil.move(src_file, dst_file)


def copytemplate():
    """Copies the MMT template to builds folder"""
    source_folder = "template"
    destination_folder = "builds"

    cprint("Combining Template", "black", "on_green", attrs=["bold"])
    shutil.copytree(source_folder, destination_folder)


def combinegapps():
    """Combines NikGApps with the MMT template"""
    source_folder = "appset"
    destination_folder = "builds/system"

    cprint("Building Module", "black", "on_green", attrs=["bold"])
    shutil.copytree(source_folder, destination_folder)


def createarchive():
    """Creates Systemless GApps archive"""
    splitinputfilename = os.path.split(inputFilename)[1]

    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    archivepath = f"{outputDirectory}/SyG - {splitinputfilename} - {moduleVersion}"
    archivepath = archivepath.replace(".zip", "")

    # Delete existing archive if exists
    if os.path.exists(archivepath):
        os.remove(archivepath)

    cprint("Building SystemlessGApps ZIP archive", "black", "on_green", attrs=["bold"])
    shutil.make_archive(archivepath, "zip", "builds")

    # Print absolute archive path
    cprint(os.path.abspath(f"{archivepath}.zip"), "black", "on_green", attrs=["bold"])


if __name__ == "__main__":
    printbanner()

    cleanenvironment()

    # Creates module.prop from strings included in preferences.json
    createmoduleprop()

    # Extracts specified NikGApps package
    extractgapps()

    # Copies the MMT template to builds folder
    copytemplate()

    # Combines NikGApps with the MMT template
    combinegapps()

    # Creates SystemlessGApps archive
    createarchive()

    cleanenvironment()

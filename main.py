#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

#  Copyright (C) 2024  chickendrop89

import os
import sys
import shutil
import tarfile
import re
import time
import fnmatch
import fileinput

from zipfile import ZipFile
from termcolor import cprint
from pyaxmlparser import APK

# Include a list of AOSP package folders to replace
from __packages__ import getPackageReplacement

# Global variables. These will be overwritten later in the code
MODULE_VERSION       = None
MODULE_VERSION_CODE  = None
ARCHIVE_NAME         = None

# Resize window to prefectly fit the banner
sys.stdout.write("\x1b[8;35;96t")

BANNER = r"""
       _____           _                 _                  _____                          
      / ____|         | |               | |                / ____|   /\                    
     | (___  _   _ ___| |_ ___ _ __ ___ | | ___  ___ ___  | |  __   /  \   _ __  _ __  ___ 
      \___ \| | | / __| __/ _ \ '_ ` _ \| |/ _ \/ __/ __| | | |_ | / /\ \ | '_ \| '_ \/ __|
      ____) | |_| \__ \ ||  __/ | | | | | |  __/\__ \__ \ | |__| |/ ____ \| |_) | |_) \__ \
     |_____/ \__, |___/\__\___|_| |_| |_|_|\___||___/___/  \_____/_/    \_\ .__/| .__/|___/
              __/ |                                                       | |   | |        
             |___/                                                        |_|   |_|        

    * Systemless GApps by @chickendrop89              
    * USAGE: python3 main.py <input: nikgapps package> <output directory>            
"""

template_path = os.path.join(".", "template")
appset_path   = os.path.join(".", ".appset")
gapps_path    = os.path.join(".", ".gapps")
builds_path   = os.path.join(".", ".builds")

internal_directory_list = [appset_path, gapps_path, builds_path]

def __printBanner():
    """Prints the 'Systemless GApps' banner"""
    __coloredPrint("info", BANNER)

def __coloredPrint(message_type: str, message: str):
    """Prints colored output for desired type"""
    match message_type:
        case "info":
            cprint(message, "black", "on_green", attrs=["bold"])
        case "info-dirs":
            cprint(message, "black", "on_magenta", attrs=["bold"])
        case "error":
            cprint(message, "white", "on_red", attrs=["bold"])
            sys.exit(1)

try:
    # I/O Parameters
    input_filename   = os.path.abspath(sys.argv[1])
    output_directory = os.path.abspath(sys.argv[2])

    if not os.path.exists(input_filename):
        raise IndexError

# Handle IndexError as a sign that no/invalid parameters were passed
except IndexError:
    __printBanner()
    sys.exit(1)

def cleanEnvironment():
    """Cleans environment of build-related folders"""
    __coloredPrint("info", "Cleaning environment")

    for directory in internal_directory_list:
        if os.path.exists(directory):
            shutil.rmtree(directory)

def prepareEnvironment():
    """First removes, and later creates build related folders"""
    cleanEnvironment()

    for directory in internal_directory_list:
        os.mkdir(directory)

def extractGapps():
    """Extracts specified NikGApps package into the .appset/ folder"""

    with ZipFile(input_filename, "r") as zip_ref:
        zip_ref.extractall(gapps_path)

    # Fetch zip_name.txt (included in every nikgapps package)
    with open(f"{gapps_path}/zip_name.txt", "r", encoding="utf-8") as data:
        contents = data.read()

        version_regex    = re.search(r"(\d{2}-\d{8})", contents).group(1)
        after_first_dash = contents[contents.find("-") + 1:]

        global MODULE_VERSION
        global MODULE_VERSION_CODE
        global ARCHIVE_NAME

        MODULE_VERSION      = f"{version_regex}"
        # Magisk doesn't tolerate dashes
        MODULE_VERSION_CODE = f"{version_regex.replace("-", "")}"
        ARCHIVE_NAME        = f"systemless-gapps-{after_first_dash}"

        # Strip "-signed" from the archive name to reduce length
        if ARCHIVE_NAME.endswith("-signed"):
            ARCHIVE_NAME = ARCHIVE_NAME[:-7]

    for dirpath, __subdirs, files in os.walk(f"{gapps_path}/AppSet"):
        # Some subpackages are compressed in zip, and some in tar.xz

        for filename in fnmatch.filter(files, "*.zip"):
            subpackage_path = os.path.join(dirpath, filename)
            printable_path  = os.path.relpath(subpackage_path)

            __coloredPrint("info-dirs", f"Extracting {printable_path}")

            with ZipFile(subpackage_path) as zip_file:
                zip_file.extractall(appset_path)

        for filename in fnmatch.filter(files, "*.tar.xz"):
            subpackage_path = os.path.join(dirpath, filename)
            printable_path  = os.path.relpath(subpackage_path)

            __coloredPrint("info-dirs", f"Extracting {printable_path}")

            with tarfile.open(subpackage_path, "r:xz") as tar_file:
                # We need to do this, because when are making the final archive,
                # ZIP complains about not supporting timestamps before 1980.
                for member in tar_file:
                    # Set subpackage create time to current time to walk around it
                    member.mtime = time.time()
                    tar_file.extract(member, path=appset_path, filter="tar")

    os.remove(f"{appset_path}/installer.sh")
    os.remove(f"{appset_path}/uninstaller.sh")

def resolveGappsDirectories():
    """Translates subpackage dirnames to normal directories"""

    def __preventDuplicateSystem():
        """
            Pixel DPS sub-package (DevicePersonalizationServices.{zip, tar.gz})
            creates duplicate system directory (/system/system)
            Fix it, and prevent it from happening for other sub-packages as well
        """
        system_path = os.path.join(appset_path, "system")

        for __dirpath, subdirs, __files in os.walk(system_path):
            # System subdirectory path (ex: "appset/system/etc")
            subdirectory = os.path.join(system_path, *subdirs)

            # Parent directory name of the sub-subdirectory (ex: "etc")
            sub_subdirectory_parent = subdirectory.split("/")[-1]

            # Sub-subdirectory name (ex: "textclassifier")
            sub_subdirectory = os.listdir(subdirectory)[0]

            shutil.move(
                f"{subdirectory}/{sub_subdirectory}",
                f"{appset_path}/{sub_subdirectory_parent}/{sub_subdirectory}"
            )
            shutil.rmtree(system_path)

    for filename in os.listdir(appset_path):
        src_file = os.path.join(appset_path, filename)

        def replaceUnderscoresWith(replace_with: str):
            return src_file.replace("___", replace_with)

        dst_file = replaceUnderscoresWith(os.sep)

        # Short workarund:
        # /system/overlay is rejected by magisk, use /product/overlay instead
        if "overlay" in filename:
            shutil.move(src_file, replaceUnderscoresWith("product/"))
        else:
            shutil.move(src_file, dst_file)

            if "system" in filename:
                __preventDuplicateSystem()

def moveFoldersToModulePath():
    """Moves the extracted subpackages and the template to the builds directory"""
    __coloredPrint("info", "Building Module")

    shutil.copytree(template_path, builds_path, dirs_exist_ok=True)
    shutil.move(appset_path, f"{builds_path}/system")
    
def replaceAospApps():
    """Replaces AOSP apps with GApps"""
    aosp_replacer_script="extra/aosp_replace_util.sh"

    def __replaceLine(old_line, new_line):
        with fileinput.input(f"{builds_path}/{aosp_replacer_script}", inplace=True) as file:
            for line in file:
                if line.startswith(old_line):
                    print(new_line, end="")
                else:
                    print(line, end="")

    combined_arrays = []

    for dirpath, __subdirs, files in os.walk(f"{builds_path}/system"):
        for file in files:
            if file.endswith(".apk"):
                apk_path = os.path.join(dirpath, file)
                package_name = APK(apk_path).package
                combined_arrays.extend(getPackageReplacement(package_name))

    __replaceLine("packages=()", f"packages=({' '.join(combined_arrays)})")

def modifyModuleProps():
    """Modifies the version and versionCode to NikGApps version"""
    with open(f"{builds_path}/module.prop", "r+", encoding="utf-8") as properties:
        contents = properties.read()

        updated_version = re.sub(
            r"version=.*",
            f"version={MODULE_VERSION}",
            contents
        )
        updated_version = re.sub(
            r"versionCode=.*", 
            f"versionCode={MODULE_VERSION_CODE}",
            updated_version
        )

        properties.seek(0)
        properties.write(updated_version)

def createArchive():
    """Creates final systemless-gapps archive"""
    archive_path = os.path.join(output_directory, ARCHIVE_NAME)
    archive_path = os.path.abspath(archive_path)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    __coloredPrint("info", "Creating final systemless-gapps archive")
    shutil.make_archive(archive_path, "zip", builds_path)

    # Print absolute path of the archive
    __coloredPrint("info", f"{archive_path}.zip")

if __name__ == "__main__":
    __printBanner()
    __coloredPrint("info-dirs", input_filename)
    prepareEnvironment()

    # GApps
    extractGapps()
    resolveGappsDirectories()

    # Module
    moveFoldersToModulePath()
    replaceAospApps()
    modifyModuleProps()
    createArchive()

    cleanEnvironment()

"""Workarounds for systemless-gapps"""

import os
import shutil

from termcolor import cprint

def __coloredWorkaroundPrint(message: str):
    """Colored workaround print"""
    cprint(f"Workaround: {message}", "black", "on_green", attrs=["bold"])

def replaceAospApp(app_path: str, appset_path: str):
    """
        Some Google Apps don't work due to the roles already being occupied by
        their AOSP relatives (ex. DocumentsUI), and require "replacing"
    """
    aosp_app_path = os.path.join(appset_path, app_path)
    os.makedirs(aosp_app_path)

    # pylint: disable=unspecified-encoding
    with open(os.path.join(aosp_app_path, ".replace"), "w") as __blank:
        pass

def preventDuplicateSystem(appset_path: str):
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

    # Notify that the workaround was used
    __coloredWorkaroundPrint("prevent duplicate system")

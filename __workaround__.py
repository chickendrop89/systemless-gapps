"""Workarounds for systemless-gapps"""

import os
import shutil

from termcolor import cprint

def __coloredWorkaroundPrint(message: str):
    """Colored workaround print"""
    cprint(f"Workaround: {message}", "black", "on_green", attrs=["bold"])

def replaceAospDocumentsUI(appsetpath: str):
    """
        Google DocumentsUI package doesn't work if the AOSP variant is still installed
        Replace it.
    """

    documentsui_path = os.path.join(appsetpath, "___priv-app___DocumentsUI")
    os.makedirs(documentsui_path)

    # pylint: disable=unspecified-encoding
    with open(os.path.join(documentsui_path, ".replace"), "w") as __blank:
        pass

    # Notify that the workaround was used
    __coloredWorkaroundPrint("replace AOSP DocumentsUI")

def preventDuplicateSystem(appsetpath: str):
    """
        Pixel DPS sub-package (DevicePersonalizationServices.{zip, tar.gz})
        creates duplicate system directory (/system/system)
        Fix it, and prevent it from happening for other sub-packages as well
    """
    system_path = os.path.join(appsetpath, "system")

    for __dirpath, subdirs, __files in os.walk(system_path):
        # System subdirectory path (ex: "appset/system/etc")
        subdirectory = os.path.join(system_path, *subdirs)

        # Parent directory name of the sub-subdirectory (ex: "etc")
        sub_subdirectory_parent = subdirectory.split("/")[-1]

        # Sub-subdirectory name (ex: "textclassifier")
        sub_subdirectory = os.listdir(subdirectory)[0]

        shutil.move(
            f"{subdirectory}/{sub_subdirectory}",
            f"{appsetpath}/{sub_subdirectory_parent}/{sub_subdirectory}"
        )
        shutil.rmtree(system_path)

    # Notify that the workaround was used
    __coloredWorkaroundPrint("prevent duplicate system")

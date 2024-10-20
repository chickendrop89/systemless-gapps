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

"""Workarounds for systemless-gapps"""

import os
import shutil

from termcolor import cprint

def __coloredWorkaroundPrint(message: str):
    """Colored workaround print"""
    cprint(f"Workaround: {message}", "black", "on_green", attrs=["bold"])

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

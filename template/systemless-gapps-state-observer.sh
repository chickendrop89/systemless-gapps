#!/system/bin/sh

# When the module is disabled, GMS will be left installed on the device as user app.
# Observe the "disable" file in the module root path and act accordingly.

# Under normal conditions, outputs /data/adb
MAGISK_ADB_PATH=$(dirname "${0%/*}")
MODULE_PATH=$MAGISK_ADB_PATH/modules/systemless-gapps

# If the module path doesn't exist anymore, self-destruct.
if [ ! -d "$MODULE_PATH" ];
    then
        rm -- "$0"
        exit 0
fi

if [ -f "$MODULE_PATH/disable" ];
    then
        pm disable com.google.android.gms
    else
        pm enable com.google.android.gms
fi

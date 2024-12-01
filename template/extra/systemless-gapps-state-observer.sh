#!/system/bin/sh

# When the module is disabled, GMS will be left installed on the device as user app.
# Observe the "disable" file in the module root path and act accordingly.

# Under normal conditions, outputs /data/adb
MAGISK_ADB_PATH=$(dirname "${0%/*}")
MODULE_PATH=$MAGISK_ADB_PATH/modules/systemless-gapps

# Wait until system boot is completed
resetprop -w sys.boot_completed 0

# Check if module path doesn't exist
if [ ! -d "$MODULE_PATH" ];
    then
        # If GMS isn't installed as system app, uninstall it
        if ! pm list packages -s -a | grep "com.google.android.gms" > /dev/null 2>&1; 
            then
                pm uninstall com.google.android.gms >/dev/null 2>&1
        fi

        # Self-destruct this script, and exit
        rm -- "$0"
        exit 0
fi

# Disable GMS only if aren't overlapping existing *not system-less* package
if [ -f "$MODULE_PATH/disable" ] && [ ! -f "/data/adb/.system_gapps_installation" ];
    then
        pm disable com.google.android.gms >/dev/null 2>&1
    else
        pm enable com.google.android.gms >/dev/null 2>&1
fi

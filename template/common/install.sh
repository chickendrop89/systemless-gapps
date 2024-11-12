#!/system/bin/sh

SETUP_WIZARD_INTENT="com.google.android.setupwizard"
SETUP_WIZARD_INTENT="$SETUP_WIZARD_INTENT/$SETUP_WIZARD_INTENT.SetupWizardActivity"
EXTRA_DIR="$MODPATH/extra"

wipe_cache(){
    rm -rf /data/system/package_cache/*
    rm -rf /data/dalvik-cache/*
}

replace_aosp_apps(){
    if [ -f /system/bin/bash ]; 
        then
            bash_path="/system/bin/bash"
    elif [ -f /system_ext/bin/bash ];
        then
            # Optional/extra android partition
            bash_path="/system_ext/bin/bash"
    elif [ -f /data/data/com.termux/files/usr/bin/bash ];
        then
            # Last resort. Might work if Termux is installed
            bash_path="/data/data/com.termux/files/usr/bin/bash"
    else
        ui_print "! No bash installation detected *anywhere*"
        abort "! Please instal the 'mkshrc' magisk module, aborting"
    fi

    # This script can't be rewritten to support (d)ash/posix-sh
    # While keeping it still readable. Try searching for a bash installation instead.
    $bash_path "$EXTRA_DIR/aosp_replace_util.sh"
}

trigger_setup_wizard(){
    pm enable --user 0 "$SETUP_WIZARD_INTENT" >/dev/null 2>&1
    settings put secure user_setup_complete 0 >/dev/null 2>&1
    settings put global device_provisioned 0 >/dev/null 2>&1
}

state_observer_script(){
    cp "$EXTRA_DIR/systemless-gapps-state-observer.sh" "/data/adb/service.d" >/dev/null 2>&1
}

if [ ! -f "$MODPATH/.DONT_REPLACE" ]; 
    then
        ui_print "- Replacing AOSP apps with their Google counterparts"
        replace_aosp_apps
    else
        ui_print "- Not replacing AOSP apps, as requested during creation"
fi

ui_print "- Wiping cache to prevent undefined behaviour"
wipe_cache

state_observer_script

if [ ! -d "${MODPATH//_update/}" ] || [ -f "$MODPATH/.FORCE_SW" ]; 
    then
        ui_print "- Setup wizard will be triggered on next boot"
        ui_print "- Rebooting is recommended after the installation completes"
        trigger_setup_wizard
    else
        ui_print "- Existing installation detected, not triggering setup wizard"
fi

#!/system/bin/sh

SETUP_WIZARD_INTENT="com.google.android.setupwizard"
SETUP_WIZARD_INTENT="$SETUP_WIZARD_INTENT/$SETUP_WIZARD_INTENT.SetupWizardActivity"
EXTRA_DIR="$MODPATH/extra"

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

detect_overlap(){
    $bash_path "$EXTRA_DIR/overlap_detect_util.sh"

    if [ -f "/data/adb/.system_gapps_installation" ];
        then ui_print "- Detected foreign GApps installation, not doing a cleanup on removal"
    fi
}

replace_aosp_apps(){
    $bash_path "$EXTRA_DIR/aosp_replace_util.sh"
}

wipe_cache(){
    rm -rf /data/system/package_cache/*
    rm -rf /data/dalvik-cache/*
}

trigger_setup_wizard(){
    pm enable --user 0 "$SETUP_WIZARD_INTENT" >/dev/null 2>&1
    settings put secure user_setup_complete 0 >/dev/null 2>&1
    settings put global device_provisioned 0 >/dev/null 2>&1
}

state_observer_script(){
    mv "$EXTRA_DIR/systemless-gapps-state-observer.sh" "/data/adb/service.d" >/dev/null 2>&1
}

if [ ! -d "${MODPATH//_update/}" ] && [ ! -f "/data/adb/.system_gapps_installation" ]; 
    then
        detect_overlap
fi

if [ ! -f "$MODPATH/.DONT_REPLACE" ]; 
    then
        ui_print "- Replacing AOSP apps with their Google counterparts"
        replace_aosp_apps
    else
        ui_print "- Not replacing AOSP apps, as requested during creation"
fi

ui_print "- Wiping cache to prevent undefined behaviour"
wipe_cache

if [ -f "$MODPATH/.DISABLE_SW" ];
    then
        ui_print "- Not triggering setup wizard as requested during creation"
        
elif [ ! -d "${MODPATH//_update/}" ] || [ -f "$MODPATH/.FORCE_SW" ]; 
    then
        ui_print "- Setup wizard will be triggered on next boot"
        ui_print "- Rebooting is recommended after the installation completes"
        trigger_setup_wizard
    else
        ui_print "- Existing installation detected, not triggering setup wizard"
fi

state_observer_script

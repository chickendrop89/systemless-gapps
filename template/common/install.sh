#!/system/bin/sh

SETUP_WIZARD_INTENT="com.google.android.setupwizard"
SETUP_WIZARD_INTENT="$SETUP_WIZARD_INTENT/$SETUP_WIZARD_INTENT.SetupWizardActivity"

wipe_cache(){
    rm -rf /data/dalvik-cache
    rm -rf /data/system/package_cache/*
    rm -rf /data/resource-cache/*
}

ui_print "- Wiping cache to prevent undefined behaviour"
wipe_cache

trigger_setup_wizard(){
    pm enable --user 0 "$SETUP_WIZARD_INTENT" > /dev/null
    settings put secure user_setup_complete 0
    settings put global device_provisioned 0
}

ui_print "- Setup wizard will be triggered on next boot"
ui_print "- Rebooting is recommended after the installation completes"
trigger_setup_wizard

state_observer_script(){
    mv "$MODPATH/systemless-gapps-state-observer.sh" "/data/adb/service.d"
}

state_observer_script
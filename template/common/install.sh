SETUP_WIZARD_INTENT="com.google.android.setupwizard"
SETUP_WIZARD_INTENT="$SETUP_WIZARD_INTENT/$SETUP_WIZARD_INTENT.SetupWizardActivity"

wipe_cache(){
    if [[ -e "/data/system/package_cache" ]]; 
      then
        rm -rf /data/system/package_cache/*
    fi
    if [[ -e "/data/dalvik-cache" ]]; 
      then 
        rm -rf "/data/dalvik-cache"
    fi
}

ui_print "- Wiping cache to prevent undefined behaviour"
wipe_cache

trigger_setup_wizard(){
    pm enable --user 0 "$SETUP_WIZARD_INTENT"
    settings put secure user_setup_complete 0
    settings put global device_provisioned 0
}

ui_print "- Setup wizard will be triggered on next boot"
ui_print "- Rebooting is recommended after the installation completes"
trigger_setup_wizard

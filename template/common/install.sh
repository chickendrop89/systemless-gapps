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

ui_print "- Wiping cache to prevent weird behaviour"
wipe_cache

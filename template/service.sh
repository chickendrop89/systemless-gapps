#!/system/bin/sh

# This is run only on the first boot with this module to set correct runtime permissions 
# to core packages. Without it, basic features and apps are strangely broken

MODDIR=${0%/*}

# Wait until system boot is completed
resetprop -w sys.boot_completed 0

# List all core *system* packages with "google" in their name.
# This does not include user-installed google apps (such as YouTube)
for package in $(pm list packages -s -a | grep "google" | cut -d ":" -f 2); 
    do
        # Grant all permissions
        pm grant --all-permissions "$package"
done

# Rename this file, so magisk does not recognize it
mv "$MODDIR/service.sh" "$MODDIR/__service.sh"

su -lp 2000 -c "cmd notification post -S bigtext -t 'Systemless GApps - Installed' tag \
'Systemless GApps were succesfully installed and post-installation scripts were executed'"

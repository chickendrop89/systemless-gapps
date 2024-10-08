#!/system/bin/sh

# This is run only on the first boot with this module to set correct runtime permissions 
# to core packages. Without it, basic features and apps are strangely broken

MODDIR=${0%/*}

# Wait until system boot is completed
while [ "$(getprop sys.boot_completed)" != "1" ]; 
  do
    sleep 1
done

# List all core *system* packages with "google" in their name.
# This does not include user-installed google apps (such as YouTube)
for package in $(pm list packages -s -a | grep "google" | cut -d ":" -f 2); 
    do
        # Grant all permissions
        pm grant --all-permissions "$package"
done

# Rename this file, so magisk does not recognize it
mv "$MODDIR/service.sh" "$MODDIR/__service.sh"

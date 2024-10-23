#!/system/bin/sh

# This is run only on the first boot with this module to set runtime permissions 
# to core packages (and execute extras). Without it, basic features/apps are broken

MODDIR=${0%/*}
PACKAGE_LIST=${MODDIR}/extra/package_list.txt

# Wait until system boot is completed
resetprop -w sys.boot_completed 0

# We are getting rate-limited by audit.
# Set SElinux to permissive (if it wasn't) for a brief moment
if [ "$(getenforce)" = "Enforcing" ]; 
    then
        setenforce 0
        WAS_ENABLED=1
fi

while IFS= read -r package; do
    pm grant --all-permissions "$package"
done < "$PACKAGE_LIST"

# Re-enable it (if it was previously enabled)
if [ "$WAS_ENABLED" -eq 1 ];
    then
        setenforce 1
fi

# Extra: run a batch dexopt and do a cleanup 
pm art dexopt-packages -r boot-after-ota >/dev/null 2>&1
pm art cleanup >/dev/null 2>&1

# Rename this file, so magisk does not recognize it
mv "$MODDIR/service.sh" "$MODDIR/__service.sh" >/dev/null 2>&1

su -lp 2000 -c "cmd notification post -S bigtext -t 'Systemless GApps - Installed' tag \
'Systemless GApps were succesfully installed and post-installation scripts were executed'"

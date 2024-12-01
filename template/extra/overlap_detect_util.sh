#!/system_ext/bin/bash

persistent_path=/data/adb

# Todo: Hard-coded module path
module_path=/data/adb/modules_update/systemless-gapps
package_list=$module_path/extra/package_list.txt

# We are getting rate-limited by audit.
# Set SElinux to permissive (if it wasn't) for a brief moment
if [ "$(getenforce)" = "Enforcing" ]; 
    then setenforce 0; WAS_ENABLED=1
fi

# Initialize an empty array to store installed packages
installed_packages=()

# Check if we are overwriting existing foreign GApps installation
while IFS= read -r package; do
    if [ -n "$(pm list packages -s "$package")" ]; then
        installed_packages+=("$package")

        # Check if the array exceeds 3 packages to be extra sure
        if [[ ${#installed_packages[@]} -gt 3 ]]; then
            touch $persistent_path/.system_gapps_installation
            break
        fi
    fi
done < $package_list

# Re-enable it (if it was previously enabled)
if [ "$WAS_ENABLED" -eq 1 ];
    then setenforce 1
fi

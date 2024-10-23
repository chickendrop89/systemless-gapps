#!/system_ext/bin/bash

# This script "removes" conflicting AOSP apps in order to replace them with GApps
# It has to be run during the module installation

# Array of packages to look for. This is filled during build
packages=()

# Array of partitions to search
search_dirs=(/system /vendor /product /odm /system_ext)

# Todo: Hard-coded module path
module_path=/data/adb/modules_update/systemless-gapps

find_dirs() {
  __path="$1"

  # Iterate through each directory in the current path
  for dir in $__path; do
    if [ -d "$dir" ]; then
      # Check if the directory name is in the packages array
      for package in "${packages[@]}"; do
        # Check if the directory name matches a package
        if [ "$(basename "$dir")" == "$package" ]; then
          overlay_system_dir="$module_path/system/$dir"

          if [[ "$dir" == *"system/"* ]]; then
            overlay_system_dir="$module_path/$dir"
          fi

          mkdir -p "$overlay_system_dir"
          touch "$overlay_system_dir/.replace"
        fi
      done
    fi
  done
}

for dir in "${search_dirs[@]}"; do
  find_dirs "$dir/priv-app/*"
done

for dir in "${search_dirs[@]}"; do 
  find_dirs "$dir/app/*"
done

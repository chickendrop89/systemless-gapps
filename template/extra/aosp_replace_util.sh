#!/system_ext/bin/bash

# This script "removes" conflicting AOSP apps in order to replace them with GApps
# It has to be run during the module installation

# Array of packages to look for. This is filled during build
packages=()

# Array of partitions to search
search_dirs=(/system /vendor /product /odm /system_ext)

# Todo: Hard-coded module path
module_path=/data/adb/modules_update/systemless-gapps

# Function to find directories and create overlays
find_dirs() {
  __path="$1"

  # List directories in the current path
  dirs=$(ls "$__path" 2> /dev/null)

  # Iterate through each directory
  for dir in $dirs; do
    if [ -d "$__path/$dir" ]; then
      # Check if the directory name is in the packages array
      for package in "${packages[@]}"; do
        # Check if the directory name matches a package
        if [ "$dir" == "$package" ]; then
          overlay_system_dir="$module_path/system/$__path/$dir"

          if [[ "$__path" == *"system/"* ]]; then
            overlay_system_dir="$module_path/$__path/$dir"
          fi

          mkdir -p "$overlay_system_dir"
          touch "$overlay_system_dir/.replace"
        fi
      done
    fi
  done
}

for dir in "${search_dirs[@]}"; 
  do
    find_dirs "$dir/priv-app/"
done

for dir in "${search_dirs[@]}"; 
  do
    find_dirs "$dir/app/"
done

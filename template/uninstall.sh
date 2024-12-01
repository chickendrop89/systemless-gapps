PACKAGE_LIST=${MODDIR}/extra/package_list.txt

# Remove traces of GApps, if we aren't overlapping existing not system-less* package
if [ ! -f "/data/adb/.system_gapps_installation" ]; then
  # We are getting rate-limited by audit.
  # Set SElinux to permissive (if it wasn't) for a brief moment
  if [ "$(getenforce)" = "Enforcing" ]; 
      then setenforce 0; WAS_ENABLED=1
  fi

  while IFS= read -r package; do
      pm uninstall "$package"
  done < "$PACKAGE_LIST"

  # Re-enable it (if it was previously enabled)
  if [ "$WAS_ENABLED" -eq 1 ];
    then setenforce 1
  fi
fi

# Clear cache to prevent weird behaviour after uninstalling
pm art cleanup 2>&1
rm -rf /data/system/package_cache/*

# Don't modify anything after this
if [ -f $INFO ]; then
  while read LINE; do
    if [ "$(echo -n $LINE | tail -c 1)" == "~" ]; then
      continue
    elif [ -f "$LINE~" ]; then
      mv -f $LINE~ $LINE
    else
      rm -f $LINE
      while true; do
        LINE=$(dirname $LINE)
        [ "$(ls -A $LINE 2>/dev/null)" ] && break 1 || rm -rf $LINE
      done
    fi
  done < $INFO
  rm -f $INFO
fi

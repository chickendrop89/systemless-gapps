##########################################################################################
#
# MMT Extended Config Script
#
##########################################################################################

##########################################################################################
# Config Flags
##########################################################################################

# Uncomment and change 'MINAPI' and 'MAXAPI' to the minimum and maximum android version for your mod
# Uncomment DYNLIB if you want libs installed to vendor for oreo+ and system for anything older
# Uncomment PARTOVER if you have a workaround in place for extra partitions in regular magisk install (can mount them yourself - you will need to do this each boot as well). If unsure, keep commented
# Uncomment PARTITIONS and list additional partitions you will be modifying (other than system and vendor), for example: PARTITIONS="/odm /product /system_ext"
MINAPI=34
#MAXAPI=25
#DYNLIB=true
#PARTOVER=true
PARTITIONS="/product"

SERVICE_D="/data/adb/service.d/systemless-gapps-state-observer.sh"

##########################################################################################
# Replace list
##########################################################################################

# List all directories you want to directly replace in the system
# Check the documentations for more info why you would need this

# Construct your list in the following format
# This is an example
REPLACE_EXAMPLE="
/system/app/Youtube
/system/priv-app/SystemUI
/system/priv-app/Settings
/system/framework
"

REPLACE="
"

##########################################################################################
# Permissions
##########################################################################################

MODDIR=${0%/*}

set_permissions() {
  set_perm "$SERVICE_D" 0 0 0744
  set_perm_recursive "$MODDIR" 0 0 0755 0644
  
  for i in "$MODDIR"/system/product/overlay "$MODDIR"/system/priv-app/* "$MODDIR"/system/app/*; do
      set_perm_recursive "$i" 0 0 0755 0644
  done
}

##########################################################################################
# MMT Extended Logic - Don't modify anything after this
##########################################################################################

SKIPUNZIP=1
unzip -qjo "$ZIPFILE" 'common/functions.sh' -d $TMPDIR >&2
. $TMPDIR/functions.sh

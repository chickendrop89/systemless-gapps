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
PARTITIONS="/system_ext /product /odm"

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

set_permissions() {
  set_perm_recursive $MODPATH 0 0 0755 0644
  set_perm $MODPATH/extra/aosp_replace_util.sh 0 0 0700

  set_perm_recursive $MODPATH/system/lib 0 0 0755 0644 "u:object_r:system_lib_file:s0"
  set_perm_recursive $MODPATH/system/lib64 0 0 0755 0644 "u:object_r:system_lib_file:s0"
  set_perm $SERVICE_D 0 0 0744 "u:object_r:adb_data_file:s0"
}

##########################################################################################
# MMT Extended Logic - Don't modify anything after this
##########################################################################################

SKIPUNZIP=1
#unzip -qjo "$ZIPFILE" 'extra' -d $TMPDIR >&2
unzip -qjo "$ZIPFILE" 'common/functions.sh' -d $TMPDIR >&2
. $TMPDIR/functions.sh

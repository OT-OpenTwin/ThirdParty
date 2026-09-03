#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ads::qtadvanceddocking-qt6" for configuration "RelWithDebInfo"
set_property(TARGET ads::qtadvanceddocking-qt6 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ads::qtadvanceddocking-qt6 PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/qtadvanceddocking-qt6.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/qtadvanceddocking-qt6.dll"
  )

list(APPEND _cmake_import_check_targets ads::qtadvanceddocking-qt6 )
list(APPEND _cmake_import_check_files_for_ads::qtadvanceddocking-qt6 "${_IMPORT_PREFIX}/lib/qtadvanceddocking-qt6.lib" "${_IMPORT_PREFIX}/bin/qtadvanceddocking-qt6.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

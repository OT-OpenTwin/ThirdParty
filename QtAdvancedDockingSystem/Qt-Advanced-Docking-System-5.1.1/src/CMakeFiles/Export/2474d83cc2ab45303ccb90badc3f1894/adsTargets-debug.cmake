#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ads::qtadvanceddocking-qt6" for configuration "Debug"
set_property(TARGET ads::qtadvanceddocking-qt6 APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(ads::qtadvanceddocking-qt6 PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/qtadvanceddocking-qt6d.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/qtadvanceddocking-qt6d.dll"
  )

list(APPEND _cmake_import_check_targets ads::qtadvanceddocking-qt6 )
list(APPEND _cmake_import_check_files_for_ads::qtadvanceddocking-qt6 "${_IMPORT_PREFIX}/lib/qtadvanceddocking-qt6d.lib" "${_IMPORT_PREFIX}/bin/qtadvanceddocking-qt6d.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

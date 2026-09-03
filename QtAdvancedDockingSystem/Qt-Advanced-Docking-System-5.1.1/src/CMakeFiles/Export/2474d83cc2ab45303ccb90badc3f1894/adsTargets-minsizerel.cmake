#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ads::qtadvanceddocking-qt6" for configuration "MinSizeRel"
set_property(TARGET ads::qtadvanceddocking-qt6 APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(ads::qtadvanceddocking-qt6 PROPERTIES
  IMPORTED_IMPLIB_MINSIZEREL "${_IMPORT_PREFIX}/lib/qtadvanceddocking-qt6.lib"
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/bin/qtadvanceddocking-qt6.dll"
  )

list(APPEND _cmake_import_check_targets ads::qtadvanceddocking-qt6 )
list(APPEND _cmake_import_check_files_for_ads::qtadvanceddocking-qt6 "${_IMPORT_PREFIX}/lib/qtadvanceddocking-qt6.lib" "${_IMPORT_PREFIX}/bin/qtadvanceddocking-qt6.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

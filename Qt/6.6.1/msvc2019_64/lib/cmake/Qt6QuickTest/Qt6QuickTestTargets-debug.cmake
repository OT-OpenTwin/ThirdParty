#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QuickTest" for configuration "Debug"
set_property(TARGET Qt6::QuickTest APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::QuickTest PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6QuickTestd.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "Qt6::Quick;Qt6::Qml;Qt6::Core"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6QuickTestd.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::QuickTest )
list(APPEND _cmake_import_check_files_for_Qt6::QuickTest "${_IMPORT_PREFIX}/lib/Qt6QuickTestd.lib" "${_IMPORT_PREFIX}/bin/Qt6QuickTestd.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

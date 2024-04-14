#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::WebEngineWidgets" for configuration "Debug"
set_property(TARGET Qt6::WebEngineWidgets APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::WebEngineWidgets PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6WebEngineWidgetsd.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6WebEngineWidgetsd.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::WebEngineWidgets )
list(APPEND _cmake_import_check_files_for_Qt6::WebEngineWidgets "${_IMPORT_PREFIX}/lib/Qt6WebEngineWidgetsd.lib" "${_IMPORT_PREFIX}/bin/Qt6WebEngineWidgetsd.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

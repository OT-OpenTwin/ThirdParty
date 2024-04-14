#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::Coap" for configuration "Debug"
set_property(TARGET Qt6::Coap APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::Coap PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6Coapd.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6Coapd.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::Coap )
list(APPEND _cmake_import_check_files_for_Qt6::Coap "${_IMPORT_PREFIX}/lib/Qt6Coapd.lib" "${_IMPORT_PREFIX}/bin/Qt6Coapd.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

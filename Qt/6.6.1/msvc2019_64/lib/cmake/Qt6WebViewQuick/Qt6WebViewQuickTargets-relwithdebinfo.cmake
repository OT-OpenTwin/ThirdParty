#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::WebViewQuick" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::WebViewQuick APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::WebViewQuick PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6WebViewQuick.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::Qml"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6WebViewQuick.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::WebViewQuick )
list(APPEND _cmake_import_check_files_for_Qt6::WebViewQuick "${_IMPORT_PREFIX}/lib/Qt6WebViewQuick.lib" "${_IMPORT_PREFIX}/bin/Qt6WebViewQuick.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

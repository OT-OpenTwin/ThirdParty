#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::DeclarativeOpcua" for configuration "Debug"
set_property(TARGET Qt6::DeclarativeOpcua APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::DeclarativeOpcua PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6DeclarativeOpcuad.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "Qt6::Qml"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6DeclarativeOpcuad.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::DeclarativeOpcua )
list(APPEND _cmake_import_check_files_for_Qt6::DeclarativeOpcua "${_IMPORT_PREFIX}/lib/Qt6DeclarativeOpcuad.lib" "${_IMPORT_PREFIX}/bin/Qt6DeclarativeOpcuad.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

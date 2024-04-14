#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::DeclarativeOpcua" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::DeclarativeOpcua APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::DeclarativeOpcua PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6DeclarativeOpcua.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::Qml"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6DeclarativeOpcua.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::DeclarativeOpcua )
list(APPEND _cmake_import_check_files_for_Qt6::DeclarativeOpcua "${_IMPORT_PREFIX}/lib/Qt6DeclarativeOpcua.lib" "${_IMPORT_PREFIX}/bin/Qt6DeclarativeOpcua.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

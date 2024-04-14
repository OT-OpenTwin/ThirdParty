#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::FlowView" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::FlowView APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::FlowView PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6FlowView.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::Qml;Qt6::Core"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6FlowView.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::FlowView )
list(APPEND _cmake_import_check_files_for_Qt6::FlowView "${_IMPORT_PREFIX}/lib/Qt6FlowView.lib" "${_IMPORT_PREFIX}/bin/Qt6FlowView.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

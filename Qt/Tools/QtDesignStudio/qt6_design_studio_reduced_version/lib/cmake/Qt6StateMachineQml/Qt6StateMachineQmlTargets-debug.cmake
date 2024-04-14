#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::StateMachineQml" for configuration "Debug"
set_property(TARGET Qt6::StateMachineQml APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::StateMachineQml PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6StateMachineQmld.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "Qt6::Qml"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6StateMachineQmld.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::StateMachineQml )
list(APPEND _cmake_import_check_files_for_Qt6::StateMachineQml "${_IMPORT_PREFIX}/lib/Qt6StateMachineQmld.lib" "${_IMPORT_PREFIX}/bin/Qt6StateMachineQmld.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

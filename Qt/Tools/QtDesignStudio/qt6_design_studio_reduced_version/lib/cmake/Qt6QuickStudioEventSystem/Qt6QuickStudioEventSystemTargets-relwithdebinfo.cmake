#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QuickStudioEventSystem" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QuickStudioEventSystem APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QuickStudioEventSystem PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6QuickStudioEventSystem.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::Qml;Qt6::Core"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6QuickStudioEventSystem.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::QuickStudioEventSystem )
list(APPEND _cmake_import_check_files_for_Qt6::QuickStudioEventSystem "${_IMPORT_PREFIX}/lib/Qt6QuickStudioEventSystem.lib" "${_IMPORT_PREFIX}/bin/Qt6QuickStudioEventSystem.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

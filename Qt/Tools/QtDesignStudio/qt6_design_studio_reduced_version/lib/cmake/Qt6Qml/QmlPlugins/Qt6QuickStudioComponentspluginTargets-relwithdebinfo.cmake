#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QuickStudioComponentsplugin" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QuickStudioComponentsplugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QuickStudioComponentsplugin PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELWITHDEBINFO ""
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/./qml/QtQuick/Studio/Components/quickstudiocomponentsplugin.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::QuickStudioComponentsplugin )
list(APPEND _cmake_import_check_files_for_Qt6::QuickStudioComponentsplugin "${_IMPORT_PREFIX}/./qml/QtQuick/Studio/Components/quickstudiocomponentsplugin.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

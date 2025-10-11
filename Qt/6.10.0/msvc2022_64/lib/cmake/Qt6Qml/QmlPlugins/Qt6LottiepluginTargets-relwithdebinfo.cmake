#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::Lottieplugin" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::Lottieplugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::Lottieplugin PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELWITHDEBINFO ""
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/qml/Qt/labs/lottieqt/lottieplugin.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::Lottieplugin )
list(APPEND _cmake_import_check_files_for_Qt6::Lottieplugin "${_IMPORT_PREFIX}/qml/Qt/labs/lottieqt/lottieplugin.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

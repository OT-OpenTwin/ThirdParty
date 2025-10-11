#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::Lottie" for configuration "Debug"
set_property(TARGET Qt6::Lottie APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::Lottie PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6Lottied.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "Qt6::Core;Qt6::Gui;Qt6::Qml;Qt6::Quick"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6Lottied.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::Lottie )
list(APPEND _cmake_import_check_files_for_Qt6::Lottie "${_IMPORT_PREFIX}/lib/Qt6Lottied.lib" "${_IMPORT_PREFIX}/bin/Qt6Lottied.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

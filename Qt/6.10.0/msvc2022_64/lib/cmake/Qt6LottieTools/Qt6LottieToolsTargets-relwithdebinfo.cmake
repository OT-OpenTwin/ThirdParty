#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::lottietoqml" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::lottietoqml APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::lottietoqml PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/lottietoqml.exe"
  )

list(APPEND _cmake_import_check_targets Qt6::lottietoqml )
list(APPEND _cmake_import_check_files_for_Qt6::lottietoqml "${_IMPORT_PREFIX}/bin/lottietoqml.exe" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::repc" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::repc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::repc PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/./bin/repc.exe"
  )

list(APPEND _cmake_import_check_targets Qt6::repc )
list(APPEND _cmake_import_check_files_for_Qt6::repc "${_IMPORT_PREFIX}/./bin/repc.exe" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

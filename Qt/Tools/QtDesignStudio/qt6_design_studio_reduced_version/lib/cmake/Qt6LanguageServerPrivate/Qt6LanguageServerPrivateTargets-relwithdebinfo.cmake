#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::LanguageServerPrivate" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::LanguageServerPrivate APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::LanguageServerPrivate PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6LanguageServer.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6LanguageServer.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::LanguageServerPrivate )
list(APPEND _cmake_import_check_files_for_Qt6::LanguageServerPrivate "${_IMPORT_PREFIX}/lib/Qt6LanguageServer.lib" "${_IMPORT_PREFIX}/bin/Qt6LanguageServer.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

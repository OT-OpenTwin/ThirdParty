#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::TextToSpeech" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::TextToSpeech APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::TextToSpeech PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6TextToSpeech.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6TextToSpeech.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::TextToSpeech )
list(APPEND _cmake_import_check_files_for_Qt6::TextToSpeech "${_IMPORT_PREFIX}/lib/Qt6TextToSpeech.lib" "${_IMPORT_PREFIX}/bin/Qt6TextToSpeech.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::Quick3DSpatialAudioPrivate" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::Quick3DSpatialAudioPrivate APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::Quick3DSpatialAudioPrivate PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6Quick3DSpatialAudio.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::Qml"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6Quick3DSpatialAudio.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::Quick3DSpatialAudioPrivate )
list(APPEND _cmake_import_check_files_for_Qt6::Quick3DSpatialAudioPrivate "${_IMPORT_PREFIX}/lib/Qt6Quick3DSpatialAudio.lib" "${_IMPORT_PREFIX}/bin/Qt6Quick3DSpatialAudio.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

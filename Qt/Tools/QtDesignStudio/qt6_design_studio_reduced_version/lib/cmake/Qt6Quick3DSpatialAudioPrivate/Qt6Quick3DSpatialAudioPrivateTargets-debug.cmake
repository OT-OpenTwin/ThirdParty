#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::Quick3DSpatialAudioPrivate" for configuration "Debug"
set_property(TARGET Qt6::Quick3DSpatialAudioPrivate APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::Quick3DSpatialAudioPrivate PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6Quick3DSpatialAudiod.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "Qt6::Qml"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6Quick3DSpatialAudiod.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::Quick3DSpatialAudioPrivate )
list(APPEND _cmake_import_check_files_for_Qt6::Quick3DSpatialAudioPrivate "${_IMPORT_PREFIX}/lib/Qt6Quick3DSpatialAudiod.lib" "${_IMPORT_PREFIX}/bin/Qt6Quick3DSpatialAudiod.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

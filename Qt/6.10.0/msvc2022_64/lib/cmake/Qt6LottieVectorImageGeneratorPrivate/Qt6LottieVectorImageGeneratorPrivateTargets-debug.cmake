#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::LottieVectorImageGeneratorPrivate" for configuration "Debug"
set_property(TARGET Qt6::LottieVectorImageGeneratorPrivate APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::LottieVectorImageGeneratorPrivate PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6LottieVectorImageGeneratord.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "Qt6::Core;Qt6::Quick;Qt6::QuickShapesPrivate;Qt6::QuickVectorImageGeneratorPrivate;Qt6::Lottie"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6LottieVectorImageGeneratord.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::LottieVectorImageGeneratorPrivate )
list(APPEND _cmake_import_check_files_for_Qt6::LottieVectorImageGeneratorPrivate "${_IMPORT_PREFIX}/lib/Qt6LottieVectorImageGeneratord.lib" "${_IMPORT_PREFIX}/bin/Qt6LottieVectorImageGeneratord.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

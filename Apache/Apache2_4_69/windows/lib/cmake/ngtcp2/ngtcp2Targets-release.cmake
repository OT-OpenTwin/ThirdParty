#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ngtcp2::ngtcp2" for configuration "Release"
set_property(TARGET ngtcp2::ngtcp2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngtcp2::ngtcp2 PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/ngtcp2.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/ngtcp2.dll"
  )

list(APPEND _cmake_import_check_targets ngtcp2::ngtcp2 )
list(APPEND _cmake_import_check_files_for_ngtcp2::ngtcp2 "${_IMPORT_PREFIX}/lib/ngtcp2.lib" "${_IMPORT_PREFIX}/bin/ngtcp2.dll" )

# Import target "ngtcp2::ngtcp2_static" for configuration "Release"
set_property(TARGET ngtcp2::ngtcp2_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngtcp2::ngtcp2_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/ngtcp2_static.lib"
  )

list(APPEND _cmake_import_check_targets ngtcp2::ngtcp2_static )
list(APPEND _cmake_import_check_files_for_ngtcp2::ngtcp2_static "${_IMPORT_PREFIX}/lib/ngtcp2_static.lib" )

# Import target "ngtcp2::ngtcp2_crypto_ossl" for configuration "Release"
set_property(TARGET ngtcp2::ngtcp2_crypto_ossl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngtcp2::ngtcp2_crypto_ossl PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/ngtcp2_crypto_ossl.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/ngtcp2_crypto_ossl.dll"
  )

list(APPEND _cmake_import_check_targets ngtcp2::ngtcp2_crypto_ossl )
list(APPEND _cmake_import_check_files_for_ngtcp2::ngtcp2_crypto_ossl "${_IMPORT_PREFIX}/lib/ngtcp2_crypto_ossl.lib" "${_IMPORT_PREFIX}/bin/ngtcp2_crypto_ossl.dll" )

# Import target "ngtcp2::ngtcp2_crypto_ossl_static" for configuration "Release"
set_property(TARGET ngtcp2::ngtcp2_crypto_ossl_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ngtcp2::ngtcp2_crypto_ossl_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/ngtcp2_crypto_ossl_static.lib"
  )

list(APPEND _cmake_import_check_targets ngtcp2::ngtcp2_crypto_ossl_static )
list(APPEND _cmake_import_check_files_for_ngtcp2::ngtcp2_crypto_ossl_static "${_IMPORT_PREFIX}/lib/ngtcp2_crypto_ossl_static.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

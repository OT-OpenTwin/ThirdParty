#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::PdfQuick" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::PdfQuick APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::PdfQuick PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt6PdfQuick.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::Qml;Qt6::Core"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt6PdfQuick.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::PdfQuick )
list(APPEND _cmake_import_check_files_for_Qt6::PdfQuick "${_IMPORT_PREFIX}/lib/Qt6PdfQuick.lib" "${_IMPORT_PREFIX}/bin/Qt6PdfQuick.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

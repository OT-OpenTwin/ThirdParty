#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::3DQuickLogic" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::3DQuickLogic APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::3DQuickLogic PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Qt63DQuickLogic.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::3DCore;Qt6::3DLogic;Qt6::Core;Qt6::Gui;Qt6::Qml"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Qt63DQuickLogic.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::3DQuickLogic )
list(APPEND _cmake_import_check_files_for_Qt6::3DQuickLogic "${_IMPORT_PREFIX}/lib/Qt63DQuickLogic.lib" "${_IMPORT_PREFIX}/bin/Qt63DQuickLogic.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

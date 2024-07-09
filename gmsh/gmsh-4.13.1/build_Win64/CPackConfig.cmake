# This file will be configured to contain variables for CPack. These variables
# should be set in the CMake list file of the project before CPack module is
# included. The list of available CPACK_xxx variables and their associated
# documentation may be obtained using
#  cpack --help-variable-list
#
# Some variables are common to all generators (e.g. CPACK_PACKAGE_NAME)
# and some are specific to a generator
# (e.g. CPACK_NSIS_EXTRA_INSTALL_COMMANDS). The generator specific variables
# usually begin with CPACK_<GENNAME>_xxxx.


set(CPACK_BUILD_SOURCE_DIRS "C:/OT/ThirdParty/gmsh/gmsh-4.13.1;C:/OT/ThirdParty/gmsh/gmsh-4.13.1/build_Win64")
set(CPACK_CMAKE_GENERATOR "Visual Studio 17 2022")
set(CPACK_COMPONENT_UNSPECIFIED_HIDDEN "TRUE")
set(CPACK_COMPONENT_UNSPECIFIED_REQUIRED "TRUE")
set(CPACK_DEFAULT_PACKAGE_DESCRIPTION_FILE "C:/Program Files/CMake/share/cmake-3.28/Templates/CPack.GenericDescription.txt")
set(CPACK_DEFAULT_PACKAGE_DESCRIPTION_SUMMARY "gmsh built using CMake")
set(CPACK_DMG_SLA_USE_RESOURCE_FILE_LICENSE "ON")
set(CPACK_GENERATOR "ZIP")
set(CPACK_INNOSETUP_ARCHITECTURE "x64")
set(CPACK_INSTALL_CMAKE_PROJECTS "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/build_Win64;gmsh;ALL;/")
set(CPACK_INSTALL_PREFIX "C:/Program Files (x86)/gmsh")
set(CPACK_MODULE_PATH "")
set(CPACK_NSIS_DISPLAY_NAME "gmsh")
set(CPACK_NSIS_INSTALLER_ICON_CODE "")
set(CPACK_NSIS_INSTALLER_MUI_ICON_CODE "")
set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES64")
set(CPACK_NSIS_PACKAGE_NAME "gmsh")
set(CPACK_NSIS_UNINSTALL_NAME "Uninstall")
set(CPACK_OUTPUT_CONFIG_FILE "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/build_Win64/CPackConfig.cmake")
set(CPACK_PACKAGE_DEFAULT_LOCATION "/")
set(CPACK_PACKAGE_DESCRIPTION_FILE "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/doc/WELCOME.txt")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "3D finite element mesh generator with built-in CAD engine and post-processor")
set(CPACK_PACKAGE_EXECUTABLE "gmsh")
set(CPACK_PACKAGE_FILE_NAME "gmsh-git-Windows64-sdk")
set(CPACK_PACKAGE_INSTALL_DIRECTORY "gmsh")
set(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "gmsh")
set(CPACK_PACKAGE_NAME "gmsh")
set(CPACK_PACKAGE_RELOCATABLE "true")
set(CPACK_PACKAGE_VENDOR "Christophe Geuzaine and Jean-Francois Remacle")
set(CPACK_PACKAGE_VERSION "4.13.1")
set(CPACK_PACKAGE_VERSION_MAJOR "4")
set(CPACK_PACKAGE_VERSION_MINOR "13")
set(CPACK_PACKAGE_VERSION_PATCH "1")
set(CPACK_RESOURCE_FILE_LICENSE "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/LICENSE.txt")
set(CPACK_RESOURCE_FILE_README "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/doc/WELCOME.txt")
set(CPACK_RESOURCE_FILE_WELCOME "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/doc/WELCOME.txt")
set(CPACK_SET_DESTDIR "OFF")
set(CPACK_SOURCE_GENERATOR "TGZ")
set(CPACK_SOURCE_IGNORE_FILES "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/build_Win64;/CVS/;/.svn;/.git;~$;DS_Store$;GmshConfig.h$;GmshVersion.h$;/benchmarks/;/tmp/;/bin/;/lib/;/nightly/;GPATH;GRTAGS;GSYMS;GTAGS;/HTML/;/contrib/3M/;/contrib/Parasolid/")
set(CPACK_SOURCE_OUTPUT_CONFIG_FILE "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/build_Win64/CPackSourceConfig.cmake")
set(CPACK_SOURCE_PACKAGE_FILE_NAME "gmsh-git-source")
set(CPACK_STRIP_FILES "TRUE")
set(CPACK_SYSTEM_NAME "win64")
set(CPACK_THREADS "1")
set(CPACK_TOPLEVEL_TAG "win64")
set(CPACK_WIX_SIZEOF_VOID_P "8")

if(NOT CPACK_PROPERTIES_FILE)
  set(CPACK_PROPERTIES_FILE "C:/OT/ThirdParty/gmsh/gmsh-4.13.1/build_Win64/CPackProperties.cmake")
endif()

if(EXISTS ${CPACK_PROPERTIES_FILE})
  include(${CPACK_PROPERTIES_FILE})
endif()

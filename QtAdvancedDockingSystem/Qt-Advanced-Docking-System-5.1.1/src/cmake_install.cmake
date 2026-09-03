# Install script for directory: C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files (x86)/QtADS")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/qtadvanceddocking-qt6" TYPE FILE FILES
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/ads_globals.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockAreaTabBar.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockAreaTitleBar.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockAreaTitleBar_p.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockAreaWidget.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockContainerWidget.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockManager.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockOverlay.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockSplitter.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockWidget.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockWidgetTab.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockingStateReader.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockFocusController.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/ElidingLabel.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/FloatingDockContainer.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/FloatingDragPreview.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/IconProvider.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/DockComponentsFactory.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/AutoHideSideBar.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/AutoHideTab.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/AutoHideDockContainer.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/PushButton.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/ResizeHandle.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/ComponentsFactory.h"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/ads_version.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "license" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ads/license" TYPE FILE FILES
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/../LICENSE"
    "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/../gnu-lgpl-v2.1.md"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/lib/Debug/qtadvanceddocking-qt6d.lib")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/lib/Release/qtadvanceddocking-qt6.lib")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/lib/MinSizeRel/qtadvanceddocking-qt6.lib")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/lib/RelWithDebInfo/qtadvanceddocking-qt6.lib")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/bin/Debug/qtadvanceddocking-qt6d.dll")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/bin/Release/qtadvanceddocking-qt6.dll")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/bin/MinSizeRel/qtadvanceddocking-qt6.dll")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/x64/bin/RelWithDebInfo/qtadvanceddocking-qt6.dll")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6/adsTargets.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6/adsTargets.cmake"
         "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/CMakeFiles/Export/2474d83cc2ab45303ccb90badc3f1894/adsTargets.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6/adsTargets-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6/adsTargets.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/CMakeFiles/Export/2474d83cc2ab45303ccb90badc3f1894/adsTargets.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/CMakeFiles/Export/2474d83cc2ab45303ccb90badc3f1894/adsTargets-debug.cmake")
  endif()
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/CMakeFiles/Export/2474d83cc2ab45303ccb90badc3f1894/adsTargets-minsizerel.cmake")
  endif()
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/CMakeFiles/Export/2474d83cc2ab45303ccb90badc3f1894/adsTargets-relwithdebinfo.cmake")
  endif()
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/CMakeFiles/Export/2474d83cc2ab45303ccb90badc3f1894/adsTargets-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE RENAME "qtadvanceddocking-qt6Config.cmake" FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/qtadvanceddockingConfig.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/qtadvanceddocking-qt6" TYPE FILE FILES "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/qtadvanceddocking-qt6ConfigVersion.cmake")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "C:/OpenTwin/ThirdParty/QtAdvancedDockingSystem/Qt-Advanced-Docking-System-5.1.1/src/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()

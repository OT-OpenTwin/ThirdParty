# Install script for directory: C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files/VTK")
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

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/vtk-9.0" TYPE FILE FILES
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleDrawPolygon.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleFlight.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleImage.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleJoystickActor.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleJoystickCamera.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleMultiTouchCamera.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleRubberBand2D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleRubberBand3D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleRubberBandPick.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleRubberBandZoom.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleTerrain.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleTrackball.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleTrackballActor.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleTrackballCamera.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleUnicam.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleUser.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkInteractorStyleSwitch.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Interaction/Style/vtkParallelCoordinatesInteractorStyle.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/Interaction/Style/vtkInteractionStyleModule.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/vtk/hierarchy/VTK" TYPE FILE RENAME "vtkInteractionStyle-hierarchy.txt" FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/vtk/hierarchy/VTK/vtkInteractionStyle-hierarchy.txt")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Debug/vtkInteractionStyle-9.0d.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Release/vtkInteractionStyle-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/MinSizeRel/vtkInteractionStyle-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/RelWithDebInfo/vtkInteractionStyle-9.0.lib")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Debug/vtkInteractionStyle-9.0d.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Release/vtkInteractionStyle-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/MinSizeRel/vtkInteractionStyle-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/RelWithDebInfo/vtkInteractionStyle-9.0.dll")
  endif()
endif()


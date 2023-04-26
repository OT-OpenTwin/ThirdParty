# Install script for directory: C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid

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
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkAdaptiveDataSetSurfaceFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkBSplineTransform.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkDepthSortPolyData.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkDSPFilterDefinition.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkDSPFilterGroup.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkEarthSource.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkFacetReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkForceTime.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkGreedyTerrainDecimation.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkGridTransform.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkImageToPolyDataFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkImplicitModeller.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkPCAAnalysisFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkPolyDataSilhouette.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkProcrustesAlignmentFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkProjectedTerrainPath.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkRenderLargeImage.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTemporalArrayOperatorFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTemporalDataSetCache.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTemporalFractal.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTemporalInterpolator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTemporalShiftScale.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTemporalSnapToTimeStep.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkTransformToGrid.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/Hybrid/vtkWeightedTransformFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/Filters/Hybrid/vtkFiltersHybridModule.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/vtk/hierarchy/VTK" TYPE FILE RENAME "vtkFiltersHybrid-hierarchy.txt" FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/vtk/hierarchy/VTK/vtkFiltersHybrid-hierarchy.txt")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Debug/vtkFiltersHybrid-9.0d.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Release/vtkFiltersHybrid-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/MinSizeRel/vtkFiltersHybrid-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/RelWithDebInfo/vtkFiltersHybrid-9.0.lib")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Debug/vtkFiltersHybrid-9.0d.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Release/vtkFiltersHybrid-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/MinSizeRel/vtkFiltersHybrid-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/RelWithDebInfo/vtkFiltersHybrid-9.0.dll")
  endif()
endif()


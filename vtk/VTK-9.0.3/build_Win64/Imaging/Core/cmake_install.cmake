# Install script for directory: C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core

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
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageProbeFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkAbstractImageInterpolator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkExtractVOI.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageAppendComponents.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageBlend.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageBSplineCoefficients.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageBSplineInternals.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageBSplineInterpolator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageCacheFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageCast.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageChangeInformation.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageClip.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageConstantPad.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageDataStreamer.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageDecomposeFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageDifference.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageExtractComponents.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageFlip.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageInterpolator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageIterateFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageMagnify.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageMapToColors.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageMask.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageMirrorPad.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImagePadFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImagePermute.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImagePointDataIterator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImagePointIterator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageResample.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageResize.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageReslice.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageResliceToColors.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageShiftScale.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageShrink3D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageSincInterpolator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageStencilAlgorithm.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageStencilData.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageStencilIterator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageStencilSource.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageThreshold.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageTranslateExtent.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkImageWrapPad.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Imaging/Core/vtkRTAnalyticSource.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/Imaging/Core/vtkImagingCoreModule.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/vtk/hierarchy/VTK" TYPE FILE RENAME "vtkImagingCore-hierarchy.txt" FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/vtk/hierarchy/VTK/vtkImagingCore-hierarchy.txt")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Debug/vtkImagingCore-9.0d.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Release/vtkImagingCore-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/MinSizeRel/vtkImagingCore-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/RelWithDebInfo/vtkImagingCore-9.0.lib")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Debug/vtkImagingCore-9.0d.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Release/vtkImagingCore-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/MinSizeRel/vtkImagingCore-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/RelWithDebInfo/vtkImagingCore-9.0.dll")
  endif()
endif()


# Install script for directory: C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML

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
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkRTXMLPolyDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLCompositeDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLCompositeDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLDataObjectWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLDataSetWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLFileReadTester.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLGenericDataObjectReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLHierarchicalBoxDataFileConverter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLHierarchicalBoxDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLHierarchicalBoxDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLHierarchicalDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLHyperTreeGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLHyperTreeGridWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLImageDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLImageDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLMultiBlockDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLMultiBlockDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLMultiGroupDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPDataObjectReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPHyperTreeGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPImageDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPPolyDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPRectilinearGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPStructuredDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPStructuredGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPTableReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPUnstructuredDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPUnstructuredGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPartitionedDataSetCollectionReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPartitionedDataSetCollectionWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPartitionedDataSetReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPartitionedDataSetWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPolyDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLPolyDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLRectilinearGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLRectilinearGridWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLStructuredDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLStructuredDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLStructuredGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLStructuredGridWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLTableReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLTableWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLUniformGridAMRReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLUniformGridAMRWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLUnstructuredDataReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLUnstructuredDataWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLUnstructuredGridReader.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLUnstructuredGridWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLWriter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/IO/XML/vtkXMLWriterC.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/IO/XML/vtkIOXMLModule.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/vtk/hierarchy/VTK" TYPE FILE RENAME "vtkIOXML-hierarchy.txt" FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/vtk/hierarchy/VTK/vtkIOXML-hierarchy.txt")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Debug/vtkIOXML-9.0d.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Release/vtkIOXML-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/MinSizeRel/vtkIOXML-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/RelWithDebInfo/vtkIOXML-9.0.lib")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Debug/vtkIOXML-9.0d.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Release/vtkIOXML-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/MinSizeRel/vtkIOXML-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/RelWithDebInfo/vtkIOXML-9.0.dll")
  endif()
endif()


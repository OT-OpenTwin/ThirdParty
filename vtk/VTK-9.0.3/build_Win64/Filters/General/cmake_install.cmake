# Install script for directory: C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General

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
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkAnnotationLink.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkAppendLocationAttributes.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkAppendPoints.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkApproximatingSubdivisionFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkAreaContourSpectrumFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkAxes.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkBlankStructuredGrid.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkBlankStructuredGridWithImage.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkBlockIdScalars.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkBooleanOperationPolyDataFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkBoxClipDataSet.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkBrownianPoints.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCellDerivatives.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCellTreeLocator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCellValidator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkClipClosedSurface.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkClipConvexPolyData.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkClipDataSet.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkClipVolume.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCoincidentPoints.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkContourTriangulator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCountFaces.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCountVertices.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCursor2D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCursor3D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkCurvatures.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDataSetGradient.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDataSetGradientPrecompute.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDataSetTriangleFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDateToNumeric.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDeformPointSet.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDensifyPolyData.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDicer.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDiscreteFlyingEdges2D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDiscreteFlyingEdges3D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDiscreteFlyingEdgesClipper2D.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDiscreteMarchingCubes.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkDistancePolyDataFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkEdgePoints.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkExtractArray.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkExtractSelectedFrustum.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkExtractSelectionBase.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkGradientFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkGraphLayoutFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkGraphToPoints.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkGraphWeightEuclideanDistanceFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkGraphWeightFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkHierarchicalDataLevelFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkHyperStreamline.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkIconGlyphFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkImageDataToPointSet.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkImageMarchingCubes.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkInterpolateDataSetAttributes.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkInterpolatingSubdivisionFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkIntersectionPolyDataFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkLevelIdScalars.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkLinkEdgels.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkLoopBooleanPolyDataFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMarchingContourFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMatricizeArray.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMergeArrays.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMergeCells.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMultiBlockDataGroupFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMultiBlockFromTimeSeriesFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMultiBlockMergeFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkMultiThreshold.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkNormalizeMatrixVectors.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkOBBDicer.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkOBBTree.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkOverlappingAMRLevelIdScalars.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkPassArrays.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkPassSelectedArrays.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkPassThrough.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkPointConnectivityFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkPolyDataStreamer.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkPolyDataToReebGraphFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkProbePolyhedron.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkQuadraturePointInterpolator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkQuadraturePointsGenerator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkQuadratureSchemeDictionaryGenerator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkQuantizePolyDataPoints.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkRandomAttributeGenerator.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkRectilinearGridClip.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkRectilinearGridToPointSet.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkRectilinearGridToTetrahedra.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkRecursiveDividingCubes.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkReflectionFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkRotationFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSampleImplicitFunctionFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkShrinkFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkShrinkPolyData.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSpatialRepresentationFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSplineFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSplitByCellScalarFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSplitColumnComponents.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSplitField.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkStructuredGridClip.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSubPixelPositionEdgels.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSubdivisionFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkSynchronizeTimeFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTableBasedClipDataSet.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTableToPolyData.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTableToStructuredGrid.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTemporalPathLineFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTemporalStatistics.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTessellatorFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTimeSourceExample.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTransformFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkTransformPolyDataFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkUncertaintyTubeFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkVertexGlyphFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkVolumeContourSpectrumFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkVoxelContoursToSurfaceFilter.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkWarpLens.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkWarpScalar.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkWarpTo.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkWarpVector.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/Filters/General/vtkYoungsMaterialInterface.h"
    "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/Filters/General/vtkFiltersGeneralModule.h"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/vtk/hierarchy/VTK" TYPE FILE RENAME "vtkFiltersGeneral-hierarchy.txt" FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/vtk/hierarchy/VTK/vtkFiltersGeneral-hierarchy.txt")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevelopmentx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Debug/vtkFiltersGeneral-9.0d.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/Release/vtkFiltersGeneral-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/MinSizeRel/vtkFiltersGeneral-9.0.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/lib/RelWithDebInfo/vtkFiltersGeneral-9.0.lib")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xruntimex" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Debug/vtkFiltersGeneral-9.0d.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/Release/vtkFiltersGeneral-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/MinSizeRel/vtkFiltersGeneral-9.0.dll")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/vtk/VTK-9.0.3/build_Win64/bin/RelWithDebInfo/vtkFiltersGeneral-9.0.dll")
  endif()
endif()


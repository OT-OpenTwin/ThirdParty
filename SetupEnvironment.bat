REM @ECHO OFF
REM This script requires the following environment variables to be set:
REM 1. OPENTWIN_THIRDPARTY_ROOT

REM Ensure that the setup will only be performed once
if "%OPENTWIN_THIRDPARTY_ENV_DEFINED%"=="1" (
	goto END
)

SET OPENTWIN_THIRDPARTY_ENV_DEFINED=1

IF "%OPENTWIN_THIRDPARTY_ROOT%" == "" (
	ECHO Please specify the following environment variables: OPENTWIN_THIRDPARTY_ROOT
	goto END
)

REM Set Qt Environment 
SET QDIR=%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64
SET QTDIR=%QDIR%
SET QT_DLLR=%QDIR%\bin
SET QT_DLLD=%QDIR%\bin
SET QT_INC=%QDIR%\include


REM Set QWT and QWT wrapper Environment
SET QWT_LIB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\qwt\qwt-6.2.0
SET QWT_LIB_INCD=%QWT_LIB_ROOT%\src
SET QWT_LIB_INCR=%QWT_LIB_ROOT%\src
SET QWT_LIB_LIBD=qwtd.lib
SET QWT_LIB_LIBR=qwt.lib
SET QWT_LIB_LIBPATHD=%QWT_LIB_ROOT%\lib
SET QWT_LIB_LIBPATHR=%QWT_LIB_ROOT%\lib
SET QWT_LIB_DLLD=%QWT_LIB_ROOT%\lib
SET QWT_LIB_DLLR=%QWT_LIB_ROOT%\lib

REM QwtPolar is now part of Qwt (since Qwt6.2)
REM SET QWTPOLAR_LIB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\qwtpolar\qwtpolar-1.1.1
REM SET QWTPOLAR_LIB_INCD=%QWTPOLAR_LIB_ROOT%\src
REM SET QWTPOLAR_LIB_INCR=%QWTPOLAR_LIB_ROOT%\src
REM SET QWTPOLAR_LIB_LIBD=qwtpolard.lib
REM SET QWTPOLAR_LIB_LIBR=qwtpolar.lib
REM SET QWTPOLAR_LIB_LIBPATHD=%QWTPOLAR_LIB_ROOT%\lib
REM SET QWTPOLAR_LIB_LIBPATHR=%QWTPOLAR_LIB_ROOT%\lib
REM SET QWTPOLAR_LIB_DLLD=%QWTPOLAR_LIB_ROOT%\lib
REM SET QWTPOLAR_LIB_DLLR=%QWTPOLAR_LIB_ROOT%\lib

REM Set Open Scene Graph (OSG) Root Directory
SET OSG_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenSceneGraph\OpenSceneGraph-OpenSceneGraph-3.6.3
SET OSG_INCD=%OSG_ROOT%\include
SET OSG_INCR=%OSG_ROOT%\include
SET OSG_LIBD=OpenThreadsd.lib;osgAnimationd.lib;osgd.lib;osgDBd.lib;osgFXd.lib;osgGAd.lib;osgManipulatord.lib;osgParticled.lib;osgPresentationd.lib;osgQt5d.lib;osgShadowd.lib;osgSimd.lib;osgTerraind.lib;osgTextd.lib;osgUId.lib;osgUtild.lib;osgViewerd.lib;osgVolumed.lib;osgWidgetd.lib;
SET OSG_LIBR=OpenThreads.lib;osgAnimation.lib;osg.lib;osgDB.lib;osgFX.lib;osgGA.lib;osgManipulator.lib;osgParticle.lib;osgPresentation.lib;osgQt5.lib;osgShadow.lib;osgSim.lib;osgTerrain.lib;osgText.lib;osgUI.lib;osgUtil.lib;osgViewer.lib;osgVolume.lib;osgWidget.lib;
SET OSG_LIBPATHD=%OSG_ROOT%\lib\Debug
SET OSG_LIBPATHR=%OSG_ROOT%\lib\Release
SET OSG_DLLD=%OSG_ROOT%\bin\Debug
SET OSG_DLLR=%OSG_ROOT%\bin\Release

REM Set Open Cascade Root Directory
SET OC_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\opencascade-7.5.0
SET OC_INCD=%OC_ROOT%\inc
SET OC_INCR=%OC_ROOT%\inc
SET OC_LIBPATHD=%OC_ROOT%\win64\vc14\lib
SET OC_LIBPATHR=%OC_ROOT%\win64\vc14\lib
SET OC_DLLD=%OC_ROOT%\win64\vc14\bin
SET OC_DLLR=%OC_ROOT%\win64\vc14\bin

SET TBB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\tbb_2017.0.100
SET TBB_DLLR=%TBB_ROOT%\bin\intel64\vc14

SET FRI_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\freeimage-3.17.0-vc14-64
SET FRI_DLLR=%FRI_ROOT%\bin

SET FRT_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\freetype-2.5.5-vc14-64
SET FRT_DLLR=%FRT_ROOT%\bin

SET FMP_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\ffmpeg-3.3.4-64
SET FMP_DLLR=%FMP_ROOT%\bin

SET OVR_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\openvr-1.14.15-64
SET OVR_DLLR=%OVR_ROOT%\bin\win64

SET CFG_OC_LIBS=TKBin.lib;TKBinL.lib;TKBinTObj.lib;TKBinXCAF.lib;TKBO.lib;TKBool.lib;TKBRep.lib;TKCAF.lib;TKCDF.lib;TKD3DHost.lib;TKDCAF.lib;TKDFBrowser.lib;TKDraw.lib;TKernel.lib;TKFeat.lib;TKFillet.lib;TKG2d.lib;TKG3d.lib;TKGeomAlgo.lib;TKGeomBase.lib;TKHLR.lib;TKIGES.lib;TKIVtk.lib;TKIVtkDraw.lib;TKLCAF.lib;TKMath.lib;TKMesh.lib;TKMeshVS.lib;TKOffset.lib;TKOpenGl.lib;TKPrim.lib;TKQADraw.lib;TKService.lib;TKShapeView.lib;TKShHealing.lib;TKStd.lib;TKStdL.lib;TKSTEP.lib;TKSTEP209.lib;TKSTEPAttr.lib;TKSTEPBase.lib;TKSTL.lib;TKTInspector.lib;TKTInspectorAPI.lib;TKTObj.lib;TKTObjDRAW.lib;TKToolsDraw.lib;TKTopAlgo.lib;TKTopTest.lib;TKTreeModel.lib;TKV3d.lib;TKVCAF.lib;TKView.lib;TKViewerTest.lib;TKVInspector.lib;TKVRML.lib;TKXCAF.lib;TKXDEDRAW.lib;TKXDEIGES.lib;TKXDESTEP.lib;TKXMesh.lib;TKXml.lib;TKXmlL.lib;TKXmlTObj.lib;TKXmlXCAF.lib;TKXSBase.lib;TKXSDRAW.lib
SET CFG_OC_DLLS=$(OC_ROOT)\win64\vc14\bin\TKBin.dll;$(OC_ROOT)\win64\vc14\bin\TKBinL.dll;$(OC_ROOT)\win64\vc14\bin\TKBinTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKBinXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKBO.dll;$(OC_ROOT)\win64\vc14\bin\TKBool.dll;$(OC_ROOT)\win64\vc14\bin\TKBRep.dll;$(OC_ROOT)\win64\vc14\bin\TKCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKCDF.dll;$(OC_ROOT)\win64\vc14\bin\TKD3DHost.dll;$(OC_ROOT)\win64\vc14\bin\TKDCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKDFBrowser.dll;$(OC_ROOT)\win64\vc14\bin\TKDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKernel.dll;$(OC_ROOT)\win64\vc14\bin\TKFeat.dll;$(OC_ROOT)\win64\vc14\bin\TKFillet.dll;$(OC_ROOT)\win64\vc14\bin\TKG2d.dll;$(OC_ROOT)\win64\vc14\bin\TKG3d.dll;$(OC_ROOT)\win64\vc14\bin\TKGeomAlgo.dll;$(OC_ROOT)\win64\vc14\bin\TKGeomBase.dll;$(OC_ROOT)\win64\vc14\bin\TKHLR.dll;$(OC_ROOT)\win64\vc14\bin\TKIGES.dll;$(OC_ROOT)\win64\vc14\bin\TKIVtk.dll;$(OC_ROOT)\win64\vc14\bin\TKIVtkDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKLCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKMath.dll;$(OC_ROOT)\win64\vc14\bin\TKMesh.dll;$(OC_ROOT)\win64\vc14\bin\TKMeshVS.dll;$(OC_ROOT)\win64\vc14\bin\TKOffset.dll;$(OC_ROOT)\win64\vc14\bin\TKOpenGl.dll;$(OC_ROOT)\win64\vc14\bin\TKPrim.dll;$(OC_ROOT)\win64\vc14\bin\TKQADraw.dll;$(OC_ROOT)\win64\vc14\bin\TKService.dll;$(OC_ROOT)\win64\vc14\bin\TKShapeView.dll;$(OC_ROOT)\win64\vc14\bin\TKShHealing.dll;$(OC_ROOT)\win64\vc14\bin\TKStd.dll;$(OC_ROOT)\win64\vc14\bin\TKStdL.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEP.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEP209.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEPAttr.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEPBase.dll;$(OC_ROOT)\win64\vc14\bin\TKSTL.dll;$(OC_ROOT)\win64\vc14\bin\TKTInspector.dll;$(OC_ROOT)\win64\vc14\bin\TKTInspectorAPI.dll;$(OC_ROOT)\win64\vc14\bin\TKTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKTObjDRAW.dll;$(OC_ROOT)\win64\vc14\bin\TKToolsDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKTopAlgo.dll;$(OC_ROOT)\win64\vc14\bin\TKTopTest.dll;$(OC_ROOT)\win64\vc14\bin\TKTreeModel.dll;$(OC_ROOT)\win64\vc14\bin\TKV3d.dll;$(OC_ROOT)\win64\vc14\bin\TKVCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKView.dll;$(OC_ROOT)\win64\vc14\bin\TKViewerTest.dll;$(OC_ROOT)\win64\vc14\bin\TKVInspector.dll;$(OC_ROOT)\win64\vc14\bin\TKVRML.dll;$(OC_ROOT)\win64\vc14\bin\TKXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKXDEDRAW.dll;$(OC_ROOT)\win64\vc14\bin\TKXDEIGES.dll;$(OC_ROOT)\win64\vc14\bin\TKXDESTEP.dll;$(OC_ROOT)\win64\vc14\bin\TKXMesh.dll;$(OC_ROOT)\win64\vc14\bin\TKXml.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlL.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKXSBase.dll;$(OC_ROOT)\win64\vc14\bin\TKXSDRAW.dll

REM Set Tab Toolbar Root Directory
SET QT_TT_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\QtTabToolbar
SET QT_TT_INCD=%QT_TT_ROOT%\include
SET QT_TT_INCR=%QT_TT_ROOT%\include
SET QT_TT_LIBD=TabToolbard.lib
SET QT_TT_LIBR=TabToolbar.lib
SET QT_TT_LIBPATHD=%QT_TT_ROOT%\src\TabToolbar\Debug
SET QT_TT_LIBPATHR=%QT_TT_ROOT%\src\TabToolbar\Release
SET QT_TT_DLLD=%QT_TT_ROOT%\src\TabToolbar\Debug
SET QT_TT_DLLR=%QT_TT_ROOT%\src\TabToolbar\Release

REM Set Rapid JSON Directory
SET R_JSON_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\rapidjson
SET R_JSON_INCD=%R_JSON_ROOT%\include
SET R_JSON_INCR=%R_JSON_ROOT%\include

REM Set Gmsh Root Directory
SET GMSH_ROOT_INC=%OPENTWIN_THIRDPARTY_ROOT%\gmsh\gmsh-4.8.0\api
SET GMSH_ROOT_BIN=%OPENTWIN_THIRDPARTY_ROOT%\gmsh\gmsh-4.8.0\build_win64\Release

REM Set MongoDb Directory
SET MONGO_C_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\MongoDb\mongo-c-1.21.0\x64
SET MONGO_C_INCD=%MONGO_C_ROOT%\Debug\include
SET MONGO_C_INCR=%MONGO_C_ROOT%\Release\include
SET MONGO_C_LIBPATHD=%MONGO_C_ROOT%\Debug\lib
SET MONGO_C_LIBPATHR=%MONGO_C_ROOT%\Release\lib
SET MONGO_C_LIBD=bson-1.0.lib;mongoc-1.0.lib
SET MONGO_C_LIBR=bson-1.0.lib;mongoc-1.0.lib
SET MONGO_C_DLLD=%MONGO_C_ROOT%\Debug\bin
SET MONGO_C_DLLR=%MONGO_C_ROOT%\Release\bin

SET MONGO_CXX_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\MongoDb\mongo-cxx-r3.6.6\x64
SET MONGO_CXX_INCD=%MONGO_CXX_ROOT%\Debug\include
SET MONGO_CXX_INCR=%MONGO_CXX_ROOT%\Release\include
SET MONGO_CXX_LIBPATHD=%MONGO_CXX_ROOT%\Debug\lib
SET MONGO_CXX_LIBPATHR=%MONGO_CXX_ROOT%\Release\lib
SET MONGO_CXX_LIBD=bsoncxx.lib;mongocxx.lib
SET MONGO_CXX_LIBR=bsoncxx.lib;mongocxx.lib
SET MONGO_CXX_DLLD=%MONGO_CXX_ROOT%\Debug\bin
SET MONGO_CXX_DLLR=%MONGO_CXX_ROOT%\Release\bin

SET MONGO_BOOST_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\MongoDb\boost-1.72.0\

REM Set VTK Directory
SET VTK_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\vtk\VTK-9.0.3
SET VTK_LIB=%VTK_ROOT%\build_Win64\lib\
SET VTK_DLL=%VTK_ROOT%\build_Win64\bin\
SET VTK_DLLR=%VTK_ROOT%\build_Win64\bin\Release
SET VTK_DLLD=%VTK_ROOT%\build_Win64\bin\Debug
SET VTK_DIR=%VTK_ROOT%\build_Win64
SET VTK_DIR=%VTK_DIR:\=/%
SET VTK_INC=$(VTK_ROOT)\Rendering\Core;$(VTK_ROOT)\Filters\Sources;$(VTK_ROOT)\Filters\Core;$(VTK_ROOT)\Filters\Modeling;$(VTK_ROOT)\Filters\Core;$(VTK_ROOT)\Filters\Geometry;$(VTK_ROOT)\Filters\Extraction;$(VTK_ROOT)\Common\Color;$(VTK_ROOT)\Common\Core;$(VTK_ROOT)\Common\Misc;$(VTK_ROOT)\build_Win64\Common\Core;$(VTK_ROOT)\Utilities\KWIML;$(VTK_ROOT)\build_Win64\Utilities\KWIML;$(VTK_ROOT)\build_Win64\Rendering\Core;$(VTK_ROOT)\build_Win64\Filters\Core;$(VTK_ROOT)\Common\DataModel;$(VTK_ROOT)\Common\Math;$(VTK_ROOT)\build_Win64\Filters\Sources;$(VTK_ROOT)\build_Win64\Filters\Modeling;$(VTK_ROOT)\build_Win64\Filters\Geometry;$(VTK_ROOT)\build_Win64\Filters\Extraction;$(VTK_ROOT)\Common\ExecutionModel;$(VTK_ROOT)\build_Win64\Common\ExecutionModel;$(VTK_ROOT)\build_Win64\Common\DataModel;$(VTK_ROOT)\build_Win64\Common\Color;$(VTK_ROOT)\build_Win64\Common\Misc;$(VTK_ROOT)\Rendering\External;$(VTK_ROOT)\Rendering\OpenGL2;$(VTK_ROOT)\build_Win64\Rendering\OpenGL2;$(VTK_ROOT)\build_Win64\Rendering\UI;$(VTK_ROOT)\build_Win64\Rendering\External;$(VTK_ROOT)\Rendering\External;$(VTK_ROOT)\IO\Legacy;$(VTK_ROOT)\build_Win64\IO\Legacy

SET VTK_LIBLIST_RELEASE=vtkChartsCore-9.0.lib;vtkCommonColor-9.0.lib;vtkCommonComputationalGeometry-9.0.lib;vtkCommonCore-9.0.lib;vtkCommonDataModel-9.0.lib;vtkCommonExecutionModel-9.0.lib;vtkCommonMath-9.0.lib;vtkCommonMisc-9.0.lib;vtkCommonSystem-9.0.lib;vtkCommonTransforms-9.0.lib;vtkDICOMParser-9.0.lib;vtkDomainsChemistry-9.0.lib;vtkDomainsChemistryOpenGL2-9.0.lib;vtkdoubleconversion-9.0.lib;vtkexodusII-9.0.lib;vtkexpat-9.0.lib;vtkFiltersAMR-9.0.lib;vtkFiltersCore-9.0.lib;vtkFiltersExtraction-9.0.lib;vtkFiltersFlowPaths-9.0.lib;vtkFiltersGeneral-9.0.lib;vtkFiltersGeneric-9.0.lib;vtkFiltersGeometry-9.0.lib;vtkFiltersHybrid-9.0.lib;vtkFiltersHyperTree-9.0.lib;vtkFiltersImaging-9.0.lib;vtkFiltersGeometry-9.0.lib;vtkFiltersModeling-9.0.lib;vtkFiltersParallel-9.0.lib;vtkFiltersParallelImaging-9.0.lib;vtkFiltersPoints-9.0.lib;vtkFiltersProgrammable-9.0.lib;vtkFiltersSelection-9.0.lib;vtkFiltersSMP-9.0.lib;vtkFiltersSources-9.0.lib;vtkFiltersStatistics-9.0.lib;vtkFiltersTexture-9.0.lib;vtkFiltersTopology-9.0.lib;vtkFiltersVerdict-9.0.lib;vtkfreetype-9.0.lib;vtkGeovisCore-9.0.lib;vtkgl2ps-9.0.lib;vtkglew-9.0.lib;vtkhdf5-9.0.lib;vtkhdf5_hl-9.0.lib;vtkImagingColor-9.0.lib;vtkImagingCore-9.0.lib;vtkImagingFourier-9.0.lib;vtkImagingGeneral-9.0.lib;vtkImagingHybrid-9.0.lib;vtkImagingMath-9.0.lib;vtkImagingMorphological-9.0.lib;vtkImagingSources-9.0.lib;vtkImagingStatistics-9.0.lib;vtkImagingStencil-9.0.lib;vtkInfovisCore-9.0.lib;vtkInfovisLayout-9.0.lib;vtkInteractionImage-9.0.lib;vtkInteractionStyle-9.0.lib;vtkInteractionWidgets-9.0.lib;vtkIOAMR-9.0.lib;vtkIOAsynchronous-9.0.lib;vtkIOCityGML-9.0.lib;vtkIOCore-9.0.lib;vtkIOEnSight-9.0.lib;vtkIOExodus-9.0.lib;vtkIOExport-9.0.lib;vtkIOExportGL2PS-9.0.lib;vtkIOExportPDF-9.0.lib;vtkIOGeometry-9.0.lib;vtkIOImage-9.0.lib;vtkIOImport-9.0.lib;vtkIOInfovis-9.0.lib;vtkIOLegacy-9.0.lib;vtkIOLSDyna-9.0.lib;vtkIOMINC-9.0.lib;vtkIOMotionFX-9.0.lib;vtkIOMovie-9.0.lib;vtkIONetCDF-9.0.lib;vtkIOOggTheora-9.0.lib;vtkIOParallel-9.0.lib;vtkIOParallelXML-9.0.lib;vtkIOPLY-9.0.lib;vtkIOSegY-9.0.lib;vtkIOSQL-9.0.lib;vtkIOTecplotTable-9.0.lib;vtkIOVeraOut-9.0.lib;vtkIOVideo-9.0.lib;vtkIOXML-9.0.lib;vtkIOXMLParser-9.0.lib;vtkjpeg-9.0.lib;vtkjsoncpp-9.0.lib;vtklibharu-9.0.lib;vtklibproj-9.0.lib;vtklibxml2-9.0.lib;vtkloguru-9.0.lib;vtklz4-9.0.lib;vtklzma-9.0.lib;vtkmetaio-9.0.lib;vtknetcdf-9.0.lib;vtkogg-9.0.lib;vtkParallelCore-9.0.lib;vtkParallelDIY-9.0.lib;vtkpng-9.0.lib;vtkpugixml-9.0.lib;vtkRenderingAnnotation-9.0.lib;vtkRenderingContext2D-9.0.lib;vtkRenderingContextOpenGL2-9.0.lib;vtkRenderingCore-9.0.lib;vtkRenderingFreeType-9.0.lib;vtkRenderingGL2PSOpenGL2-9.0.lib;vtkRenderingImage-9.0.lib;vtkRenderingLabel-9.0.lib;vtkRenderingLOD-9.0.lib;vtkRenderingOpenGL2-9.0.lib;vtkRenderingSceneGraph-9.0.lib;vtkRenderingUI-9.0.lib;vtkRenderingVolume-9.0.lib;vtkRenderingVolumeOpenGL2-9.0.lib;vtkRenderingVtkJS-9.0.lib;vtksqlite-9.0.lib;vtksys-9.0.lib;vtkTestingRendering-9.0.lib;vtktheora-9.0.lib;vtktiff-9.0.lib;vtkverdict-9.0.lib;vtkViewsContext2D-9.0.lib;vtkViewsCore-9.0.lib;vtkViewsInfovis-9.0.lib;vtkWrappingTools-9.0.lib;vtkzlib-9.0.lib

SET VTK_LIBLIST_DEBUG=vtkChartsCore-9.0d.lib;vtkCommonColor-9.0d.lib;vtkCommonComputationalGeometry-9.0d.lib;vtkCommonCore-9.0d.lib;vtkCommonDataModel-9.0d.lib;vtkCommonExecutionModel-9.0d.lib;vtkCommonMath-9.0d.lib;vtkCommonMisc-9.0d.lib;vtkCommonSystem-9.0d.lib;vtkCommonTransforms-9.0d.lib;vtkDICOMParser-9.0d.lib;vtkDomainsChemistry-9.0d.lib;vtkDomainsChemistryOpenGL2-9.0d.lib;vtkdoubleconversion-9.0d.lib;vtkexodusII-9.0d.lib;vtkexpat-9.0d.lib;vtkFiltersAMR-9.0d.lib;vtkFiltersCore-9.0d.lib;vtkFiltersExtraction-9.0d.lib;vtkFiltersFlowPaths-9.0d.lib;vtkFiltersGeneral-9.0d.lib;vtkFiltersGeneric-9.0d.lib;vtkFiltersGeometry-9.0d.lib;vtkFiltersHybrid-9.0d.lib;vtkFiltersHyperTree-9.0d.lib;vtkFiltersImaging-9.0d.lib;vtkFiltersModeling-9.0d.lib;vtkFiltersParallel-9.0d.lib;vtkFiltersParallelImaging-9.0d.lib;vtkFiltersPoints-9.0d.lib;vtkFiltersProgrammable-9.0d.lib;vtkFiltersSelection-9.0d.lib;vtkFiltersSMP-9.0d.lib;vtkFiltersSources-9.0d.lib;vtkFiltersStatistics-9.0d.lib;vtkFiltersTexture-9.0d.lib;vtkFiltersTopology-9.0d.lib;vtkFiltersVerdict-9.0d.lib;vtkfreetype-9.0d.lib;vtkGeovisCore-9.0d.lib;vtkgl2ps-9.0d.lib;vtkglew-9.0d.lib;vtkhdf5-9.0d.lib;vtkhdf5_hl-9.0d.lib;vtkImagingColor-9.0d.lib;vtkImagingCore-9.0d.lib;vtkImagingFourier-9.0d.lib;vtkImagingGeneral-9.0d.lib;vtkImagingHybrid-9.0d.lib;vtkImagingMath-9.0d.lib;vtkImagingMorphological-9.0d.lib;vtkImagingSources-9.0d.lib;vtkImagingStatistics-9.0d.lib;vtkImagingStencil-9.0d.lib;vtkInfovisCore-9.0d.lib;vtkInfovisLayout-9.0d.lib;vtkInteractionImage-9.0d.lib;vtkInteractionStyle-9.0d.lib;vtkInteractionWidgets-9.0d.lib;vtkIOAMR-9.0d.lib;vtkIOAsynchronous-9.0d.lib;vtkIOCityGML-9.0d.lib;vtkIOCore-9.0d.lib;vtkIOEnSight-9.0d.lib;vtkIOExodus-9.0d.lib;vtkIOExport-9.0d.lib;vtkIOExportGL2PS-9.0d.lib;vtkIOExportPDF-9.0d.lib;vtkIOGeometry-9.0d.lib;vtkIOImage-9.0d.lib;vtkIOImport-9.0d.lib;vtkIOInfovis-9.0d.lib;vtkIOLegacy-9.0d.lib;vtkIOLSDyna-9.0d.lib;vtkIOMINC-9.0d.lib;vtkIOMotionFX-9.0d.lib;vtkIOMovie-9.0d.lib;vtkIONetCDF-9.0d.lib;vtkIOOggTheora-9.0d.lib;vtkIOParallel-9.0d.lib;vtkIOParallelXML-9.0d.lib;vtkIOPLY-9.0d.lib;vtkIOSegY-9.0d.lib;vtkIOSQL-9.0d.lib;vtkIOTecplotTable-9.0d.lib;vtkIOVeraOut-9.0d.lib;vtkIOVideo-9.0d.lib;vtkIOXML-9.0d.lib;vtkIOXMLParser-9.0d.lib;vtkjpeg-9.0d.lib;vtkjsoncpp-9.0d.lib;vtklibharu-9.0d.lib;vtklibproj-9.0d.lib;vtklibxml2-9.0d.lib;vtkloguru-9.0d.lib;vtklz4-9.0d.lib;vtklzma-9.0d.lib;vtkmetaio-9.0d.lib;vtknetcdf-9.0d.lib;vtkogg-9.0d.lib;vtkParallelCore-9.0d.lib;vtkParallelDIY-9.0d.lib;vtkpng-9.0d.lib;vtkpugixml-9.0d.lib;vtkRenderingAnnotation-9.0d.lib;vtkRenderingContext2D-9.0d.lib;vtkRenderingContextOpenGL2-9.0d.lib;vtkRenderingCore-9.0d.lib;vtkRenderingFreeType-9.0d.lib;vtkRenderingGL2PSOpenGL2-9.0d.lib;vtkRenderingImage-9.0d.lib;vtkRenderingLabel-9.0d.lib;vtkRenderingLOD-9.0d.lib;vtkRenderingOpenGL2-9.0d.lib;vtkRenderingSceneGraph-9.0d.lib;vtkRenderingUI-9.0d.lib;vtkRenderingVolume-9.0d.lib;vtkRenderingVolumeOpenGL2-9.0d.lib;vtkRenderingVtkJS-9.0d.lib;vtksqlite-9.0d.lib;vtksys-9.0d.lib;vtkTestingRendering-9.0d.lib;vtktheora-9.0d.lib;vtktiff-9.0d.lib;vtkverdict-9.0d.lib;vtkViewsContext2D-9.0d.lib;vtkViewsCore-9.0d.lib;vtkViewsInfovis-9.0d.lib;vtkWrappingTools-9.0d.lib;vtkzlib-9.0d.lib

REM Set CURL Directory
SET CURL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\curl\curl-7.62.0
SET CURL_INCD=%CURL_ROOT%\build-win-x64\Debug\include
SET CURL_INCR=%CURL_ROOT%\build-win-x64\Release\include
SET CURL_LIBD=libcurl_debug.lib
SET CURL_LIBR=libcurl.lib
SET CURL_LIBPATHD=%CURL_ROOT%\build-win-x64\Debug\lib
SET CURL_LIBPATHR=%CURL_ROOT%\build-win-x64\Release\lib
SET CURL_DLLD=%CURL_ROOT%\build-win-x64\Debug\bin
SET CURL_DLLR=%CURL_ROOT%\build-win-x64\Release\bin

REM Set OpenSSL Directory
SET OPENSSL_WEBSOCKET_DLLR=%OPENTWIN_THIRDPARTY_ROOT%\OpenSSL\LibsForQtWebsocket
SET OPENSSL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenSSL\OpenSSL-1.1.1
SET OPENSSL_DLL=%OPENSSL_ROOT%\build-win-x64\dll\x64\Release\bin

REM Set BASE64 Directory
SET BASE64_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\base64

REM Set ZLIB Directory
SET ZLIB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\zlib\zlib-1.2.11\x64
SET ZLIB_INCD=%ZLIB_ROOT%\Debug\include
SET ZLIB_INCR=%ZLIB_ROOT%\Release\include
SET ZLIB_LIBPATHD=%ZLIB_ROOT%\Debug\lib
SET ZLIB_LIBPATHR=%ZLIB_ROOT%\Release\lib
SET ZLIB_LIBD=zlibd.lib
SET ZLIB_LIBR=zlib.lib
SET ZLIB_DLLPATHD=%ZLIB_ROOT%\Debug\bin
SET ZLIB_DLLPATHR=%ZLIB_ROOT%\Release\bin

REM Set EMBREE Directory
SET EMBREE_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\embree\embree-3.13.0\windows
SET EMBREE_INCD=%EMBREE_ROOT%\include
SET EMBREE_INCR=%EMBREE_ROOT%\include
SET EMBREE_LIBPATHD=%EMBREE_ROOT%\lib
SET EMBREE_LIBPATHR=%EMBREE_ROOT%\lib
SET EMBREE_BIN=%EMBREE_ROOT%\bin

REM Set Python Directory
SET PYTHON310_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\Python\Python310
SET PYTHON310_INC=%PYTHON310_ROOT%\include

SET PYTHON_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64
SET PYTHONPATH=%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64;%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64\Scripts
SET PYTHON_INCD=%PYTHON_ROOT%/include
SET PYTHON_INCR=%PYTHON_ROOT%/include
SET PYTHON_LIBPATHD=%PYTHON_ROOT%/libs
SET PYTHON_LIBPATHR=%PYTHON_ROOT%/libs

SET PATH=%PYTHONPATH%;%PATH%

REM Set CGAL Directory
SET CGAL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\CGAL\CGAL-5.3
SET CGAL_INCD=%CGAL_ROOT%\include
SET CGAL_INCR=%CGAL_ROOT%\include
SET GMP_INCD=%CGAL_ROOT%\auxiliary\gmp\include
SET GMP_INCR=%CGAL_ROOT%\auxiliary\gmp\include
SET GMP_LIBPATHD=%CGAL_ROOT%\auxiliary\gmp\lib
SET GMP_LIBPATHR=%CGAL_ROOT%\auxiliary\gmp\lib
SET GMP_DLLPATHD=%CGAL_ROOT%\auxiliary\gmp\lib
SET GMP_DLLPATHR=%CGAL_ROOT%\auxiliary\gmp\lib

REM Set Boost Directory
SET BOOST_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\boost\boost_1_71_0
SET BOOST_INCD=%BOOST_ROOT%
SET BOOST_INCR=%BOOST_ROOT%
SET BOOST_LIBPATHD=%BOOST_ROOT%\lib64-msvc-14.1
SET BOOST_LIBPATHR=%BOOST_ROOT%\lib64-msvc-14.1
SET BOOST_DLLPATHD=%BOOST_ROOT%\lib64-msvc-14.1
SET BOOST_DLLPATHR=%BOOST_ROOT%\lib64-msvc-14.1

REM Set Expression Evaluator Directory
SET EXPREVAL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\tinyexpr
SET EXPREVAL_INC=%EXPREVAL_ROOT%

REM Set Google Test Directories
SET GOOGLE_TEST_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\GoogleTest
SET GOOGLE_TEST_INC=%GOOGLE_TEST_ROOT%\googletest\include
SET GOOGLE_TEST_LIBPATHD=%GOOGLE_TEST_ROOT%\build\x64-Debug\lib
SET GOOGLE_TEST_LIBPATHR=%GOOGLE_TEST_ROOT%\build\x64-Release\lib
SET GOOGLE_TEST_LIB=gtest_main.lib;gtest.lib

REM Set GETDP Directory
SET GETDP_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\getdp
SET GETDP_BIN=%GETDP_ROOT%\Windows

REM SET NGSpice Directory
SET NGSPICE_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\mySpice\ngspice-41

REM Set VisualStudio Redist Directory
SET VC_REDIST_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\VisualStudioRuntime

REM Set Apache Directory
SET APACHE_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\Apache\Apache24\Windows

REM Set Certificate creation tools Directory
SET CERT_CREATE_TOOLS=%OPENTWIN_THIRDPARTY_ROOT%\CertificateCreation

ECHO OpenTwin Third Party environment was set up successfully.

:END


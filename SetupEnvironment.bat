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
SET QDIR=%OPENTWIN_THIRDPARTY_ROOT%\Qt\5.11.2\msvc2017_64
SET QTDIR=%QDIR%

REM Set QWT and QWT wrapper Environment
SET QWT_LIB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\qwt\qwt-6.1.4
SET QWT_POLAR_LIB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\qwtpolar\qwtpolar-1.1.1

REM Set Open Scene Graph (OSG) Root Directory
SET OSG_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenSceneGraph\OpenSceneGraph-OpenSceneGraph-3.6.3

REM Set Open Cascade Root Directory
SET OC_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\opencascade-7.5.0
SET TBB_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\tbb_2017.0.100
SET FRI_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\freeimage-3.17.0-vc14-64
SET FRT_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\freetype-2.5.5-vc14-64
SET FMP_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.5.0-vc14-64\ffmpeg-3.3.4-64

SET CFG_OC_LIBS=TKBin.lib;TKBinL.lib;TKBinTObj.lib;TKBinXCAF.lib;TKBO.lib;TKBool.lib;TKBRep.lib;TKCAF.lib;TKCDF.lib;TKD3DHost.lib;TKDCAF.lib;TKDFBrowser.lib;TKDraw.lib;TKernel.lib;TKFeat.lib;TKFillet.lib;TKG2d.lib;TKG3d.lib;TKGeomAlgo.lib;TKGeomBase.lib;TKHLR.lib;TKIGES.lib;TKIVtk.lib;TKIVtkDraw.lib;TKLCAF.lib;TKMath.lib;TKMesh.lib;TKMeshVS.lib;TKOffset.lib;TKOpenGl.lib;TKPrim.lib;TKQADraw.lib;TKService.lib;TKShapeView.lib;TKShHealing.lib;TKStd.lib;TKStdL.lib;TKSTEP.lib;TKSTEP209.lib;TKSTEPAttr.lib;TKSTEPBase.lib;TKSTL.lib;TKTInspector.lib;TKTInspectorAPI.lib;TKTObj.lib;TKTObjDRAW.lib;TKToolsDraw.lib;TKTopAlgo.lib;TKTopTest.lib;TKTreeModel.lib;TKV3d.lib;TKVCAF.lib;TKView.lib;TKViewerTest.lib;TKVInspector.lib;TKVRML.lib;TKXCAF.lib;TKXDEDRAW.lib;TKXDEIGES.lib;TKXDESTEP.lib;TKXMesh.lib;TKXml.lib;TKXmlL.lib;TKXmlTObj.lib;TKXmlXCAF.lib;TKXSBase.lib;TKXSDRAW.lib
SET CFG_OC_DLLS=$(OC_ROOT)\win64\vc14\bin\TKBin.dll;$(OC_ROOT)\win64\vc14\bin\TKBinL.dll;$(OC_ROOT)\win64\vc14\bin\TKBinTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKBinXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKBO.dll;$(OC_ROOT)\win64\vc14\bin\TKBool.dll;$(OC_ROOT)\win64\vc14\bin\TKBRep.dll;$(OC_ROOT)\win64\vc14\bin\TKCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKCDF.dll;$(OC_ROOT)\win64\vc14\bin\TKD3DHost.dll;$(OC_ROOT)\win64\vc14\bin\TKDCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKDFBrowser.dll;$(OC_ROOT)\win64\vc14\bin\TKDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKernel.dll;$(OC_ROOT)\win64\vc14\bin\TKFeat.dll;$(OC_ROOT)\win64\vc14\bin\TKFillet.dll;$(OC_ROOT)\win64\vc14\bin\TKG2d.dll;$(OC_ROOT)\win64\vc14\bin\TKG3d.dll;$(OC_ROOT)\win64\vc14\bin\TKGeomAlgo.dll;$(OC_ROOT)\win64\vc14\bin\TKGeomBase.dll;$(OC_ROOT)\win64\vc14\bin\TKHLR.dll;$(OC_ROOT)\win64\vc14\bin\TKIGES.dll;$(OC_ROOT)\win64\vc14\bin\TKIVtk.dll;$(OC_ROOT)\win64\vc14\bin\TKIVtkDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKLCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKMath.dll;$(OC_ROOT)\win64\vc14\bin\TKMesh.dll;$(OC_ROOT)\win64\vc14\bin\TKMeshVS.dll;$(OC_ROOT)\win64\vc14\bin\TKOffset.dll;$(OC_ROOT)\win64\vc14\bin\TKOpenGl.dll;$(OC_ROOT)\win64\vc14\bin\TKPrim.dll;$(OC_ROOT)\win64\vc14\bin\TKQADraw.dll;$(OC_ROOT)\win64\vc14\bin\TKService.dll;$(OC_ROOT)\win64\vc14\bin\TKShapeView.dll;$(OC_ROOT)\win64\vc14\bin\TKShHealing.dll;$(OC_ROOT)\win64\vc14\bin\TKStd.dll;$(OC_ROOT)\win64\vc14\bin\TKStdL.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEP.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEP209.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEPAttr.dll;$(OC_ROOT)\win64\vc14\bin\TKSTEPBase.dll;$(OC_ROOT)\win64\vc14\bin\TKSTL.dll;$(OC_ROOT)\win64\vc14\bin\TKTInspector.dll;$(OC_ROOT)\win64\vc14\bin\TKTInspectorAPI.dll;$(OC_ROOT)\win64\vc14\bin\TKTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKTObjDRAW.dll;$(OC_ROOT)\win64\vc14\bin\TKToolsDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKTopAlgo.dll;$(OC_ROOT)\win64\vc14\bin\TKTopTest.dll;$(OC_ROOT)\win64\vc14\bin\TKTreeModel.dll;$(OC_ROOT)\win64\vc14\bin\TKV3d.dll;$(OC_ROOT)\win64\vc14\bin\TKVCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKView.dll;$(OC_ROOT)\win64\vc14\bin\TKViewerTest.dll;$(OC_ROOT)\win64\vc14\bin\TKVInspector.dll;$(OC_ROOT)\win64\vc14\bin\TKVRML.dll;$(OC_ROOT)\win64\vc14\bin\TKXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKXDEDRAW.dll;$(OC_ROOT)\win64\vc14\bin\TKXDEIGES.dll;$(OC_ROOT)\win64\vc14\bin\TKXDESTEP.dll;$(OC_ROOT)\win64\vc14\bin\TKXMesh.dll;$(OC_ROOT)\win64\vc14\bin\TKXml.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlL.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKXSBase.dll;$(OC_ROOT)\win64\vc14\bin\TKXSDRAW.dll

REM Set Tab Toolbar Root Directory
SET QT_TT_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\QtTabToolbar

REM Set Rapid JSON Directory
SET R_JSON_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\rapidjson
SET RJSON_INCLUDE=%R_JSON_ROOT%\include

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
SET VTK_DIR=%VTK_ROOT%\build_Win64
SET VTK_DIR=%VTK_DIR:\=/%
SET VTK_INC=$(VTK_ROOT)\Rendering\Core;$(VTK_ROOT)\Filters\Sources;$(VTK_ROOT)\Filters\Core;$(VTK_ROOT)\Filters\Modeling;$(VTK_ROOT)\Filters\Core;$(VTK_ROOT)\Filters\Geometry;$(VTK_ROOT)\Filters\Extraction;$(VTK_ROOT)\Common\Color;$(VTK_ROOT)\Common\Core;$(VTK_ROOT)\Common\Misc;$(VTK_ROOT)\build_Win64\Common\Core;$(VTK_ROOT)\Utilities\KWIML;$(VTK_ROOT)\build_Win64\Utilities\KWIML;$(VTK_ROOT)\build_Win64\Rendering\Core;$(VTK_ROOT)\build_Win64\Filters\Core;$(VTK_ROOT)\Common\DataModel;$(VTK_ROOT)\Common\Math;$(VTK_ROOT)\build_Win64\Filters\Sources;$(VTK_ROOT)\build_Win64\Filters\Modeling;$(VTK_ROOT)\build_Win64\Filters\Geometry;$(VTK_ROOT)\build_Win64\Filters\Extraction;$(VTK_ROOT)\Common\ExecutionModel;$(VTK_ROOT)\build_Win64\Common\ExecutionModel;$(VTK_ROOT)\build_Win64\Common\DataModel;$(VTK_ROOT)\build_Win64\Common\Color;$(VTK_ROOT)\build_Win64\Common\Misc;$(VTK_ROOT)\Rendering\External;$(VTK_ROOT)\Rendering\OpenGL2;$(VTK_ROOT)\build_Win64\Rendering\OpenGL2;$(VTK_ROOT)\build_Win64\Rendering\UI;$(VTK_ROOT)\build_Win64\Rendering\External;$(VTK_ROOT)\Rendering\External;$(VTK_ROOT)\IO\Legacy;$(VTK_ROOT)\build_Win64\IO\Legacy

SET VTK_LIBLIST_RELEASE=vtkChartsCore-9.0.lib;vtkCommonColor-9.0.lib;vtkCommonComputationalGeometry-9.0.lib;vtkCommonCore-9.0.lib;vtkCommonDataModel-9.0.lib;vtkCommonExecutionModel-9.0.lib;vtkCommonMath-9.0.lib;vtkCommonMisc-9.0.lib;vtkCommonSystem-9.0.lib;vtkCommonTransforms-9.0.lib;vtkDICOMParser-9.0.lib;vtkDomainsChemistry-9.0.lib;vtkDomainsChemistryOpenGL2-9.0.lib;vtkdoubleconversion-9.0.lib;vtkexodusII-9.0.lib;vtkexpat-9.0.lib;vtkFiltersAMR-9.0.lib;vtkFiltersCore-9.0.lib;vtkFiltersExtraction-9.0.lib;vtkFiltersFlowPaths-9.0.lib;vtkFiltersGeneral-9.0.lib;vtkFiltersGeneric-9.0.lib;vtkFiltersGeometry-9.0.lib;vtkFiltersHybrid-9.0.lib;vtkFiltersHyperTree-9.0.lib;vtkFiltersImaging-9.0.lib;vtkFiltersGeometry-9.0.lib;vtkFiltersModeling-9.0.lib;vtkFiltersParallel-9.0.lib;vtkFiltersParallelImaging-9.0.lib;vtkFiltersPoints-9.0.lib;vtkFiltersProgrammable-9.0.lib;vtkFiltersSelection-9.0.lib;vtkFiltersSMP-9.0.lib;vtkFiltersSources-9.0.lib;vtkFiltersStatistics-9.0.lib;vtkFiltersTexture-9.0.lib;vtkFiltersTopology-9.0.lib;vtkFiltersVerdict-9.0.lib;vtkfreetype-9.0.lib;vtkGeovisCore-9.0.lib;vtkgl2ps-9.0.lib;vtkglew-9.0.lib;vtkhdf5-9.0.lib;vtkhdf5_hl-9.0.lib;vtkImagingColor-9.0.lib;vtkImagingCore-9.0.lib;vtkImagingFourier-9.0.lib;vtkImagingGeneral-9.0.lib;vtkImagingHybrid-9.0.lib;vtkImagingMath-9.0.lib;vtkImagingMorphological-9.0.lib;vtkImagingSources-9.0.lib;vtkImagingStatistics-9.0.lib;vtkImagingStencil-9.0.lib;vtkInfovisCore-9.0.lib;vtkInfovisLayout-9.0.lib;vtkInteractionImage-9.0.lib;vtkInteractionStyle-9.0.lib;vtkInteractionWidgets-9.0.lib;vtkIOAMR-9.0.lib;vtkIOAsynchronous-9.0.lib;vtkIOCityGML-9.0.lib;vtkIOCore-9.0.lib;vtkIOEnSight-9.0.lib;vtkIOExodus-9.0.lib;vtkIOExport-9.0.lib;vtkIOExportGL2PS-9.0.lib;vtkIOExportPDF-9.0.lib;vtkIOGeometry-9.0.lib;vtkIOImage-9.0.lib;vtkIOImport-9.0.lib;vtkIOInfovis-9.0.lib;vtkIOLegacy-9.0.lib;vtkIOLSDyna-9.0.lib;vtkIOMINC-9.0.lib;vtkIOMotionFX-9.0.lib;vtkIOMovie-9.0.lib;vtkIONetCDF-9.0.lib;vtkIOOggTheora-9.0.lib;vtkIOParallel-9.0.lib;vtkIOParallelXML-9.0.lib;vtkIOPLY-9.0.lib;vtkIOSegY-9.0.lib;vtkIOSQL-9.0.lib;vtkIOTecplotTable-9.0.lib;vtkIOVeraOut-9.0.lib;vtkIOVideo-9.0.lib;vtkIOXML-9.0.lib;vtkIOXMLParser-9.0.lib;vtkjpeg-9.0.lib;vtkjsoncpp-9.0.lib;vtklibharu-9.0.lib;vtklibproj-9.0.lib;vtklibxml2-9.0.lib;vtkloguru-9.0.lib;vtklz4-9.0.lib;vtklzma-9.0.lib;vtkmetaio-9.0.lib;vtknetcdf-9.0.lib;vtkogg-9.0.lib;vtkParallelCore-9.0.lib;vtkParallelDIY-9.0.lib;vtkpng-9.0.lib;vtkpugixml-9.0.lib;vtkRenderingAnnotation-9.0.lib;vtkRenderingContext2D-9.0.lib;vtkRenderingContextOpenGL2-9.0.lib;vtkRenderingCore-9.0.lib;vtkRenderingFreeType-9.0.lib;vtkRenderingGL2PSOpenGL2-9.0.lib;vtkRenderingImage-9.0.lib;vtkRenderingLabel-9.0.lib;vtkRenderingLOD-9.0.lib;vtkRenderingOpenGL2-9.0.lib;vtkRenderingSceneGraph-9.0.lib;vtkRenderingUI-9.0.lib;vtkRenderingVolume-9.0.lib;vtkRenderingVolumeOpenGL2-9.0.lib;vtkRenderingVtkJS-9.0.lib;vtksqlite-9.0.lib;vtksys-9.0.lib;vtkTestingRendering-9.0.lib;vtktheora-9.0.lib;vtktiff-9.0.lib;vtkverdict-9.0.lib;vtkViewsContext2D-9.0.lib;vtkViewsCore-9.0.lib;vtkViewsInfovis-9.0.lib;vtkWrappingTools-9.0.lib;vtkzlib-9.0.lib

SET VTK_LIBLIST_DEBUG=vtkChartsCore-9.0d.lib;vtkCommonColor-9.0d.lib;vtkCommonComputationalGeometry-9.0d.lib;vtkCommonCore-9.0d.lib;vtkCommonDataModel-9.0d.lib;vtkCommonExecutionModel-9.0d.lib;vtkCommonMath-9.0d.lib;vtkCommonMisc-9.0d.lib;vtkCommonSystem-9.0d.lib;vtkCommonTransforms-9.0d.lib;vtkDICOMParser-9.0d.lib;vtkDomainsChemistry-9.0d.lib;vtkDomainsChemistryOpenGL2-9.0d.lib;vtkdoubleconversion-9.0d.lib;vtkexodusII-9.0d.lib;vtkexpat-9.0d.lib;vtkFiltersAMR-9.0d.lib;vtkFiltersCore-9.0d.lib;vtkFiltersExtraction-9.0d.lib;vtkFiltersFlowPaths-9.0d.lib;vtkFiltersGeneral-9.0d.lib;vtkFiltersGeneric-9.0d.lib;vtkFiltersGeometry-9.0d.lib;vtkFiltersHybrid-9.0d.lib;vtkFiltersHyperTree-9.0d.lib;vtkFiltersImaging-9.0d.lib;vtkFiltersModeling-9.0d.lib;vtkFiltersParallel-9.0d.lib;vtkFiltersParallelImaging-9.0d.lib;vtkFiltersPoints-9.0d.lib;vtkFiltersProgrammable-9.0d.lib;vtkFiltersSelection-9.0d.lib;vtkFiltersSMP-9.0d.lib;vtkFiltersSources-9.0d.lib;vtkFiltersStatistics-9.0d.lib;vtkFiltersTexture-9.0d.lib;vtkFiltersTopology-9.0d.lib;vtkFiltersVerdict-9.0d.lib;vtkfreetype-9.0d.lib;vtkGeovisCore-9.0d.lib;vtkgl2ps-9.0d.lib;vtkglew-9.0d.lib;vtkhdf5-9.0d.lib;vtkhdf5_hl-9.0d.lib;vtkImagingColor-9.0d.lib;vtkImagingCore-9.0d.lib;vtkImagingFourier-9.0d.lib;vtkImagingGeneral-9.0d.lib;vtkImagingHybrid-9.0d.lib;vtkImagingMath-9.0d.lib;vtkImagingMorphological-9.0d.lib;vtkImagingSources-9.0d.lib;vtkImagingStatistics-9.0d.lib;vtkImagingStencil-9.0d.lib;vtkInfovisCore-9.0d.lib;vtkInfovisLayout-9.0d.lib;vtkInteractionImage-9.0d.lib;vtkInteractionStyle-9.0d.lib;vtkInteractionWidgets-9.0d.lib;vtkIOAMR-9.0d.lib;vtkIOAsynchronous-9.0d.lib;vtkIOCityGML-9.0d.lib;vtkIOCore-9.0d.lib;vtkIOEnSight-9.0d.lib;vtkIOExodus-9.0d.lib;vtkIOExport-9.0d.lib;vtkIOExportGL2PS-9.0d.lib;vtkIOExportPDF-9.0d.lib;vtkIOGeometry-9.0d.lib;vtkIOImage-9.0d.lib;vtkIOImport-9.0d.lib;vtkIOInfovis-9.0d.lib;vtkIOLegacy-9.0d.lib;vtkIOLSDyna-9.0d.lib;vtkIOMINC-9.0d.lib;vtkIOMotionFX-9.0d.lib;vtkIOMovie-9.0d.lib;vtkIONetCDF-9.0d.lib;vtkIOOggTheora-9.0d.lib;vtkIOParallel-9.0d.lib;vtkIOParallelXML-9.0d.lib;vtkIOPLY-9.0d.lib;vtkIOSegY-9.0d.lib;vtkIOSQL-9.0d.lib;vtkIOTecplotTable-9.0d.lib;vtkIOVeraOut-9.0d.lib;vtkIOVideo-9.0d.lib;vtkIOXML-9.0d.lib;vtkIOXMLParser-9.0d.lib;vtkjpeg-9.0d.lib;vtkjsoncpp-9.0d.lib;vtklibharu-9.0d.lib;vtklibproj-9.0d.lib;vtklibxml2-9.0d.lib;vtkloguru-9.0d.lib;vtklz4-9.0d.lib;vtklzma-9.0d.lib;vtkmetaio-9.0d.lib;vtknetcdf-9.0d.lib;vtkogg-9.0d.lib;vtkParallelCore-9.0d.lib;vtkParallelDIY-9.0d.lib;vtkpng-9.0d.lib;vtkpugixml-9.0d.lib;vtkRenderingAnnotation-9.0d.lib;vtkRenderingContext2D-9.0d.lib;vtkRenderingContextOpenGL2-9.0d.lib;vtkRenderingCore-9.0d.lib;vtkRenderingFreeType-9.0d.lib;vtkRenderingGL2PSOpenGL2-9.0d.lib;vtkRenderingImage-9.0d.lib;vtkRenderingLabel-9.0d.lib;vtkRenderingLOD-9.0d.lib;vtkRenderingOpenGL2-9.0d.lib;vtkRenderingSceneGraph-9.0d.lib;vtkRenderingUI-9.0d.lib;vtkRenderingVolume-9.0d.lib;vtkRenderingVolumeOpenGL2-9.0d.lib;vtkRenderingVtkJS-9.0d.lib;vtksqlite-9.0d.lib;vtksys-9.0d.lib;vtkTestingRendering-9.0d.lib;vtktheora-9.0d.lib;vtktiff-9.0d.lib;vtkverdict-9.0d.lib;vtkViewsContext2D-9.0d.lib;vtkViewsCore-9.0d.lib;vtkViewsInfovis-9.0d.lib;vtkWrappingTools-9.0d.lib;vtkzlib-9.0d.lib

REM Set CURL Directory
SET CURL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\curl\curl-7.62.0
SET CURL_LIB=%CURL_ROOT%\build-win-x64\Release\lib
SET CURL_INC=%CURL_ROOT%\build-win-x64\Release\include
SET CURL_DLL=%CURL_ROOT%\build-win-x64\Release\bin
SET CURL_LIBD=%CURL_ROOT%\build-win-x64\Debug\lib
SET CURL_DLLD=%CURL_ROOT%\build-win-x64\Debug\bin

REM Set OpenSSL Directory
set OPENSSL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\OpenSSL\OpenSSL-1.1.1
set OPENSSL_DLL=%OPENSSL_ROOT%\build-win-x64\dll\x64\Release\bin

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
SET EMBREE_INC=%EMBREE_ROOT%\include
SET EMBREE_LIB=%EMBREE_ROOT%\lib
SET EMBREE_BIN=%EMBREE_ROOT%\bin

REM Set Python Directory
SET PYTHONPATH=%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64;%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64\Scripts
SET PATH=%PYTHONPATH%;%PATH%

REM Set CGAL Directory
SET CGAL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\CGAL\CGAL-5.3
SET CGAL_INC=%CGAL_ROOT%\include
SET GMP_INC=%CGAL_ROOT%\auxiliary\gmp\include
SET GMP_LIB=%CGAL_ROOT%\auxiliary\gmp\lib

REM Set Boost Directory
SET BOOST_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\boost\boost_1_71_0
SET BOOST_INC=%BOOST_ROOT%
SET BOOST_LIB=%BOOST_ROOT%\lib64-msvc-14.1

REM Set Expression Evaluator Directory
SET EXPREVAL_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\tinyexpr
SET EXPREVAL_INC=%EXPREVAL_ROOT%

REM Set Google Test Directories
SET GOOGLE_TEST_ROOT=%OPENTWIN_THIRDPARTY_ROOT%\GoogleTest
SET GOOGLE_TEST_INC=%GOOGLE_TEST_ROOT%\googletest\include
SET GOOGLE_TEST_LIB=%GOOGLE_TEST_ROOT%\build

ECHO Third Party environment was set up successfully.

:END


import re

_VAR = re.compile(r"%([^%]+)%")

VARS = {
    # ===== Qt =====
    "QDIR": r"%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.10.0\msvc2022_64",
    "QTVER": "6.10.0",
    "QTDIR": r"%QDIR%",
    "QT_DIR": r"%QDIR%",
    "QT_DLLR": r"%QDIR%\bin",
    "QT_DLLD": r"%QDIR%\bin",
    "QT_INC": r"%QDIR%\include",
    "QT_LIBPATH": r"%QDIR%\lib",
    "QT_PLUGINS": r"%QDIR%\plugins",

    # ===== QWT =====
    "QWT_LIB_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\qwt\qwt-6.2.0",
    "QWT_LIB_INC": r"%QWT_LIB_ROOT%\src",
    "QWT_LIB_INCD": r"%QWT_LIB_INC%",
    "QWT_LIB_INCR": r"%QWT_LIB_INC%",
    "QWT_LIB_LIBD": "qwtd.lib",
    "QWT_LIB_LIBR": "qwt.lib",
    "QWT_LIB_LIBPATHD": r"%QWT_LIB_ROOT%\lib",
    "QWT_LIB_LIBPATHR": r"%QWT_LIB_ROOT%\lib",
    "QWT_LIB_DLLD": r"%QWT_LIB_ROOT%\lib",
    "QWT_LIB_DLLR": r"%QWT_LIB_ROOT%\lib",

    # ===== Advanced Docking System =====
    "QT_ADS_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\QtAdvancedDockingSystem\Qt-Advanced-Docking-System-5.1.1",
    "QT_ADS_INC": r"%QT_ADS_ROOT%\include",
    "QT_ADS_LIBPATH": r"%QT_ADS_ROOT%\lib",
    "QT_ADS_LIBD": "qtadvanceddocking-qt6d.lib",
    "QT_ADS_LIBR": "qtadvanceddocking-qt6.lib",

    # ===== Open Scene Graph =====
    "OSG_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenSceneGraph\OpenSceneGraph-OpenSceneGraph-3.6.3",
    "OSG_INCD": r"%OSG_ROOT%\include",
    "OSG_INCR": r"%OSG_ROOT%\include",
    "OSG_LIBD": "OpenThreadsd.lib;osgAnimationd.lib;osgd.lib;osgDBd.lib;osgFXd.lib;osgGAd.lib;osgManipulatord.lib;osgParticled.lib;osgPresentationd.lib;osgQt5d.lib;osgShadowd.lib;osgSimd.lib;osgTerraind.lib;osgTextd.lib;osgUId.lib;osgUtild.lib;osgViewerd.lib;osgVolumed.lib;osgWidgetd.lib;",
    "OSG_LIBR": "OpenThreads.lib;osgAnimation.lib;osg.lib;osgDB.lib;osgFX.lib;osgGA.lib;osgManipulator.lib;osgParticle.lib;osgPresentation.lib;osgQt5.lib;osgShadow.lib;osgSim.lib;osgTerrain.lib;osgText.lib;osgUI.lib;osgUtil.lib;osgViewer.lib;osgVolume.lib;osgWidget.lib;",
    "OSG_LIBPATHD": r"%OSG_ROOT%\lib\Debug",
    "OSG_LIBPATHR": r"%OSG_ROOT%\lib\Release",
    "OSG_DLLD": r"%OSG_ROOT%\bin\Debug",
    "OSG_DLLR": r"%OSG_ROOT%\bin\Release",

    # ===== Open Cascade =====
    "OC_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\opencascade-7.8.0",
    "OC_INCD": r"%OC_ROOT%\inc",
    "OC_INCR": r"%OC_ROOT%\inc",
    "OC_LIBPATHD": r"%OC_ROOT%\win64\vc14\lib",
    "OC_LIBPATHR": r"%OC_ROOT%\win64\vc14\lib",
    "OC_DLLD": r"%OC_ROOT%\win64\vc14\bin",
    "OC_DLLR": r"%OC_ROOT%\win64\vc14\bin",
    "TBB_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\tbb2021.5-vc14-x64",
    "TBB_DLLR": r"%TBB_ROOT%\bin",
    "FRI_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\freeimage-3.17.0-vc14-64",
    "FRI_DLLR": r"%FRI_ROOT%\bin",
    "FRT_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\freetype-2.5.5-vc14-64",
    "FRT_DLLR": r"%FRT_ROOT%\bin",
    "FMP_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\ffmpeg-3.3.4-64",
    "FMP_DLLR": r"%FMP_ROOT%\bin",
    "OVR_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\openvr-1.14.15-64",
    "OVR_DLLR": r"%OVR_ROOT%\bin\win64",
    "JEM_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\jemalloc-vc14-64",
    "JEM_DLLR": "%JEM_ROOT%\\bin\\",
    "CFG_OC_LIBS": "TKBin.lib;TKBinL.lib;TKBinTObj.lib;TKBinXCAF.lib;TKBO.lib;TKBool.lib;TKBRep.lib;TKCAF.lib;TKCDF.lib;TKD3DHost.lib;TKDCAF.lib;TKDFBrowser.lib;TKDraw.lib;TKernel.lib;TKFeat.lib;TKFillet.lib;TKG2d.lib;TKG3d.lib;TKGeomAlgo.lib;TKGeomBase.lib;TKHLR.lib;TKDEIGES.lib;TKIVtk.lib;TKIVtkDraw.lib;TKLCAF.lib;TKMath.lib;TKMesh.lib;TKMeshVS.lib;TKOffset.lib;TKOpenGl.lib;TKPrim.lib;TKQADraw.lib;TKService.lib;TKShapeView.lib;TKShHealing.lib;TKStd.lib;TKStdL.lib;TKDESTEP.lib;TKDESTL.lib;TKTInspector.lib;TKTInspectorAPI.lib;TKTObj.lib;TKTObjDRAW.lib;TKToolsDraw.lib;TKTopAlgo.lib;TKTopTest.lib;TKTreeModel.lib;TKV3d.lib;TKVCAF.lib;TKView.lib;TKViewerTest.lib;TKVInspector.lib;TKDEVRML.lib;TKXCAF.lib;TKXDEDRAW.lib;TKXMesh.lib;TKXml.lib;TKXmlL.lib;TKXmlTObj.lib;TKXmlXCAF.lib;TKXSBase.lib;TKXSDRAW.lib",
    "CFG_OC_DLLS": r"$(OC_ROOT)\win64\vc14\bin\TKBin.dll;$(OC_ROOT)\win64\vc14\bin\TKBinL.dll;$(OC_ROOT)\win64\vc14\bin\TKBinTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKBinXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKBO.dll;$(OC_ROOT)\win64\vc14\bin\TKBool.dll;$(OC_ROOT)\win64\vc14\bin\TKBRep.dll;$(OC_ROOT)\win64\vc14\bin\TKCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKCDF.dll;$(OC_ROOT)\win64\vc14\bin\TKD3DHost.dll;$(OC_ROOT)\win64\vc14\bin\TKDCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKDFBrowser.dll;$(OC_ROOT)\win64\vc14\bin\TKDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKernel.dll;$(OC_ROOT)\win64\vc14\bin\TKFeat.dll;$(OC_ROOT)\win64\vc14\bin\TKFillet.dll;$(OC_ROOT)\win64\vc14\bin\TKG2d.dll;$(OC_ROOT)\win64\vc14\bin\TKG3d.dll;$(OC_ROOT)\win64\vc14\bin\TKGeomAlgo.dll;$(OC_ROOT)\win64\vc14\bin\TKGeomBase.dll;$(OC_ROOT)\win64\vc14\bin\TKHLR.dll;$(OC_ROOT)\win64\vc14\bin\TKDEIGES.dll;$(OC_ROOT)\win64\vc14\bin\TKIVtk.dll;$(OC_ROOT)\win64\vc14\bin\TKIVtkDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKLCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKMath.dll;$(OC_ROOT)\win64\vc14\bin\TKMesh.dll;$(OC_ROOT)\win64\vc14\bin\TKMeshVS.dll;$(OC_ROOT)\win64\vc14\bin\TKOffset.dll;$(OC_ROOT)\win64\vc14\bin\TKOpenGl.dll;$(OC_ROOT)\win64\vc14\bin\TKPrim.dll;$(OC_ROOT)\win64\vc14\bin\TKQADraw.dll;$(OC_ROOT)\win64\vc14\bin\TKService.dll;$(OC_ROOT)\win64\vc14\bin\TKShapeView.dll;$(OC_ROOT)\win64\vc14\bin\TKShHealing.dll;$(OC_ROOT)\win64\vc14\bin\TKStd.dll;$(OC_ROOT)\win64\vc14\bin\TKStdL.dll;$(OC_ROOT)\win64\vc14\bin\TKDESTEP.dll;$(OC_ROOT)\win64\vc14\bin\TKDESTL.dll;$(OC_ROOT)\win64\vc14\bin\TKTInspector.dll;$(OC_ROOT)\win64\vc14\bin\TKTInspectorAPI.dll;$(OC_ROOT)\win64\vc14\bin\TKTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKTObjDRAW.dll;$(OC_ROOT)\win64\vc14\bin\TKToolsDraw.dll;$(OC_ROOT)\win64\vc14\bin\TKTopAlgo.dll;$(OC_ROOT)\win64\vc14\bin\TKTopTest.dll;$(OC_ROOT)\win64\vc14\bin\TKTreeModel.dll;$(OC_ROOT)\win64\vc14\bin\TKV3d.dll;$(OC_ROOT)\win64\vc14\bin\TKVCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKView.dll;$(OC_ROOT)\win64\vc14\bin\TKViewerTest.dll;$(OC_ROOT)\win64\vc14\bin\TKVInspector.dll;$(OC_ROOT)\win64\vc14\bin\TKDEVRML.dll;$(OC_ROOT)\win64\vc14\bin\TKXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKXDEDRAW.dll;$(OC_ROOT)\win64\vc14\bin\TKXMesh.dll;$(OC_ROOT)\win64\vc14\bin\TKXml.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlL.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlTObj.dll;$(OC_ROOT)\win64\vc14\bin\TKXmlXCAF.dll;$(OC_ROOT)\win64\vc14\bin\TKXSBase.dll;$(OC_ROOT)\win64\vc14\bin\TKXSDRAW.dll",

    # ===== Tab Toolbar =====
    "QT_TT_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\QtTabToolbar",
    "QT_TT_INCD": r"%QT_TT_ROOT%\include",
    "QT_TT_INCR": r"%QT_TT_ROOT%\include",
    "QT_TT_LIBD": "TabToolbard.lib",
    "QT_TT_LIBR": "TabToolbar.lib",
    "QT_TT_LIBPATHD": r"%QT_TT_ROOT%\src\TabToolbar\Debug",
    "QT_TT_LIBPATHR": r"%QT_TT_ROOT%\src\TabToolbar\Release",
    "QT_TT_DLLD": r"%QT_TT_ROOT%\src\TabToolbar\Debug",
    "QT_TT_DLLR": r"%QT_TT_ROOT%\src\TabToolbar\Release",

    # ===== Rapid JSON =====
    "R_JSON_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\rapidjson",
    "R_JSON_INCD": r"%R_JSON_ROOT%\include",
    "R_JSON_INCR": r"%R_JSON_ROOT%\include",

    # ===== Gmsh =====
    "GMSH_ROOT_INC": r"%OPENTWIN_THIRDPARTY_ROOT%\gmsh\gmsh-4.13.1\api",
    "GMSH_ROOT_BIN": r"%OPENTWIN_THIRDPARTY_ROOT%\gmsh\gmsh-4.13.1\build_win64\Release",

    # ===== MongoDb =====
    "MONGO_C_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\MongoDb\mongo-c-driver-1.27.3\x64",
    "MONGO_C_LIBPATHD": r"%MONGO_C_ROOT%\Debug\lib",
    "MONGO_C_LIBPATHR": r"%MONGO_C_ROOT%\Release\lib",
    "MONGO_C_LIB": "bson-1.0.lib;mongoc-1.0.lib",
    "MONGO_C_DLLD": r"%MONGO_C_ROOT%\Debug\bin",
    "MONGO_C_DLLR": r"%MONGO_C_ROOT%\Release\bin",
    "MONGO_CXX_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\MongoDb\mongo-cxx-driver-r3.10.0\x64",
    "MONGO_CXX_INC": r"%MONGO_CXX_ROOT%\include",
    "MONGO_CXX_LIBPATHD": r"%MONGO_CXX_ROOT%\Debug\lib",
    "MONGO_CXX_LIBPATHR": r"%MONGO_CXX_ROOT%\Release\lib",
    "MONGO_CXX_LIB": "bsoncxx.lib;mongocxx.lib",
    "MONGO_CXX_DLLD": r"%MONGO_CXX_ROOT%\Debug\bin",
    "MONGO_CXX_DLLR": r"%MONGO_CXX_ROOT%\Release\bin",
    "MONGO_BOOST_ROOT": "%OPENTWIN_THIRDPARTY_ROOT%\\MongoDb\\boost-1.72.0\\",

    # ===== VTK =====
    "VTK_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\vtk\VTK-9.0.3",
    "VTK_LIB": "%VTK_ROOT%\\build_Win64\\lib\\",
    "VTK_DLL": "%VTK_ROOT%\\build_Win64\\bin\\",
    "VTK_DLLR": r"%VTK_ROOT%\build_Win64\bin\Release",
    "VTK_DLLD": r"%VTK_ROOT%\build_Win64\bin\Debug",
    "VTK_DIR": r"%VTK_ROOT%\build_Win64",
    "VTK_INC": r"$(VTK_ROOT)\Rendering\Core;$(VTK_ROOT)\Filters\Sources;$(VTK_ROOT)\Filters\Core;$(VTK_ROOT)\Filters\Sources;$(VTK_ROOT)\Filters\General;$(VTK_ROOT)\Filters\Modeling;$(VTK_ROOT)\Filters\Core;$(VTK_ROOT)\Filters\Geometry;$(VTK_ROOT)\Filters\Extraction;$(VTK_ROOT)\Common\Color;$(VTK_ROOT)\Common\Core;$(VTK_ROOT)\Common\Misc;$(VTK_ROOT)\Common\Transforms;$(VTK_ROOT)\Common\Math;$(VTK_ROOT)\build_Win64\Common\Core;$(VTK_ROOT)\build_Win64\Common\Transforms;$(VTK_ROOT)\build_Win64\Common\Math;$(VTK_ROOT)\Utilities\KWIML;$(VTK_ROOT)\build_Win64\Utilities\KWIML;$(VTK_ROOT)\build_Win64\Rendering\Core;$(VTK_ROOT)\build_Win64\Filters\Core;$(VTK_ROOT)\Common\DataModel;$(VTK_ROOT)\Common\Math;$(VTK_ROOT)\build_Win64\Filters\Sources;$(VTK_ROOT)\build_Win64\Filters\General;$(VTK_ROOT)\build_Win64\Filters\Modeling;$(VTK_ROOT)\build_Win64\Filters\Geometry;$(VTK_ROOT)\build_Win64\Filters\Extraction;$(VTK_ROOT)\Common\ExecutionModel;$(VTK_ROOT)\build_Win64\Common\ExecutionModel;$(VTK_ROOT)\build_Win64\Common\DataModel;$(VTK_ROOT)\build_Win64\Common\Color;$(VTK_ROOT)\build_Win64\Common\Misc;$(VTK_ROOT)\Rendering\External;$(VTK_ROOT)\Rendering\OpenGL2;$(VTK_ROOT)\build_Win64\Rendering\OpenGL2;$(VTK_ROOT)\build_Win64\Rendering\UI;$(VTK_ROOT)\build_Win64\Rendering\External;$(VTK_ROOT)\Rendering\External;$(VTK_ROOT)\IO\Legacy;$(VTK_ROOT)\build_Win64\IO\Legacy;$(VTK_ROOT)\IO\XML;$(VTK_ROOT)\build_Win64\IO\XML",
    "VTK_LIBLIST_RELEASE": "vtkChartsCore-9.0.lib;vtkCommonColor-9.0.lib;vtkCommonComputationalGeometry-9.0.lib;vtkCommonCore-9.0.lib;vtkCommonDataModel-9.0.lib;vtkCommonExecutionModel-9.0.lib;vtkCommonMath-9.0.lib;vtkCommonMisc-9.0.lib;vtkCommonSystem-9.0.lib;vtkCommonTransforms-9.0.lib;vtkDICOMParser-9.0.lib;vtkDomainsChemistry-9.0.lib;vtkDomainsChemistryOpenGL2-9.0.lib;vtkdoubleconversion-9.0.lib;vtkexodusII-9.0.lib;vtkexpat-9.0.lib;vtkFiltersAMR-9.0.lib;vtkFiltersCore-9.0.lib;vtkFiltersExtraction-9.0.lib;vtkFiltersFlowPaths-9.0.lib;vtkFiltersGeneral-9.0.lib;vtkFiltersGeneric-9.0.lib;vtkFiltersGeometry-9.0.lib;vtkFiltersHybrid-9.0.lib;vtkFiltersHyperTree-9.0.lib;vtkFiltersImaging-9.0.lib;vtkFiltersGeometry-9.0.lib;vtkFiltersModeling-9.0.lib;vtkFiltersParallel-9.0.lib;vtkFiltersParallelImaging-9.0.lib;vtkFiltersPoints-9.0.lib;vtkFiltersProgrammable-9.0.lib;vtkFiltersSelection-9.0.lib;vtkFiltersSMP-9.0.lib;vtkFiltersSources-9.0.lib;vtkFiltersStatistics-9.0.lib;vtkFiltersTexture-9.0.lib;vtkFiltersTopology-9.0.lib;vtkFiltersVerdict-9.0.lib;vtkfreetype-9.0.lib;vtkGeovisCore-9.0.lib;vtkgl2ps-9.0.lib;vtkglew-9.0.lib;vtkhdf5-9.0.lib;vtkhdf5_hl-9.0.lib;vtkImagingColor-9.0.lib;vtkImagingCore-9.0.lib;vtkImagingFourier-9.0.lib;vtkImagingGeneral-9.0.lib;vtkImagingHybrid-9.0.lib;vtkImagingMath-9.0.lib;vtkImagingMorphological-9.0.lib;vtkImagingSources-9.0.lib;vtkImagingStatistics-9.0.lib;vtkImagingStencil-9.0.lib;vtkInfovisCore-9.0.lib;vtkInfovisLayout-9.0.lib;vtkInteractionImage-9.0.lib;vtkInteractionStyle-9.0.lib;vtkInteractionWidgets-9.0.lib;vtkIOAMR-9.0.lib;vtkIOAsynchronous-9.0.lib;vtkIOCityGML-9.0.lib;vtkIOCore-9.0.lib;vtkIOEnSight-9.0.lib;vtkIOExodus-9.0.lib;vtkIOExport-9.0.lib;vtkIOExportGL2PS-9.0.lib;vtkIOExportPDF-9.0.lib;vtkIOGeometry-9.0.lib;vtkIOImage-9.0.lib;vtkIOImport-9.0.lib;vtkIOInfovis-9.0.lib;vtkIOLegacy-9.0.lib;vtkIOLSDyna-9.0.lib;vtkIOMINC-9.0.lib;vtkIOMotionFX-9.0.lib;vtkIOMovie-9.0.lib;vtkIONetCDF-9.0.lib;vtkIOOggTheora-9.0.lib;vtkIOParallel-9.0.lib;vtkIOParallelXML-9.0.lib;vtkIOPLY-9.0.lib;vtkIOSegY-9.0.lib;vtkIOSQL-9.0.lib;vtkIOTecplotTable-9.0.lib;vtkIOVeraOut-9.0.lib;vtkIOVideo-9.0.lib;vtkIOXML-9.0.lib;vtkIOXMLParser-9.0.lib;vtkjpeg-9.0.lib;vtkjsoncpp-9.0.lib;vtklibharu-9.0.lib;vtklibproj-9.0.lib;vtklibxml2-9.0.lib;vtkloguru-9.0.lib;vtklz4-9.0.lib;vtklzma-9.0.lib;vtkmetaio-9.0.lib;vtknetcdf-9.0.lib;vtkogg-9.0.lib;vtkParallelCore-9.0.lib;vtkParallelDIY-9.0.lib;vtkpng-9.0.lib;vtkpugixml-9.0.lib;vtkRenderingAnnotation-9.0.lib;vtkRenderingContext2D-9.0.lib;vtkRenderingContextOpenGL2-9.0.lib;vtkRenderingCore-9.0.lib;vtkRenderingFreeType-9.0.lib;vtkRenderingGL2PSOpenGL2-9.0.lib;vtkRenderingImage-9.0.lib;vtkRenderingLabel-9.0.lib;vtkRenderingLOD-9.0.lib;vtkRenderingOpenGL2-9.0.lib;vtkRenderingSceneGraph-9.0.lib;vtkRenderingUI-9.0.lib;vtkRenderingVolume-9.0.lib;vtkRenderingVolumeOpenGL2-9.0.lib;vtkRenderingVtkJS-9.0.lib;vtksqlite-9.0.lib;vtksys-9.0.lib;vtkTestingRendering-9.0.lib;vtktheora-9.0.lib;vtktiff-9.0.lib;vtkverdict-9.0.lib;vtkViewsContext2D-9.0.lib;vtkViewsCore-9.0.lib;vtkViewsInfovis-9.0.lib;vtkWrappingTools-9.0.lib;vtkzlib-9.0.lib",
    "VTK_LIBLIST_DEBUG": "vtkChartsCore-9.0d.lib;vtkCommonColor-9.0d.lib;vtkCommonComputationalGeometry-9.0d.lib;vtkCommonCore-9.0d.lib;vtkCommonDataModel-9.0d.lib;vtkCommonExecutionModel-9.0d.lib;vtkCommonMath-9.0d.lib;vtkCommonMisc-9.0d.lib;vtkCommonSystem-9.0d.lib;vtkCommonTransforms-9.0d.lib;vtkDICOMParser-9.0d.lib;vtkDomainsChemistry-9.0d.lib;vtkDomainsChemistryOpenGL2-9.0d.lib;vtkdoubleconversion-9.0d.lib;vtkexodusII-9.0d.lib;vtkexpat-9.0d.lib;vtkFiltersAMR-9.0d.lib;vtkFiltersCore-9.0d.lib;vtkFiltersExtraction-9.0d.lib;vtkFiltersFlowPaths-9.0d.lib;vtkFiltersGeneral-9.0d.lib;vtkFiltersGeneric-9.0d.lib;vtkFiltersGeometry-9.0d.lib;vtkFiltersHybrid-9.0d.lib;vtkFiltersHyperTree-9.0d.lib;vtkFiltersImaging-9.0d.lib;vtkFiltersModeling-9.0d.lib;vtkFiltersParallel-9.0d.lib;vtkFiltersParallelImaging-9.0d.lib;vtkFiltersPoints-9.0d.lib;vtkFiltersProgrammable-9.0d.lib;vtkFiltersSelection-9.0d.lib;vtkFiltersSMP-9.0d.lib;vtkFiltersSources-9.0d.lib;vtkFiltersStatistics-9.0d.lib;vtkFiltersTexture-9.0d.lib;vtkFiltersTopology-9.0d.lib;vtkFiltersVerdict-9.0d.lib;vtkfreetype-9.0d.lib;vtkGeovisCore-9.0d.lib;vtkgl2ps-9.0d.lib;vtkglew-9.0d.lib;vtkhdf5-9.0d.lib;vtkhdf5_hl-9.0d.lib;vtkImagingColor-9.0d.lib;vtkImagingCore-9.0d.lib;vtkImagingFourier-9.0d.lib;vtkImagingGeneral-9.0d.lib;vtkImagingHybrid-9.0d.lib;vtkImagingMath-9.0d.lib;vtkImagingMorphological-9.0d.lib;vtkImagingSources-9.0d.lib;vtkImagingStatistics-9.0d.lib;vtkImagingStencil-9.0d.lib;vtkInfovisCore-9.0d.lib;vtkInfovisLayout-9.0d.lib;vtkInteractionImage-9.0d.lib;vtkInteractionStyle-9.0d.lib;vtkInteractionWidgets-9.0d.lib;vtkIOAMR-9.0d.lib;vtkIOAsynchronous-9.0d.lib;vtkIOCityGML-9.0d.lib;vtkIOCore-9.0d.lib;vtkIOEnSight-9.0d.lib;vtkIOExodus-9.0d.lib;vtkIOExport-9.0d.lib;vtkIOExportGL2PS-9.0d.lib;vtkIOExportPDF-9.0d.lib;vtkIOGeometry-9.0d.lib;vtkIOImage-9.0d.lib;vtkIOImport-9.0d.lib;vtkIOInfovis-9.0d.lib;vtkIOLegacy-9.0d.lib;vtkIOLSDyna-9.0d.lib;vtkIOMINC-9.0d.lib;vtkIOMotionFX-9.0d.lib;vtkIOMovie-9.0d.lib;vtkIONetCDF-9.0d.lib;vtkIOOggTheora-9.0d.lib;vtkIOParallel-9.0d.lib;vtkIOParallelXML-9.0d.lib;vtkIOPLY-9.0d.lib;vtkIOSegY-9.0d.lib;vtkIOSQL-9.0d.lib;vtkIOTecplotTable-9.0d.lib;vtkIOVeraOut-9.0d.lib;vtkIOVideo-9.0d.lib;vtkIOXML-9.0d.lib;vtkIOXMLParser-9.0d.lib;vtkjpeg-9.0d.lib;vtkjsoncpp-9.0d.lib;vtklibharu-9.0d.lib;vtklibproj-9.0d.lib;vtklibxml2-9.0d.lib;vtkloguru-9.0d.lib;vtklz4-9.0d.lib;vtklzma-9.0d.lib;vtkmetaio-9.0d.lib;vtknetcdf-9.0d.lib;vtkogg-9.0d.lib;vtkParallelCore-9.0d.lib;vtkParallelDIY-9.0d.lib;vtkpng-9.0d.lib;vtkpugixml-9.0d.lib;vtkRenderingAnnotation-9.0d.lib;vtkRenderingContext2D-9.0d.lib;vtkRenderingContextOpenGL2-9.0d.lib;vtkRenderingCore-9.0d.lib;vtkRenderingFreeType-9.0d.lib;vtkRenderingGL2PSOpenGL2-9.0d.lib;vtkRenderingImage-9.0d.lib;vtkRenderingLabel-9.0d.lib;vtkRenderingLOD-9.0d.lib;vtkRenderingOpenGL2-9.0d.lib;vtkRenderingSceneGraph-9.0d.lib;vtkRenderingUI-9.0d.lib;vtkRenderingVolume-9.0d.lib;vtkRenderingVolumeOpenGL2-9.0d.lib;vtkRenderingVtkJS-9.0d.lib;vtksqlite-9.0d.lib;vtksys-9.0d.lib;vtkTestingRendering-9.0d.lib;vtktheora-9.0d.lib;vtktiff-9.0d.lib;vtkverdict-9.0d.lib;vtkViewsContext2D-9.0d.lib;vtkViewsCore-9.0d.lib;vtkViewsInfovis-9.0d.lib;vtkWrappingTools-9.0d.lib;vtkzlib-9.0d.lib",

    # ===== CURL =====
    "CURL_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\curl\curl-7.62.0",
    "CURL_INCD": r"%CURL_ROOT%\build-win-x64\Debug\include",
    "CURL_INCR": r"%CURL_ROOT%\build-win-x64\Release\include",
    "CURL_LIBD": "libcurl_debug.lib",
    "CURL_LIBR": "libcurl.lib",
    "CURL_LIBPATHD": r"%CURL_ROOT%\build-win-x64\Debug\lib",
    "CURL_LIBPATHR": r"%CURL_ROOT%\build-win-x64\Release\lib",
    "CURL_DLLD": r"%CURL_ROOT%\build-win-x64\Debug\bin",
    "CURL_DLLR": r"%CURL_ROOT%\build-win-x64\Release\bin",

    # ===== OpenSSL =====
    "OPENSSL_WEBSOCKET_DLLR": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenSSL\LibsForQtWebsocket",
    "OPENSSL_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\OpenSSL\OpenSSL-1.1.1",
    "OPENSSL_DLL": r"%OPENSSL_ROOT%\build-win-x64\dll\x64\Release\bin",

    # ===== BASE64 =====
    "BASE64_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\base64",

    # ===== ZLIB =====
    "ZLIB_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\zlib\zlib-1.2.11\x64",
    "ZLIB_INCD": r"%ZLIB_ROOT%\Debug\include",
    "ZLIB_INCR": r"%ZLIB_ROOT%\Release\include",
    "ZLIB_LIBPATHD": r"%ZLIB_ROOT%\Debug\lib",
    "ZLIB_LIBPATHR": r"%ZLIB_ROOT%\Release\lib",
    "ZLIB_LIBD": "zlibd.lib",
    "ZLIB_LIBR": "zlib.lib",
    "ZLIB_DLLPATHD": r"%ZLIB_ROOT%\Debug\bin",
    "ZLIB_DLLPATHR": r"%ZLIB_ROOT%\Release\bin",

    # ===== EMBREE =====
    "EMBREE_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\embree\embree-3.13.0\windows",
    "EMBREE_INCD": r"%EMBREE_ROOT%\include",
    "EMBREE_INCR": r"%EMBREE_ROOT%\include",
    "EMBREE_LIBPATHD": r"%EMBREE_ROOT%\lib",
    "EMBREE_LIBPATHR": r"%EMBREE_ROOT%\lib",
    "EMBREE_BIN": r"%EMBREE_ROOT%\bin",

    # ===== Python =====
    "OT_PYTHON_BIN_NAME": r"python311",
    "OT_CURRENT_PYTHON_PATH": r"Python\Python3_11_9",
    "OT_PYTHON_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\%OT_CURRENT_PYTHON_PATH%",
    "OT_PYTHON_INC": r"%OT_PYTHON_ROOT%\include",
    "OT_PYTHON_LIBPATH": r"%OT_PYTHON_ROOT%\libs",
    "OT_PYTHON_BIN": r"%OT_PYTHON_ROOT%\Interpreter",
    "OT_PYTHON_ROOT_LEGACY": r"%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64",
    "OT_PYTHON_INC_LEGACY": r"%OT_PYTHON_ROOT_LEGACY%\include",
    "OT_PYTHON_LIBPATH_LEGACY": r"%OT_PYTHON_ROOT_LEGACY%\libs",
    "OT_PYTHONPATH_LEGACY": r"%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64;%OPENTWIN_THIRDPARTY_ROOT%\Python\python-3.9.5.amd64\Scripts",

    # ===== Pyrit =====
    "OT_PYRIT_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\Pyrit",

    # ===== CGAL =====
    "CGAL_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\CGAL\CGAL-5.3",
    "CGAL_INCD": r"%CGAL_ROOT%\include",
    "CGAL_INCR": r"%CGAL_ROOT%\include",
    "GMP_INCD": r"%CGAL_ROOT%\auxiliary\gmp\include",
    "GMP_INCR": r"%CGAL_ROOT%\auxiliary\gmp\include",
    "GMP_LIBPATHD": r"%CGAL_ROOT%\auxiliary\gmp\lib",
    "GMP_LIBPATHR": r"%CGAL_ROOT%\auxiliary\gmp\lib",
    "GMP_DLLPATHD": r"%CGAL_ROOT%\auxiliary\gmp\lib",
    "GMP_DLLPATHR": r"%CGAL_ROOT%\auxiliary\gmp\lib",

    # ===== Boost =====
    "BOOST_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\boost\boost_1_86_0",
    "BOOST_INCD": r"%BOOST_ROOT%",
    "BOOST_INCR": r"%BOOST_ROOT%",
    "BOOST_LIBPATHD": r"%BOOST_ROOT%\lib64-msvc-14.3",
    "BOOST_LIBPATHR": r"%BOOST_ROOT%\lib64-msvc-14.3",
    "BOOST_DLLPATHD": r"%BOOST_ROOT%\lib64-msvc-14.3",
    "BOOST_DLLPATHR": r"%BOOST_ROOT%\lib64-msvc-14.3",

    # ===== Expression Evaluator =====
    "EXPREVAL_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\tinyexpr",
    "EXPREVAL_INC": r"%EXPREVAL_ROOT%",

    # ===== earcut =====
    "EARCUT_INC": r"%OPENTWIN_THIRDPARTY_ROOT%\earcut\include\mapbox",

    # ===== Google Test =====
    "GOOGLE_TEST_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\GoogleTest",
    "GOOGLE_TEST_INC": r"%GOOGLE_TEST_ROOT%\googletest\include",
    "GOOGLE_TEST_LIBPATHD": r"%GOOGLE_TEST_ROOT%\build\x64-Debug\lib",
    "GOOGLE_TEST_LIBPATHR": r"%GOOGLE_TEST_ROOT%\build\x64-Release\lib",
    "GOOGLE_TEST_LIB": "gtest_main.lib;gtest.lib",

    # ===== GETDP =====
    "GETDP_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\getdp",
    "GETDP_BIN": r"%GETDP_ROOT%\Windows",

    # ===== FDTD / openEMS =====
    "FDTD_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\openEMS\openEMS_v0.0.36",
    "FDTD_INC": r"%OPENTWIN_THIRDPARTY_ROOT%\openEMS\openEMS_v0.0.36\include",
    "FDTD_BIN": r"%FDTD_ROOT%",

    # ===== tinyxml2 =====
    "TINYXML2_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\tinyxml2\tinyxml2-11.0.0",
    "TINYXML2_BIN": r"%TINYXML2_ROOT%",

    # ===== ELMERFEM =====
    "ELMERFEM_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\ElmerFEM\9.0",
    "ELMERFEM_BIN": r"%ELMERFEM_ROOT%",

    # ===== NGSpice =====
    "NGSPICE_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\mySpice\ngspice-41",

    # ===== VisualStudio Redist =====
    "VC_REDIST_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\VisualStudioRuntime",

    # ===== Apache =====
    "APACHE_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\Apache\Apache24\Windows",

    # ===== Certificate creation tools =====
    "CERT_CREATE_TOOLS": r"%OPENTWIN_THIRDPARTY_ROOT%\CertificateCreation",

    # ===== NGSpice lib paths =====
    "NGSPICE_LIBPATHD": r"%OPENTWIN_THIRDPARTY_ROOT%\mySpice\ngspice-41\visualc\sharedspice\Debug.x64",
    "NGSPICE_LIBPATHR": r"%OPENTWIN_THIRDPARTY_ROOT%\mySpice\ngspice-41\visualc\sharedspice\Release.x64",

    # ===== Graphviz =====
    "GRAPHVIZ_BIN": r"%OPENTWIN_THIRDPARTY_ROOT%\Graphviz\Graphviz-12.2.1-win64\bin",

    # ===== MathJax =====
    "MATHJAX_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\MathJax\MathJax-3.2.2\es5",
    "MATHJAX_REL_PATH_SUFFIX": r"MathJax\MathJax-3.2.2\es5",

    # ===== expat =====
    "EXPAT_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\expat\2.8.3",
    "EXPAT_INC": r"%EXPAT_ROOT%\include",
    "EXPAT_LIBPATHD": r"%EXPAT_ROOT%\Bin",
    "EXPAT_LIBPATHR": r"%EXPAT_ROOT%\Bin",
    "EXPAT_LIBD": "libexpat.lib",
    "EXPAT_LIBR": "libexpat.lib",
    "EXPAT_BIN": r"%EXPAT_ROOT%\Bin",

    # ===== mdflib =====
    "MDFLIB_ROOT": r"%OPENTWIN_THIRDPARTY_ROOT%\mdflib\mdflib-2.3.0",
    "MDFLIB_INC": r"%MDFLIB_ROOT%\include",
    "MDFLIB_BIN": r"%MDFLIB_ROOT%\bin",
    "MDFLIB_LIBPATHD": r"%MDFLIB_ROOT%\lib",
    "MDFLIB_LIBPATHR": r"%MDFLIB_ROOT%\lib",
    "MDFLIB_LIBD": "mdfd.lib",
    "MDFLIB_LIBR": "mdf.lib",
}


def _get(env, name):
    if name in env:
        return env[name]
    low = name.lower()
    return next((v for k, v in env.items() if k.lower() == low), "")


def _expand(env, value):
    return _VAR.sub(lambda m: _get(env, m.group(1)), value)


def apply(env):
    if env.get("OPENTWIN_THIRDPARTY_ENV_DEFINED") == "1":
        return env
    env["OPENTWIN_THIRDPARTY_ENV_DEFINED"] = "1"
    for name, template in VARS.items():
        env[name] = _expand(env, template)
    env["VTK_DIR"] = env["VTK_DIR"].replace("\\", "/")
    env["PATH"] = _expand(env, r"%OT_PYTHONPATH_LEGACY%;%OPENTWIN_THIRDPARTY_ROOT%\doxygen;%PATH%")
    print("OpenTwin Third Party environment was set up successfully.")
    return env

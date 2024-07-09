echo off

rem CASDEB comes as third argument

if /I "%VCVER%" == "vc14" (
  if "%ARCH%" == "64" (
    rem set environment variables used by OCCT
    set CSF_FPE=0

    set "TCL_DIR=%THIRDPARTY_DIR%/tcltk-86-64/bin"
    set "TK_DIR=%THIRDPARTY_DIR%/tcltk-86-64/bin"
    set "FREETYPE_DIR=%THIRDPARTY_DIR%/freetype-2.5.5-vc14-64/bin"
    set "FREEIMAGE_DIR=%THIRDPARTY_DIR%/freeimage-3.17.0-vc14-64/bin"
    set "EGL_DIR=%THIRDPARTY_DIR%/angle-gles2-2.1.0-vc14-64/bin;%THIRDPARTY_DIR%/angle-gles2-2.1.0-vc14-64/bin;"
    set "GLES2_DIR=%THIRDPARTY_DIR%/angle-gles2-2.1.0-vc14-64/bin;%THIRDPARTY_DIR%/angle-gles2-2.1.0-vc14-64/bin;"
    set "TBB_DIR=%THIRDPARTY_DIR%/tbb2021.5-vc14-x64/bin"
    set "VTK_DIR=%THIRDPARTY_DIR%/VTK-6.1.0-vc14-64/bin"
    set "FFMPEG_DIR=%THIRDPARTY_DIR%/ffmpeg-3.3.4-64/bin"
    set "JEMALLOC_DIR=%THIRDPARTY_DIR%/jemalloc-vc14-64/bin"
    set "OPENVR_DIR=%THIRDPARTY_DIR%/openvr-1.14.15-64/bin/win64"

    if exist "%THIRDPARTY_DIR%/qt5.11.2-vc14-64" (
      set "QTDIR=%THIRDPARTY_DIR%/qt5.11.2-vc14-64"
    ) else (
      set "QTDIR=%~dp0/../qt5.11.2-vc14-64"
    )
    set "TCL_VERSION_WITH_DOT=8.6"
    set "TK_VERSION_WITH_DOT=8.6"

    set "CSF_OCCTBinPath=%CASROOT%/win64/vc14/bin%3"
    set "CSF_OCCTLibPath=%CASROOT%/win64/vc14/lib%3"

    set "CSF_OCCTIncludePath=%CASROOT%/inc"
    set "CSF_OCCTResourcePath=%CASROOT%/src"
    set "CSF_OCCTDataPath=%CASROOT%/data"
    set "CSF_OCCTSamplesPath=%CASROOT%/samples"
    set "CSF_OCCTTestsPath=%CASROOT%/tests"
    set "CSF_OCCTDocPath=%CASROOT%/doc"
  )
)


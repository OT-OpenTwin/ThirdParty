@ECHO OFF

REM This script will descompress all the files that were too large to push to git.
REM Note that the original file will NOT be deleted.
REM Note that if the decompressed file already exists the operation will skip

REM This script requires the following environment variables to be set:
REM 1. OPENTWIN_DEV_ROOT
REM 2. DEVENV_ROOT_2022

IF "%OPENTWIN_DEV_ROOT%" == "" (
	ECHO Please specify the following environment variables: OPENTWIN_DEV_ROOT
	goto PAUSE_END
)

IF "%OPENTWIN_THIRDPARTY_ROOT%" == "" (
	ECHO Please specify the following environment variables: OPENTWIN_THIRDPARTY_ROOT
	goto PAUSE_END
)

REM Setup environment
CALL "%OPENTWIN_DEV_ROOT%\Scripts\SetupEnvironment.bat"

REM Ensure that the script finished successfully
IF NOT "%OPENTWIN_DEV_ENV_DEFINED%" == "1" (
    echo Failed to set up Environment
	goto PAUSE_END
)

REM Qt bin
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt6Guid.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt6Pdfd.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt6Qmld.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt6Quickd.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt63DRenderd.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin"

REM Qt lib
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6QmlDomd.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6BundledPhysXd.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6QmlLSd.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6BundledPhysX.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6QmlDom.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6QmlLS.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib\Qt6BundledResonanceAudiod.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"

REM Qt Tools
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\Tools\QtDesignStudio\qt6_design_studio_reduced_version\bin\Qt6WebEngineCore.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\DecompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\Tools\QtDesignStudio\qt6_design_studio_reduced_version\bin\Qt6WebEngineCored.7z" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\lib"

goto END
:PAUSE_END
pause

:END
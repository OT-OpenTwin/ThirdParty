@ECHO OFF

REM This script will compress all the files that are too large to push to git.
REM Run Decompress to decompress all the files.
REM Note that the original file will NOT be deleted.

REM This script requires the following environment variables to be set:
REM 1. OPENTWIN_DEV_ROOT
REM 2. OPENTWIN_THIRDPARTY_ROOT

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

REM Qt
CALL "%OPENTWIN_DEV_ROOT%\Scripts\Other\CompressFile.bat" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt6Guid.pdb" "%OPENTWIN_THIRDPARTY_ROOT%\Qt\6.6.1\msvc2019_64\bin\Qt6Guid.7z"

goto END
:PAUSE_END
pause

:END
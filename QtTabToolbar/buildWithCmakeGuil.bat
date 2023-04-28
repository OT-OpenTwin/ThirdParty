@ECHO OFF

REM The first argument of the shell defines whether a release or debug build shall be performed. "BOTH" (default) , "RELEASE", "DEBUG" 
REM The second argument of hte shell defines whetehr a full rebuild or just a build is performed. "BUILD" (default), "REBUILD"

REM This script requires the following environment variables to be set:
REM 1. OPENTWIN_DEV_ROOT
REM 2. DEVENV_ROOT

IF "%OPENTWIN_DEV_ROOT%"=="" (
	ECHO Please specify the following environment variables: OPENTWIN_DEV_ROOT
	goto END
)

IF "%DEVENV_ROOT%"=="" (
	ECHO Please specify the following environment variables: DEVENV_ROOT
	goto END
)

REM Setup eviroment

CALL "%OPENTWIN_DEV_ROOT%\Scripts\SetupEnvironment.bat"

ECHO Setup Qt5 enviroment

REM Set Qt Environment 
SET Qt5Core_DIR=%QDIR%\lib\cmake\Qt5Core
SET Qt5Gui_DIR=%QDIR%\lib\cmake\Qt5Gui
SET Qt5Widgets_DIR=%QDIR%\lib\cmake\Qt5Widgets

ECHO call cmake-gui

cmake-gui %cd%

:END

ECHO Done

pause
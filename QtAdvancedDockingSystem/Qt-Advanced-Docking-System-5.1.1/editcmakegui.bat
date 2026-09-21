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

IF "%DEVENV_ROOT_2022%"=="" (
	ECHO Please specify the following environment variables: DEVENV_ROOT_2022
	goto END
)

CALL "%OPENTWIN_DEV_ROOT%\Scripts\Python\set_python.bat"

ECHO Setup Qt6 enviroment

ECHO call cmake-gui

"%OT_PYTHON%" "%OPENTWIN_DEV_ROOT%\Scripts\Python\run.py" "Qt6_DIR=%%QDIR%%\lib\cmake" "Qt6Core_DIR=%%QDIR%%\lib\cmake\Qt6Core" "Qt6Gui_DIR=%%QDIR%%\lib\cmake\Qt6Gui" "Qt6Widgets_DIR=%%QDIR%%\lib\cmake\Qt6Widgets" cmake-gui %cd%

:END

ECHO Done

pause
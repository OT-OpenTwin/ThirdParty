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

REM Setup eviroment

CALL "%OPENTWIN_DEV_ROOT%\Scripts\SetupEnvironment.bat"

ECHO Setup Qt6 enviroment

REM Set Qt Environment 
SET Qt6Core_DIR=%QDIR%\lib\cmake\Qt6Core
SET Qt6Gui_DIR=%QDIR%\lib\cmake\Qt6Gui
SET Qt6Widgets_DIR=%QDIR%\lib\cmake\Qt6Widgets

ECHO call qtcreator

ECHO %OPENTWIN_THIRDPARTY_ROOT%\Qt\Tools\QtCreator\bin\qtcreator.exe
%OPENTWIN_THIRDPARTY_ROOT%\Qt\Tools\QtCreator\bin\qtcreator.exe

:END

ECHO Done

pause

@ECHO OFF

REM This script requires the following environment variables to be set:
REM 1. OPENTWIN_DEV_ROOT
REM 2. DEVENV_ROOT
IF "%OPENTWIN_DEV_ROOT%" == "" (
	ECHO Please specify the following environment variables: OPENTWIN_DEV_ROOT
	goto END
)

IF "%DEVENV_ROOT%" == "" (
	ECHO Please specify the following environment variables: DEVENV_ROOT
	goto END
)

ECHO Setting up environment
CALL "%OPENTWIN_DEV_ROOT%\Scripts\SetupEnvironment.bat"

"%DEVENV_ROOT_2022%\devenv.exe" "%OPENTWIN_THIRDPARTY_ROOT%\qwt\qwt-6.1.4\qwt.sln"

  
:END
@ECHO OFF

REM This script requires the following environment variables to be set:
REM 1. SIM_PLAT_ROOT
REM 2. DEVENV_ROOT
IF "%SIM_PLAT_ROOT%" == "" (
	ECHO Please specify the following environment variables: SIM_PLAT_ROOT
	goto END
)

IF "%DEVENV_ROOT%" == "" (
	ECHO Please specify the following environment variables: DEVENV_ROOT
	goto END
)

ECHO Setting up environment
CALL "%SIM_PLAT_ROOT%\MasterBuild\set_env.bat"

"%DEVENV_ROOT%\devenv.exe" "%SIM_PLAT_ROOT%\Third_Party_Libraries\qwt-6.1.4\qwt.sln"

  
:END
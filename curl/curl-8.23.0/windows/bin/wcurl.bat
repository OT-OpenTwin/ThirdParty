@set sh=
@set bb=
@set PATH=%~dp0;%PATH%
@if "%sh%" equ "" for %%P in ("%PATH:;=" "%") do @dir /b "%%~P\sh.exe" >nul 2>&1 && set sh=%%~P\sh.exe
@if "%sh%" equ "" for %%P in ("%PATH:;=" "%") do @dir /b "%%~P\busybox.exe" >nul 2>&1 && (set sh=%%~P\busybox.exe& set bb=sh)
@if "%sh%" equ "" echo Error: requires a POSIX shell (sh.exe or busybox.exe) in PATH.
@if "%sh%" neq "" "%sh%" %bb% "%~dp0wcurl" %*

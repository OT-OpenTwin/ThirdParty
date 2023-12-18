@ECHO OFF
SET LIBDIR=%ELMER_HOME%/bin
SET INCLUDE=%ELMER_HOME%/share/elmersolver/include

SET LD="%ELMER_HOME%/stripped_gfortran/bin/x86_64-w64-mingw32-gfortran.exe"

REM SET CMD=%LD% -shared %* -L"%LIBDIR%" -L"%ELMER_HOME%/bin" -lelmersolver
SET CMD=%LD%  -fallow-argument-mismatch  -shared %* -L"C:/Program Files (x86)/Elmer/lib/elmersolver" -L"%LIBDIR%" -lelmersolver
echo %cmd%
%cmd%

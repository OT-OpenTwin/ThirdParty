@ECHO OFF
SET LIBDIR=%ELMER_HOME%/bin
SET INCLUDE=%ELMER_HOME%/share/elmersolver/include

SET FC="%ELMER_HOME%/stripped_gfortran/bin/x86_64-w64-mingw32-gfortran.exe"

SET cmd=%FC% %*  -fallow-argument-mismatch  -DCONTIG= -DMINGW32 -DWIN32 -DHAVE_EXECUTECOMMANDLINE -DUSE_ISO_C_BINDINGS -DUSE_ARPACK -O3 -DNDEBUG -O3  -shared -I"%INCLUDE%" -L"%LIBDIR%" -shared -lelmersolver
echo %cmd%
%cmd%

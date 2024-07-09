Installing and compiling Gmsh
=============================

Gmsh needs to be compiled in order to ensure that the same version of OpenCASCADE is used for the model as well as for Gmsh. Otherwise the shape date can not be passed from the model to the meshing library as a pointer.

The compilation of Gmsh on Windows needs to be done with Cygwin / MinGW compilers if OpenMP support is needed.


----------------------------------------------------------------------------------------------------------------------------
Compilation with Visual Studio (no OpenMP support)
----------------------------------------------------------------------------------------------------------------------------

Get the desired version of gmsh from http://gmsh.info/. Make sure to download the source code packages

Uncompress the source code in this folder and create a new subdirectory for the version.

Open cmake GUI, select the source code root and the build directory. 

Press configure

Add a path variable:
MAKE_PREFIX_PATH=C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\opencascade-7.8.0;C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\freetype-2.5.5-vc14-64;C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\opencascade-7.3.0\win64\vc14

Enable Build Shared
Enable Build LIB
Enable Build Dynamic
Disable OpenMP
Diable FLTK

The following path entries need to be specified:
FREETYPE_INCLUDE_DIRS=C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64/freetype-2.5.5-vc14-64/include
FREETYPE_LIBRARY=C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\freetype-2.5.5-vc14-64\lib\freetype.lib

Also the Windows system environment variable needs to be set for Open Cascade:

CASROOT=C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.8.0-vc14-64\opencascade-7.8.0;C:\OT\ThirdParty\OpenCASCADE\OpenCASCADE-7.3.0-vc14-64\opencascade-7.3.0\win64\vc14\lib

Press Configure again
Press Generate

Open the project and rebuild everything (Release) from scratch.

Remove the large files (.vs) from the build results to ensure that there will be no problems when pushing the results to GitHub. The tests tXX_cpp.dir can also be removed. Same for xXX_cpp.dir.




----------------------------------------------------------------------------------------------------------------------------
Cygwin Installation (can be skipped if Cygwin is already installed)
----------------------------------------------------------------------------------------------------------------------------

Install Cygwin from https://www.cygwin.com. Accept all defaults and select View "Full". Install the following packages:

	mingw64_x86_64-gcc-g++
	mingw64_x86_64-gcc-fortran
	cmake
	make
	openssh
	python3
	autoconf
	automake
	git
	wget
	unzip
	
Add the path to the Cygwin executables to the system Path:

	C:\cygwin64\usr\local\bin
	C:\cygwin64\usr\local\lib
	C:\cygwin64\usr\x86_64-w64-mingw32\sys-root\mingw\bin
	
Setup the environment variables:

	Open the Cygwin terminal.
	Edit the ~/.bash_profile and add the following at the end:
	
	export PATH="${PATH}:/usr/x86_64-w64-mingw32/sys-root/mingw/bin:/usr/local/bin"
	export CXX=x86_64-w64-mingw32-g++
	export CC=x86_64-w64-mingw32-gcc
	export FC=x86_64-w64-mingw32-gfortran
	
Close and re-open the Cygwin terminal.

----------------------------------------------------------------------------------------------------------------------------
Install and compile a new version of Gmsh
----------------------------------------------------------------------------------------------------------------------------

Get the desired version of gmsh from http://gmsh.info/. Make sure to download the source code packages

Uncompress the source code in this folder and create a new subdirectory for the version.

Edit the CMakeLists.txt file in the root directoy of the source code folder. After the opt(...) lines, add a new variable to the file:
	set(CMAKE_PREFIX_PATH "" CACHE FILEPATH "Make Prefix")
	
Create a new build directory, e.g. build_Win64

Open the Cygwin shell and cd into the build directory.

Type:
	cmake ..
	
This will open the configuration for the build. Now press c to configure the setup.

Enable / Disable the build options as needed. Make sure to enable the build of the shared libraries and OpenMP. The build of FLTK can be disabled.

Modify the variable CMAKE_PREFIX_PATH and enter the following path (this is necessary to find the OCC (OpenCASCADE) installation):

CMAKE_PREFIX_PATH=/cygdrive/c/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/OpenCASCADE-7.3.0-vc14-64/opencascade-7.3.0;/cygdrive/c/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/OpenBLAS/OpenBLAS-0.3.9/build;/cygdrive/c/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/OpenCASCADE-7.3.0-vc14-64/freetype-2.5.5-vc14-64;/cygdrive/c/Daten/Projekte/SimulationPlatform/Third_Party_Libraries/OpenCASCADE-7.3.0-vc14-64/opencascade-7.3.0/win64/vc14

Press c to configure again. Now OCC should be found. Press g to generate the make files.

Start the compilation with
	cmake --build .
	
	

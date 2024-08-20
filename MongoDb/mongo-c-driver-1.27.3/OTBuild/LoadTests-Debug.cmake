      set (TEST_LIBMONGOC_EXE [[C:/Users/JWagner/Downloads/mongo-c-driver-1.27.3/OTBuild/src/libmongoc/Debug/test-libmongoc.exe]])
      set (SRC_ROOT [[C:/Users/JWagner/Downloads/mongo-c-driver-1.27.3]])
      set (IS_MULTICONF 1)
      if (NOT IS_MULTICONF OR CTEST_CONFIGURATION_TYPE STREQUAL "Debug")
         # We are not in multi-conf, or the current config matches our config.
         include ("${SRC_ROOT}/build/cmake/LoadTests.cmake")
      elseif (NOT CTEST_CONFIGURATION_TYPE)
         # We are in multi-conf, but no '-C' config was specified
         message (WARNING "Specify a --build-config when using CTest with a multi-config build")
      else ()
         # Do nothing. Not our config.
      endif ()
   
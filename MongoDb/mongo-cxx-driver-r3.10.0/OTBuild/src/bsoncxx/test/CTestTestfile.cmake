# CMake generated Testfile for 
# Source directory: C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/src/bsoncxx/test
# Build directory: C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/OTBuild/src/bsoncxx/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(bson "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/OTBuild/src/bsoncxx/test/Debug/test_bson.exe")
  set_tests_properties(bson PROPERTIES  _BACKTRACE_TRIPLES "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/src/bsoncxx/test/CMakeLists.txt;67;add_test;C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/src/bsoncxx/test/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(bson "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/OTBuild/src/bsoncxx/test/Release/test_bson.exe")
  set_tests_properties(bson PROPERTIES  _BACKTRACE_TRIPLES "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/src/bsoncxx/test/CMakeLists.txt;67;add_test;C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/src/bsoncxx/test/CMakeLists.txt;0;")
else()
  add_test(bson NOT_AVAILABLE)
endif()

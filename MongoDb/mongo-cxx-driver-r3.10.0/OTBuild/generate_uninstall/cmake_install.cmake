# Install script for directory: C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/generate_uninstall

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/x64")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  
      string(REPLACE ";" "\n" MONGOCXX_INSTALL_MANIFEST_CONTENT
         "${CMAKE_INSTALL_MANIFEST_FILES}")
      string(REPLACE "/" "\\" MONGOCXX_INSTALL_MANIFEST_CONTENT_WIN32
         "${MONGOCXX_INSTALL_MANIFEST_CONTENT}")
      file(WRITE "mongocxx_install_manifest.txt"
         "${MONGOCXX_INSTALL_MANIFEST_CONTENT_WIN32}")
      execute_process (
         COMMAND
            C:/Program Files/CMake/bin/cmake.exe -E env
            cmd.exe /c
            " for /f " delims= " %d in ('dir C:\\Users\\JWagner\\Downloads\\mongo-cxx-driver-r3.10.0\\x64 /s /b /ad ^| C:\\Windows\\System32\\sort.exe /r') do rmdir %d "
         OUTPUT_QUIET
         ERROR_QUIET
      )
      execute_process (
         COMMAND
            C:/Program Files/CMake/bin/cmake.exe -E env
            cmd.exe /c
            "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/etc/generate-uninstall.cmd"
            mongocxx_install_manifest.txt
            C:\\Users\\JWagner\\Downloads\\mongo-cxx-driver-r3.10.0\\x64
         OUTPUT_FILE
            "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/OTBuild/generate_uninstall/uninstall.cmd"
      )
   
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/mongo-cxx-driver" TYPE FILE PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE FILES "C:/Users/JWagner/Downloads/mongo-cxx-driver-r3.10.0/OTBuild/generate_uninstall/uninstall.cmd")
endif()


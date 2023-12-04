#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::ProtobufWellKnownTypes" for configuration "Debug"
set_property(TARGET Qt6::ProtobufWellKnownTypes APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::ProtobufWellKnownTypes PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/Qt6ProtobufWellKnownTypesd.lib"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/Qt6ProtobufWellKnownTypesd.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::ProtobufWellKnownTypes )
list(APPEND _cmake_import_check_files_for_Qt6::ProtobufWellKnownTypes "${_IMPORT_PREFIX}/lib/Qt6ProtobufWellKnownTypesd.lib" "${_IMPORT_PREFIX}/bin/Qt6ProtobufWellKnownTypesd.dll" )

# Import target "Qt6::ProtobufWellKnownTypes_protobuf_registration" for configuration "Debug"
set_property(TARGET Qt6::ProtobufWellKnownTypes_protobuf_registration APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::ProtobufWellKnownTypes_protobuf_registration PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_DEBUG ""
  IMPORTED_OBJECTS_DEBUG "${_IMPORT_PREFIX}/lib/objects-Debug/ProtobufWellKnownTypes_protobuf_registration/google/protobuf/any_protobuftyperegistrations.cpp.obj"
  )

list(APPEND _cmake_import_check_targets Qt6::ProtobufWellKnownTypes_protobuf_registration )
list(APPEND _cmake_import_check_files_for_Qt6::ProtobufWellKnownTypes_protobuf_registration "${_IMPORT_PREFIX}/lib/objects-Debug/ProtobufWellKnownTypes_protobuf_registration/google/protobuf/any_protobuftyperegistrations.cpp.obj" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

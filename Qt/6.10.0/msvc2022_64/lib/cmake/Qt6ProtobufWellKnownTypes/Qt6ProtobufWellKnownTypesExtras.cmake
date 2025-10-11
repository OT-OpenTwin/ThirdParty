# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: BSD-3-Clause

if(NOT QT_NO_CREATE_TARGETS)
    get_target_property(_ProtobufWellKnownTypes_protobuf_wellknowntypes Qt6::ProtobufWellKnownTypes
        _qt_internal_protobuf_wellknown_types)
    set(_ProtobufWellKnownTypes_proto_external_include_dirs "")
    set(_ProtobufWellKnownTypes_types_not_found "")
    set(_ProtobufWellKnownTypes_include_lookup_dirs
        "${protobuf_ROOT}"
        "${Protobuf_ROOT}"
        "$ENV{protobuf_ROOT}"
        "$ENV{Protobuf_ROOT}"
    )

    foreach(extra_protobuf_dir_path "${protobuf_DIR}" "${Protobuf_DIR}" "$ENV{protobuf_DIR}"
        "$ENV{Protobuf_DIR}")
        if(extra_protobuf_dir_path)
            list(APPEND _ProtobufWellKnownTypes_include_lookup_dirs
                "${extra_protobuf_dir_path}/../.." "${extra_protobuf_dir_path}")
        endif()
        unset(extra_protobuf_dir_path)
    endforeach()

    foreach(type IN LISTS _ProtobufWellKnownTypes_protobuf_wellknowntypes)
        unset(_ProtobufWellKnownTypes_proto_file_dir)
        find_path(_ProtobufWellKnownTypes_proto_file_dir
            NAMES "${type}"
            PATHS ${_ProtobufWellKnownTypes_include_lookup_dirs}
            PATH_SUFFIXES include
            NO_CACHE
        )
        if(_ProtobufWellKnownTypes_proto_file_dir)
            if(NOT _ProtobufWellKnownTypes_proto_file_dir IN_LIST _ProtobufWellKnownTypes_proto_external_include_dirs)
                list(APPEND _ProtobufWellKnownTypes_proto_external_include_dirs "${_ProtobufWellKnownTypes_proto_file_dir}")
            endif()
        else()
            list(APPEND _ProtobufWellKnownTypes_types_not_found "${type}")
        endif()
    endforeach()
    unset(type)

    if(NOT _ProtobufWellKnownTypes_types_not_found)
        include(
            "${CMAKE_CURRENT_LIST_DIR}/Qt6ProtobufWellKnownTypesProtobufProperties.cmake")
    else()
        set(Qt6ProtobufWellKnownTypes_FOUND FALSE)
        list(JOIN _ProtobufWellKnownTypes_types_not_found "\n    " _ProtobufWellKnownTypes_types_not_found_string)
        string(JOIN "" Qt6ProtobufWellKnownTypes_NOT_FOUND_MESSAGE
            "Qt6ProtobufWellKnownTypes lacks the following protobuf schemas:"
            "\n    ${_ProtobufWellKnownTypes_types_not_found_string}\n"
            "Please check your protobuf installation and ensure the missing schemas are in the"
            " CMake find paths. If you use a custom protobuf installation point to its location"
            " in protobuf_ROOT, Protobuf_ROOT, protobuf_DIR or Protobuf_DIR environment or"
            " cache variables.")
        unset(_ProtobufWellKnownTypes_types_not_found_string)
    endif()

    unset(_ProtobufWellKnownTypes_include_lookup_dirs)
    unset(_ProtobufWellKnownTypes_types_not_found)
    unset(_ProtobufWellKnownTypes_proto_external_include_dirs)
    unset(_ProtobufWellKnownTypes_protobuf_wellknowntypes)
endif()

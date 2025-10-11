# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: BSD-3-Clause

if(NOT QT_NO_CREATE_TARGETS)
    set(_ProtobufQtCoreTypes_proto_include_dirs "include/QtProtobufQtCoreTypes")
    foreach(proto_include_dir IN LISTS _ProtobufQtCoreTypes_proto_include_dirs)
        set_property(TARGET ${QT_CMAKE_EXPORT_NAMESPACE}::ProtobufQtCoreTypes APPEND PROPERTY
            QT_PROTO_INCLUDES "${QT6_INSTALL_PREFIX}/${proto_include_dir}")
        if(CMAKE_STAGING_PREFIX)
            set_property(TARGET ${QT_CMAKE_EXPORT_NAMESPACE}::ProtobufQtCoreTypes APPEND PROPERTY
                QT_PROTO_INCLUDES "${CMAKE_STAGING_PREFIX}/${proto_include_dir}")
        endif()
    endforeach()

    foreach(proto_include_dir IN LISTS _ProtobufQtCoreTypes_proto_external_include_dirs)
        if(NOT IS_ABSOLUTE "${proto_include_dir}")
            if(NOT QT_NO_WARN_PROTOBUF_BROKEN_INCLUDES)
                message(WRANING "The protobuf include directory ${proto_include_dir} must be an"
                    " absolute path. Skipping adding it to the ProtobufQtCoreTypes module QT_PROTO_INCLUDES."
                    " Use QT_NO_WARN_PROTOBUF_BROKEN_INCLUDES to suppress this warning.")
            endif()
            continue()
        endif()
        if(NOT EXISTS "${proto_include_dir}")
            if(NOT QT_NO_WARN_PROTOBUF_BROKEN_INCLUDES)
                message(WARNING "The protobuf include directory ${proto_include_dir} doesn't exist."
                    " Skipping adding it to the ProtobufQtCoreTypes module QT_PROTO_INCLUDES."
                    " Use QT_NO_WARN_PROTOBUF_BROKEN_INCLUDES to suppress this warning.")
            endif()
            continue()
        endif()

        set_property(TARGET ${QT_CMAKE_EXPORT_NAMESPACE}::ProtobufQtCoreTypes APPEND PROPERTY
            QT_PROTO_INCLUDES "${proto_include_dir}")
    endforeach()

    unset(_ProtobufQtCoreTypes_proto_include_dirs)
endif()

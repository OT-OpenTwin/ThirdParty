# This file is copyrighted under the BSD-license for buildsystem files of KDE
# copyright 2010, Patrick Spendrin <ps_ml@gmx.de>

if (FALSE) # XXX(kitware): Force build settings.
project(expat)

cmake_minimum_required(VERSION 2.8.10)
set(PACKAGE_BUGREPORT "expat-bugs@libexpat.org")
set(PACKAGE_NAME "expat")
set(PACKAGE_VERSION "2.2.6")
set(PACKAGE_STRING "${PACKAGE_NAME} ${PACKAGE_VERSION}")
set(PACKAGE_TARNAME "${PACKAGE_NAME}")

include(GNUInstallDirs)

if(WINCE)
    set(BUILD_tools_default OFF)
else()
    set(BUILD_tools_default ON)
endif()
if(MSVC OR NOT BUILD_tools_default)
    set(BUILD_doc_default OFF)
else()
    find_program(DOCBOOK_TO_MAN NAMES docbook2x-man db2x_docbook2man docbook2man docbook-to-man)
    if(DOCBOOK_TO_MAN)
        set(BUILD_doc_default ON)
    else()
        set(BUILD_doc_default OFF)
    endif()
endif()

option(BUILD_tools "build the xmlwf tool for expat library" ${BUILD_tools_default})
option(BUILD_examples "build the examples for expat library" ON)
option(BUILD_tests "build the tests for expat library" ON)
option(BUILD_shared "build a shared expat library" ON)
option(BUILD_doc "build man page for xmlwf" ${BUILD_doc_default})
option(USE_libbsd "utilize libbsd (for arc4random_buf)" OFF)
option(INSTALL "install expat files in cmake install target" ON)
else ()
set(BUILD_tools OFF)
set(BUILD_examples OFF)
set(BUILD_tests OFF)
set(BUILD_shared ${BUILD_SHARED_LIBS})
set(BUILD_doc OFF)
set(USE_libbsd OFF)
set(INSTALL OFF)
endif ()

if(USE_libbsd)
    find_library(LIB_BSD NAMES bsd)
    if(NOT LIB_BSD)
        message(FATAL_ERROR "USE_libbsd option is enabled, but libbsd was not found")
    else()
        set(HAVE_LIBBSD TRUE)
    endif()
endif()

# configuration options
if (FALSE) # XXX(kitware): Force configuration values.
set(XML_CONTEXT_BYTES 1024 CACHE STRING "Define to specify how much context to retain around the current parse point")
option(XML_DTD "Define to make parameter entity parsing functionality available" ON)
option(XML_NS "Define to make XML Namespaces functionality available" ON)
option(WARNINGS_AS_ERRORS "Treat all compiler warnings as errors" OFF)
else ()
set(XML_CONTEXT_BYTES 1024)
set(XML_DTD ON)
set(XML_NS ON)
set(WARNINGS_AS_ERRORS OFF)
endif ()
if(NOT WIN32)
    if (FALSE) # XXX(kitware): Force configuration values.
    option(XML_DEV_URANDOM "Define to include code reading entropy from `/dev/urandom'." ON)
    else ()
    set(XML_DEV_URANDOM ON)
    endif ()
    if(XML_DEV_URANDOM)
        set(XML_DEV_URANDOM 1)
    else(XML_DEV_URANDOM)
        set(XML_DEV_URANDOM 0)
    endif(XML_DEV_URANDOM)
endif()
if (FALSE) # XXX(kitware): Force configuration values.
option(XML_UNICODE "Use UTF-16 encoded chars (two bytes) instead of UTF-8" OFF)
option(XML_UNICODE_WCHAR_T "Use wchar_t to represent UTF-16 instead of unsigned short" OFF)
else ()
set(XML_UNICODE OFF)
set(XML_UNICODE_WCHAR_T OFF)
endif ()

if(XML_DTD)
    set(XML_DTD 1)
else(XML_DTD)
    set(XML_DTD 0)
endif(XML_DTD)
if(XML_NS)
    set(XML_NS 1)
else(XML_NS)
    set(XML_NS 0)
endif(XML_NS)
if(XML_UNICODE)
    set(XML_UNICODE 1)
else(XML_UNICODE)
    set(XML_UNICODE 0)
endif(XML_UNICODE)
if(XML_UNICODE_WCHAR_T)
    set(XML_UNICODE_WCHAR_T 1)
else(XML_UNICODE_WCHAR_T)
    set(XML_UNICODE_WCHAR_T 0)
endif(XML_UNICODE_WCHAR_T)

if(XML_UNICODE_WCHAR_T AND NOT XML_UNICODE)
    message(SEND_ERROR "Option XML_UNICODE_WCHAR_T=ON may not be used without XML_UNICODE=ON.")
    set(XML_UNICODE 1)
endif(XML_UNICODE_WCHAR_T AND NOT XML_UNICODE)

if(BUILD_tools AND (XML_UNICODE AND NOT XML_UNICODE_WCHAR_T))
    message(SEND_ERROR "The xmlwf tool can not be built with option XML_UNICODE_WCHAR_T=OFF and XML_UNICODE=ON. Either set XML_UNICODE_WCHAR_T=ON or BUILD_tools=OFF.")
endif()

if(BUILD_tests)
    enable_testing()
endif(BUILD_tests)

include(${CMAKE_CURRENT_LIST_DIR}/ConfigureChecks.cmake)

if (FALSE) # XXX(kitware): This flag only works on GCC alikes. Upstream should address this.
set(EXTRA_COMPILE_FLAGS)
if(FLAG_NO_STRICT_ALIASING)
    set(EXTRA_COMPILE_FLAGS "${EXTRA_COMPILE_FLAGS} -fno-strict-aliasing")
endif()
if (WARNINGS_AS_ERRORS)
    if(MSVC)
        add_definitions(/WX)
    else(MSVC)
        set(EXTRA_COMPILE_FLAGS "${EXTRA_COMPILE_FLAGS} -Werror")
    endif(MSVC)
endif(WARNINGS_AS_ERRORS)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${EXTRA_COMPILE_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${EXTRA_COMPILE_FLAGS}")
endif ()

if (FALSE) # XXX(kitware): Force build settings.
set(MSVC_USE_STATIC_CRT OFF CACHE BOOL "Use /MT flag (static CRT) when compiling in MSVC")
else ()
set(MSVC_USE_STATIC_CRT OFF)
endif ()
if (MSVC)
    if (MSVC_USE_STATIC_CRT)
        message("-- Using static CRT ${MSVC_USE_STATIC_CRT}")
        foreach(flag_var
                CMAKE_CXX_FLAGS_DEBUG
                CMAKE_CXX_FLAGS_RELEASE
                CMAKE_CXX_FLAGS_MINSIZEREL
                CMAKE_CXX_FLAGS_RELWITHDEBINFO
                CMAKE_C_FLAGS_DEBUG
                CMAKE_C_FLAGS_RELEASE
                CMAKE_C_FLAGS_MINSIZEREL
                CMAKE_C_FLAGS_RELWITHDEBINFO
                )
            string(REPLACE "/MD" "/MT" ${flag_var} "${${flag_var}}")
        endforeach()
    endif()
endif()

include_directories(${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/lib)

if (FALSE) # XXX(kitware): Settings handled by VTK.
if(MSVC)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS -wd4996)
endif(MSVC)
if(WIN32)
    set(CMAKE_DEBUG_POSTFIX "d" CACHE STRING "Add a suffix, usually d on Windows")
endif(WIN32)
endif ()

set(expat_SRCS
    lib/loadlibrary.c
    lib/xmlparse.c
    lib/xmlrole.c
    lib/xmltok.c
    lib/xmltok_impl.c
    lib/xmltok_ns.c
)

if(BUILD_shared)
    set(_SHARED SHARED)
    if(WIN32)
        if (FALSE) # XXX(kitware): Exporting is handled via generate_export_header
        set(expat_SRCS ${expat_SRCS} lib/libexpat.def)
        endif ()
    endif(WIN32)
else(BUILD_shared)
    set(_SHARED STATIC)
    if(WIN32)
        add_definitions(-DXML_STATIC)
    endif(WIN32)
endif(BUILD_shared)

if (FALSE) # XXX(kitware): Use VTK's build macros.
add_library(expat ${_SHARED} ${expat_SRCS})
if(USE_libbsd)
    target_link_libraries(expat ${LIB_BSD})
endif()

set(LIBCURRENT 7)   # sync
set(LIBREVISION 8)  # with
set(LIBAGE 6)       # configure.ac!
math(EXPR LIBCURRENT_MINUS_AGE "${LIBCURRENT} - ${LIBAGE}")

if(NOT WIN32)
    set_property(TARGET expat PROPERTY VERSION ${LIBCURRENT_MINUS_AGE}.${LIBAGE}.${LIBREVISION})
    set_property(TARGET expat PROPERTY SOVERSION ${LIBCURRENT_MINUS_AGE})
    set_property(TARGET expat PROPERTY NO_SONAME ${NO_SONAME})
endif(NOT WIN32)

macro(expat_install)
    if(INSTALL)
        install(${ARGN})
    endif()
endmacro()

expat_install(TARGETS expat RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
                      LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
                      ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
else ()
set(expat_headers
    lib/expat.h
    lib/expat_external.h
    lib/vtk_expat_mangle.h)

if (NOT BUILD_SHARED_LIBS)
  set(XML_STATIC 1)
endif ()

vtk_module_add_module(VTK::expat
  SOURCES ${expat_SRCS}
  HEADERS ${expat_headers}
  HEADERS_SUBDIR "vtkexpat/lib")
target_compile_definitions(expat
  PRIVATE
    # Support XML files >2GB.
    XML_LARGE_SIZE)
endif ()

if (FALSE) # XXX(kitware): Do not install a .pc file.
set(prefix ${CMAKE_INSTALL_PREFIX})
set(exec_prefix "\${prefix}")
set(libdir "\${exec_prefix}/lib")
set(includedir "\${prefix}/include")
configure_file(expat.pc.in ${CMAKE_CURRENT_BINARY_DIR}/expat.pc @ONLY)

expat_install(FILES lib/expat.h lib/expat_external.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
expat_install(FILES ${CMAKE_CURRENT_BINARY_DIR}/expat.pc DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)
endif ()

if(BUILD_tools)
    set(xmlwf_SRCS
        xmlwf/xmlwf.c
        xmlwf/xmlfile.c
        xmlwf/codepage.c
        xmlwf/readfilemap.c
    )

    add_executable(xmlwf ${xmlwf_SRCS})
    set_property(TARGET xmlwf PROPERTY RUNTIME_OUTPUT_DIRECTORY xmlwf)
    target_link_libraries(xmlwf expat)
    expat_install(TARGETS xmlwf DESTINATION ${CMAKE_INSTALL_BINDIR})
    if(BUILD_doc)
        add_custom_command(TARGET expat PRE_BUILD COMMAND "${DOCBOOK_TO_MAN}" "${PROJECT_SOURCE_DIR}/doc/xmlwf.xml" && mv "XMLWF.1" "${PROJECT_SOURCE_DIR}/doc/xmlwf.1")
        expat_install(FILES "${PROJECT_SOURCE_DIR}/doc/xmlwf.1" DESTINATION ${CMAKE_INSTALL_MANDIR}/man1)
    endif()
endif()

if(BUILD_examples)
    add_executable(elements examples/elements.c)
    set_property(TARGET elements PROPERTY RUNTIME_OUTPUT_DIRECTORY examples)
    target_link_libraries(elements expat)

    add_executable(outline examples/outline.c)
    set_property(TARGET outline PROPERTY RUNTIME_OUTPUT_DIRECTORY examples)
    target_link_libraries(outline expat)
endif(BUILD_examples)

if(BUILD_tests)
    ## these are unittests that can be run on any platform
    add_executable(runtests tests/runtests.c tests/chardata.c tests/structdata.c tests/minicheck.c tests/memcheck.c)
    set_property(TARGET runtests PROPERTY RUNTIME_OUTPUT_DIRECTORY tests)
    target_link_libraries(runtests expat)
    add_test(runtests tests/runtests)

    add_executable(runtestspp tests/runtestspp.cpp tests/chardata.c tests/structdata.c tests/minicheck.c tests/memcheck.c)
    set_property(TARGET runtestspp PROPERTY RUNTIME_OUTPUT_DIRECTORY tests)
    target_link_libraries(runtestspp expat)
    add_test(runtestspp tests/runtestspp)
endif(BUILD_tests)

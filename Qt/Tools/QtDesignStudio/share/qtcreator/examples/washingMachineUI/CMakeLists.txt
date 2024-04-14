cmake_minimum_required (VERSION 3.15)

project(washingMachineUI VERSION 0.0.1 LANGUAGES C CXX ASM ASM_MASM)

if (NOT TARGET Qul::Core)
    find_package(Qul)
endif()

if (Qul_VERSION VERSION_GREATER_EQUAL "1.7")
    qul_add_target(washingMachineUI)
elseif (Qul_VERSION VERSION_EQUAL "1.6")
    add_executable(washingMachineUI)
    target_link_libraries(washingMachineUI
        Qul::QuickUltralite
        Qul::QuickUltralitePlatform)
elseif (Qul_VERSION VERSION_LESS "1.6")
    message(FATAL_ERROR "QUL versions below 1.6 are not supported in this project.")
endif()

if (Qul_VERSION VERSION_GREATER_EQUAL "2.0")
    set_property(TARGET washingMachineUI APPEND PROPERTY QUL_FONT_FILES
        "${CMAKE_CURRENT_SOURCE_DIR}/fonts/MavenPro-Regular.ttf")
elseif (Qul_VERSION VERSION_GREATER_EQUAL "1.7")
    set_property(TARGET washingMachineUI APPEND PROPERTY QUL_FONTS_DIR
        "${CMAKE_CURRENT_SOURCE_DIR}/fonts")
else()
    set(QUL_FONTS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/fonts,${QUL_FONTS_DIR}")
endif()

file(GLOB_RECURSE imgSources "*.png")
if (imgSources)
    qul_add_resource(washingMachineUI FILES ${imgSources})
endif()

file(GLOB_RECURSE qmlSources "*.qml")
qul_target_qml_sources(washingMachineUI ${qmlSources})

if (Qul_VERSION VERSION_GREATER_EQUAL "2.0")
    target_link_libraries(washingMachineUI PRIVATE
        Qul::Timeline
        Qul::Controls)
else()
    target_link_libraries(washingMachineUI
        Qul::QuickUltraliteTimeline
        Qul::QuickUltraliteControlsStyleDefault)
endif()

app_target_setup_os(washingMachineUI)

if (Qul_VERSION VERSION_GREATER_EQUAL "1.7")
    app_target_default_entrypoint(washingMachineUI washingMachineUI)
else()
    app_target_default_main(washingMachineUI washingMachineUI)
endif()

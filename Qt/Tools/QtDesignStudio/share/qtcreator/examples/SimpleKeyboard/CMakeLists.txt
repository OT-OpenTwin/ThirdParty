# SimpleKeyboard example shows how to use Qt Virtual Keyboard
# for example in an embedded application.

cmake_minimum_required(VERSION 3.18)

project(SimpleKeyboardApp LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 COMPONENTS Gui Qml Quick)
add_executable(SimpleKeyboardApp src/main.cpp)

target_link_libraries(SimpleKeyboardApp PRIVATE
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Gui
    Qt${QT_VERSION_MAJOR}::Quick
    Qt${QT_VERSION_MAJOR}::Qml
)

include(${CMAKE_CURRENT_SOURCE_DIR}/qmlmodules)

qt_add_resources(SimpleKeyboardApp "configuration"
PREFIX "/"
FILES
qtquickcontrols2.conf
)


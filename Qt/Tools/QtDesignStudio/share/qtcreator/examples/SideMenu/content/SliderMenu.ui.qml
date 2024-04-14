
/****************************************************************************
**
** Copyright (C) 2019 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Design Studio.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/
import QtQuick 2.8
import QtQuick.Timeline 1.0
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.0

Item {
    id: sliderMenu
    width: 200
    height: 200
    property alias slider_4BValue: slider_4B.value
    property alias slider_4AValue: slider_4A.value
    property alias slider_1CValue: slider_1C.value
    property alias slider_1BValue: slider_1B.value
    property alias slider_1AValue: slider_1A.value

    Text {
        id: mainMenu4
        x: 8
        y: 338
        color: "#242121"
        text: qsTr("BRIGHTNESS & CONTRAST")
        Item {
            id: submenu_4
            x: 0
            y: 50
            width: 276
            height: 190
            Text {
                id: subMenu_4A
                x: -2
                y: 0
                color: "#242121"
                text: qsTr("BRIGHTNESS")
                font.family: "IBM Plex Mono"
                font.pixelSize: 16
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                font.weight: Font.ExtraLight
            }

            Slider {
                id: slider_4A
                x: -6
                y: 23
                width: 282
                height: 17
                handle: Rectangle {
                    x: slider_4A.leftPadding + slider_4A.visualPosition
                       * (slider_4A.availableWidth - width)
                    y: slider_4A.topPadding + slider_4A.availableHeight / 2 - height / 2
                    color: slider_4A.pressed ? "#f0f0f0" : "#f6f6f6"
                    radius: 2
                    implicitHeight: 16
                    implicitWidth: 4
                }
                value: 0
                background: Rectangle {
                    x: slider_4A.leftPadding
                    y: slider_4A.topPadding + slider_4A.availableHeight / 2 - height / 2
                    width: slider_4A.availableWidth
                    height: implicitHeight
                    color: "#313437"
                    radius: 2
                    Rectangle {
                        width: slider_4A.visualPosition * parent.width
                        height: parent.height
                        color: "#fbfbfb"
                        radius: 2
                    }
                    implicitHeight: 2
                    implicitWidth: 200
                }
                to: 1
                stepSize: 0
                from: -1
            }

            Text {
                id: subMenu_4B
                x: -2
                y: 46
                color: "#242121"
                text: qsTr("CONTRAST")
                font.family: "IBM Plex Mono"
                font.pixelSize: 16
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                font.weight: Font.ExtraLight
            }

            Slider {
                id: slider_4B
                x: -6
                y: 69
                width: 282
                height: 17
                from: -1
                handle: Rectangle {
                    x: slider_4B.leftPadding + slider_4B.visualPosition
                       * (slider_4B.availableWidth - width)
                    y: slider_4B.topPadding + slider_4B.availableHeight / 2 - height / 2
                    color: slider_4B.pressed ? "#f0f0f0" : "#f6f6f6"
                    radius: 2
                    implicitHeight: 16
                    implicitWidth: 4
                }
                value: 0
                background: Rectangle {
                    x: slider_4B.leftPadding
                    y: slider_4B.topPadding + slider_4B.availableHeight / 2 - height / 2
                    width: slider_4B.availableWidth
                    height: implicitHeight
                    color: "#313437"
                    radius: 2
                    Rectangle {
                        width: slider_4B.visualPosition * parent.width
                        height: parent.height
                        color: "#fbfbfb"
                        radius: 2
                    }
                    implicitHeight: 2
                    implicitWidth: 200
                }
                to: 1
                stepSize: 0
            }
        }
        font.family: "IBM Plex Mono"
        font.pixelSize: 23
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        font.weight: Font.ExtraLight
    }

    Text {
        id: mainMenu1
        x: 8
        y: 132
        color: "#242121"
        text: qsTr("HUE & SATURATION")
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        font.weight: Font.ExtraLight
        font.family: "IBM Plex Mono"
        font.pixelSize: 23

        Item {
            id: submenu_1
            x: 0
            y: 48
            width: 276
            height: 190

            Text {
                id: subMenu_1A
                x: -2
                y: 0
                color: "#242121"
                text: qsTr("HUE")
                font.pixelSize: 16
                font.weight: Font.ExtraLight
                font.family: "IBM Plex Mono"
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            Slider {
                id: slider_1A
                x: -6
                y: 23
                width: 282
                height: 17
                stepSize: 0.1
                value: 0.5

                background: Rectangle {
                    x: slider_1A.leftPadding
                    y: slider_1A.topPadding + slider_1A.availableHeight / 2 - height / 2
                    implicitWidth: 200
                    implicitHeight: 2
                    width: slider_1A.availableWidth
                    height: implicitHeight
                    radius: 2
                    color: "#313437"

                    Rectangle {
                        width: slider_1A.visualPosition * parent.width
                        height: parent.height
                        color: "#fbfbfb"
                        radius: 2
                    }
                }

                handle: Rectangle {
                    x: slider_1A.leftPadding + slider_1A.visualPosition
                       * (slider_1A.availableWidth - width)
                    y: slider_1A.topPadding + slider_1A.availableHeight / 2 - height / 2
                    implicitWidth: 4
                    implicitHeight: 16
                    radius: 2
                    color: slider_1A.pressed ? "#f0f0f0" : "#f6f6f6"
                }
            }

            Text {
                id: subMenu_1B
                x: -2
                y: 46
                color: "#242121"
                text: qsTr("LIGHTNESS")
                font.pixelSize: 16
                font.family: "IBM Plex Mono"
                font.weight: Font.ExtraLight
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            Slider {
                id: slider_1B
                x: -6
                y: 69
                width: 282
                height: 17
                from: -1
                to: 1
                stepSize: 0
                enabled: true
                handle: Rectangle {
                    x: slider_1B.leftPadding + slider_1B.visualPosition
                       * (slider_1B.availableWidth - width)
                    y: slider_1B.topPadding + slider_1B.availableHeight / 2 - height / 2
                    color: slider_1B.pressed ? "#f0f0f0" : "#f6f6f6"
                    radius: 2
                    implicitHeight: 16
                    implicitWidth: 4
                }
                background: Rectangle {
                    x: slider_1B.leftPadding
                    y: slider_1B.topPadding + slider_1B.availableHeight / 2 - height / 2
                    width: slider_1B.availableWidth
                    height: implicitHeight
                    color: "#313437"
                    radius: 2
                    implicitHeight: 2
                    implicitWidth: 200
                    Rectangle {
                        width: slider_1B.visualPosition * parent.width
                        height: parent.height
                        color: "#fbfbfb"
                        radius: 2
                    }
                }
                value: 0
            }

            Text {
                id: subMenu_1C
                x: 0
                y: 92
                color: "#242121"
                text: qsTr("SATURATION")
                font.pixelSize: 16
                font.weight: Font.ExtraLight
                font.family: "IBM Plex Mono"
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            Slider {
                id: slider_1C
                x: -4
                y: 115
                width: 282
                height: 17
                from: 0
                handle: Rectangle {
                    x: slider_1C.leftPadding + slider_1C.visualPosition
                       * (slider_1C.availableWidth - width)
                    y: slider_1C.topPadding + slider_1C.availableHeight / 2 - height / 2
                    color: slider_1C.pressed ? "#f0f0f0" : "#f6f6f6"
                    radius: 2
                    implicitHeight: 16
                    implicitWidth: 4
                }
                background: Rectangle {
                    x: slider_1C.leftPadding
                    y: slider_1C.topPadding + slider_1C.availableHeight / 2 - height / 2
                    width: slider_1C.availableWidth
                    height: implicitHeight
                    color: "#313437"
                    radius: 2
                    implicitHeight: 2
                    implicitWidth: 200
                    Rectangle {
                        width: slider_1C.visualPosition * parent.width
                        height: parent.height
                        color: "#fbfbfb"
                        radius: 2
                    }
                }
                value: 0.5
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;height:800;width:200}
}
##^##*/


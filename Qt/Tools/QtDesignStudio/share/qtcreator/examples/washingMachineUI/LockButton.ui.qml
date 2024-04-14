/****************************************************************************
**
** Copyright (C) 2021 The Qt Company Ltd.
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

Item {
    id: smallbutton
    width: 43
    height: 43
    property bool isLocked: true
    property alias unlockediconoffSource: unlockediconoff.source
    property alias lockedicononSource: lockediconon.source
    property alias unlockedicononSource: unlockediconon.source
    property alias currenticonoffSource: currenticonoff.source

    Image {
        id: outllineoff
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        source: "assets/outllineoff.png"
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: smallbuttoniconfill
        anchors.verticalCenter: parent.verticalCenter
        source: "assets/smallbuttoniconfill.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: currenticonoff
        anchors.verticalCenter: parent.verticalCenter
        source: "assets/currenticonoff.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: unlockediconon
        anchors.verticalCenter: parent.verticalCenter
        source: "assets/unlockediconon.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: lockediconon
        anchors.verticalCenter: parent.verticalCenter
        source: "assets/lockediconon.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: unlockediconoff
        anchors.verticalCenter: parent.verticalCenter
        source: "assets/unlockediconoff.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent

        Connections {
            target: mouseArea
            onReleased: smallbutton.isLocked = !smallbutton.isLocked
        }
    }
    states: [
        State {
            name: "lockedDefault"
            when: !mouseArea.pressed && smallbutton.isLocked

            PropertyChanges {
                target: unlockediconoff
                visible: false
            }

            PropertyChanges {
                target: lockediconon
                visible: false
            }

            PropertyChanges {
                target: currenticonoff
                visible: true
            }

            PropertyChanges {
                target: unlockediconon
                visible: false
            }

            PropertyChanges {
                target: smallbuttoniconfill
                visible: false
            }
        },
        State {
            name: "lockedPressed"
            when: mouseArea.pressed && smallbutton.isLocked

            PropertyChanges {
                target: unlockediconon
                visible: false
            }

            PropertyChanges {
                target: unlockediconoff
                visible: false
            }

            PropertyChanges {
                target: lockediconon
                visible: true
            }

            PropertyChanges {
                target: currenticonoff
                visible: false
            }

            PropertyChanges {
                target: smallbuttoniconfill
                visible: true
            }
        },
        State {
            name: "unlockedDefault"
            when: !mouseArea.pressed && !smallbutton.isLocked

            PropertyChanges {
                target: currenticonoff
                visible: false
            }

            PropertyChanges {
                target: unlockediconon
                visible: false
            }

            PropertyChanges {
                target: unlockediconoff
                visible: true
            }

            PropertyChanges {
                target: lockediconon
                visible: false
            }

            PropertyChanges {
                target: smallbuttoniconfill
                visible: false
            }
        },
        State {
            name: "unlockedPressed"
            when: mouseArea.pressed && !smallbutton.isLocked

            PropertyChanges {
                target: lockediconon
                visible: false
            }

            PropertyChanges {
                target: unlockediconoff
                visible: false
            }

            PropertyChanges {
                target: unlockediconon
                visible: true
            }

            PropertyChanges {
                target: currenticonoff
                visible: false
            }

            PropertyChanges {
                target: smallbuttoniconfill
                visible: true
            }
        }
    ]
}


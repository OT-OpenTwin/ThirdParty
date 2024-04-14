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

import QtQuick 2.11

Item {
    id: presetsScreen
    width: 480
    height: 272

    signal startRun
    signal cancelPresets

    property int runDuration: 20

    Flatbackground {
        id: backgroundFull
        anchors.fill: parent
    }

    Presets {
        id: presets

        visible: true

        Connections {
            target: presets
            onPresetSelected: {
                presetsScreen.runDuration = presets.duration

                quickstart.runDuration = presetsScreen.runDuration

                presetsScreen.state = "Quickstart"
            }
        }
    }

    Quickstarts {
        id: quickstart

        visible: false

        Connections {
            target: quickstart
            onApplied: {
                startRun()
            }

            onDetailsClicked: {
                washprogram.resetSettings()
                presetsScreen.state = "WashProgram"
            }
        }
    }

    Washprogram {
        id: washprogram

        visible: false
        anchors.fill: parent

        Connections {
            target: washprogram

            onCanceled: {
                presetsScreen.state = "Quickstart"
            }

            onApplied: {
                presetsScreen.runDuration = washprogram.runDuration
                startRun()
            }
        }
    }


    Connections {
        target: presetsScreen
        onVisibleChanged: {
            if (visible) {
                presetsScreen.state = "PresetsList"
            }
        }
    }

    Timedate {
        id: settings_timedateinstance
        x: 425
        y: 8
        width: 47
        height: 30
    }

    states: [
        State {
            name: "PresetsList"

            PropertyChanges {
                target: presets
                visible: true
            }

            PropertyChanges {
                target: quickstart
                visible: false
            }

            PropertyChanges {
                target: washprogram
                visible: false
            }
        },
        State {
            name: "Quickstart"

            PropertyChanges {
                target: quickstart
                visible: true
            }

            PropertyChanges {
                target: presets
                visible: false
            }

            PropertyChanges {
                target: washprogram
                visible: false
            }
        },
        State {
            name: "WashProgram"

            PropertyChanges {
                target: quickstart
                visible: false
            }

            PropertyChanges {
                target: presets
                visible: false
            }

            PropertyChanges {
                target: washprogram
                visible: true
            }
        }
    ]
}


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
import QtQuick.Timeline 1.0

Item {
    id: running
    width: 480
    height: 272
    clip: true

    property int runDuration: 20
    property bool activated: false

    signal startRun
    signal pauseRun
    signal stopRun
    signal runFinished

    RunningLogic {
        id: logic

        Connections {
            target: logic
            onRunFinished: {
                timelineAnimation.stop()
                running.runFinished()
            }
        }
    }

    Connections {
        target: running
        onStartRun: {
            timelineAnimation.start()

            logic.runDuration = running.runDuration
            logic.startRun()

            lockbuttoninstance.isLocked = true
            pausebuttoninstance.isLocked = true
        }

        onRunFinished: {
            timelineAnimation.stop()

            logic.stopRun()
        }
    }

    Rectangle {
        id: background
        color: "#333333"
        anchors.fill: parent
    }

    WaveAni {
        id: waveAni
        y: 176
        width: 400
        height: 367
        anchors.horizontalCenter: backgroundcutout.horizontalCenter
        clip: true
    }

    Image {
        id: backgroundcutout
        y: -2
        source: "assets/backgroundcutout.png"
        anchors.horizontalCenterOffset: 2
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Image {
        id: washdrumoutlne
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenterOffset: 6
        source: "assets/washdrumoutlne.png"

        Text {
            id: text1
            x: 53
            y: 76
            visible: true
            color: "#e544a1"
            text: qsTr("Ready!")
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.verticalCenter: washdrumoutlne.verticalCenter
            anchors.horizontalCenter: washdrumoutlne.horizontalCenter
            font.family: "Maven Pro"
        }
    }

    Text {
        id: remaintimelabel
        y: 233
        color: "#B8B8B8"
        text: "Remaining Time: " + (logic.minutesLeft + " min")
        font.pixelSize: 16
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: "Maven Pro"
    }

    Text {
        id: finishingatlabel
        y: 251
        width: 104
        height: 15
        color: "#B8B8B8"
        text: "Finishing At: " + hoursStr + ":" + minutesStr
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: "Maven Pro"

        property int subminutes: datetimeinstance_running.currentMinuteInt + logic.minutesLeft
        property int minutes: subminutes % 60
        property int hours: (datetimeinstance_running.currentHourInt + (subminutes / 60)) % 24

        property string minutesStr: ((minutes < 10) ? ("0" + minutes) : minutes)
        property string hoursStr: ((hours < 10) ? ("0" + hours) : hours)
    }

    Timedate {
        id: datetimeinstance_running
        x: 425
        y: 8
        width: 47
        height: 30
    }

    LockButton {
        id: lockbuttoninstance
        width: 43
        height: 43
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 16
        anchors.topMargin: 16
    }

    LockButton {
        id: pausebuttoninstance
        width: 43
        height: 43
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 16
        anchors.rightMargin: 16
        unlockedicononSource: "assets/resumeiconon.png"
        unlockediconoffSource: "assets/resumeiconoff.png"
        lockedicononSource: "assets/pauseiconoff.png"
        currenticonoffSource: "assets/pauseiconon_1.png"
    }

    Smallbutton {
        id: stopbuttoninstance
        width: 43
        height: 43
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 16
        anchors.leftMargin: 16
        lockedicononSource: "assets/closeiconoff.png"
        currenticonoffSource: "assets/pauseiconon.png"

        Connections {
            target: stopbuttoninstance
            onClicked: stopRun()
            onStateChanged: if (stopbuttoninstance.state == "complete")
                                stopRun()
        }
    }

    states: [
        State {
            name: "inactive"
            when: !running.activated

            PropertyChanges {
                target: timeline
                enabled: false
            }
            PropertyChanges {
                target: text1
                visible: false
            }
        },
        State {
            name: "running"
            when: pausebuttoninstance.isLocked && !lockbuttoninstance.isLocked

            PropertyChanges {
                target: text1
                visible: false
            }

            PropertyChanges {
                target: logic
                isRunning: true
            }
        },
        State {
            name: "paused"
            when: !pausebuttoninstance.isLocked && !lockbuttoninstance.isLocked

            PropertyChanges {
                target: timeline
                enabled: false
            }

            PropertyChanges {
                target: text1
                text: qsTr("Paused!")
                visible: true
            }

            PropertyChanges {
                target: logic
                isRunning: false
            }
        },
        State {
            name: "runningLocked"
            when: pausebuttoninstance.isLocked && lockbuttoninstance.isLocked
            PropertyChanges {
                target: text1
                visible: false
            }

            PropertyChanges {
                target: stopbuttoninstance
                opacity: 0.203
                enabled: false
            }

            PropertyChanges {
                target: pausebuttoninstance
                opacity: 0.203
                enabled: false
            }

            PropertyChanges {
                target: logic
                isRunning: true
            }
        },
        State {
            name: "pausedLocked"
            when: !pausebuttoninstance.isLocked && lockbuttoninstance.isLocked
            PropertyChanges {
                target: timeline
                enabled: false
            }

            PropertyChanges {
                target: text1
                text: qsTr("Paused!")
                visible: true
            }

            PropertyChanges {
                target: logic
                isRunning: false
            }

            PropertyChanges {
                target: stopbuttoninstance
                opacity: 0.203
                enabled: false
            }

            PropertyChanges {
                target: pausebuttoninstance
                opacity: 0.203
                enabled: false
            }
        },
        State {
            name: "finished"
            PropertyChanges {
                target: text1
                visible: true
                text: qsTr("Ready!")
            }

            PropertyChanges {
                target: pausebuttoninstance
                opacity: 0.203
                enabled: false
            }
        }
    ]

    Timeline {
        id: timeline
        animations: [
            TimelineAnimation {
                id: timelineAnimation
                running: true
                loops: 1
                duration: 100000
                to: 10000
                from: 0
            }
        ]
        enabled: true
        endFrame: 10000
        startFrame: 0

        KeyframeGroup {
            target: waveAni
            property: "y"
            Keyframe {
                value: -92
                frame: 10000
            }

            Keyframe {
                value: 176
                frame: 0
            }
        }
    }
}


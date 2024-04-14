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
    id: bigbutton
    width: 84
    height: 84
    property alias presetlabelFontpixelSize: presetlabel.fontPixelSize
    property alias presetlabelColor: presetlabel.color
    property alias presetlabelText: presetlabel.text
    state: "default"

    MultSegmentArc {
        id: multSegmentArc
        x: -11
        y: -9
        clip: false
        maskColor: "#333333"
        arcSegment1Source: "assets/bigArcSeg1.png"
        arcSegment2Source: "assets/bigArcSeg2.png"
        arcSegment3Source: "assets/bigArcSeg3.png"
        arcSegment4Source: "assets/bigArcSeg4.png"
    }

    Image {
        id: presetoutline
        x: 2
        y: 2
        source: "assets/presetoutline.png"
    }

    Image {
        id: bigbuttoniconfill
        x: 3
        y: 3
        width: 77
        height: 77
        source: "assets/bigbuttoniconfill.png"
        fillMode: Image.PreserveAspectFit
    }

    Text {
        property real fontPixelSize: 16

        id: presetlabel
        x: 18
        y: 32
        width: 47
        height: 16
        color: "#B8B8B8"
        text: "Preset"
        font.pixelSize: 16
        horizontalAlignment: Text.AlignHCenter
        font.family: "Maven Pro"
//        font.styleName: "Regular"
    }

    states: [
        State {
            name: "default"
            when: !mouseArea.pressed

            PropertyChanges {
                target: bigbuttoniconfill
                visible: false
            }

            PropertyChanges {
                target: presetlabel
                color: "#e544a1"
            }

            PropertyChanges {
                target: timeline
                enabled: false
            }
        },
        State {
            name: "pressed"
            when: mouseArea.pressed

            PropertyChanges {
                target: timeline
                enabled: true
            }

            PropertyChanges {
                target: timelineAnimation
                running: true
            }

            PropertyChanges {
                target: multSegmentArc
                x: -11
                y: -10
                clip: false
            }
        }
    ]

    MouseArea {
        id: mouseArea
        anchors.fill: parent
    }

    Timeline {
        id: timeline
        animations: [
            TimelineAnimation {
                id: timelineAnimation
                running: false
                loops: 1
                duration: 1000
                to: 1000
                from: 0
            }
        ]
        startFrame: 0
        endFrame: 1000
        enabled: false

        KeyframeGroup {
            target: multSegmentArc
            property: "timelineCurrentFrame"
            Keyframe {
                frame: 0
                value: 0
            }

            Keyframe {
                frame: 1000
                value: 1000
            }
        }
    }
}


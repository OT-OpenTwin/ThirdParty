/****************************************************************************
**
** Copyright (C) 2023 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of Qt Creator.
**
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 as published by the Free Software
** Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
****************************************************************************/

import QtQuick
import QtQuick.Controls
import QtQuick.Timeline

Rectangle {
    id: rectangle
    width: 400
    height: 400
    color: "#ffffff"

    Rectangle {
        id: rectangle1
        width: 200
        height: 200
        color: "#ffffff"
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Rectangle {
            id: rectangle2
            x: 40
            y: 40
            width: 120
            height: 120
            color: "#8c8c8c"
            radius: 60
            border.width: 0

            Item {
                id: item1
                x: 0
                y: 0
                width: 120
                height: 120
                rotation: 360

                Rectangle {
                    id: rectangle3
                    x: 55
                    y: -5
                    width: 10
                    height: 65
                    color: "#000000"
                }
            }
        }
    }

    Timeline {
        id: timeline
        animations: [
            TimelineAnimation {
                id: timelineAnimation
                pingPong: true
                loops: -1
                duration: 1000
                running: true
                to: 1000
                from: 0
            }
        ]
        endFrame: 1000
        startFrame: 0
        enabled: true

        KeyframeGroup {
            target: item1
            property: "rotation"

            Keyframe {
                easing.bezierCurve: [0.198, 0.68, 0.856, 0.573, 1, 1]
                frame: 0
                value: 0
            }

            Keyframe {
                easing.bezierCurve: [0.252, -0.021, 0.333, 1.2, 1, 1]
                frame: 1000
                value: 360
            }
        }
    }

    states: [
        State {
            name: "clicked"
            when: button.checked
        }
    ]
}

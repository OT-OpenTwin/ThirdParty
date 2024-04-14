/****************************************************************************
**
** Copyright (C) 2022 The Qt Company Ltd.
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
import QtQuick.Layouts
import WelcomeScreen 1.0
import projectmodel 1.0

Item {
    id: blogBanner
    height: 300
    width: 300

    Text {
        id: textItem

        text: "Qt Design Studio 4.3 released!"
        anchors.fill: parent
        font.pixelSize: 18

        color: Constants.currentBrand
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        wrapMode: Text.WordWrap
        font.underline: linkArea.containsMouse

        anchors.margins: 8
        anchors.topMargin: 46
        font.bold: true
    }

    Image {
        id: bridging_the_gap
        y: 143
        source: "images/blog_3.9.png"
        anchors.horizontalCenter: parent.horizontalCenter
        sourceSize.height: 140
        sourceSize.width: 220
        fillMode: Image.PreserveAspectFit
    }

    Rectangle {
        id: rectangle
        x: 8
        y: 97

        anchors.fill: parent
        z: -1
        border.color: Constants.currentBrand
        color: linkArea.containsMouse ? Constants.currentPushButtonHoverBackground
                                      : Constants.currentPushButtonNormalBackground

        MouseArea {
            id: linkArea
            x: 8
            y: 42
            hoverEnabled: true
            anchors.fill: parent
            onClicked: Qt.openUrlExternally("https://www.qt.io/blog/qt-design-studio-4.3-released")
        }
    }
}

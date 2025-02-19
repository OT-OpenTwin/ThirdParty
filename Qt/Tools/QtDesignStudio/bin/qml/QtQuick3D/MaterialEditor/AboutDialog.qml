// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window

Dialog {
    id: root
    title: qsTr("About Material Editor")
    modal: true
    dim: false
    focus: true
    standardButtons: Dialog.Ok
    width: Math.max(implicitWidth, 340)

    ColumnLayout {
        spacing: 12

        Label {
            text: qsTr("Material Editor %1").arg(Qt.application.version)
            font.bold: true
            font.pixelSize: Qt.application.font.pixelSize * 1.1
            Layout.fillWidth: true
        }

        Label {
            text: qsTr("Copyright (C) 2021 The Qt Company Ltd.")
        }
    }
}

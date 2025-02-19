// Copyright (C) 2017 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import HelperWidgets
import QtQuick.Layouts

Section {
    id: section
    caption: qsTr("ItemDelegate")

    SectionLayout {
        Label {
            text: qsTr("Highlighted")
            tooltip: qsTr("Whether the delegate is highlighted.")
        }
        SecondColumnLayout {
            CheckBox {
                text: backendValues.highlighted.valueToString
                backendValue: backendValues.highlighted
                Layout.fillWidth: true
            }
        }
    }
}

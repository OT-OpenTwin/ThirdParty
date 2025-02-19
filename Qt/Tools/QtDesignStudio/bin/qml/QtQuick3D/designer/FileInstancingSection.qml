// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick 2.15
import QtQuick.Layouts 1.15
import HelperWidgets 2.0

Section {
    caption: qsTr("File Instancing")
    width: parent.width

    SectionLayout {
        PropertyLabel {
            text: qsTr("Source")
            tooltip: qsTr("Sets the location of an XML or binary file containing the instance data.")
        }

        SecondColumnLayout {
            UrlChooser {
                backendValue: backendValues.source
                filter: "*.xml *.bin"
            }

            ExpandingSpacer {}
        }
    }
}

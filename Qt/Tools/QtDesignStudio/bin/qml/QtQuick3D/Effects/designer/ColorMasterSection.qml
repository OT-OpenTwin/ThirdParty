// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick 2.15
import QtQuick.Layouts 1.15
import HelperWidgets 2.0
import StudioTheme 1.0 as StudioTheme

Section {
    caption: qsTr("Colors")
    width: parent.width

    SectionLayout {
        PropertyLabel {
            text: qsTr("Red Strength")
            tooltip: qsTr("Red strength.")
        }

        SecondColumnLayout {
            SpinBox {
                minimumValue: 0
                maximumValue: 2
                decimals: 2
                stepSize: 0.1
                backendValue: backendValues.redStrength
                implicitWidth: StudioTheme.Values.twoControlColumnWidth
                               + StudioTheme.Values.actionIndicatorWidth
            }

            ExpandingSpacer {}
        }

        PropertyLabel {
            text: qsTr("Green Strength")
            tooltip: qsTr("Green strength.")
        }

        SecondColumnLayout {
            SpinBox {
                minimumValue: 0
                maximumValue: 2
                decimals: 2
                stepSize: 0.1
                backendValue: backendValues.greenStrength
                implicitWidth: StudioTheme.Values.twoControlColumnWidth
                               + StudioTheme.Values.actionIndicatorWidth
            }

            ExpandingSpacer {}
        }

        PropertyLabel {
            text: qsTr("Blue Strength")
            tooltip: qsTr("Blue strength.")
        }

        SecondColumnLayout {
            SpinBox {
                minimumValue: 0
                maximumValue: 2
                decimals: 2
                stepSize: 0.1
                backendValue: backendValues.blueStrength
                implicitWidth: StudioTheme.Values.twoControlColumnWidth
                               + StudioTheme.Values.actionIndicatorWidth
            }

            ExpandingSpacer {}
        }

        PropertyLabel {
            text: qsTr("Saturation")
            tooltip: qsTr("Color saturation.")
        }

        SecondColumnLayout {
            SpinBox {
                minimumValue: -1
                maximumValue: 1
                decimals: 2
                stepSize: 0.1
                backendValue: backendValues.saturation
                implicitWidth: StudioTheme.Values.twoControlColumnWidth
                               + StudioTheme.Values.actionIndicatorWidth
            }

            ExpandingSpacer {}
        }
    }
}

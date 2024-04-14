/****************************************************************************
**
** Copyright (C) 2022 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt Safe Renderer module
**
** $QT_BEGIN_LICENSE:COMM$
**
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** $QT_END_LICENSE$
**
**
**
**
**
**
**
**
****************************************************************************/

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Templates 2.15 as T
import QtQuickDesignerTheme 1.0
import HelperWidgets 2.0
import StudioControls 1.0 as StudioControls
import StudioTheme 1.0 as StudioTheme

Rectangle {
    id: itemPane
    width: 320
    height: 400
    color: Theme.qmlDesignerBackgroundColorDarkAlternate()

    Component.onCompleted: Controller.mainScrollView = mainScrollView

    MouseArea {
        anchors.fill: parent
        onClicked: forceActiveFocus()
    }

    ScrollView {
        id: mainScrollView
        clip: true
        anchors.fill: parent

        Column {
            id: mainColumn
            y: -1
            width: itemPane.width

            onWidthChanged: StudioTheme.Values.responsiveResize(itemPane.width)
            Component.onCompleted: StudioTheme.Values.responsiveResize(itemPane.width)

            ComponentSection {}

            Section {
                caption: qsTr("Safe Image")
                anchors.left: parent.left
                anchors.right: parent.right

                SectionLayout {
                    PropertyLabel { text: qsTr("Position") }

                    SecondColumnLayout {
                        SpinBox {
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            backendValue: backendValues.x
                            maximumValue: 0xffff
                            minimumValue: -0xffff
                            decimals: 0
                        }

                        Spacer { implicitWidth: StudioTheme.Values.controlLabelGap }

                        ControlLabel { text: "X" }

                        Spacer { implicitWidth: StudioTheme.Values.controlGap }

                        SpinBox {
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            backendValue: backendValues.y
                            maximumValue: 0xffff
                            minimumValue: -0xffff
                            decimals: 0
                        }

                        Spacer { implicitWidth: StudioTheme.Values.controlLabelGap }

                        ControlLabel { text: "Y" }

                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Size") }

                    SecondColumnLayout {
                        SpinBox {
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            backendValue: backendValues.width
                            maximumValue: 0xffff
                            minimumValue: 1
                            decimals: 0
                        }

                        Spacer { implicitWidth: StudioTheme.Values.controlLabelGap }

                        ControlLabel {
                            //: The width of the object
                            text: qsTr("W", "width")
                        }

                        Spacer { implicitWidth: StudioTheme.Values.controlGap }

                        SpinBox {
                            id: heightSpinBox
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            backendValue: backendValues.height
                            maximumValue: 0xffff
                            minimumValue: 1
                            decimals: 0
                        }

                        Spacer { implicitWidth: StudioTheme.Values.controlLabelGap }

                        ControlLabel {
                            //: The height of the object
                            text: qsTr("H", "height")
                        }

                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Source") }

                    SecondColumnLayout {
                        UrlChooser {
                            backendValue: backendValues.source
                        }

                        ExpandingSpacer {}
                    }
                    PropertyLabel { text: qsTr("fillColor") }

                    ColorEditor {
                        backendValue: backendValues.fillColor
                        supportGradient: false
                    }

                    PropertyLabel { text: qsTr("Opacity") }

                    SecondColumnLayout {
                        SpinBox {
                            implicitWidth: StudioTheme.Values.singleControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            sliderIndicatorVisible: true
                            backendValue: backendValues.opacity
                            decimals: 2
                            minimumValue: 0
                            maximumValue: 1
                            hasSlider: true
                            stepSize: 0.1
                        }

                        ExpandingSpacer {}
                    }
                }
            }
        }
    }
}

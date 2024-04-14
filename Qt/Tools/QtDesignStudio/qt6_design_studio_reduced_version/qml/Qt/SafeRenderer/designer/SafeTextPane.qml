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
                caption: qsTr("Safe Text")
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

                    PropertyLabel { text: qsTr("Text") }

                    SecondColumnLayout {
                        LineEdit {
                            implicitWidth: StudioTheme.Values.singleControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            width: implicitWidth
                            backendValue: backendValues.text
                        }

                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Color") }

                    ColorEditor {
                        backendValue: backendValues.color
                        supportGradient: false
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

                    PropertyLabel { text: qsTr("Font") }

                    SecondColumnLayout {
                        FontComboBox {
                            id: fontComboBox
                            property string familyName: backendValue.value
                            backendValue: backendValues.font_family
                            implicitWidth: StudioTheme.Values.singleControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            width: implicitWidth
                        }

                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Size") }

                    SecondColumnLayout {
                        SpinBox {
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            backendValue: backendValues.font_pixelSize
                            minimumValue: 0
                            maximumValue: 400
                            decimals: 0
                        }

                        Spacer { implicitWidth: StudioTheme.Values.controlLabelGap }

                        ControlLabel { text: "px" }

                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Emphasis") }

                    SecondColumnLayout {
                        BoolButtonRowButton {
                            id: boldButton
                            buttonIcon: StudioTheme.Constants.fontStyleBold
                            backendValue: backendValues.font_bold
                        }

                        Spacer {
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                                           - (boldButton.implicitWidth + italicButton.implicitWidth)
                        }

                        BoolButtonRowButton {
                            id: italicButton
                            buttonIcon: StudioTheme.Constants.fontStyleItalic
                            backendValue: backendValues.font_italic
                        }

                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Alignment H") }

                    SecondColumnLayout {
                        AlignmentHorizontalButtons {
                            scope: "SafeText"
                        }
                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Alignment V") }

                    SecondColumnLayout {
                        AlignmentVerticalButtons {
                            scope: "SafeText"
                        }
                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Wrap mode") }

                    SecondColumnLayout {
                        ComboBox {
                            implicitWidth: StudioTheme.Values.singleControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            width: implicitWidth
                            backendValue: backendValues.wrapMode
                            scope: "SafeText"
                            model: ["NoWrap", "WordWrap", "WrapAnywhere", "Wrap"]
                            enabled: backendValue.isAvailable
                        }
                        ExpandingSpacer {}
                    }

                    PropertyLabel { text: qsTr("Dynamic") }

                    SecondColumnLayout {
                        CheckBox {
                            text: backendValue.valueToString
                            implicitWidth: StudioTheme.Values.twoControlColumnWidth
                                           + StudioTheme.Values.actionIndicatorWidth
                            backendValue: backendValues.runtimeEditable
                        }

                        ExpandingSpacer {}
                    }
                }
            }
        }
    }
}

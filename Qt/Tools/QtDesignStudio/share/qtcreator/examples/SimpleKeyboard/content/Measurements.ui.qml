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
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtDataVisualization 1.15
import SimpleKeyboard 1.0

Rectangle {
    id: rectangle

    width: Constants.width
    height: Constants.pageHeight
    color: "#ffffff"
    border.color: "#ffffff"

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        anchors.rightMargin: 20
        anchors.bottomMargin: 20
        anchors.leftMargin: 20
        anchors.topMargin: 20

        Item {
            Layout.fillHeight: true
        }
        RowLayout {
            GridLayout {
                columns: 2
                Text {
                    Layout.alignment: Qt.AlignRight
                    text: qsTr("Measurement name:")
                    font.pointSize: 24
                    font.family: Constants.font.family
                }
                Text {
                    Layout.fillWidth: true
                    font.pointSize: 24
                    font.family: Constants.font.family
                    text: dataModel.name
                }
                Text {
                    Layout.alignment: Qt.AlignRight
                    text: qsTr("Description:")
                    font.pointSize: 24
                    font.family: Constants.font.family
                }
                Text {
                    Layout.fillWidth: true
                    font.pointSize: 24
                    font.family: Constants.font.family
                    text: dataModel.description
                }
                Text {
                    Layout.alignment: Qt.AlignRight | Qt.AlignTop
                    text: qsTr("Measured data:")
                    font.pointSize: 24
                    font.family: Constants.font.family
                }
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: dataModel.dataList
                    delegate: Text {
                        text: modelData
                        font.pointSize: 16
                        font.family: Constants.font.family
                    }
                }
                Text {
                    Layout.alignment: Qt.AlignRight
                    text: qsTr("Comments:")
                    font.pointSize: 24
                    font.family: Constants.font.family
                }
                TextField {
                    Layout.fillWidth: true
                    font.pointSize: 24
                    font.family: Constants.font.family
                    text: dataModel.measurementComments
                    onTextChanged: dataModel.measurementComments = text
                }
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.33}D{i:2}D{i:3}D{i:1}
}
##^##*/


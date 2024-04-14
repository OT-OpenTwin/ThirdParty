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

Item {
    id: root

    property int settingsModelId: 4

    property int activeColorId: defaultIds.color
    property int activeSoilId: defaultIds.soil
    property int activeFabricId: defaultIds.fabric
    property int activeTimeId: defaultIds.time
    property int activeTemperatureId: defaultIds.temperature
    property int activeTimerId: defaultIds.timer
    property int activeWeightId: defaultIds.weight
    property int activeSpinId: defaultIds.spin
    property int activeWaterId: defaultIds.water

    readonly property real delegateHeight: 30

    QtObject {
        id: defaultIds
        readonly property int color: 1
        readonly property int soil: 1
        readonly property int fabric: 2
        readonly property int time: 2
        readonly property int temperature: 2
        readonly property int timer: 0
        readonly property int weight: 1
        readonly property int spin: 2
        readonly property int water: 1
    }

    function resetActiveIds() {
        root.activeColorId = defaultIds.color
        root.activeSoilId = defaultIds.soil
        root.activeFabricId = defaultIds.fabric
        root.activeTimeId = defaultIds.time
        root.activeTemperatureId = defaultIds.temperature
        root.activeTimerId = defaultIds.timer
        root.activeWeightId = defaultIds.weight
        root.activeSpinId = defaultIds.spin
        root.activeWaterId = defaultIds.water
    }

    function updateActiveView() {
        switch (settingsModelId) {
        case 0:
            colorView.updateView()
            break
        case 1:
            soilView.updateView()
            break
        case 2:
            fabricView.updateView()
            break
        case 3:
            timeView.updateView()
            break
        case 4:
            temperatureView.updateView()
            break
        case 5:
            timerView.updateView()
            break
        case 6:
            weightView.updateView()
            break
        case 7:
            spinView.updateView()
            break
        case 8:
            waterView.updateView()
            break
        default: break;
        }
    }

    function getTimeValue() : int {
        return timeModel.get(activeTimeId).value
    }

    function getColorName(modelIndex : int) : string {
        if (modelIndex < colorModel.count)
            return colorModel.get(modelIndex).name
        return ""
    }
    function getSoilName(modelIndex : int) : string {
        if (modelIndex < soilModel.count)
            return soilModel.get(modelIndex).name
        return ""
    }
    function getFabricName(modelIndex : int) : string {
        if (modelIndex < fabricModel.count)
            return fabricModel.get(modelIndex).name
        return ""
    }
    function getTimeName(modelIndex : int) : string {
        if (modelIndex < timeModel.count)
            return timeModel.get(modelIndex).name
        return ""
    }
    function getTemperatureName(modelIndex : int) : string {
        if (modelIndex < temperatureModel.count)
            return temperatureModel.get(modelIndex).name
        return ""
    }
    function getTimerName(modelIndex : int) : string {
        if (modelIndex < timerModel.count)
            return timerModel.get(modelIndex).name
        return ""
    }
    function getWeightName(modelIndex : int) : string {
        if (modelIndex < weightModel.count)
            return weightModel.get(modelIndex).name
        return ""
    }
    function getSpinName(modelIndex : int)  : string {
        if (modelIndex < spinModel.count)
            return spinModel.get(modelIndex).name
        return ""
    }
    function getWaterName(modelIndex : int) : string {
        if (modelIndex < waterModel.count)
            return waterModel.get(modelIndex).name
        return ""
    }




    function newItemSelected(index : int) {
        //pick correct model
        var i
        var element

        switch (settingsModelId) {
        case 0:
            for (i = 0; i < colorModel.count; i++) {
                element = colorView.itemAtIndex(i)
//                if (element !== null) //check is not supported in qt4mcu 1.6 for that type
                element.selected = false
            }
            colorView.itemAtIndex(index).selected = true
            activeColorId = index
            break;
        case 1:
            for (i = 0; i < soilModel.count; i++) {
                element = soilView.itemAtIndex(i)
                element.selected = false
            }
            soilView.itemAtIndex(index).selected = true
            activeSoilId = index
            break;
        case 2:
            for (i = 0; i < fabricModel.count; i++) {
                element = fabricView.itemAtIndex(i)
                element.selected = false
            }
            fabricView.itemAtIndex(index).selected = true
            activeFabricId = index
            break;
        case 3:
            for (i = 0; i < timeModel.count; i++) {
                element = timeView.itemAtIndex(i)
                element.selected = false
            }
            timeView.itemAtIndex(index).selected = true
            activeTimeId = index
            break;
        case 4:
            for (i = 0; i < temperatureModel.count; i++) {
                element = temperatureView.itemAtIndex(i)
                element.selected = false
            }
            temperatureView.itemAtIndex(index).selected = true
            activeTemperatureId = index
            break;
        case 5:
            for (i = 0; i < timerModel.count; i++) {
                element = timerView.itemAtIndex(i)
                element.selected = false
            }
            timerView.itemAtIndex(index).selected = true
            activeTimerId = index
            break;
        case 6:
            for (i = 0; i < weightModel.count; i++) {
                element = weightView.itemAtIndex(i)
                element.selected = false
            }
            weightView.itemAtIndex(index).selected = true
            activeWeightId = index
            break;
        case 7:
            for (i = 0; i < spinModel.count; i++) {
                element = spinView.itemAtIndex(i)
                element.selected = false
            }
            spinView.itemAtIndex(index).selected = true
            activeSpinId = index
            break;
        case 8:
            for (i = 0; i < waterModel.count; i++) {
                element = waterView.itemAtIndex(i)
                element.selected = false
            }
            waterView.itemAtIndex(index).selected = true
            activeWaterId = index
            break;
        default: return;
        }
    }

    Component {
        id: textDelegate

        Item {
            id: delegateItem

            width: 60
            height: delegateHeight
            anchors.horizontalCenter: parent.horizontalCenter

            property bool selected

            Text {
                id: delegateText
                text: model.name
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.family: "Maven Pro"
                color: "#B8B8B8"
                visible: !delegateItem.selected
            }

            Text {
                id: delegateSelectedText
                text: model.name
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 22
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.family: "Maven Pro"
                color: "#B8B8FF"
                visible: delegateItem.selected
            }

            MouseArea {
                id: delegateMA
                anchors.fill: parent

                onClicked: {
                    newItemSelected(index)
                }
            }
        }
    }

    ListView {
        id: colorView
        height: (colorModel.count * root.delegateHeight + colorModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: colorModel

        visible: false

        function updateView() {
            for (var i = 0; i < colorModel.count; i++) {
                var element = colorView.itemAtIndex(i)
                element.selected = false
            }
            colorView.itemAtIndex(activeColorId).selected = true
        }
    }


    ListView {
        id: soilView
        height: (soilModel.count * root.delegateHeight + soilModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: soilModel

        visible: false

        function updateView() {
            for (var i = 0; i < soilModel.count; i++) {
                var element = soilView.itemAtIndex(i)
                element.selected = false
            }
            soilView.itemAtIndex(activeSoilId).selected = true
        }
    }

    ListView {
        id: fabricView
        height: (fabricModel.count * root.delegateHeight + fabricModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: fabricModel

        visible: false

        function updateView() {
            for (var i = 0; i < fabricModel.count; i++) {
                var element = fabricView.itemAtIndex(i)
                element.selected = false
            }
            fabricView.itemAtIndex(activeFabricId).selected = true
        }
    }

    ListView {
        id: timeView
        height: (timeModel.count * root.delegateHeight + timeModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: timeModel

        visible: false

        function updateView() {
            for (var i = 0; i < timeModel.count; i++) {
                var element = timeView.itemAtIndex(i)
                element.selected = false
            }
            timeView.itemAtIndex(activeTimeId).selected = true
        }
    }

    ListView {
        id: temperatureView
        height: (temperatureModel.count * root.delegateHeight + temperatureModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: temperatureModel

        visible: false

        function updateView() {
            for (var i = 0; i < temperatureModel.count; i++) {
                var element = temperatureView.itemAtIndex(i)
                element.selected = false
            }
            temperatureView.itemAtIndex(activeTemperatureId).selected = true
        }
    }

    ListView {
        id: timerView
        height: (timerModel.count * root.delegateHeight + timerModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: timerModel

        visible: false

        function updateView() {
            for (var i = 0; i < timerModel.count; i++) {
                var element = timerView.itemAtIndex(i)
                element.selected = false
            }
            timerView.itemAtIndex(activeTimerId).selected = true
        }
    }

    ListView {
        id: weightView
        height: (weightModel.count * root.delegateHeight + weightModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: weightModel

        visible: false

        function updateView() {
            for (var i = 0; i < weightModel.count; i++) {
                var element = weightView.itemAtIndex(i)
                element.selected = false
            }
            weightView.itemAtIndex(activeWeightId).selected = true
        }
    }

    ListView {
        id: spinView
        height: (spinModel.count * root.delegateHeight + spinModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: spinModel

        visible: false

        function updateView() {
            for (var i = 0; i < spinModel.count; i++) {
                var element = spinView.itemAtIndex(i)
                element.selected = false
            }
            spinView.itemAtIndex(activeSpinId).selected = true
        }
    }

    ListView {
        id: waterView
        height: (waterModel.count * root.delegateHeight + waterModel.count * spacing)
        width: 80
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        delegate: textDelegate

        model: waterModel

        visible: false

        function updateView() {
            for (var i = 0; i < waterModel.count; i++) {
                var element = waterView.itemAtIndex(i)
                element.selected = false
            }
            waterView.itemAtIndex(activeWaterId).selected = true
        }
    }


    ListModel {
        id: colorModel

        ListElement {
            name: "Colors"
        }
        ListElement {
            name: "White"
        }
        ListElement {
            name: "Dark"
        }
    }

    ListModel {
        id: soilModel

        ListElement {
            name: "Light"
        }
        ListElement {
            name: "Medium"
        }
        ListElement {
            name: "Heavy"
        }
    }

    ListModel {
        id: fabricModel

        ListElement {
            name: "Wool"
        }
        ListElement {
            name: "Synthetic"
        }
        ListElement {
            name: "Cotton"
        }
        ListElement {
            name: "Silk"
        }
        ListElement {
            name: "Delicates"
        }
    }

    ListModel {
        id: timeModel

        ListElement {
            name: "30 min."
            value: 30
        }
        ListElement {
            name: "60 min."
            value: 60
        }
        ListElement {
            name: "90 min."
            value: 90
        }
        ListElement {
            name: "120 min."
            value: 120
        }
        ListElement {
            name: "180 min."
            value: 180
        }
    }

    ListModel {
        id: temperatureModel

        ListElement {
            name: "20°"
        }
        ListElement {
            name: "30°"
        }
        ListElement {
            name: "40°"
        }
        ListElement {
            name: "60°"
        }
        ListElement {
            name: "90°"
        }
    }

    ListModel {
        id: timerModel

        ListElement {
            name: "Off"
        }
    }

    ListModel {
        id: weightModel

        ListElement {
            name: "Light"
        }
        ListElement {
            name: "Medium"
        }
        ListElement {
            name: "Heavy"
        }
    }

    ListModel {
        id: spinModel

        ListElement {
            name: "400"
        }
        ListElement {
            name: "800"
        }
        ListElement {
            name: "1200"
        }
        ListElement {
            name: "1600"
        }
        ListElement {
            name: "2000"
        }
    }

    ListModel {
        id: waterModel

        ListElement {
            name: "Less"
        }
        ListElement {
            name: "Medium"
        }
        ListElement {
            name: "More"
        }
    }


    states: [
        State {
            name: "colorState"
            when: settingsModelId === 0
            PropertyChanges {
                target: colorView
                visible: true
            }
        },
        State {
            name: "soilState"
            when: settingsModelId === 1
            PropertyChanges {
                target: soilView
                visible: true
            }
        },
        State {
            name: "fabricState"
            when: settingsModelId === 2
            PropertyChanges {
                target: fabricView
                visible: true
            }
        },
        State {
            name: "timeState"
            when: settingsModelId === 3
            PropertyChanges {
                target: timeView
                visible: true
            }
        },
        State {
            name: "temperatureState"
            when: settingsModelId === 4
            PropertyChanges {
                target: temperatureView
                visible: true
            }
        },
        State {
            name: "timerState"
            when: settingsModelId === 5
            PropertyChanges {
                target: timerView
                visible: true
            }
        },
        State {
            name: "weightState"
            when: settingsModelId === 6
            PropertyChanges {
                target: weightView
                visible: true
            }
        },
        State {
            name: "spinState"
            when: settingsModelId === 7
            PropertyChanges {
                target: spinView
                visible: true
            }
        },
        State {
            name: "waterState"
            when: settingsModelId === 8
            PropertyChanges {
                target: waterView
                visible: true
            }
        }
    ]
}

/*##^##
Designer {
    D{i:0;height:149;width:81}
}
##^##*/

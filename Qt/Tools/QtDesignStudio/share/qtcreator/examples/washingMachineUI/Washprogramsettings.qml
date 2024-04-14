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
    id: washprogramsettings
    width: 130
    height: 272

    signal cancelClicked
    signal applyClicked

    property int activeItem: 4

    property string colorStr: programList.getColorName(programList.activeColorId)
    property string soilStr: programList.getSoilName(programList.activeSoilId)
    property string fabricStr: programList.getFabricName(programList.activeFabricId)
    property string timeStr: programList.getTimeName(programList.activeTimeId)
    property string temperatureStr: programList.getTemperatureName(programList.activeTemperatureId)
    property string timerStr: programList.getTimerName(programList.activeTimerId)
    property string weightStr: programList.getWeightName(programList.activeWeightId)
    property string spinStr: programList.getSpinName(programList.activeSpinId)
    property string waterStr: programList.getWaterName(programList.activeWaterId)

    property int timeInt: programList.getTimeValue()

    signal resetSettingsScreen

    onActiveItemChanged: {
        programList.settingsModelId = washprogramsettings.activeItem
        programList.updateActiveView()
    }

    onResetSettingsScreen: {
        programList.resetActiveIds()
    }

    Smallbutton {
        id: washSettingsCancel
        width: 43
        height: 43
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        currenticonoffSource: "assets/closeiconoff.png"
        lockedicononSource: "assets/closeiconoff.png"

        Connections {
            target: washSettingsCancel
            onClicked: {
                washprogramsettings.cancelClicked()
            }
        }
    }

    Smallbutton {
        id: washSettingsOK
        width: 43
        height: 43
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.rightMargin: 10
        currenticonoffSource: "assets/goiconoff.png"
        lockedicononSource: "assets/goiconon.png"

        Connections {
            target: washSettingsOK
            onClicked: {
                washprogramsettings.applyClicked()
            }
        }
    }

    Item {
        id: programs
        width: 80
        height: 150
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -15
        anchors.horizontalCenter: parent.horizontalCenter

        WashProgramList {
            id: programList
            anchors.fill: parent
        }
    }
}




/****************************************************************************
**
** Copyright (C) 2019 The Qt Company Ltd.
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
import QtQuick.Layouts 1.0
import QtQuick.Studio.Components 1.0
import Data 1.0 as Data

Item {
    id: iso_195_156
    width: 900
    height: 68

    Image {
        id: iso_195_156Asset
        x: 8
        y: -13
        width: 888
        height: 90
        source: "assets/iso_195_156.png"
    }

    RowLayout {
        x: 17
        y: 0
        scale: 0.9
        spacing: 40

        IsoIcon {
            id: engineIcon
            x: 0
            y: 0
            active: Data.Values.engineTemp
            engineIconOffSource: "icons/engineIconOff.png"
            engineIconOnSource: "icons/engineIconOn.png"
        }

        IsoIcon {
            id: seatbeltIcon
            x: 0
            y: 0
            engineIconOffSource: "icons/seatbeltIcon.png"
        }

        IsoIcon {
            id: parkingBrakeIcon
            x: 0
            y: 0
            engineIconOffSource: "icons/parkingBrakeIcon.png"
        }

        IsoIcon {
            id: parkingLightIcon
            x: 0
            y: 0
            engineIconOffSource: "icons/parkingLightIcon.png"
        }

        IsoIcon {
            id: iceIcon
            x: 0
            y: 0
            engineIconOffSource: "icons/iceIcon.png"
        }

        IsoIcon {
            id: absIcon
            x: 0
            y: 0
            engineIconOffSource: "icons/absIcon.png"
        }

        IsoIcon {
            id: fuelIcon
            x: 0
            y: 0
            active: Data.Values.fuelLevel
            engineIconOnSource: "icons/fuelIconOn.png"
            engineIconOffSource: "icons/fuelIconOff.png"
        }
    }
}

/*##^## Designer {
    D{i:0;width:900;height:68}D{i:3;active__AT__NodeInstance:false}D{i:4;active__AT__NodeInstance:false}
D{i:5;active__AT__NodeInstance:false}D{i:6;active__AT__NodeInstance:false}D{i:7;active__AT__NodeInstance:false}
D{i:8;active__AT__NodeInstance:false}D{i:9;active__AT__NodeInstance:false}
}
 ##^##*/


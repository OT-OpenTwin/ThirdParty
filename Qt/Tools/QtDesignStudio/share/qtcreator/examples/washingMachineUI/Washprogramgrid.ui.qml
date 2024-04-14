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
    id: washprogramgrid
    width: 270
    height: 270

    property int activeItem: 4

    property alias colorLabel: washprogramitem0.currentvaluelabelText
    property alias soilLabel: washprogramitem1.currentvaluelabelText
    property alias fabricLabel: washprogramitem2.currentvaluelabelText
    property alias timeLabel: washprogramitem3.currentvaluelabelText
    property alias temperatureLabel: washprogramitem4.currentvaluelabelText
    property alias timerLabel: washprogramitem5.currentvaluelabelText
    property alias weightLabel: washprogramitem6.currentvaluelabelText
    property alias spinLabel: washprogramitem7.currentvaluelabelText
    property alias waterLabel: washprogramitem8.currentvaluelabelText

    Image {
        id: gridimage
        x: 9
        y: 0
        source: "assets/gridimage.png"
    }

    Washprogramitem {
        id: washprogramitem0
        x: 0
        y: 7
        width: 85
        height: 84

        temperatureiconoffSource: "assets/coloriconoff.png"
        washprogramiconSource: "assets/coloriconon.png"
        currentvaluelabelText: "Dark"

        Connections {
            target: washprogramitem0
            onPressed: {
                washprogramgrid.activeItem = 0
            }
        }
    }

    Washprogramitem {
        id: washprogramitem1
        x: 86
        y: 7
        width: 85
        height: 84

        washprogramiconSource: "assets/soiliconon.png"
        temperatureiconoffSource: "assets/soiliconoff.png"
        currentvaluelabelText: "Heavy"

        Connections {
            target: washprogramitem1
            onPressed: {
                washprogramgrid.activeItem = 1
            }
        }
    }

    Washprogramitem {
        id: washprogramitem2
        x: 172
        y: 8
        width: 85
        height: 84

        washprogramiconSource: "assets/fabriciconon.png"
        temperatureiconoffSource: "assets/fabriciconoff.png"
        currentvaluelabelText: "Cotton"

        Connections {
            target: washprogramitem2
            onPressed: {
                washprogramgrid.activeItem = 2
            }
        }
    }

    Washprogramitem {
        id: washprogramitem3
        x: 0
        y: 92
        width: 85
        height: 84

        washprogramiconSource: "assets/timeiconon.png"
        temperatureiconoffSource: "assets/timeiconoff.png"
        currentvaluelabelText: "120 Mins"

        Connections {
            target: washprogramitem3
            onPressed: {
                washprogramgrid.activeItem = 3
            }
        }
    }

    Washprogramitem {
        id: washprogramitem4
        x: 86
        y: 92
        width: 85
        height: 84

        washprogramiconSource: "assets/washprogramicon.png"
        temperatureiconoffSource: "assets/temperatureiconoff.png"
        currentvaluelabelText: "60°"

        Connections {
            target: washprogramitem4
            onPressed: {
                washprogramgrid.activeItem = 4
            }
        }
    }

    Washprogramitem {
        id: washprogramitem5
        x: 172
        y: 92
        width: 85
        height: 84

        washprogramiconSource: "assets/timericonon.png"
        temperatureiconoffSource: "assets/timericonoff.png"
        currentvaluelabelText: "Off"

        Connections {
            target: washprogramitem5
            onPressed: {
                washprogramgrid.activeItem = 5
            }
        }
    }

    Washprogramitem {
        id: washprogramitem6
        x: 0
        y: 177
        width: 85
        height: 84

        washprogramiconSource: "assets/weighticonon.png"
        temperatureiconoffSource: "assets/weighticonoff.png"
        currentvaluelabelText: "2.5 kg"

        Connections {
            target: washprogramitem6
            onPressed: {
                washprogramgrid.activeItem = 6
            }
        }
    }

    Washprogramitem {
        id: washprogramitem7
        x: 86
        y: 177
        width: 85
        height: 84

        washprogramiconSource: "assets/spiniconon.png"
        temperatureiconoffSource: "assets/spiniconoff.png"
        currentvaluelabelText: "1200"

        Connections {
            target: washprogramitem7
            onPressed: {
                washprogramgrid.activeItem = 7
            }
        }
    }

    Washprogramitem {
        id: washprogramitem8
        x: 172
        y: 177
        width: 85
        height: 84

        washprogramiconSource: "assets/watericonon.png"
        temperatureiconoffSource: "assets/watericonoff.png"
        currentvaluelabelText: "Medium"

        Connections {
            target: washprogramitem8
            onPressed: {
                washprogramgrid.activeItem = 8
            }
        }
    }

    states: [
        State {
            name: "colorState"
            when: activeItem === 0
            PropertyChanges {
                target: washprogramitem0
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "soilState"
            when: activeItem === 1
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "fabricState"
            when: activeItem === 2
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "timeState"
            when: activeItem === 3
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "temperatureState"
            when: activeItem === 4
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "timerState"
            when: activeItem === 5
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "weightState"
            when: activeItem === 6
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "spinState"
            when: activeItem === 7
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: true
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: false
            }
        },
        State {
            name: "waterState"
            when: activeItem === 8
            PropertyChanges {
                target: washprogramitem0
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem1
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem2
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem3
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem4
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem5
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem6
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem7
                toggled: false
            }
            PropertyChanges {
                target: washprogramitem8
                toggled: true
            }
        }
    ]
}


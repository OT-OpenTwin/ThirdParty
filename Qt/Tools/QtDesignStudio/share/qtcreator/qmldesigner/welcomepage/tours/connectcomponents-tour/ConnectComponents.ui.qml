/****************************************************************************
**
** Copyright (C) 2023 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of Qt Creator.
**
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 as published by the Free Software
** Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
****************************************************************************/

import QtQuick
import QtQuick.Controls
import QtQuick.Timeline
import UiTour

Slide {
    id: slide2
    caption: ""
    title: qsTr("Connecting Components")
    state: "State1"

    Image {
        id: _01_Some_Components
        source: "images/01_Some_Components.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: _02_Open_Connections_Editor_for_First_Button
        visible: false
        source: "images/02_Open_Connections_Editor_for_First_Button.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
        }
    }

    Image {
        id: _03_Select_the_Connecting_Component
        visible: false
        source: "images/03_Select_the_Connecting_Component.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
        }
    }

    Image {
        id: _04_Select_Action_for_Connecting_Component
        visible: false
        source: "images/04_Select_Action_for_Connecting_Component.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
        }
    }

    Image {
        id: _02_Open_Connections_Editor_for_Next_Button
        visible: false
        source: "images/02_Open_Connections_Editor_for_Next_Button.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
        }
    }

    Image {
        id: _05_Select_the_Connecting_Component
        visible: false
        source: "images/05_Select_the_Connecting_Component.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
        }
    }

    Image {
        id: _06_Select_the_Action_for_Connected_Component
        visible: false
        source: "images/06_Select_the_Action_for_Connected_Component.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
        }
    }

    Image {
        id: _07_Run_the_Project
        visible: false
        source: "images/07_Run_the_Project.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
        }
    }

    Image {
        id: _08_Beginning_Project_State
        visible: false
        source: "images/08_Beginning_Project_State.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
        }
    }

    Image {
        id: _09_Press_First_Button
        visible: false
        source: "images/09_Press_First_Button.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight9
        }
    }

    Image {
        id: _10_Press_Second_Button
        visible: false
        source: "images/10_Press_Second_Button.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight10
        }
    }
    states: [
        State {
            name: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 489
                y: 352
                width: 375
                height: 361
            }

            PropertyChanges {
                target: slide2
                caption: "Here are four components. Two buttons, and two checkboxes. In this tour you will learn to enable a button to change the state of the checkbox. For that, you need to connect them together."
            }
        },
        State {
            name: "State2"

            PropertyChanges {
                target: _02_Open_Connections_Editor_for_First_Button
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: 560
                y: 422
                width: 871
                height: 528
            }

            PropertyChanges {
                target: slide2
                caption: "Select the \"Select Yes\" button, press right mouse button to open up the option menu. From there select Connections > Add Signal Handler > clicked > Open Connections Editor. This will open the editor where you can connect the components. "
            }
        },
        State {
            name: "State3"

            PropertyChanges {
                target: strongHighlight2
                x: 512
                y: 611
                width: 753
                height: 302
            }

            PropertyChanges {
                target: _03_Select_the_Connecting_Component
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: "From the Connection Editor select the checkbox you want to connect with this button. In this case \"checkBox\" is the correct one."
            }
        },
        State {
            name: "State4"

            PropertyChanges {
                target: _04_Select_Action_for_Connecting_Component
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 511
                y: 612
                width: 751
                height: 302
            }

            PropertyChanges {
                target: slide2
                caption: "Select \"toggle\" from the dropdown menu next to the selected component dropdown menu. Then select \"OK\" to bind the action."
            }
        },
        State {
            name: "State5"

            PropertyChanges {
                target: _02_Open_Connections_Editor_for_Next_Button
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 575
                y: 458
                width: 850
                height: 524
            }

            PropertyChanges {
                target: slide2
                caption: "Next, select the \"Select No\" button, press right mouse button to open up the option menu. From there select Connections > Add Signal Handler > clicked > Open Connections Editor. "
            }
        },
        State {
            name: "State6"

            PropertyChanges {
                target: _05_Select_the_Connecting_Component
                visible: true
            }

            PropertyChanges {
                target: strongHighlight5
                x: 480
                y: 557
                width: 756
                height: 305
            }

            PropertyChanges {
                target: slide2
                caption: "From the Connection Editor select \"checkBox1\"."
            }
        },
        State {
            name: "State7"

            PropertyChanges {
                target: _06_Select_the_Action_for_Connected_Component
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: 479
                y: 560
                width: 757
                height: 304
            }

            PropertyChanges {
                target: slide2
                caption: "Select \"toggle\" from the dropdown menu next to the selected component dropdown menu. Then select \"OK\" to bind the action."
            }
        },
        State {
            name: "State8"

            PropertyChanges {
                target: strongHighlight7
                x: 42
                y: 39
                width: 174
                height: 90
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: "Select \"Run Project\" or \"Live Preview\" to check the connections."
            }

            PropertyChanges {
                target: _05_Select_the_Connecting_Component
                visible: false
            }

            PropertyChanges {
                target: _01_Some_Components
                visible: false
            }

            PropertyChanges {
                target: _07_Run_the_Project
                visible: true
            }
        },
        State {
            name: "State9"

            PropertyChanges {
                target: _08_Beginning_Project_State
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: -16
                y: -9
                width: 1936
                height: 1097
            }

            PropertyChanges {
                target: slide2
                caption: "A new application window will open up with all the components and connections. "
            }
        },
        State {
            name: "State10"

            PropertyChanges {
                target: _09_Press_First_Button
                visible: true
            }

            PropertyChanges {
                target: strongHighlight9
                x: 684
                y: 447
                width: 188
                height: 56
            }

            PropertyChanges {
                target: slide2
                caption: "Select the button \"Select Yes\" and it will make the checkbox with value \"Yes\" true."
            }
        },
        State {
            name: "State11"

            PropertyChanges {
                target: strongHighlight10
                x: 680
                y: 488
                width: 193
                height: 68
                visible: true
            }

            PropertyChanges {
                target: _10_Press_Second_Button
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: "Select the button \"Select No\" and it will make the checkbox with value \"No\" true."
            }
        }
    ]
}

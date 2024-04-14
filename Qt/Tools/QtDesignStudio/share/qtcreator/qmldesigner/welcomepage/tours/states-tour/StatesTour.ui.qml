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
    visible: true
    state: "StateBegin Focus"
    caption: qsTr("States Tour")
    title: qsTr("States")

    Image {
        id: _1
        source: "images/1_Base_State.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
        }
    }

    Image {
        id: _2
        visible: false
        source: "images/2_Select_Next_State.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
        }
    }

    Image {
        id: _3
        visible: false
        source: "images/3_Changing_Backgroundcolor.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
        }
    }

    Image {
        id: _4
        visible: false
        source: "images/4_Changing_Text_in_next_state.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
        }
    }

    Image {
        id: _6
        visible: false
        source: "images/6_Changing_Binding_of_Control.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
        }
    }

    Image {
        id: _11
        visible: false
        source: "images/11_Live_Project_before_button_click.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
        }
    }

    Image {
        id: _12
        visible: false
        source: "images/12_Live_Project_after_button_click.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
        }
    }

    Image {
        id: _61
        visible: false
        source: "images/6_Changing_Binding_of_Control.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
        }
    }

    Image {
        id: _8
        visible: false
        source: "images/8_Remove_a_Property_Change.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
        }
    }

    states: [
        State {
            name: "StateBegin Focus"

            PropertyChanges {
                target: strongHighlight
                x: 368
                y: 724
                width: 1034
                height: 314
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can set changes into the design or action with different states. This is the state view, which hold all the states created by you.")
            }
        },
        State {
            name: "States Focus"
            extend: "StateBegin Focus"

            PropertyChanges {
                target: strongHighlight
                x: 370
                y: 788
                width: 484
                height: 250
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Here are two states. The more states you create the space will extend stacking the latest ones besides the previous ones. You can scroll through them and select whichever you need to work on.")
            }
        },
        State {
            name: "CreateState Focus"
            extend: "StateBegin Focus"

            PropertyChanges {
                target: strongHighlight
                x: 842
                y: 790
                width: 252
                height: 248
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select here to add a new state to the design.")
            }
        },
        State {
            name: "ChangeDefaultState Focus"
            extend: "StateBegin Focus"

            PropertyChanges {
                target: strongHighlight
                x: 616
                y: 798
                width: 227
                height: 49
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can change the default state by selecting default in any state. Also, you can change the state name to match your need.")
            }
        },
        State {
            name: "Start changing Clicked state Focus"

            PropertyChanges {
                target: _1
                visible: false
            }

            PropertyChanges {
                target: _2
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: 604
                y: 790
                width: 250
                height: 250
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can now make some changes in the state named clicked. First, select the state.")
            }
        },
        State {
            name: "Select Rectangle Focus"
            extend: "Start changing Clicked state Focus"

            PropertyChanges {
                target: strongHighlight1
                x: 363
                y: 148
                width: 1026
                height: 578
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("While in this state, select the background of your design by clicking on it.")
            }
        },
        State {
            name: "Change Color for the background Focus"
            extend: "Start changing Clicked state Focus"

            PropertyChanges {
                target: strongHighlight1
                x: 1452
                y: 750
                width: 422
                height: 52
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You need to click on the fill color box next under the Rectangle section in the Properties view. Since this background is drawn with a rectangle component, the setting can be edited from here. Alternatively you can also write the color code in the box here to have your preferred color for the background.")
            }
        },
        State {
            name: "Select from color picker Focus"

            PropertyChanges {
                target: _1
                visible: false
            }

            PropertyChanges {
                target: _3
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 1491
                y: 259
                width: 261
                height: 781
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can pick the color from a color picker window after clicking the fill color. It would change the background color for the selected state only.")
            }
        },
        State {
            name: "SelectText Focus"

            PropertyChanges {
                target: _1
                visible: false
            }

            PropertyChanges {
                target: _4
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 798
                y: 508
                width: 168
                height: 46
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Change the text for the selected state by selecting the text first.")
            }
        },
        State {
            name: "UpdateSelectedText Focus"
            extend: "SelectText Focus"

            PropertyChanges {
                target: strongHighlight3
                x: 1484
                y: 749
                width: 428
                height: 53
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Next, write the new text in the Text field under Characters section in the Properties view. Here, selecting the \"tr\" option would make the text translatable across languages.")
            }
        },
        State {
            name: "ChangeBinding Focus"
            extend: "SelectText Focus"

            PropertyChanges {
                target: strongHighlight3
                x: 1531
                y: 757
                width: 39
                height: 37
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("If you find the text or any other property not functioning properly in the design, you can bring your mouse next to the property which is broken and it will pop up this tool icon.")
            }
        },
        State {
            name: "Reset Binding focus"

            PropertyChanges {
                target: _1
                visible: false
            }

            PropertyChanges {
                target: _6
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 1531
                y: 749
                width: 204
                height: 156
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Selecting the tool icon you would get a menu, from there select Reset to bring the setting to default. For all the other fields in the Properties view you can follow this process to reach the default setting.")
            }
        },
        State {
            name: "RunProject Focus"

            PropertyChanges {
                target: strongHighlight
                x: 48
                y: 44
                width: 161
                height: 55
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can test this demo project by selecting Run button or the Live Preview.")
            }
        },
        State {
            name: "Application window focus"

            PropertyChanges {
                target: _1
                visible: false
            }

            PropertyChanges {
                target: strongHighlight5
                x: 823
                y: 501
                width: 275
                height: 179
            }

            PropertyChanges {
                target: _11
                visible: true
            }

            PropertyChanges {
                target: slide2
                visible: true
                caption: qsTr("After selecting Run or Live Preview a window will pop up with your application. Here you will find the clickable button and the text. Select the button to observe the color change.")
            }
        },
        State {
            name: "Application Changed Focus"

            PropertyChanges {
                target: _11
                visible: true
            }

            PropertyChanges {
                target: _12
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: 0
                y: 28
                width: 1920
                height: 1052
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You will see the whole window changing color following the state change and the text is also updated. Close the window after you finish testing.")
            }
        },
        State {
            name: "Properties change view Focus"

            PropertyChanges {
                target: _8
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: 1350
                y: 624
                width: 49
                height: 50
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can switch between the Thumbnails or Property change view for the states. Select this option to switch to access the property changes options for each state.")
            }
        },
        State {
            name: "Edit State Focus"
            extend: "Properties change view Focus"

            PropertyChanges {
                target: strongHighlight8
                x: 727
                y: 675
                width: 358
                height: 356
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("From here you can remove any change that was applied in any particular state just by selecting \"x\".")
            }
        },
        State {
            name: "Thumbnails view Focus"
            extend: "Properties change view Focus"

            PropertyChanges {
                target: strongHighlight8
                x: 1312
                y: 623
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Return to the Thumbnails view selecting this.")
            }
        }
    ]
}

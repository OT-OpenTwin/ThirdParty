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
    title: qsTr("Sorting Components")
    state: "State1"

    Image {
        id: projectwithComponents
        source: "images/01_Empty_Project.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: _02_Drag_a_Button
        visible: false
        source: "images/02_Drag_a_Button.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
        }
    }

    Image {
        id: _03_Change_button_text
        visible: false
        source: "images/03_Change_button_text.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
        }
    }

    Image {
        id: _04_Drag_next_button
        visible: false
        source: "images/04_Drag_next_button.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
        }
    }

    Image {
        id: _05_Drag_Checkbox
        visible: false
        source: "images/05_Drag_Checkbox.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
        }
    }

    Image {
        id: _06_Drag_second_Checkbox
        visible: false
        source: "images/06_Drag_second_Checkbox.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
        }
    }

    Image {
        id: _07_Select_all_Components
        visible: false
        source: "images/07_Select_all_Components.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
        }
    }

    Image {
        id: _08_Put_them_in_a_Grid
        visible: false
        source: "images/08_Put_them_in_a_Grid.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
        }
    }

    Image {
        id: _09_After_Sorting
        visible: false
        source: "images/09_After_Sorting.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
        }
    }

    states: [
        State {
            name: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 65
                y: 719
                width: 61
                height: 72
            }

            PropertyChanges {
                target: slide2
                caption: "Select the \"Button\" component and drag it to the 2D view."
            }
        },
        State {
            name: "State2"

            PropertyChanges {
                target: _02_Drag_a_Button
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: 563
                y: 460
                width: 164
                height: 95
            }

            PropertyChanges {
                target: slide2
                caption: "Have the button selected to access its properties."
            }
        },
        State {
            name: "State3"

            PropertyChanges {
                target: _03_Change_button_text
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 1462
                y: 435
                width: 423
                height: 53
            }

            PropertyChanges {
                target: slide2
                caption: "Change the name of the button in its \"Text\" property."
            }
        },
        State {
            name: "State4"
            extend: "State3"

            PropertyChanges {
                target: strongHighlight2
                x: 576
                y: 467
                width: 141
                height: 81
            }

            PropertyChanges {
                target: slide2
                caption: "The change would immediately take place after you press return."
            }
        },
        State {
            name: "State5"

            PropertyChanges {
                target: _04_Drag_next_button
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 558
                y: 431
                width: 204
                height: 216
            }

            PropertyChanges {
                target: slide2
                caption: "Drag another button to the 2D view and edit the display text following the previous process."
            }
        },
        State {
            name: "State6"

            PropertyChanges {
                target: _05_Drag_Checkbox
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 578
                y: 415
                width: 323
                height: 273
            }

            PropertyChanges {
                target: slide2
                caption: "Now drag a Check Box component from the Qt Quick Controls. Select it and edit the display text from the Properties view."
            }
        },
        State {
            name: "State7"

            PropertyChanges {
                target: strongHighlight5
                x: 496
                y: 379
                width: 499
                height: 347
            }

            PropertyChanges {
                target: _06_Drag_second_Checkbox
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: "Drag in the second checkbox and edit the text from the Properties view."
            }
        },
        State {
            name: "State8"

            PropertyChanges {
                target: _07_Select_all_Components
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: 367
                y: 179
                width: 955
                height: 807
            }

            PropertyChanges {
                target: slide2
                caption: "Now select all the components in the 2D view. They are unorganized now, but soon that will be fixed."
            }
        },
        State {
            name: "State9"

            PropertyChanges {
                target: _08_Put_them_in_a_Grid
                visible: true
            }

            PropertyChanges {
                target: strongHighlight7
                x: 546
                y: 425
                width: 795
                height: 584
            }

            PropertyChanges {
                target: slide2
                caption: "Now click the right mouse button on any of the components to bring up the menu. Select Layout and then Grid Layout. This will organize the components in a 2 x 2 grid. You can also place them as a single row or a column by selecting other options. "
            }
        },
        State {
            name: "State10"

            PropertyChanges {
                target: _09_After_Sorting
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: 495
                y: 396
                width: 348
                height: 239
            }

            PropertyChanges {
                target: slide2
                caption: "After getting sorted in a grid the components will look like this."
            }
        }
    ]
}

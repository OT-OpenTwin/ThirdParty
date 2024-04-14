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
    title: qsTr("Studio Components: Ellipse and Pie")
    state: "State1"

    Image {
        id: _01_Add_studio_components_to_the_project
        visible: false
        source: "images/01_Add_studio_components_to_the_project.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: false
        }
    }

    Image {
        id: _02_Locate_the_studio_components
        visible: false
        source: "images/02_Locate_the_studio_components.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _04_Increase_size_of_the_ellipse
        visible: false
        source: "images/04_Increase_size_of_the_ellipse.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _05_Select_border_style
        visible: false
        source: "images/05_Select_border_style.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _06_Change_stroke_width
        visible: false
        source: "images/06_Change_stroke_width.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _07_Select_fill_color_style
        visible: false
        source: "images/07_Select_fill_color_style.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _08_Select_first_color_for_the_gradiant
        visible: false
        source: "images/08_Select_first_color_for_the_gradiant.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _09_Select_second_color_for_the_gradiant
        visible: false
        source: "images/09_Select_second_color_for_the_gradiant.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _10_Select_stroke_color
        visible: false
        source: "images/10_Select_stroke_color.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _11_Drag_a_pie_into_the_ellipse
        visible: false
        source: "images/11_Drag_a_pie_into_the_ellipse.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight9
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _12_Increase_the_pie_size
        visible: false
        source: "images/12_Increase_the_pie_size.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight10
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _13_Set_pie_start_and_end_point
        visible: false
        source: "images/13_Set_pie_start_and_end_point.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight11
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _14_Make_pie_stroke_transperrent
        visible: false
        source: "images/14_Make_pie_stroke_transperrent.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight12
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _15_Set_a_semi_transparent_fill_color
        visible: false
        source: "images/15_Set_a_semi_transparent_fill_color.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight13
            x: -9
            y: -9
            visible: false
        }
    }

    Image {
        id: _16_The_final_outcome
        visible: false
        source: "images/16_The_final_outcome.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight14
            x: -9
            y: -9
            visible: false
        }
    }

    states: [
        State {
            name: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 734
                width: 50
                height: 54
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Create a new project. Initially, it would not have Qt Quick Studio Components available, so you need to add them. Select “+” to open the list.")
            }

            PropertyChanges {
                target: _01_Add_studio_components_to_the_project
                visible: true
            }
        },

        State {
            name: "State2"
            extend: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 694
                width: 398
                height: 54
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Write “studio” in the Search bar.")
            }
        },
        State {
            name: "State3"
            extend: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 773
                width: 394
                height: 81
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select “QtQuick.Studio.Components” from the found component list to add it to the usable component set. Then select “<” to return to the usable Components view.")
            }
        },
        State {
            name: "State4"

            PropertyChanges {
                target: _02_Locate_the_studio_components
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: -5
                y: 671
                width: 410
                height: 373
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Scroll down in the Components view to find the Qt Quick Studio Components.")
            }
        },
        State {
            name: "State5"
            extend: "State4"

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag an Ellipse component from the Components view to the 2D view.")
            }

            PropertyChanges {
                target: strongHighlight1
                x: 119
                y: 901
                width: 73
                height: 72
            }
        },
        State {
            name: "State6"

            PropertyChanges {
                target: _04_Increase_size_of_the_ellipse
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 1529
                y: 157
                width: 391
                height: 250
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Ellipse to access its properties in the Properties view. From the Geometry – 2D properties, increase the width to 250 pixels and height to 250 pixels. Keeping the same length for the height and weight would make this Ellipse circular.")
            }
        },
        State {
            name: "State7"

            PropertyChanges {
                target: _05_Select_border_style
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 1528
                y: 665
                width: 392
                height: 213
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("From the Stroke Details section of the Properties view, select the Stroke style “Dot” for the Ellipse component.")
            }
        },
        State {
            name: "State8"

            PropertyChanges {
                target: _06_Change_stroke_width
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 1527
                y: 528
                width: 393
                height: 150
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Stroke width to “3.0” from the Ellipse Item section in the Properties view.")
            }
        },
        State {
            name: "State9"
            extend: "State8"

            PropertyChanges {
                target: strongHighlight4
                x: 1527
                y: 528
                width: 393
                height: 110
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Fill color in the Ellipse Item section of the Properties view to bring up the color picker.")
            }
        },
        State {
            name: "State10"

            PropertyChanges {
                target: _07_Select_fill_color_style
                visible: true
            }

            PropertyChanges {
                target: strongHighlight5
                x: 1567
                y: 309
                width: 268
                height: 636
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select “Conical” as the gradient style.")
            }
        },
        State {
            name: "State11"

            PropertyChanges {
                target: _08_Select_first_color_for_the_gradiant
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: 1568
                y: 310
                width: 258
                height: 632
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the leftmost color picker to choose the beginning color of the gradient. Set the color “#d28686” in the Hex value.")
            }
        },
        State {
            name: "State12"

            PropertyChanges {
                target: _09_Select_second_color_for_the_gradiant
                visible: true
            }

            PropertyChanges {
                target: strongHighlight7
                x: 1566
                y: 277
                width: 267
                height: 600
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the rightmost color picker. Set the color “#ffffff” in the Hex value.")
            }
        },
        State {
            name: "State13"

            PropertyChanges {
                target: _10_Select_stroke_color
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: 1567
                y: 222
                width: 265
                height: 664
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Stroke color in the Ellipse Item section of the Properties view to bring up the color picker. Select “Solid” as the color style. Set the color “#000000” in the Hex value. This will make the Stroke color black.")
            }
        },
        State {
            name: "State14"

            PropertyChanges {
                target: _11_Drag_a_pie_into_the_ellipse
                visible: true
            }

            PropertyChanges {
                target: strongHighlight9
                x: 876
                y: 364
                width: 169
                height: 148
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag a Pie component from the Components view and place it in the middle of the Ellipse component in the 2D view.")
            }
        },
        State {
            name: "State15"

            PropertyChanges {
                target: _12_Increase_the_pie_size
                visible: true
            }

            PropertyChanges {
                target: strongHighlight10
                x: 1525
                y: 240
                width: 400
                height: 248
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("With the Pie component selected, go to the Properties view and set the Size to Width 150 pixels and Height 150 pixels.")
            }
        },
        State {
            name: "State16"

            PropertyChanges {
                target: _13_Set_pie_start_and_end_point
                visible: true
            }

            PropertyChanges {
                target: strongHighlight11
                x: 1526
                y: 503
                width: 394
                height: 241
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Locate the Pie Item section in the Properties view. Set the Pie start to 30 degrees and the Pie end to 270 degrees.")
            }
        },
        State {
            name: "State17"
            extend: "State16"

            PropertyChanges {
                target: strongHighlight11
                x: 1652
                y: 589
                width: 97
                height: 50
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Stroke Color now to bring up the color picker.")
            }
        },
        State {
            name: "State18"

            PropertyChanges {
                target: _14_Make_pie_stroke_transperrent
                visible: true
            }

            PropertyChanges {
                target: strongHighlight12
                x: 1571
                y: 726
                width: 262
                height: 48
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Slide the transparency control slider to the right-most position to make the Pie component’s stroke completely transparent.")
            }
        },
        State {
            name: "State19"

            PropertyChanges {
                target: _15_Set_a_semi_transparent_fill_color
                visible: true
            }

            PropertyChanges {
                target: strongHighlight13
                x: 1568
                y: 344
                width: 265
                height: 600
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Fill color in the Pie Item section of the Properties view to bring up the color picker. Select “Solid” as the color style. Set the color “#623552b5” in the Hex value. This will change the color of the Pie component with transparency applied to it.")
            }
        },
        State {
            name: "State20"

            PropertyChanges {
                target: _16_The_final_outcome
                visible: true
            }

            PropertyChanges {
                target: strongHighlight14
                x: 663
                y: 173
                width: 594
                height: 528
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("The final design will look like this. Feel free to try other properties to manipulate the components according to your project’s needs.")
            }
        }
    ]
}

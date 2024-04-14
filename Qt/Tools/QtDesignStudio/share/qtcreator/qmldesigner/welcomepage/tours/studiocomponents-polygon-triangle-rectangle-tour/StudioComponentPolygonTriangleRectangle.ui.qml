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
    title: qsTr("Studio Components: Polygon, Triangle and Rectangle")
    state: "State1"

    Image {
        id: _1_Add_studio_components_in_components_view
        visible: false
        source: "images/1_Add_studio_components_in_components_view.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _2_Locate_studio_components_in_components_view
        visible: false
        source: "images/2_Locate_studio_components_in_components_view.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _3_Drag_regular_polygon_component_in_2D_view
        visible: false
        source: "images/3_Drag_regular_polygon_component_in_2D_view.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _4_Enlarge_the_regular_polygon
        visible: false
        source: "images/4_Enlarge_the_regular_polygon.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _5_Change_Fill_and_border_colors_and_the_radius
        visible: false
        source: "images/5_Change_Fill_and_border_colors_and_the_radius.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _6_Drag_a_triangle_component_in_2D_view_and_change_zstack
        visible: false
        source: "images/6_Drag_a_triangle_component_in_2D_view_and_change_zstack.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _7_Change_fill_and_border_colors_and_change_navigation_level
        visible: false
        source: "images/7_Change_fill_and_border_colors_and_change_navigation_level.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _8_Change_corner_radius_of_the_triangle
        visible: false
        source: "images/8_Change_corner_radius_of_the_triangle.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _9_Make_a_duplicate_and_place_it_parallelly
        visible: false
        source: "images/9_Make_a_duplicate_and_place_it_parallelly.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _10_Drag_a_rectangle_in_2D_view
        visible: false
        source: "images/10_Drag_a_rectangle_in_2D_view.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight9
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _11_Update_the_zstack_and_size_of_the_rectangle
        visible: false
        source: "images/11_Update_the_zstack_and_size_of_the_rectangle.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight10
            x: 0
            y: 734
            visible: false
        }
    }

    Image {
        id: _12_Update_corner_radius_and_bavel_of_the_rectangle
        visible: false
        source: "images/12_Update_corner_radius_and_bavel_of_the_rectangle.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight11
            x: 0
            y: 734
            visible: true
        }
    }

    Image {
        id: _13_Change_the_fill_color_of_the_rectangle
        visible: false
        source: "images/13_Change_the_fill_color_of_the_rectangle.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight12
            x: 0
            y: 734
            visible: true
        }
    }

    Image {
        id: _14_Update_the_stroke_color_of_the_rectangle
        visible: false
        source: "images/14_Update_the_stroke_color_of_the_rectangle.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight13
            x: 0
            y: 734
            visible: true
        }
    }

    Image {
        id: _15_Drag_the_rectangle_below_the_triangles_inside_the_regular_polygon
        visible: false
        source: "images/15_Drag_the_rectangle_below_the_triangles_inside_the_regular_polygon.webp"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight14
            x: 0
            y: 734
            visible: true
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
                target: _1_Add_studio_components_in_components_view
                visible: true
            }
        },

        State {
            name: "State2"
            extend: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 700
                width: 393
                height: 42
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
                y: 777
                width: 398
                height: 75
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select “QtQuick.Studio.Components” from the found component list to add it to the usable component set. Then select “<” to return to the usable Components view.")
            }
        },
        State {
            name: "State4"

            PropertyChanges {
                target: _2_Locate_studio_components_in_components_view
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: -7
                y: 872
                width: 401
                height: 168
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
                target: strongHighlight1
                x: 63
                y: 962
                width: 66
                height: 74
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select and drag the Regular Polygon component from the Components view to the 2D view.")
            }
        },
        State {
            name: "State6"

            PropertyChanges {
                target: _3_Drag_regular_polygon_component_in_2D_view
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 689
                y: 179
                width: 543
                height: 510
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Keep the Regular Polygon selected in the 2D view to access its properties in the Properties view.")
            }
        },
        State {
            name: "State7"

            PropertyChanges {
                target: _4_Enlarge_the_regular_polygon
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 1526
                y: 116
                width: 394
                height: 251
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Size of the Regular Polygon component in the “GEOMETRY – 2D” section of the properties editor. Make the width 450 pixels and the height 450 pixels. Also, set the Z stack value to “1”. When several components are on the same navigation level, this Z stack index value helps to decide in which order components stack on each other.")
            }
        },
        State {
            name: "State8"

            PropertyChanges {
                target: _5_Change_Fill_and_border_colors_and_the_radius
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 1524
                y: 462
                width: 396
                height: 208
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Fill color to “#875454” and the Stroke color to “#7f000000”.")
            }
        },
        State {
            name: "State9"
            extend: "State8"

            PropertyChanges {
                target: strongHighlight4
                x: 1527
                y: 866
                width: 385
                height: 91
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Regular Polygon’s Radius to “50”. It would make the corners nicely rounded.")
            }
        },
        State {
            name: "State10"

            PropertyChanges {
                target: _6_Drag_a_triangle_component_in_2D_view_and_change_zstack
                visible: true
            }

            PropertyChanges {
                target: strongHighlight5
                x: 184
                y: 962
                width: 62
                height: 66
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag a Triangle component from the Components view to the 2D view and place it on top of the Regular Polygon.")
            }
        },
        State {
            name: "State11"

            PropertyChanges {
                target: _7_Change_fill_and_border_colors_and_change_navigation_level
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: 1529
                y: 465
                width: 383
                height: 169
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("With the Triangle component selected, update the Fill color to “#000000” and the Stroke color to “#80000000”.")
            }
        },

        State {
            name: "State12"
            extend: "State11"

            PropertyChanges {
                target: strongHighlight6
                x: 1529
                y: 120
                width: 383
                height: 244
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Z stack to “2” in the GEOMETRY – 2D property. This will help keep the Tringle component on top of the Regular Polygon component as it has a higher Z stack index.")
            }
        },

        State {
            name: "State13"
            extend: "State11"

            PropertyChanges {
                target: strongHighlight6
                x: -7
                y: 92
                width: 406
                height: 267
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("In the Navigator view, you will find the Triangle component as a child of the Regular Polygon component. To bring them on the level, select the Triangle component here and drag it to the top of the Rectangle component, which works here as a canvas.")
            }
        },

        State {
            name: "State14"

            PropertyChanges {
                target: _8_Change_corner_radius_of_the_triangle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight7
                x: -8
                y: 89
                width: 401
                height: 239
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("It would appear like this once they are at the same level in the Navigation view.")
            }
        },
        State {
            name: "State15"
            extend: "State14"

            PropertyChanges {
                target: strongHighlight7
                x: 1525
                y: 828
                width: 395
                height: 78
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Radius of the Triangle component to “10”; it will round up the corners nicely.")
            }
        },

        State {
            name: "State16"

            PropertyChanges {
                target: _9_Make_a_duplicate_and_place_it_parallelly
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: 570
                y: 170
                width: 600
                height: 522
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Make a copy of the Triangle component. Drag and place it in a symmetrical position within the Regular Polygon component.")
            }
        },
        State {
            name: "State17"

            PropertyChanges {
                target: _10_Drag_a_rectangle_in_2D_view
                visible: true
            }

            PropertyChanges {
                target: strongHighlight9
                x: 0
                y: 959
                width: 73
                height: 72
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag a Rectangle component and place it besides the Regular polygon component within the 2D view.")
            }
        },
        State {
            name: "State18"

            PropertyChanges {
                target: _11_Update_the_zstack_and_size_of_the_rectangle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight10
                x: 1524
                y: 90
                width: 388
                height: 273
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Rectangle component in the 2D view to access its properties. Update the Size: Width to 230 pixels and the Height to 120 pixels in the GEOMETRY – 2D section. Set the Z stack to “2” to keep it visible on top of the Regular Polygon component.")
            }
        },
        State {
            name: "State19"

            PropertyChanges {
                target: _12_Update_corner_radius_and_bavel_of_the_rectangle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight11
                x: 1525
                y: 617
                width: 395
                height: 292
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("To set a uniform style in the corners of the Rectangle component, update the Global to “20” in the CORNER RADIUSES section.  Also, toggle the Global to be selected in the CORNER BEVEL section. That would give a flat cut in all the corners of the Rectangle component at the 20-radius point.")
            }
        },
        State {
            name: "State20"
            extend: "State19"

            PropertyChanges {
                target: strongHighlight11
                x: 1651
                y: 509
                width: 97
                height: 49
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Next, to change the Fill color of the Rectangle component, click on the default white color in the Fill color field within the RECTANGLE ITEM section. It will bring up the detailed color selection options.")
            }
        },

        State {
            name: "State21"

            PropertyChanges {
                target: strongHighlight8
                visible: true
            }

            PropertyChanges {
                target: strongHighlight11
                visible: true
            }

            PropertyChanges {
                target: _13_Change_the_fill_color_of_the_rectangle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight12
                x: 1566
                y: 123
                width: 267
                height: 837
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the “Radial” style for the color gradient for the Rectangle component. Then, in the COLOR DETAILS section, put the value “#74a58f8f”. This will select a transparent shade of black as the Fill color.")
            }
        },
        State {
            name: "State22"

            PropertyChanges {
                target: _14_Update_the_stroke_color_of_the_rectangle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight13
                x: 1535
                y: 401
                width: 377
                height: 49
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Update the Stroke color of the Rectangle component to “#7f000000”.")
            }
        },
        State {
            name: "State23"

            PropertyChanges {
                target: _15_Drag_the_rectangle_below_the_triangles_inside_the_regular_polygon
                visible: true
            }

            PropertyChanges {
                target: strongHighlight14
                x: 660
                y: 188
                width: 600
                height: 501
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag the Rectangle component on top of the Regular Polygon component and place it below the Triangle components. Using the knowledge from this tour, you can shape and arrange Qt Quick Studio Components as per your needs in your projects.")
            }
        }
    ]
}

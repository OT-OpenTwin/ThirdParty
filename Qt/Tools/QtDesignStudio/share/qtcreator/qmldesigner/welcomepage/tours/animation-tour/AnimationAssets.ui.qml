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
    state: "State0"
    title: qsTr("Creating 2D Animation")
    caption: qsTr("Take an empty project and select \"2D Animation\" from the top toolbar.")

    Image {
        id: _01_Get_2D_animation_controls
        visible: true
        source: "images/01_Get_2D_animation_controls.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: _02_Rectangle_to_2D_workspace
        visible: false
        source: "images/02_Rectangle_to_2D_workspace.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
            visible: true
        }
    }

    Image {
        id: _03_2nd_rectangle_turned_circle
        visible: false
        source: "images/03_2nd_rectangle_turned_circle.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
            visible: true
        }
    }

    Image {
        id: _04_Put_the_circle_in_the_rectangle
        visible: false
        source: "images/04_Put_the_circle_in_the_rectangle.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
            visible: true
        }
    }

    Image {
        id: _05_Drag_item_component_on_top_of_the_circle_component
        visible: false
        source: "images/05_Drag_item_component_on_top_of_the_circle_component.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
            visible: true
        }
    }

    Image {
        id: _6_Take_another_rectangle_and_resize
        visible: false
        source: "images/6_Take_another_rectangle_and_resize.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
            visible: true
        }
    }

    Image {
        id: _7_Put_the_new_rectangle_into_the_item_component
        visible: false
        source: "images/7_Put_the_new_rectangle_into_the_item_component.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
            visible: true
        }
    }

    Image {
        id: _8_Adding_a_animation_timeline
        visible: false
        source: "images/8_Adding_a_animation_timeline.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
            visible: true
        }
    }

    Image {
        id: _9_Adding_first_keyframe
        visible: false
        source: "images/9_Adding_first_keyframe.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
            visible: true
        }
    }

    Image {
        id: _10_Moving_pointer_to_the_end
        visible: false
        source: "images/10_Moving_pointer_to_the_end.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight9
            visible: true
        }
    }

    Image {
        id: _11_Adding_end_keyframe
        visible: false
        source: "images/11_Adding_end_keyframe.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight10
            visible: true
        }
    }

    Image {
        id: _12_Stopping_record
        visible: false
        source: "images/12_Stopping_record.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight11
            visible: true
        }
    }

    Image {
        id: _13_Add_easing_curve_to_manipulate_the_motion_accleration
        visible: false
        source: "images/13_Add_easing_curve_to_manipulate_the_motion_accleration.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight12
            visible: true
        }
    }

    Image {
        id: _14_Adjust_easing_motion_behaviour
        visible: false
        source: "images/14_Adjust_easing_motion_behaviour.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight13
            visible: true
        }
    }

    Image {
        id: _15_Adjust_easing_motion_behaviour_for_end_keyframe
        visible: false
        source: "images/15_Adjust_easing_motion_behaviour_for_end_keyframe.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight14
            visible: true
        }
    }

    Image {
        id: _16_Run_to_check_the_animation
        visible: false
        source: "images/16_Run_to_check_the_animation.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight15
            visible: true
        }
    }

    Rectangle {
        id: rectangle
        visible: false
        color: "#909090"
        anchors.fill: parent
    }

    states: [
        State {
            name: "State0"

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: true
            }

            PropertyChanges {
                target: strongHighlight
                x: 1525
                y: 43
                width: 236
                height: 390
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Take an empty project and select \"2D Animation\" from the top toolbar.")
            }
        },
        State {
            name: "State1"

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }

            PropertyChanges {
                target: _02_Rectangle_to_2D_workspace
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: 118
                y: 628
                width: 79
                height: 70
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag a Rectangle component to the 2D view.")
            }
        },
        State {
            name: "State2"

            PropertyChanges {
                target: _03_2nd_rectangle_turned_circle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 1110
                y: 298
                width: 278
                height: 296
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag another Rectangle component and place it beside the first Rectangle component. You need to make it a circle by manipulating its properties.")
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }
        },
        State {
            name: "State3"
            extend: "State2"

            PropertyChanges {
                target: strongHighlight2
                x: 1444
                y: 143
                width: 468
                height: 552
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Here are the properties you need to change. Make the Size both \"120\" in height and width. And change the Radius to \"60\" to make it round. Also, you need to change the Fill color to make it look different than the previous Rectangle.")
            }
        },
        State {
            name: "State4"

            PropertyChanges {
                target: _04_Put_the_circle_in_the_rectangle
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 670
                y: 214
                width: 454
                height: 458
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag the circle on top of the first Rectangle. Place it exactly in the middle. ")
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }
        },
        State {
            name: "State5"

            PropertyChanges {
                target: _05_Drag_item_component_on_top_of_the_circle_component
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 0
                y: 624
                width: 68
                height: 68
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Find the Item component in the Basic Components.")
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }
        },
        State {
            name: "State6"
            extend: "State5"

            PropertyChanges {
                target: strongHighlight4
                x: 0
                y: 238
                width: 368
                height: 68
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag it to the modified 2nd Rectangle in the Navigator view.")
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }
        },
        State {
            name: "State7"

            PropertyChanges {
                target: strongHighlight5
                x: 478
                y: 298
                width: 181
                height: 245
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag another Rectangle in 2D view.")
            }

            PropertyChanges {
                target: _6_Take_another_rectangle_and_resize
                visible: true
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }
        },
        State {
            name: "State8"
            extend: "State7"

            PropertyChanges {
                target: strongHighlight5
                x: 1437
                y: 88
                width: 475
                height: 625
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Change the Fill color and Size.")
            }
        },
        State {
            name: "State9"

            PropertyChanges {
                target: slide2
                visible: true
                caption: qsTr("Drag this new Rectangle component onto the previously placed Item in the Navigator view.")
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }

            PropertyChanges {
                target: _7_Put_the_new_rectangle_into_the_item_component
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: 14
                y: 239
                width: 345
                height: 94
            }
        },
        State {
            name: "State10"
            extend: "State9"

            PropertyChanges {
                target: strongHighlight6
                x: 683
                y: 222
                width: 434
                height: 439
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("The new rectangle would be placed like this inside the circle shape. If needed, you can move it inside the 2D view to have this placement.")
            }
        },
        State {
            name: "State11"
            extend: "State9"

            PropertyChanges {
                target: strongHighlight6
                x: 0
                y: 729
                width: 194
                height: 64
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("All the components are in the correct position now. Select \"+\" from the Timeline view to start including animation.")
            }
        },
        State {
            name: "State12"

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }

            PropertyChanges {
                target: _8_Adding_a_animation_timeline
                visible: true
            }

            PropertyChanges {
                target: strongHighlight7
                x: 596
                y: 204
                width: 709
                height: 647
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Here you can set up the animation timeline. First, give the animation timeline a suitable \"Timeline ID\". Define the start and end frame in milliseconds. You can select \"Continuous\" to have a self-repeating animation. You can select \"Ping pong\" for an animation that will go back and forth.")
            }
        },
        State {
            name: "State13"

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }

            PropertyChanges {
                target: _9_Adding_first_keyframe
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: -8
                y: 728
                width: 1934
                height: 311
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("The timeline you just created will be available here now.")
            }
        },
        State {
            name: "State14"
            extend: "State13"

            PropertyChanges {
                target: strongHighlight8
                x: -8
                y: 728
                width: 1934
                height: 77
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("This bar contains the timeline controls. You can go to the beginning or end of the timeline and can jump a few frames if needed. Also, you can play, pause, and manipulate animation acceleration and ending motions with specific controls. Going to specific frames or stretching the timeline to have fine details within the animation is also possible with these controls.")
            }
        },
        State {
            name: "State15"
            extend: "State13"

            PropertyChanges {
                target: strongHighlight8
                x: 190
                y: 790
                width: 1730
                height: 220
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("All the keyframes for the animation you are creating stay here.")
            }
        },
        State {
            name: "State16"
            extend: "State13"

            PropertyChanges {
                target: strongHighlight8
                x: 19
                y: 260
                width: 349
                height: 42
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the item in the Navigation view. You will put rotation on the item in the following steps. Hence, the small rectangle inside it would turn to make an animation.")
            }
        },
        State {
            name: "State17"
            extend: "State13"

            PropertyChanges {
                target: strongHighlight8
                x: 608
                y: 746
                width: 56
                height: 55
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Auto Key to record the keyframes in the animation timeline.")
            }
        },

        State {
            name: "State18"
            extend: "State13"

            PropertyChanges {
                target: strongHighlight8
                x: 184
                y: 728
                width: 60
                height: 311
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Drag the timeline pointer to the beginning to put a keyframe at the start.")
            }
        },
        State {
            name: "State19"
            extend: "State13"

            PropertyChanges {
                target: strongHighlight8
                x: 1444
                y: 265
                width: 461
                height: 260
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Go to the \"Geometry – 2D\" section in the Property view and find the \"Rotation\" field. Reach near the left of the input field to get the tool icon. Select it to bring up the menu and select \"Insert Keyframe\" from there. The rotation angle is now at \"0.0\" degrees, which will stay as the beginning frame at the start of the animation timeline.")
            }

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }
        },
        State {
            name: "State20"

            PropertyChanges {
                target: _10_Moving_pointer_to_the_end
                visible: true
            }

            PropertyChanges {
                target: strongHighlight9
                x: -6
                y: 787
                width: 241
                height: 118
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You will find a diamond-shaped icon in the timeline to indicate your animation keyframe. On the leftmost side of the timeline, you will find details about which property of which component the keyframe was applied on.")
            }
        },
        State {
            name: "State21"
            extend: "State20"

            PropertyChanges {
                target: strongHighlight9
                x: 1673
                y: 783
                width: 178
                height: 214
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Move the pointer to the end of the timeline. Do not turn off the Auto Key. You will set the end keyframe here for the item rotation.")
            }
        },
        State {
            name: "State22"

            PropertyChanges {
                target: _11_Adding_end_keyframe
                visible: true
            }

            PropertyChanges {
                target: strongHighlight10
                x: 1490
                y: 367
                width: 281
                height: 160
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the item in the Navigation view, go to the Rotation property on the Properties view, and make the value 360 degrees there. Now add it as a keyframe with \"Insert Keyframe\" for the end frame of the animation timeline.")
            }
        },
        State {
            name: "State23"

            PropertyChanges {
                target: _12_Stopping_record
                visible: true
            }

            PropertyChanges {
                target: strongHighlight11
                x: 600
                y: 749
                width: 72
                height: 51
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("All the keyframes are in the right places now. Turn off the Auto Key.")
            }
        },
        State {
            name: "State24"

            PropertyChanges {
                target: _13_Add_easing_curve_to_manipulate_the_motion_accleration
                visible: true
            }

            PropertyChanges {
                target: strongHighlight12
                x: 178
                y: 824
                width: 64
                height: 78
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can edit the Easing Curve for any keyframe to manipulate the motion speed in the animation. Select the first diamond-shaped Keyframe in the timeline. It changes the color to confirm the selection.")
            }
        },
        State {
            name: "State25"
            extend: "State24"

            PropertyChanges {
                target: strongHighlight12
                x: 675
                y: 748
                width: 177
                height: 83
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the Easing Curve Editor to have all the options for manipulation.")
            }
        },
        State {
            name: "State26"

            PropertyChanges {
                target: _14_Adjust_easing_motion_behaviour
                visible: true
            }

            PropertyChanges {
                target: strongHighlight13
                x: 1302
                y: 117
                width: 236
                height: 837
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("For easy manipulation, you can choose any of these presets.")
            }
        },
        State {
            name: "State27"
            extend: "State26"

            PropertyChanges {
                target: strongHighlight13
                x: 244
                y: 144
                width: 1072
                height: 846
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select the top or bottom orange handles to control the easing curve yourself. Selecting \"Preview\" gives you an output of the customized effect.")
            }
        },
        State {
            name: "State28"
            extend: "State26"

            PropertyChanges {
                target: strongHighlight13
                x: 1302
                y: 938
                width: 264
                height: 51
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select \"Ok\" to apply the easing curve to the keyframe, or select \"Cancel\" to close the editor without applying. You can save the custom preset by selecting \"Save\" and giving it a proper name.")
            }
        },
        State {
            name: "State29"

            PropertyChanges {
                target: _15_Adjust_easing_motion_behaviour_for_end_keyframe
                visible: true
            }

            PropertyChanges {
                target: strongHighlight14
                x: 234
                y: 40
                width: 1437
                height: 979
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Following the previous steps, also apply this easing on the end keyframe.")
            }
        },
        State {
            name: "State31"

            PropertyChanges {
                target: _16_Run_to_check_the_animation
                visible: true
            }

            PropertyChanges {
                target: strongHighlight15
                x: 184
                y: 780
                width: 1613
                height: 111
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("After you apply the easing curves successfully, the icons will change their shapes from Diamond to Hourglass.")
            }
        },
        State {
            name: "State32"
            extend: "State31"

            PropertyChanges {
                target: strongHighlight15
                x: 41
                y: 40
                width: 171
                height: 65
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("Select \"Run Project\" or \"Live Preview\" to test the animation you have created.")
            }
        },
        State {
            name: "State34"

            PropertyChanges {
                target: _01_Get_2D_animation_controls
                visible: false
            }

            PropertyChanges {
                target: animationOutput
                x: 744
                y: 331
                visible: true
            }

            PropertyChanges {
                target: rectangle
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You will observe an animation with the middle rectangle moving in back-and-forth motion following the applied easing curves to speed up and down.")
            }
        }
    ]

    AnimationOutput {
        id: animationOutput
        visible: false
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
    }
}

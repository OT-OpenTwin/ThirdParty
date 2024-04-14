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
    id: slide
    width: 1920
    height: 1080
    visible: true
    state: "MenuFocus"
    //    caption: "This is Qt Design Studio Welcome Page."
    caption: "blub"
    title: qsTr("Workspaces")

    Image {
        id: projectWithProjectsOpened
        source: "images/Project_With_Projects_Opened.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: projectWithNavigatorOpened
        visible: false
        source: "images/Project_With_Navigator_Opened.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
        }
    }

    Image {
        id: projectWithComponentsOpened
        visible: false
        source: "images/Project_With_Components_Opened.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2

            Image {
                id: viewComponents
                x: 395
                y: -115
                source: "images/View_Components.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: basicComponents
                x: 396
                y: -375
                visible: false
                source: "images/Basic_Components.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: positionerComponent
                source: "images/Positioner_Component.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: animationComponents
                x: 760
                y: -243
                source: "images/Animation_Components.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: instancerscomponents
                source: "images/Instancers_components.png"
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: qtQuickComponents
                x: 1120
                y: -353
                source: "images/Qt_Quick_Components.png"
                fillMode: Image.PreserveAspectFit
            }
        }
    }

    Image {
        id: projectWithComponentsOpened1
        visible: false
        source: "images/Project_With_Components_Opened.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
        }

        Item {
            id: propertyFocused
            x: 1442
            y: 96
            width: 470
            height: 854
            visible: false
            clip: true

            Image {
                id: projectWithComponentsOpened2
                x: -1443
                y: -94
                width: 1920
                height: 1077
                visible: true
                source: "images/Project_With_Components_Opened.png"
                fillMode: Image.PreserveAspectFit
            }

            Highlight {
                id: highlight
                anchors.fill: parent
            }
        }
    }

    Image {
        id: projectWithButtonSelectedinCodeView
        visible: false
        source: "images/Project_With_Button_Selected_in_Code_View.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
            visible: false
        }
    }

    states: [
        State {
            name: "MenuFocus"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 17
                width: 232
                height: 35
                visible: true
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can find all the actions and features under the menu items. Visit each option thoroughly to get an overall idea.")
            }
        },
        State {
            name: "TopToolBarFocus"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 37
                width: 1920
                height: 67
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can control, share, and interact with projects from the top toolbar. This is a place with easy access controls for project manipulation. Check the top toolbar tour to get a detailed idea about its controls.")
            }
        },
        State {
            name: "ProjectFocus"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 88
                width: 367
                height: 472
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can access different files related to project from here. Select the corresponding file to have them opened in the workspace and edit them in code or design.")
            }
        },
        State {
            name: "NavigatorFocus"

            PropertyChanges {
                target: projectWithNavigatorOpened
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: 0
                y: 89
                width: 365
                height: 476
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can navigate the component hierarchy of the project from here. You can select any component, drag them to another level to change dependencies. You can also change their properties or add functionalities to them while they are selected.")
            }
        },
        State {
            name: "AssetsFocus"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 560
                width: 370
                height: 479
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can add external assets to the project. Select, the \"+\", find your asset, select it. Later, you can drag this assets into the Navigator or 2D view to have them as components in the project.")
            }
        },
        State {
            name: "ComponentFocus"

            PropertyChanges {
                target: projectWithComponentsOpened
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: -8
                y: 557
                width: 379
                height: 478
            }

            PropertyChanges {
                target: viewComponents
                visible: false
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can access all the components available in Qt Design Studio here. If an existing component is not visible, you can select \"+\" and add it yourself. You can also use \"Search\" to find any component you need. Components created by you can also be found here when you add it to the project.")
            }

            PropertyChanges {
                target: qtQuickComponents
                visible: false
            }

            PropertyChanges {
                target: animationComponents
                visible: false
            }

            PropertyChanges {
                target: instancerscomponents
                x: 24
                y: -206
                visible: false
            }

            PropertyChanges {
                target: positionerComponent
                visible: false
            }
        },
        State {
            name: "ComponentFocus_Examples"
            extend: "ComponentFocus"

            PropertyChanges {
                target: basicComponents
                visible: true
            }

            PropertyChanges {
                target: viewComponents
                x: 396
                y: -119
                width: 348
                height: 94
                visible: true
            }

            PropertyChanges {
                target: positionerComponent
                x: 758
                y: -375
                width: 348
                height: 98
                visible: true
            }

            PropertyChanges {
                target: animationComponents
                x: 759
                y: -264
                width: 347
                height: 161
                visible: true
            }

            PropertyChanges {
                target: instancerscomponents
                x: 758
                y: -88
                width: 348
                height: 100
                visible: true
            }

            PropertyChanges {
                target: qtQuickComponents
                x: 1123
                y: -375
                visible: true
            }

            PropertyChanges {
                target: slide
                caption: qsTr("Here are some basic component groups. You can find more with search or \"+\" in the components section.")
            }
        },
        State {
            name: "ButtonFocus"

            PropertyChanges {
                target: strongHighlight
                x: 836
                y: 408
                width: 125
                height: 65
                visible: false
            }

            PropertyChanges {
                target: projectWithComponentsOpened1
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 836
                y: 408
                width: 124
                height: 63
            }

            PropertyChanges {
                target: propertyFocused
                x: 1438
                y: 80
                visible: true
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can select a component from the Navigator or 2D view to access its properties. Adjust the settings for the component from there.")
            }
        },
        State {
            name: "DesignViewFocus"

            PropertyChanges {
                target: strongHighlight
                x: 362
                y: 90
                width: 1080
                height: 643
            }

            PropertyChanges {
                target: slide
                caption: qsTr("This is the main workspace. You can either have 2D or 3D design here depending on which type of project you are working on. You will find the visual representation of all the components and items here. Interact and adjust them with the intuitive controls.")
            }
        },
        State {
            name: "CodeViewFocus"

            PropertyChanges {
                target: projectWithButtonSelectedinCodeView
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 363
                y: 89
                width: 1079
                height: 642
                visible: true
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can always switch to the Code view in the workspace to make direct adjustment in the code. These codes are generated automatically as you set up the design with components in Qt Design Studio.")
            }
        },
        State {
            name: "StatesFocus"

            PropertyChanges {
                target: strongHighlight
                x: 368
                y: 722
                width: 1072
                height: 315
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can create and maintain actions across different states in Qt Design Studio. Learn more about the states in the States tour.")
            }
        }
    ]
}

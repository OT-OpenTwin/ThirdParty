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
    state: "Topbar total"
    caption: ""
    title: qsTr("Top Toolbar")

    Image {
        id: projectwithComponents
        source: "images/Project_with_Components.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: shareBoxOpened
        visible: false
        source: "images/Share_Box_Opened.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
        }
    }

    states: [
        State {
            name: "Topbar total"

            PropertyChanges {
                target: strongHighlight
                x: -1
                y: 44
                width: 1920
                height: 52
            }

            PropertyChanges {
                target: slide2
                width: 1920
                height: 1080
                caption: qsTr("You can find a few of the important controls packed in the top Toolbar.")
            }
        },
        State {
            name: "Topbar Home"

            PropertyChanges {
                target: strongHighlight
                x: 8
                y: 49
                width: 43
                height: 45
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can switch between Qt Design Studio Home and Project view selecting this.")
            }
        },
        State {
            name: "Topbar Play"

            PropertyChanges {
                target: strongHighlight
                x: 50
                y: 46
                width: 47
                height: 50
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can run a project selecting this. Qt Design Studio will ask you to save all the changes and make your application live afterwards.")
            }
        },
        State {
            name: "Topbar Live Preview"

            PropertyChanges {
                target: strongHighlight
                x: 93
                y: 43
                width: 116
                height: 55
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can have a live preview of the application by selecting this. Your changes in the application space will instantly reflect in the preview. It is a good option for prototyping small changes in the application.")
            }
        },
        State {
            name: "Topbar Opened File Selector"

            PropertyChanges {
                target: strongHighlight
                x: 201
                y: 39
                width: 338
                height: 61
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can select the opened files in your project from here.")
            }
        },
        State {
            name: "Topbar File Manipulator"

            PropertyChanges {
                target: strongHighlight
                x: 536
                y: 44
                width: 137
                height: 56
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can close the current file, go back to the previous file or the next file using these controls.")
            }
        },
        State {
            name: "Topbar Component Creator"

            PropertyChanges {
                target: strongHighlight
                x: 1440
                y: 45
                width: 49
                height: 50
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can create a component with your currently selected item.")
            }
        },
        State {
            name: "Topbar Component Editor"

            PropertyChanges {
                target: strongHighlight
                x: 1486
                y: 45
                width: 50
                height: 51
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can edit a created component from here.")
            }
        },
        State {
            name: "Topbar Change Workspace"

            PropertyChanges {
                target: strongHighlight
                x: 1525
                y: 42
                width: 236
                height: 58
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can change between the workspaces here.")
            }
        },
        State {
            name: "Topbar Share button"

            PropertyChanges {
                target: strongHighlight
                x: 1758
                y: 42
                width: 118
                height: 58
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can share your created Qt Design Studio project online by selecting this option.")
            }
        },
        State {
            name: "Topbar Share Window"
            extend: "Topbar Share button"

            PropertyChanges {
                target: shareBoxOpened
                visible: true
            }

            PropertyChanges {
                target: strongHighlight1
                x: 759
                y: 307
                width: 310
                height: 381
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You should click on share and receive the link for Qt Design Viewer. Share the link with others to let them have a look from their browsers.")
            }
        },
        State {
            name: "Topbar See more button"

            PropertyChanges {
                target: strongHighlight
                x: 1867
                y: 44
                width: 53
                height: 57
            }

            PropertyChanges {
                target: slide2
                caption: qsTr("You can find the hidden controls from here if they are not visible due to the window being small in size.")
            }
        }
    ]
}

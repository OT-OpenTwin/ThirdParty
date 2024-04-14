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
    state: "Create_OpenProjectFocus"
    caption: qsTr("This is Qt Design Studio Welcome Page.")
    title: qsTr("Welcome Page")

    Image {
        id: home_page
        source: "images/01.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: home_page_example
        visible: false
        source: "images/05.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
        }
    }

    Image {
        id: home_page_tutorials
        visible: false
        source: "images/06.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
        }
    }

    Image {
        id: home_page_buttom_bar
        visible: false
        source: "images/07.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
        }
    }

    states: [
        State {
            name: "Create_OpenProjectFocus"

            PropertyChanges {
                target: strongHighlight
                x: 8
                y: 234
                width: 272
                height: 142
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can create a new Qt Design Studio project or open an existing project from here.")
            }
        },
        State {
            name: "Examples Button"

            PropertyChanges {
                target: home_page_example
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 8
                y: 560
                width: 274
                height: 66
            }

            PropertyChanges {
                target: slide
                caption: qsTr("Access example projects. You will be able to experience the immense potential of Qt Design Studio.")
            }
        },
        State {
            name: "Examples Button Window"
            extend: "Examples Button"

            PropertyChanges {
                target: strongHighlight2
                x: 294
                y: 245
                width: 1570
                height: 741
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You will find all the available examples here after selecting the button.")
            }
        },
        State {
            name: "Tutorials Button"

            PropertyChanges {
                target: home_page_tutorials
                visible: true
            }

            PropertyChanges {
                target: strongHighlight3
                x: 8
                y: 616
                width: 274
                height: 64
            }

            PropertyChanges {
                target: slide
                caption: qsTr("Learn Qt Design Studio tools and workflow with the tutorials.")
            }
        },
        State {
            name: "Tutorials Button Window"
            extend: "Tutorials Button"

            PropertyChanges {
                target: strongHighlight3
                x: 285
                y: 247
                width: 1580
                height: 734
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You will find all the available tutorials here after selecting the button.")
            }
        },
        State {
            name: "Home Page Buttom Bar"

            PropertyChanges {
                target: home_page_buttom_bar
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 278
                y: 987
                width: 1598
                height: 51
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can access more information related to Qt Design Studio usage and account here. Take a look at our forums and blogs for in depth discussion.")
            }
        }
    ]
}

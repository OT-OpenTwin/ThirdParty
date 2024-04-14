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
    caption: qsTr("This is Qt Design Studio Welcome Page.")
    state: "Home Page"
    title: qsTr("States")

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
            name: "Home Page"

            PropertyChanges {
                target: strongHighlight
                x: 0
                y: 119
                width: 577
                height: 103
            }

            PropertyChanges {
                target: slide
                caption: qsTr("Welcome to Qt Design Studio.")
            }
        },
        State {
            name: "Design Studio Menu"

            PropertyChanges {
                target: strongHighlight
                x: -6
                y: 15
                width: 219
                height: 37
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can access various setup and adjustment options for Qt Design Studio projects and environment here.")
            }
        },
        State {
            name: "Recent Projects"

            PropertyChanges {
                target: strongHighlight
                x: 14
                y: 509
                width: 264
                height: 58
            }

            PropertyChanges {
                target: slide
                caption: qsTr("All your recently created projects can be found here.")
            }
        },
        State {
            name: "QtDs Blog"

            PropertyChanges {
                target: strongHighlight
                x: 8
                y: 702
                width: 274
                height: 325
            }

            PropertyChanges {
                target: slide
                caption: qsTr("From here you can visit the blog post related to newly released Qt Design Studio.")
            }
        },
        State {
            name: "Create Project Button"

            PropertyChanges {
                target: strongHighlight
                x: 8
                y: 234
                width: 272
                height: 71
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can create a new project from here. After selecting, it would bring you a wizard for creating a fresh project.")
            }
        },
        State {
            name: "Open Project Button"

            PropertyChanges {
                target: strongHighlight
                x: 8
                y: 299
                width: 272
                height: 75
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can open a previously created or imported project from here. After selecting, browse to your “qmlproject” file and select “Open”.")
            }
        },
        State {
            name: "Get Started Button"

            PropertyChanges {
                target: strongHighlight
                x: 8
                y: 413
                width: 272
                height: 70
            }

            PropertyChanges {
                target: slide
                caption: qsTr("You can access detailed documentation on tools and components of Qt Design Studio here.")
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
                caption: qsTr("Access example projects. You will be able to experience the immense potential of Qt Design Studio. ")
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
                caption: qsTr("Access example projects. You will be able to experience the immense potential of Qt Design Studio. ")
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
                caption: qsTr("Learn Qt Design Studio tools and workflow with the tutorials.")
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

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
    caption: "Create a new project in Qt Design Studio."
    title: qsTr("Adding Assets")
    state: "State1"

    Image {
        id: _01_Begin_to_add_assts
        source: "images/01_Begin_to_add_assts.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight
            visible: true
        }
    }

    Image {
        id: _02_Browse_and_select_the_images
        visible: false
        source: "images/02_Browse_and_select_the_images.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight1
        }
    }

    Image {
        id: _03_Carry_on_the_import_process
        visible: false
        source: "images/03_Carry_on_the_import_process.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight2
        }
    }

    Image {
        id: _04_The_images_in_QDS
        visible: false
        source: "images/04_The_images_in_QDS.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight3
        }
    }

    Image {
        id: _05_Start_adding_fonts
        visible: false
        source: "images/05_Start_adding_fonts.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight4
        }
    }

    Image {
        id: _06_Browse_and_select_the_fonts
        visible: false
        source: "images/06_Browse_and_select_the_fonts.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight5
        }
    }

    Image {
        id: _07_The_fonts_in_QDS
        visible: false
        source: "images/07_The_fonts_in_QDS.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight6
        }
    }

    Image {
        id: _08_Add_image_1
        visible: false
        source: "images/08_Add_image_1.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight7
        }
    }

    Image {
        id: _11_Add_image_4
        visible: false
        source: "images/11_Add_image_4.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight8
        }
    }

    Image {
        id: _12_Add_text
        visible: false
        source: "images/12_Add_text.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight9
        }
    }

    Image {
        id: _14_Change_the_text
        visible: false
        source: "images/14_Change_the_text.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight10
        }
    }

    Image {
        id: _15_The_final_output
        visible: false
        source: "images/15_The_final_output.png"
        fillMode: Image.PreserveAspectFit

        StrongHighlight {
            id: strongHighlight11
        }
    }

    states: [
        State {
            name: "State1"

            PropertyChanges {
                target: strongHighlight
                x: 120
                y: 805
                width: 93
                height: 88
            }

            PropertyChanges {
                target: slide2
                caption: "You will find this option at the beginning of a newly created project because no Asset is yet added to it. Select \"+\" to browse through your local drive for Assets you want to include in the project."
            }
        },
        State {
            name: "State2"

            PropertyChanges {
                target: _02_Browse_and_select_the_images
                visible: true
                source: "images/02_Browse_and_select_the_images.png"
            }

            PropertyChanges {
                target: strongHighlight1
                x: 504
                y: 195
                width: 889
                height: 596
            }

            PropertyChanges {
                target: slide2
                caption: "Browse the files you want to include, select them and select Open."
            }
        },
        State {
            name: "State3"

            PropertyChanges {
                target: _03_Carry_on_the_import_process
                visible: true
            }

            PropertyChanges {
                target: strongHighlight2
                x: 706
                y: 366
                width: 491
                height: 322
            }

            PropertyChanges {
                target: slide2
                caption: "Here you can select where the imported files get saved. By default it would save inside your project directory within the images folder. Select Ok to continue."
            }
        },
        State {
            name: "State4"

            PropertyChanges {
                target: _04_The_images_in_QDS
                visible: true
            }

            PropertyChanges {
                target: slide2
                caption: "You will find your imported image files here under the assets section."
            }

            PropertyChanges {
                target: strongHighlight3
                x: -8
                y: 588
                width: 351
                height: 429
            }
        },
        State {
            name: "State5"

            PropertyChanges {
                target: _05_Start_adding_fonts
                visible: true
            }

            PropertyChanges {
                target: strongHighlight4
                x: 0
                y: 651
                width: 340
                height: 72
            }

            PropertyChanges {
                target: slide2
                caption: "There are already some assets in this section now. So you need to select this \"+\" button to include new Assets to the project."
            }
        },
        State {
            name: "State6"

            PropertyChanges {
                target: _06_Browse_and_select_the_fonts
                visible: true
            }

            PropertyChanges {
                target: strongHighlight5
                x: 497
                y: 196
                width: 906
                height: 600
            }

            PropertyChanges {
                target: slide2
                caption: "Browse and select some fonts to include in the project next. Then, select Open."
            }
        },
        State {
            name: "State7"

            PropertyChanges {
                target: _07_The_fonts_in_QDS
                visible: true
            }

            PropertyChanges {
                target: strongHighlight6
                x: -7
                y: 588
                width: 348
                height: 449
            }

            PropertyChanges {
                target: slide2
                caption: "Your selected fonts can also be found under the Assets section in its sub-section."
            }
        },
        State {
            name: "State8"

            PropertyChanges {
                target: _08_Add_image_1
                visible: true
            }

            PropertyChanges {
                target: strongHighlight7
                x: 685
                y: 295
                width: 246
                height: 181
            }

            PropertyChanges {
                target: slide2
                caption: "Drag the images you need from the Assets to the 2D view to add them to your design."
            }
        },
        State {
            name: "State9"

            PropertyChanges {
                target: _11_Add_image_4
                visible: true
            }

            PropertyChanges {
                target: strongHighlight8
                x: 640
                y: 274
                width: 560
                height: 370
            }

            PropertyChanges {
                target: slide2
                caption: "You can drag all the other images you need to the 2D view. If you want to put them in a layout for sorting, make sure they all stay on the same level in the Navigation tree."
            }
        },
        State {
            name: "State10"

            PropertyChanges {
                target: _12_Add_text
                visible: true
            }

            PropertyChanges {
                target: strongHighlight9
                x: 849
                y: 592
                width: 115
                height: 62
            }

            PropertyChanges {
                target: slide2
                caption: "You can drag any font you like from Assets to the 2D view."
            }
        },
        State {
            name: "State11"

            PropertyChanges {
                target: _14_Change_the_text
                visible: true
            }

            PropertyChanges {
                target: strongHighlight10
                x: 1523
                y: 719
                width: 389
                height: 181
            }

            PropertyChanges {
                target: slide2
                caption: "Modify the font size and edit the Text to write what you need in the 2D view."
            }
        },
        State {
            name: "State12"

            PropertyChanges {
                target: _15_The_final_output
                visible: true
            }

            PropertyChanges {
                target: strongHighlight11
                x: 636
                y: 279
                width: 525
                height: 373
            }

            PropertyChanges {
                target: slide2
                caption: "You can modify and adjust the assets in the 2D view using the Properties view and design with them according to your needs."
            }
        }
    ]
}

// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick3D.MaterialEditor

Flickable {
    id: flickable
    property alias font: textArea.font
    property alias text: textArea.text
    property alias textDocument: textArea.textDocument
    property alias lineColumn: lineNumbers
    property alias textArea: textArea

    property int rowHeight: Math.ceil(fontMetrics.lineSpacing)
    property int marginsTop: 10
    property int marginsLeft: 4
    property int lineCountWidth: 40
    clip: true
    boundsBehavior: Flickable.StopAtBounds

    ScrollBar.vertical: ScrollBar {
        width: 15
        active: true
    }
    ScrollBar.horizontal: ScrollBar {
        width: 15
        active: true
    }

    FontMetrics {
        id: fontMetrics
        font: textArea.font
    }


    Column {
        id: lineNumbers
        anchors.left: parent.left
        anchors.leftMargin: marginsLeft
        anchors.topMargin:  marginsTop
        y: marginsTop
        width: lineCountWidth

        function labelAt(lineNr) {
            if (lineNr > 0) {
                if (lineNr > repeater.count)
                    lineNr = repeater.count; // Best guess at this point...
                return repeater.itemAt(lineNr - 1);
            }

            return null;
        }

        function range(start, end) {
            var rangeArray = new Array(end-start);
            for (var i = 0; i < rangeArray.length; i++)
                rangeArray[i] = start+i;
            return rangeArray;
        }

        Repeater {
            id: repeater
            model: textArea.lineCount
            delegate: Label {
                font: textArea.font
                width: parent.width
                horizontalAlignment: Text.AlignRight
                verticalAlignment: Text.AlignVCenter
                height: rowHeight
                renderType: Text.NativeRendering
                text: index+1
            }
        }
    }
    Rectangle {
        id: lineNumbersSeperator
        y: 4
        height: parent.height
        anchors.left: lineNumbers.right
        anchors.leftMargin: marginsLeft
        width: 1
        color: "#ddd"
    }

    SyntaxHighlighter {
        id: syntaxHighlighter
        document: textArea.textDocument
    }

    TextArea.flickable: TextArea {
        id: textArea
        textFormat: Qt.PlainText
        focus: false
        selectByMouse: true
        leftPadding: flickable.marginsLeft
        rightPadding: flickable.marginsLeft
        topPadding: flickable.marginsTop
        bottomPadding: flickable.marginsTop
        tabStopDistance: fontMetrics.averageCharacterWidth * 4;
        anchors.left: lineNumbersSeperator.right
    }
}

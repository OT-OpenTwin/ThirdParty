// Copyright (C) 2023 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.Universal

T.DialogButtonBox {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            (control.count === 1 ? implicitContentWidth * 2 : implicitContentWidth) + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)
    contentWidth: (contentItem as ListView).contentWidth // QTBUG-111283 blocks optional chaining + nullish coalescing

    spacing: 4
    padding: 24
    topPadding: position === T.DialogButtonBox.Footer ? 6 : 24
    bottomPadding: position === T.DialogButtonBox.Header ? 6 : 24
    alignment: count === 1 ? Qt.AlignRight : undefined

    delegate: Button {
        width: control.count === 1 ? control.availableWidth / 2 : undefined
    }

    contentItem: ListView {
        implicitWidth: contentWidth
        model: control.contentModel
        spacing: control.spacing
        orientation: ListView.Horizontal
        boundsBehavior: Flickable.StopAtBounds
        snapMode: ListView.SnapToItem
    }

    background: Rectangle {
        implicitHeight: 32
        color: control.Universal.chromeMediumLowColor
        x: 1; y: 1
        width: parent.width - 2
        height: parent.height - 2
    }
}

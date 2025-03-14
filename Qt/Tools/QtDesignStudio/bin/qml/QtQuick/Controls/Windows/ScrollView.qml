// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Controls.impl
import QtQuick.Templates as T

T.ScrollView {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            contentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding)

    rightPadding: ScrollBar.vertical.visible ? ScrollBar.vertical.width : 0
    bottomPadding: ScrollBar.horizontal.visible ? ScrollBar.horizontal.height : 0

    // Don't set __notCustomizable here, because it would require special-casing
    // setFlickable's call to setContentItem.

    ScrollBar.vertical: ScrollBar {
        parent: control
        x: control.mirrored ? 0 : control.width - width
        y: 0
        height: control.height - (control.ScrollBar.horizontal.visible ? control.ScrollBar.horizontal.height : 0)
        active: control.ScrollBar.horizontal.active
    }

    ScrollBar.horizontal: ScrollBar {
        parent: control
        x: 0
        y: control.height - height
        width: control.width - (control.ScrollBar.vertical.visible ? control.ScrollBar.vertical.width : 0)
        active: control.ScrollBar.vertical.active
    }
}

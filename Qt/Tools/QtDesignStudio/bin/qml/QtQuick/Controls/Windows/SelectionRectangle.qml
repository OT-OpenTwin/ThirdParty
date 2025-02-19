// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Templates as T
import QtQuick.Shapes

T.SelectionRectangle {
    id: control

    readonly property bool __notCustomizable: true

    topLeftHandle: Item {
        width: 20
        height: 20
        visible: SelectionRectangle.control.active
        // This item is deliberately empty. Selection handles don't feel at home
        // for this style. But we provide an invisible handle that the user can
        // drag on.
    }

    bottomRightHandle: Item {
        width: 20
        height: 20
        visible: SelectionRectangle.control.active
        // This item is deliberately empty. Selection handles don't feel at home
        // for this style. But we provide an invisible handle that the user can
        // drag on.
    }

}

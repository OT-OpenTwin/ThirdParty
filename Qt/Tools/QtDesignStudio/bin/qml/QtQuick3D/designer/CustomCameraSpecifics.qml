// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick 2.15
import QtQuick.Layouts 1.15
import HelperWidgets 2.0

Column {
    width: parent.width

    // Custom camera doesn't have any meaningful designable properties itself, so only add
    // the generic camera section

    CameraSection {
        width: parent.width
    }

    NodeSection {
        width: parent.width
    }
}

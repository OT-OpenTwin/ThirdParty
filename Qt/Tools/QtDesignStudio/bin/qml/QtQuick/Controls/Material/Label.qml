// Copyright (C) 2017 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.Material

T.Label {
    id: control

    color: enabled ? Material.foreground : Material.hintTextColor
    linkColor: Material.accentColor
}

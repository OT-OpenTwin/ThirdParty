// Copyright (C) 2017 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.Universal

T.Label {
    id: control

    opacity: enabled ? 1.0 : 0.2
    color: control.Universal.foreground
    linkColor: Universal.accent
}

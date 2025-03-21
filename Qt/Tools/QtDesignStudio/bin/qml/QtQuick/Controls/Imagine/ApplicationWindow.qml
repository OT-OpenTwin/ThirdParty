// Copyright (C) 2017 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick.Window
import QtQuick.Templates as T
import QtQuick.Controls.Imagine
import QtQuick.Controls.Imagine.impl

T.ApplicationWindow {
    id: window

    background: NinePatchImage {
        width: window.width
        height: window.height

        source: Imagine.url + "applicationwindow-background"
        NinePatchImageSelector on source {
            states: [
                {"active": window.active}
            ]
        }
    }
}

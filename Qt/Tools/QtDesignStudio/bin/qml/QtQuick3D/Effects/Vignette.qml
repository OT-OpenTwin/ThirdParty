// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick3D
import QtQuick3D.Effects

Effect {
    property real vignetteStrength: 15 // 0 - 15
    property vector3d vignetteColor: Qt.vector3d(0.5, 0.5, 0.5)
    property real vignetteRadius: 0.35 // 0 - 5

    Shader {
        id: vignette
        stage: Shader.Fragment
        shader: "qrc:/qtquick3deffects/shaders/vignette.frag"
    }

    passes: [
        Pass {
            shaders: vignette
        }
    ]
}

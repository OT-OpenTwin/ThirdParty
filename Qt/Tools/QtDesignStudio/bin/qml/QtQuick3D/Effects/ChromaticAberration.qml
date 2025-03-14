// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick3D
import QtQuick3D.Effects

Effect {
    property TextureInput maskTexture: TextureInput {
        texture: Texture {
            source: "qrc:/qtquick3deffects/maps/white.png"
            tilingModeHorizontal: Texture.Repeat
            tilingModeVertical: Texture.Repeat
        }
    }
    property real aberrationAmount: 50
    property real focusDepth: 600

    Shader {
        id: chromaticAberration
        stage: Shader.Fragment
        shader: "qrc:/qtquick3deffects/shaders/chromaticaberration.frag"
    }

    passes: [
        Pass {
            shaders: chromaticAberration
        }
    ]
}

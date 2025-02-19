// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick3D

Effect {
    passes: renderPass

    Pass {
        id: renderPass
        shaders: [fragShader]
    }

    Shader {
        id: fragShader
        stage: Shader.Fragment
        shader: "effect_default_shader.frag"
    }
}

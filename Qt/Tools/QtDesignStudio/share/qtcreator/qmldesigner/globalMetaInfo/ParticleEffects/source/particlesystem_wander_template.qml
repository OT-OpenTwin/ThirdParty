/****************************************************************************
**
** Copyright (C) 2021 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of Qt Design Studio.
**
** $QT_BEGIN_LICENSE:GPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 or (at your option) any later version
** approved by the KDE Free Qt Foundation. The licenses are as published by
** the Free Software Foundation and appearing in the file LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D

ParticleSystem3D {
    ParticleEmitter3D {
        id: wanderSpriteEmitter
        particle: wanderSpriteParticle
        position: wanderTarget.position
        emitRate: 100
        particleScale: 20
        particleScaleVariation: 5
        particleEndScale: 30
        particleEndScaleVariation: 10
        lifeSpanVariation: 1000

        SpriteParticle3D {
            id: wanderSpriteParticle
            sprite: spriteTexture
            particleScale: 0.2
            maxAmount: 600
            billboard: true
            fadeInEffect: Particle3D.FadeScale
            fadeInDuration: 100
            fadeOutEffect: Particle3D.FadeOpacity
            fadeOutDuration: 1500
            Texture {
                id: spriteTexture
            }
        }
    }

    Wander3D {
        uniquePace.z: 0.1
        uniquePace.y: 0.1
        uniquePace.x: 0.1
        uniqueAmount.z: 40
        uniqueAmount.y: 40
        uniqueAmount.x: 40
        uniqueAmountVariation: 1
        uniquePaceVariation: 1
        fadeInDuration: 3000
    }

    Node {
        id: wanderTarget
    }
}

import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root
    property vector3d volume: Qt.vector3d(200, 100, 200)
    property real intensity: 0.5
    property real size: 1.0

    running: root.visible
    property color color: "#8085edff"
    startTime: 5000
    ParticleEmitter3D {
        id: ambientParticleEmitter

        property real multiplier: (root.volume.x / 200.0) * (root.volume.y / 200.0)
                                  * (root.volume.z / 200.0)
        system: root

        particleScale: root.size
        particleScaleVariation: root.size
        particleEndScaleVariation: root.size
        emitRate: 1000 * ambientParticleEmitter.multiplier * root.intensity
        lifeSpanVariation: 100
        enabled: root.visible
        particleEndScale: root.size
        SpriteParticle3D {
            id: ambientParticle
            color: root.color
            blendMode: SpriteParticle3D.Screen
            billboard: true
            sprite: ambientdot
            colorVariation.w: 0.5
            colorVariation.z: 0.25
            colorVariation.y: 0.25
            colorVariation.x: 0.25
            particleScale: 2
            fadeOutDuration: 2500
            fadeInDuration: 2500
            maxAmount: 5000 * ambientParticleEmitter.multiplier * root.intensity

            Texture {
                id: ambientdot
                source: "images/ambientdot.tif"
            }
        }

        Wander3D {
            id: ambientParticleWander
            uniquePaceVariation: 1
            uniquePace.z: 1
            uniquePace.y: 1
            uniquePace.x: 1
            uniqueAmountVariation: 1
            uniqueAmount.z: 1
            uniqueAmount.y: 1
            uniqueAmount.x: 1
            particles: ambientParticle
            system: root
        }

        Attractor3D {
            id: ambientParticleAttractor
            useCachedPositions: false
            hideAtEnd: false
            durationVariation: 5000
            duration: 10000
            positionVariation.z: 500
            positionVariation.y: 500
            positionVariation.x: 500
            particles: ambientParticle
            system: root
        }

        ParticleShape3D {
            id: ambientEmitArea
            extents.x: root.volume.x
            extents.y: root.volume.y
            extents.z: root.volume.z
        }
        lifeSpan: 5000
        particle: ambientParticle
        shape: ambientEmitArea
    }

    Node {
        id: __materialLibrary__
    }
}

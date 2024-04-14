import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(30, 1, 30)
    property real intensity: 1.0
    property real size: 1
    property var timerVar: shockwaveTimer

    running: root.visible
    ParticleEmitter3D {
        id: pressurewaveemitter

        property real multiplier: (root.volume.x) * (root.volume.y) * (root.volume.z)
        enabled: root.visible
        particleScale: 0
        particleEndScaleVariation: 0
        particleEndScale: 1
        emitRate: 0
        lifeSpan: 100
        velocity: shockwaveDirection

        ModelParticle3D {
            id: shockwaveParticle
            sortMode: Particle3D.SortDistance
            fadeOutDuration: 50
            fadeInDuration: 50
        }

        VectorDirection3D {
            id: shockwaveDirection
            direction.y: 0
            directionVariation.x: 0
            directionVariation.z: 0
            directionVariation.y: 0
        }

        Model {
            source: "#Sphere"
            castsReflections: true
            receivesReflections: true
            materials: shockwaveMat
            receivesShadows: true
            scale.y: root.volume.y
            castsShadows: true
            instancing: shockwaveParticle.instanceTable
            scale.z: root.volume.z
            scale.x: root.volume.x
        }

        DynamicBurst3D {
            id: shockwaveBurst
            enabled: true
            duration: 0
            amount: 1
            time: 0
            triggerMode: DynamicBurst3D.TriggerTime
        }

        particle: shockwaveParticle
    }

    Connections {
        target: shockwaveTimer
        onTriggered: root.reset()
    }

    Connections {
        target: shockwaveTimer
        onTriggered: pressurewave1.reset()
    }

    Connections {
        target: shockwaveTimer
        onTriggered: debris.reset()
    }

    Connections {
        target: shockwaveTimer
        onTriggered: debris.startTime = debris.time
    }

    Connections {
        target: shockwaveTimer
        onTriggered: debrisSecondary.reset()
    }

    Connections {
        target: shockwaveTimer
        onTriggered: debrisSecondary.startTime = debrisSecondary.time
    }

    Timer {
        id: shockwaveTimer
        running: root.visible
        repeat: true
        interval: 5000
        triggeredOnStart: true
    }

    ParticleSystem3D {
        id: debris
        visible: true
        ParticleEmitter3D {
            id: debrisEmitter
            emitBursts: debrisBurst
            shape: debrisArea
            particleScaleVariation: 0.5
            particleRotationVelocityVariation.z: 0
            particleRotationVelocityVariation.x: 0
            lifeSpanVariation: 0
            system: debris

            enabled: root.visible
            particle: debrisParticle
            particleScale: 0.5
            particleEndScale: 0
            lifeSpan: 3000
            ModelParticle3D {
                id: debrisParticle
                colorVariation.w: 0
                colorVariation.z: 0
                colorVariation.y: 0
                colorVariation.x: 0
                alignMode: Particle3D.AlignTowardsTarget
                sortMode: Particle3D.SortDistance
                maxAmount: 500000
                fadeInDuration: 1500
                fadeOutDuration: 1500
            }

            Model {
                source: "#Sphere"
                castsReflections: true
                receivesReflections: true
                materials: shockwavedebrisMat
                receivesShadows: true
                scale.y: 1
                castsShadows: true
                instancing: debrisParticle.instanceTable
                scale.z: 5
                scale.x: 3
            }

            Attractor3D {
                id: debrisAttractor
                y: 0
                useCachedPositions: false
                durationVariation: (debris.time - debris.startTime) * 0.5
                hideAtEnd: false
                shape: debrisArea
                particles: debrisParticle
                system: debris
                duration: (debris.time - debris.startTime) * 0.5
            }

            DynamicBurst3D {
                id: debrisBurst
                enabled: true
                duration: 10
                amount: 500
                time: 100
                triggerMode: DynamicBurst3D.TriggerTime
            }

            particleEndScaleVariation: 0
            emitRate: 0
        }

        ParticleShape3D {
            id: debrisArea
            extents.x: (debris.time - debris.startTime) * 0.5
            extents.z: (debris.time - debris.startTime) * 0.5
            extents.y: 0.1
        }
    }

    ParticleSystem3D {
        id: debrisSecondary
        ParticleEmitter3D {
            id: debrisSecondaryEmitter
            system: debrisSecondary

            enabled: root.visible
            particle: debrisSecondaryParticle
            particleScale: 1
            particleScaleVariation: 0.0
            particleRotationVelocityVariation.x: 0
            particleEndScale: 0
            lifeSpan: 3000
            particleRotationVelocityVariation.z: 0
            emitBursts: debrisSecondaryBurst
            ModelParticle3D {
                id: debrisSecondaryParticle
                colorVariation.w: 0
                colorVariation.z: 0
                colorVariation.y: 0
                colorVariation.x: 0
                alignTargetPosition.y: 1
                maxAmount: 500000
                fadeInDuration: 1500
                alignMode: Particle3D.AlignTowardsTarget
                sortMode: Particle3D.SortDistance
                fadeOutDuration: 1500
            }

            Model {
                source: "#Sphere"
                castsReflections: true
                receivesReflections: true
                materials: shockwavedebrisMat
                receivesShadows: true
                scale.y: 1
                castsShadows: true
                instancing: debrisSecondaryParticle.instanceTable
                scale.z: 1
                scale.x: 2
            }

            Attractor3D {
                id: debrisSecondaryAttractor
                y: 0
                system: debrisSecondary
                durationVariation: (debrisSecondary.time - debrisSecondary.startTime) * 0.5
                hideAtEnd: false
                duration: (debrisSecondary.time - debrisSecondary.startTime) * 0.5
                useCachedPositions: false
                particles: debrisSecondaryParticle
                shape: debrisSecondaryArea
            }

            DynamicBurst3D {
                id: debrisSecondaryBurst
                enabled: true
                duration: 10
                amount: 500
                time: 0
                triggerMode: DynamicBurst3D.TriggerTime
            }

            particleEndScaleVariation: 0
            lifeSpanVariation: 3000
            emitRate: 0
            shape: debrisSecondaryArea
        }

        ParticleShape3D {
            id: debrisSecondaryArea
            extents.x: (debrisSecondary.time - debrisSecondary.startTime) * 0.5
            extents.z: (debrisSecondary.time - debrisSecondary.startTime) * 0.5
            extents.y: 0.1
        }
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: shockwaveMat
            fragmentShader: "shaders/shockwave.frag"
            depthDrawMode: Material.NeverDepthDraw
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            cullMode: Material.BackFaceCulling
            property color baseColor: "#ffffff"
            sourceBlend: CustomMaterial.One
            vertexShader: "shaders/shockwave.vert"
            objectName: "Shockwave Material"
        }

        CustomMaterial {
            id: shockwaveMat2
            fragmentShader: "shaders/shockwave.frag"
            depthDrawMode: Material.NeverDepthDraw
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.One
            cullMode: Material.BackFaceCulling
            property color baseColor: "#85e1fc"
            sourceBlend: CustomMaterial.One
            vertexShader: "shaders/shockwave.vert"
            objectName: "Shockwave Material"
        }

        CustomMaterial {
            id: shockwavedebrisMat
            fragmentShader: "shaders/debris.frag"
            depthDrawMode: Material.NeverDepthDraw
            property real brightness: 10
            property TextureInput dfMask: debristexinput
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.One
            cullMode: Material.NoCulling
            property color baseColor: "#3355ff"
            sourceBlend: CustomMaterial.SrcAlpha
            TextureInput {
                id: debristexinput
                enabled: true
                texture: debristex
            }

            Texture {
                id: debristex
                source: "images/debris.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            vertexShader: "shaders/debris.vert"
            objectName: "Debris Material"
        }
    }

    ParticleSystem3D {
        id: pressurewave1
        y: 9
        ParticleEmitter3D {
            particleRotationVariation.y: 90
            particleRotationVelocityVariation.y: 360
            emitBursts: diskburst
            velocity: flatdiskdir
            emitRate: 0
            enabled: root.visible
            particle: flatshockwave
            ModelParticle3D {
                id: flatshockwave
                maxAmount: 100
                fadeOutDuration: 1500
                fadeInDuration: 0
                sortMode: Particle3D.SortDistance
            }

            VectorDirection3D {
                id: flatdiskdir
                direction.y: 1
                directionVariation.z: 1
            }

            Model {
                source: "#Sphere"
                instancing: flatshockwave.instanceTable
                receivesReflections: true
                castsReflections: true
                receivesShadows: true
                materials: shockwaveMat2
                scale.y: 0.05
                castsShadows: true
            }

            DynamicBurst3D {
                id: diskburst
                time: 0
                duration: 0
                enabled: true
                triggerMode: DynamicBurst3D.TriggerTime
                amount: 2
            }
            particleEndScaleVariation: 10
            particleEndScale: 40
            particleScale: 0
            lifeSpan: 1500
        }
    }
}

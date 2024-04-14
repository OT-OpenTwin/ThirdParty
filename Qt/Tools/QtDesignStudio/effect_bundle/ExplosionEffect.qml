import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(50, 50, 50)
    property real intensity: 0.5
    property real size: 1
    property var timerVar: explosionTimer

    ParticleEmitter3D {
        id: explosionFireEmitter
        property real multiplier: (root.volume.x / 50) * (root.volume.y / 50) * (root.volume.z / 50)
        shape: explosionArea
        particleScaleVariation: 0
        enabled: root.visible
        system: root
        velocity: explosionFireDirection
        particleRotationVelocityVariation.y: 90
        particle: explosionFireParticle
        particleScale: 0
        particleRotationVelocityVariation.x: 90
        particleEndScale: 10 * root.intensity * explosionFireEmitter.multiplier
        lifeSpan: 500
        particleRotationVelocityVariation.z: 90
        emitBursts: explosionFireBurst
        ModelParticle3D {
            id: explosionFireParticle
            color: "#ffffff"
            maxAmount: 500 * root.intensity * explosionFireEmitter.multiplier
            fadeInDuration: 500
            fadeOutDuration: 500
        }

        VectorDirection3D {
            id: explosionFireDirection
            directionVariation.x: 25
            directionVariation.z: 25
            directionVariation.y: 25
            direction.y: 0
        }

        Model {
            source: "#Sphere"
            castsReflections: true
            receivesReflections: true
            materials: explosion_fireMat
            receivesShadows: true
            scale.y: 1
            castsShadows: true
            instancing: explosionFireParticle.instanceTable
            scale.z: 1
            scale.x: 1
        }

        DynamicBurst3D {
            id: explosionFireBurst
            enabled: root.visible
            duration: 1
            amount: 50 * root.intensity * explosionFireEmitter.multiplier
            time: 1000
        }

        lifeSpanVariation: lifeSpan
        particleEndScaleVariation: particleEndScale
        emitRate: 0
    }

    ParticleShape3D {
        id: explosionArea
        extents: root.volume
    }

    Timer {
        id: explosionTimer
        running: root.visible
        interval: 10000
        triggeredOnStart: true
        repeat: true
    }

    Connections {
        target: explosionTimer
        onTriggered: explosion_smoke.reset()
    }

    Connections {
        target: explosionTimer
        onTriggered: root.reset()
    }

    Connections {
        target: explosionTimer
        onTriggered: explosion_sparks.reset()
    }

    ParticleSystem3D {
        id: explosion_smoke
        running: true
        ParticleEmitter3D {
            id: explosionSmokeEmitter
            shape: explosionArea
            enabled: root.visible
            lifeSpanVariation: lifeSpan
            particleRotationVelocityVariation.z: 45
            particleRotationVelocityVariation.y: 45
            particleRotationVelocityVariation.x: 45
            system: explosion_smoke
            velocity: explosionSmokeDirection
            particle: explosionSmokeParticle
            particleScale: 0
            particleEndScale: 15 * root.intensity * explosionFireEmitter.multiplier
            lifeSpan: 5000
            emitBursts: explosionSmokeBurst
            ModelParticle3D {
                id: explosionSmokeParticle
                color: "#33ffffff"
                maxAmount: 200 * root.intensity * explosionFireEmitter.multiplier
                fadeInDuration: 100
                fadeOutDuration: 4900
            }

            VectorDirection3D {
                id: explosionSmokeDirection
                directionVariation.x: 100
                directionVariation.z: 100
                directionVariation.y: 100
                direction.y: 0
            }

            Model {
                source: "#Sphere"
                castsReflections: true
                receivesReflections: true
                materials: explosion_smokeMat
                receivesShadows: true
                scale.y: 1
                castsShadows: true
                instancing: explosionSmokeParticle.instanceTable
                scale.z: 1
                scale.x: 1
            }

            DynamicBurst3D {
                id: explosionSmokeBurst
                time: 1250
                enabled: root.visible
                amount: 20 * root.intensity * explosionFireEmitter.multiplier
                duration: 1000
            }

            particleEndScaleVariation: particleEndScale
            emitRate: 0
        }
    }

    ParticleSystem3D {
        id: explosion_sparks
        visible: true
        ParticleEmitter3D {
            id: explosionSparkEmitter
            shape: explosionArea
            system: explosion_sparks
            velocity: explosionSparkDirection
            enabled: root.visible
            particleRotationVelocityVariation.y: 90
            particle: explosionSparkParticle
            particleScale: 0.1
            particleRotationVelocityVariation.x: 90
            particleScaleVariation: particleScale
            particleEndScale: 0.5
            lifeSpan: 3000
            particleRotationVelocityVariation.z: 90
            emitBursts: explosionSparkBurst
            ModelParticle3D {
                id: explosionSparkParticle
                color: "#ffffff"
                maxAmount: 1000 * root.intensity * explosionFireEmitter.multiplier
                fadeInDuration: 500
                fadeOutDuration: 500
            }

            VectorDirection3D {
                id: explosionSparkDirection
                directionVariation.x: 200
                directionVariation.z: 200
                direction.y: 0
                directionVariation.y: 200
            }

            Model {
                source: "#Sphere"
                castsReflections: true
                receivesReflections: true
                materials: explosion_sparkMat
                scale.y: 1
                receivesShadows: true
                castsShadows: true
                instancing: explosionSparkParticle.instanceTable
                scale.z: 1
                scale.x: 1
            }

            DynamicBurst3D {
                id: explosionSparkBurst
                enabled: root.visible
                duration: 100
                amount: 100 * root.intensity * explosionFireEmitter.multiplier
                time: 1000
            }

            Gravity3D {
                id: explosionSparkGravity
                particles: explosionSparkParticle
                system: explosion_sparks
            }
            lifeSpanVariation: lifeSpan
            particleEndScaleVariation: particleEndScale
            emitRate: 0
        }
        running: true
    }

    ParticleSystem3D {
        id: explosion_flash
        visible: true
        ParticleEmitter3D {
            id: explosionFlashEmitter
            enabled: root.visible
            system: explosion_flash
            particle: explosionFlashParticle
            particleScale: 0
            particleEndScale: 30 * explosionFireEmitter.multiplier * root.intensity
            lifeSpan: 250
            emitBursts: explosionFlashBurst
            ModelParticle3D {
                id: explosionFlashParticle
                maxAmount: 100
                fadeInDuration: explosionFlashEmitter.lifeSpan / 4
                fadeOutDuration: explosionFlashParticle.fadeInDuration * 3
            }

            Model {
                source: "#Sphere"
                materials: explosion_flashMat
                instancing: explosionFlashParticle.instanceTable
            }

            DynamicBurst3D {
                id: explosionFlashBurst
                time: 500
                enabled: root.visible
                duration: 100 * explosionFireEmitter.multiplier * root.intensity
                amount: 1
            }
            emitRate: 0
        }
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: explosion_flashMat
            fragmentShader: "shaders/flash.frag"
            depthDrawMode: Material.NeverDepthDraw
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.One
            property color baseColor: "#ffaa11"
            property real opacity: 1.0
            cullMode: Material.NoCulling
            sourceBlend: CustomMaterial.One
            vertexShader: "shaders/flash.vert"
            objectName: "Flash Material"
        }

        CustomMaterial {
            id: explosion_smokeMat
            fragmentShader: "shaders/smoke.frag"
            depthDrawMode: Material.NeverDepthDraw
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            cullMode: Material.BackFaceCulling
            property color baseColor: "#222222"
            property color sssColor: "#222222"
            property real roughness: 0.5
            property real opacity: 1.0
            property real density: 0.5
            property real metalness: 0.0
            sourceBlend: CustomMaterial.SrcAlpha

            property TextureInput dfMask: smoketexinput1
            TextureInput {
                id: smoketexinput1
                enabled: true
                texture: smoketex1
            }

            Texture {
                id: smoketex1
                source: "images/smoke.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            vertexShader: "shaders/smoke.vert"
            objectName: "Smoke Material"
        }

        CustomMaterial {
            id: explosion_fireMat
            fragmentShader: "shaders/fire.frag"
            depthDrawMode: Material.NeverDepthDraw
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            cullMode: Material.BackFaceCulling
            property TextureInput dfMask: firetexinput1
            property color baseColor: "#d99a60"
            property real opacity: 1.0
            sourceBlend: CustomMaterial.SrcColor
            TextureInput {
                id: firetexinput1
                enabled: true
                texture: firetex1
            }

            Texture {
                id: firetex1
                source: "images/fire.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            vertexShader: "shaders/fire.vert"
            objectName: "Fire Material"
        }

        CustomMaterial {
            id: explosion_sparkMat
            cullMode: Material.NoCulling
            property color baseColor: "#e5b16d"
            property real brightness: 10
            property real opacity: 1.0
            property TextureInput dfMask: sparktexinput
            depthDrawMode: Material.NeverDepthDraw
            objectName: "New Material"
            sourceBlend: CustomMaterial.SrcAlpha
            destinationBlend: CustomMaterial.One
            TextureInput {
                id: sparktexinput
                texture: sparktex
                enabled: true
            }

            Texture {
                id: sparktex
                source: "images/spark.png"
                mipFilter: Texture.Linear
                generateMipmaps: true
            }
            vertexShader: "shaders/spark.vert"
            fragmentShader: "shaders/spark.frag"
            shadingMode: CustomMaterial.Shaded
        }
    }
}

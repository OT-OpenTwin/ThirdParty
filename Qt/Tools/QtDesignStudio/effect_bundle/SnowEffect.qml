import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(500, 200, 500)
    property real intensity: 0.5
    property real size: 1.0
    running: root.visible

    property color color: "#ffffff"
    time: 0
    startTime: 15000

    ParticleEmitter3D {
        property real multiplier: (root.volume.x / 350) * (root.volume.y / 350)
                                  * (root.volume.z / 350)
        id: snowEmitter

        enabled: root.visible
        y: root.volume.y
        velocity: snowDirection
        particleScale: 0.3 * root.size
        z: 0.00002
        particleEndScaleVariation: 0.3 * root.size
        lifeSpan: 5000 * (root.volume.y / 100)
        particleScaleVariation: 0.3 * root.size
        particleRotationVariation.y: 360
        shape: snowEmitArea
        particleRotationVariation.x: 360
        emitRate: 1000 * root.intensity * snowEmitter.multiplier
        particleRotationVelocityVariation.y: 90
        system: root
        particleRotationVelocityVariation.z: 90
        particleEndScale: 0.3 * root.size
        particleRotationVariation.z: 360
        particleRotationVelocityVariation.x: 90
        particle: snowParticle
        ModelParticle3D {
            id: snowParticle
            color: root.color
            fadeOutEffect: Particle3D.FadeNone
            fadeInEffect: Particle3D.FadeNone
            colorVariation.z: 1
            sortMode: Particle3D.SortDistance
            unifiedColorVariation: false
            maxAmount: 10000 * root.intensity * snowEmitter.multiplier * (root.volume.y / 200)
            fadeInDuration: 500
            colorVariation.x: 1
            colorVariation.y: 1
            hasTransparency: true
            fadeOutDuration: 500
        }

        ParticleShape3D {
            id: snowEmitArea
            extents.x: root.volume.x
            extents.y: 1
            extents.z: root.volume.z
        }

        Model {
            source: "#Cube"
            castsReflections: true
            castsShadows: true
            instancing: snowParticle.instanceTable
            receivesShadows: true
            materials: snowMat
            receivesReflections: true
        }

        Wander3D {
            id: snowWander
            globalPaceStart.y: 0
            globalPace.y: 0
            uniqueAmountVariation: 1
            uniquePaceVariation: 1
            uniquePace.z: 0.3
            uniquePace.y: 0
            uniquePace.x: 0.3
            uniqueAmount.z: 10
            uniqueAmount.x: 10
            globalPaceStart.z: 0.3
            globalPaceStart.x: 0.3
            globalPace.z: 0
            globalPace.x: 0
            globalAmount.z: 0
            globalAmount.x: 0
            particles: snowParticle
            system: root
        }

        VectorDirection3D {
            id: snowDirection
            direction.y: -50
        }
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: snowMat
            cullMode: Material.BackFaceCulling
            property color baseColor: root.color
            property real opacity: root.opacity
            property TextureInput dfMask: dfMask_snow
            TextureInput {
                id: dfMask_snow
                texture: dfMask_snowtex
                enabled: true
            }

            Texture {
                id: dfMask_snowtex
                source: "images/snowflake_DF_multi.tga"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            fragmentShader: "shaders/snow.frag"
            sourceBlend: CustomMaterial.SrcAlpha
            shadingMode: CustomMaterial.Shaded
            vertexShader: "shaders/snow.vert"
            depthDrawMode: Material.NeverDepthDraw
            objectName: "Snow Material"
        }
    }
}

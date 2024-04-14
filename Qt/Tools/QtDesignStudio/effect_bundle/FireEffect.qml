import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(20, 20, 20)
    property real intensity: 0.5
    property real size: 0.5

    property color color: "#db9b60"
    running: root.visible

    ParticleEmitter3D {
        id: fireEmitter
        property real multiplier: (root.volume.x / 10) * (root.volume.y / 10)
                                  * (root.volume.z / 10) * root.intensity
        x: 0
        particleScale: 20 * root.size

        enabled: root.visible
        emitRate: 10 * root.intensity * fireEmitter.multiplier
        particleRotation.x: 0
        particleRotationVariation.x: 360
        lifeSpanVariation: 0
        particleRotationVariation.z: 360
        system: root
        particleEndScaleVariation: 20 * root.size
        particleRotationVelocityVariation.y: 90
        particleEndScale: 20 * root.size
        particleRotationVelocityVariation.z: 90
        ModelParticle3D {
            id: fireParticle
            color: "#ffffff"
            unifiedColorVariation: false
            fadeInDuration: 1250
            hasTransparency: true
            colorVariation.z: 1
            sortMode: Particle3D.SortDistance
            fadeOutDuration: 250
            colorVariation.y: 1
            alignMode: Particle3D.AlignNone
            maxAmount: 100 * root.intensity * fireEmitter.multiplier
            colorVariation.x: 1
            colorVariation.w: 1
        }

        ParticleShape3D {
            id: fireArea
            extents: root.volume
        }
        particle: fireParticle
        particleRotation.y: 360
        particleScaleVariation: 20 * root.size
        particleRotationVelocity.y: 0
        particleRotationVelocityVariation.x: 90
        shape: fireArea
        lifeSpan: 1500
        particleRotationVariation.y: 360
        particleRotationVelocity.x: 0
        particleRotationVelocity.z: 0
        particleRotation.z: 360
    }

    Gravity3D {
        id: fireGravity
        particles: fireParticle
        system: root
        magnitude: 300
        direction.y: 1
    }

    Model {
        source: "#Sphere"
        castsReflections: true
        castsShadows: true
        receivesShadows: true
        scale.z: 0.1
        instancing: fireParticle.instanceTable
        materials: fireMat
        scale.y: 0.1
        scale.x: 0.1
        receivesReflections: true
    }

    Wander3D {
        id: fireWander
        uniqueAmount.x: 10
        uniquePace.x: 0.1
        globalPaceStart.z: 0.1
        globalAmount.z: 5
        system: root
        uniquePaceVariation: 1
        globalPace.y: 0.1
        uniquePace.y: 0.1
        particles: fireParticle
        uniquePace.z: 0.1
        globalPaceStart.y: 0.1
        uniqueAmount.z: 10
        globalPaceStart.x: 0.1
        globalPace.x: 0.1
        uniqueAmountVariation: 1
        globalAmount.x: 5
        globalPace.z: 0.1
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: fireMat
            cullMode: Material.BackFaceCulling
            property color baseColor: root.color
            property real opacity: root.opacity
            property TextureInput dfMask: firetexinput
            depthDrawMode: Material.NeverDepthDraw
            objectName: "Fire Material"
            sourceBlend: CustomMaterial.SrcColor
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            TextureInput {
                id: firetexinput
                texture: firetex
                enabled: true
            }

            Texture {
                id: firetex
                source: "images/fire.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            vertexShader: "shaders/fire.vert"
            fragmentShader: "shaders/fire.frag"
            shadingMode: CustomMaterial.Shaded
        }
    }
}

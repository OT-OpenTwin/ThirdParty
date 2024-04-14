import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(20, 20, 20)
    property real intensity: 0.5
    property real size: 0.5

    property color color: "#808080"

    running: root.visible
    ParticleEmitter3D {
        id: smokeEmitter

        property real multiplier: (root.volume.x / 10) * (root.volume.y / 10)
                                  * (root.volume.z / 10) * root.intensity
        enabled: root.visible
        particleScale: 20 * root.size
        particleScaleVariation: 10 * root.size
        particleRotationVelocity.z: 30
        particleRotationVelocity.y: 30
        particleRotationVelocity.x: 30
        particleRotation.z: 360
        particleRotation.y: 360
        particleRotation.x: 360
        particleEndScaleVariation: 10 * root.size
        lifeSpan: 6000
        particleRotationVariation.y: 360
        shape: smokeArea
        particleRotationVariation.x: 360
        emitRate: 10 * root.intensity * smokeEmitter.multiplier
        particleRotationVelocityVariation.y: 30
        system: root
        particleRotationVelocityVariation.z: 30
        particleEndScale: 20 * root.size
        particleRotationVariation.z: 360
        particleRotationVelocityVariation.x: 30
        particle: smokeParticle
        ModelParticle3D {
            id: smokeParticle
            color: root.color
            sortMode: Particle3D.SortDistance
            colorVariation.w: 1
            unifiedColorVariation: false
            maxAmount: 100 * root.intensity * smokeEmitter.multiplier
            fadeInDuration: 2000
            alignMode: Particle3D.AlignNone
            hasTransparency: true
            fadeOutDuration: 2000
        }

        ParticleShape3D {
            id: smokeArea
            extents: root.volume
        }
        lifeSpanVariation: 0
    }

    Gravity3D {
        id: smokeGravity
        particles: smokeParticle
        system: root
        magnitude: 20
        direction.y: 1
    }

    Model {
        source: "#Sphere"
        castsReflections: true
        scale.x: .1
        castsShadows: true
        instancing: smokeParticle.instanceTable
        scale.y: .1
        receivesShadows: false
        materials: smokeMat
        scale.z: .1
        receivesReflections: true
    }

    Wander3D {
        id: smokeWander
        uniqueAmount.z: 10
        globalPace.x: 0.1
        globalPace.y: 0.1
        uniqueAmount.x: 10
        uniquePaceVariation: 1
        globalAmount.x: 5
        uniquePace.x: 0.1
        globalPace.z: 0.1
        uniqueAmountVariation: 1
        globalPaceStart.x: 0.1
        globalAmount.z: 5
        system: root
        globalPaceStart.y: 0.1
        particles: smokeParticle
        uniquePace.z: 0.1
        uniquePace.y: 0.1
        globalPaceStart.z: 0.1
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: smokeMat
            TextureInput {
                id: smoketexinput
                enabled: true
                texture: smoketex
            }

            Texture {
                id: smoketex
                source: "images/smoke.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            cullMode: Material.BackFaceCulling

            property real specular: 0
            property real density: 0.0
            property real roughness: 1
            property real clearcoat: 1
            property real metalness: 0.0
            property real sssDistortion: 0.1
            property real sssPower: 1
            property real sssScale: 3
            property color baseColor: root.color
            property real opacity: root.opacity
            property color sssColor: "#737d80"
            property TextureInput dfMask: smoketexinput
            alwaysDirty: false
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            fragmentShader: "shaders/smoke.frag"
            sourceBlend: CustomMaterial.SrcAlpha
            vertexShader: "shaders/smoke.vert"
            shadingMode: CustomMaterial.Shaded
            depthDrawMode: Material.NeverDepthDraw
            objectName: "Smoke Material"
        }
    }
    staticFlags: 0
}

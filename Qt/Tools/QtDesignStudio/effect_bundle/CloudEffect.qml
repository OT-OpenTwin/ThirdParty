import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(100, 25, 50)
    property real intensity: 0.5
    property color color: "#ffffff"
    property real turbulence: 0.5
    running: root.visible
    time: 15000
    startTime: 15000
    ParticleEmitter3D {
        id: cloudEmitter
        property real multiplier: (root.volume.x / 100) * (root.volume.y / 100)
                                  * (root.volume.z / 100)
        particleScale: 20
        velocity: cloudDirection
        particle: cloudParticle
        enabled: root.visible
        particleRotationVariation.x: 360
        particleRotationVelocityVariation.x: root.turbulence * 20.0
        lifeSpan: 25000
        ModelParticle3D {
            id: cloudParticle
            color: "#ffffff"
            sortMode: Particle3D.SortDistance
            alignMode: Particle3D.AlignNone
            maxAmount: 1000 * root.intensity * cloudEmitter.multiplier
            fadeInDuration: 12500
            hasTransparency: true
            unifiedColorVariation: false
            fadeOutDuration: 12500
        }

        ParticleShape3D {
            id: cloudArea
            extents: root.volume
        }
        particleRotationVelocity.z: 0
        particleRotation.y: 0
        particleEndScaleVariation: 0
        shape: cloudArea
        system: root
        particleRotationVelocity.x: 0
        particleRotationVelocityVariation.y: root.turbulence * 20.0
        particleScaleVariation: 10
        particleRotationVariation.y: 360
        particleEndScale: 20
        z: -5.27116
        particleRotationVelocity.y: 0
        particleRotationVelocityVariation.z: root.turbulence * 20.0
        particleRotation.x: 0
        lifeSpanVariation: 0
        emitRate: 10 * root.intensity * cloudEmitter.multiplier
        particleRotationVariation.z: 360
    }

    Model {
        source: "#Sphere"
        castsReflections: true
        receivesReflections: true
        materials: cloudMat
        scale.y: 0.1
        receivesShadows: true
        castsShadows: true
        instancing: cloudParticle.instanceTable
        scale.z: 0.1
        scale.x: 0.1
    }

    Wander3D {
        id: cloudWander
        uniqueAmount.y: 1
        globalPace.x: 0.1
        uniqueAmountVariation: 1
        uniqueAmount.z: 1
        globalPaceStart.z: 0.1
        uniquePaceVariation: 1
        particles: cloudParticle
        globalAmount.z: 0
        uniquePace.z: 0.1
        globalPace.y: 0.1
        globalAmount.x: 0
        system: root
        uniqueAmount.x: 1
        globalPaceStart.y: 0.1
        globalPaceStart.x: 0.1
        globalPace.z: 0.1
        uniquePace.y: 0.1
        uniquePace.x: 0.1
    }

    VectorDirection3D {
        id: cloudDirection
        directionVariation.z: 1
        directionVariation.y: 1
        directionVariation.x: 5
        direction.y: 0
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: cloudMat
            TextureInput {
                id: cloudtexinput
                enabled: true
                texture: cloudtex
            }

            Texture {
                id: cloudtex
                source: "images/cloud.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            cullMode: Material.BackFaceCulling

            property real specular: 0
            property real density: 0.0
            property real opacity: root.opacity
            property real roughness: 1
            property real clearcoat: 1
            property real metalness: 0.0
            property real sssDistortion: 0.1
            property real sssPower: 1
            property real sssScale: 3
            property color baseColor: root.color
            property color sssColor: "#e5f9ff"
            property TextureInput dfMask: cloudtexinput
            alwaysDirty: false
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            fragmentShader: "shaders/cloud.frag"
            sourceBlend: CustomMaterial.SrcAlpha
            vertexShader: "shaders/cloud.vert"
            shadingMode: CustomMaterial.Shaded
            depthDrawMode: Material.NeverDepthDraw
            objectName: "Cloud Material"
        }
    }
    staticFlags: 0
}

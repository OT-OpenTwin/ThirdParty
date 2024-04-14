import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(500, 500, 500)
    property real intensity: 0.5
    property color color: "#40ffffff"
    running: root.visible
    startTime: 3000
    ParticleEmitter3D {
        id: dustpointEmitter

        property real multiplier: (root.volume.x / 500.0) * (root.volume.y / 500.0)
                                  * (root.volume.z / 500.0)
        enabled: root.visible
        emitRate: 2000 * root.intensity * dustpointEmitter.multiplier
        velocity: dustpointDirection
        particleRotationVariation.z: 360
        lifeSpanVariation: 6000
        particleRotationVariation.x: 360
        particleRotation.x: 0
        system: root
        particleEndScale: 0.1
        particleRotationVelocityVariation.y: 5
        particleEndScaleVariation: 0.1
        particleScale: 0.1
        particleRotationVelocityVariation.z: 5
        ModelParticle3D {
            id: dustParticle
            color: "#40ffffff"
            unifiedColorVariation: false
            fadeInDuration: 3000
            hasTransparency: true
            sortMode: Particle3D.SortDistance
            fadeOutDuration: 3000
            alignMode: Particle3D.AlignNone
            maxAmount: 600000 * root.intensity * dustpointEmitter.multiplier
            colorVariation.w: 0.25
        }

        ParticleShape3D {
            id: dustArea
            extents: root.volume
        }
        particle: dustParticle
        particleRotation.y: 0
        particleRotationVelocityVariation.x: 5
        particleRotationVelocity.y: 0
        particleScaleVariation: 0.1
        shape: dustArea
        lifeSpan: 6000
        particleRotationVariation.y: 360
        particleRotationVelocity.x: 0
        particleRotationVelocity.z: 0
        particleRotation.z: 0
    }

    ParticleEmitter3D {
        id: dustcloudEmitter

        enabled: root.visible
        velocity: dustCloudDirection
        particleScale: 5
        emitRate: 20 * root.intensity * dustpointEmitter.multiplier
        particleRotation.x: 0
        particleRotationVariation.x: 360
        lifeSpanVariation: 6000
        particleRotationVariation.z: 360
        system: root
        particleEndScaleVariation: 2.5
        particleRotationVelocityVariation.y: 10
        particleEndScale: 5
        particleRotationVelocityVariation.z: 10
        ModelParticle3D {
            id: dustCloudParticle
            color: "#ffffff"
            unifiedColorVariation: false
            fadeInDuration: 6000
            hasTransparency: true
            sortMode: Particle3D.SortDistance
            fadeOutDuration: 6000
            alignMode: Particle3D.AlignNone
            maxAmount: 1500 * root.intensity * dustpointEmitter.multiplier
            colorVariation.w: 1
        }
        particle: dustCloudParticle
        particleScaleVariation: 2.5
        particleRotationVelocityVariation.x: 10
        shape: dustArea
        lifeSpan: 6000
        particleRotationVariation.y: 360
    }

    Gravity3D {
        id: dustGravity
        magnitude: 1
        direction.y: -1
    }

    Model {
        source: "#Sphere"
        instancing: dustCloudParticle.instanceTable
        materials: dustMat
    }

    Wander3D {
        id: dustWander
        uniqueAmount.y: 0
        uniqueAmount.x: 0
        uniquePace.x: 100
        globalPaceStart.z: 0.1
        globalAmount.z: 5
        system: root
        uniquePaceVariation: 1
        globalPace.y: 0.1
        uniquePace.y: 100
        particles: dustCloudParticle
        uniquePace.z: 100
        globalPaceStart.y: 0.1
        uniqueAmount.z: 0
        globalPaceStart.x: 0.1
        globalPace.x: 0.1
        uniqueAmountVariation: 1
        globalAmount.x: 5
        globalPace.z: 0.1
    }

    VectorDirection3D {
        id: dustCloudDirection
        directionVariation.x: 10
        directionVariation.y: 10
        direction.y: 0
        directionVariation.z: 10
    }

    Model {
        id: dustpoint
        source: "#Sphere"
        receivesShadows: false
        castsShadows: false
        scale.z: 0.1
        instancing: dustParticle.instanceTable
        materials: dustMat
        scale.y: 0.1
        receivesReflections: false
        scale.x: 0.1
    }

    VectorDirection3D {
        id: dustpointDirection
        directionVariation.x: 10
        directionVariation.y: 10
        directionVariation.z: 10
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: dustMat
            cullMode: Material.BackFaceCulling
            property color baseColor: root.color
            property real opacity: root.opacity
            property TextureInput dfMask: dusttexinput
            depthDrawMode: Material.NeverDepthDraw
            objectName: "New Material"
            sourceBlend: CustomMaterial.SrcAlpha
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            TextureInput {
                id: dusttexinput
                texture: dusttex
                enabled: true
            }

            Texture {
                id: dusttex
                source: "images/dust.png"
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
            vertexShader: "shaders/dustcloud.vert"
            fragmentShader: "shaders/dustcloud.frag"
            shadingMode: CustomMaterial.Shaded
        }
    }
}

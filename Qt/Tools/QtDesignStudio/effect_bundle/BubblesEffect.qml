import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(10, 10, 10)
    property real intensity: 0.5
    property real size: 1
    property color color: "#ffffff"
    property real turbulence: 1
    running: root.visible
    ParticleEmitter3D {
        id: bubbleEmitter
        property real multiplier: (root.volume.x / 15) * (root.volume.y / 15) * (root.volume.z / 15)
        x: -0
        particleRotation.z: 0
        enabled: root.visible
        velocity: bubbleDirection
        particle: bubbleParticle
        particleRotationVariation.x: 0
        particleRotationVelocityVariation.x: 0
        lifeSpan: 5000
        ModelParticle3D {
            id: bubbleParticle
            color: "#ffffff"
            sortMode: Particle3D.SortDistance
            alignMode: Particle3D.AlignTowardsStartVelocity
            colorVariation.w: 0.25
            colorVariation.y: 0.25
            colorVariation.x: 0.25
            maxAmount: 10000 * root.intensity * bubbleEmitter.multiplier
            fadeInDuration: 0
            hasTransparency: true
            unifiedColorVariation: false
            colorVariation.z: 0
            fadeOutDuration: 0
        }

        ParticleShape3D {
            id: bubbleEmitArea
            extents: root.volume
        }
        particleRotationVelocity.z: 0
        particleRotation.y: 0
        particleEndScaleVariation: 0.25 * root.size
        shape: bubbleEmitArea
        system: root
        particleRotationVelocity.x: 0
        particleRotationVelocityVariation.y: 0
        particleScale: 0.25 * root.size
        particleScaleVariation: 0.25 * root.size
        particleRotationVariation.y: 0
        particleEndScale: 0.25 * root.size
        particleRotationVelocity.y: 0
        particleRotationVelocityVariation.z: 0
        particleRotation.x: 0
        lifeSpanVariation: 5000
        emitRate: 100 * root.intensity * bubbleEmitter.multiplier
        particleRotationVariation.z: 0
    }

    Gravity3D {
        id: bubbleGravity
        magnitude: 9.8
        direction.y: -1
    }

    Model {
        source: "#Sphere"
        castsReflections: true
        receivesReflections: true
        materials: bubbleMat
        receivesShadows: true
        scale.y: 1
        castsShadows: true
        instancing: bubbleParticle.instanceTable
        scale.z: 1
        scale.x: 1
    }

    Wander3D {
        id: wander5
        uniqueAmount.y: root.turbulence
        globalAmount.y: 0
        globalPace.x: 0
        uniqueAmountVariation: root.turbulence * 10
        globalPaceStart.z: 0
        uniqueAmount.z: root.turbulence
        uniquePaceVariation: root.turbulence * 10
        particles: [bubbleParticle]
        globalAmount.z: 0
        uniquePace.z: root.turbulence
        globalPace.y: 0
        globalAmount.x: 0
        system: root
        uniqueAmount.x: root.turbulence
        globalPaceStart.y: 0
        globalPaceStart.x: 0
        globalPace.z: 0
        uniquePace.y: root.turbulence
        uniquePace.x: root.turbulence
    }

    VectorDirection3D {
        id: bubbleDirection
        direction.z: 0
        directionVariation.x: 50
        directionVariation.z: 50
        directionVariation.y: 100
        direction.y: 100
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: bubbleMat
            fragmentShader: "shaders/bubble.frag"
            objectName: "New Material"
            sourceBlend: CustomMaterial.SrcAlpha
            depthDrawMode: Material.NeverDepthDraw
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            property color baseColor: root.color
            property real opacity: root.opacity
            vertexShader: "shaders/bubble.vert"
            shadingMode: CustomMaterial.Shaded
            cullMode: Material.BackFaceCulling
        }
    }
}

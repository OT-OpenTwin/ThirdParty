import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(100, 1, 100)
    property real intensity: 0.5
    property color color: "#ffffff"
    startTime: 5000
    running: root.visible
    ParticleEmitter3D {
        enabled: root.visible
        property real multiplier: (root.volume.x / 50.0) * (root.volume.y / 50)
                                  * (root.volume.z / 50.0) * root.intensity
        id: heatwaveEmitter
        particleEndScaleVariation: 0
        system: root
        particleEndScale: 1
        particle: heatwaveParticle
        emitRate: 100 * root.intensity * heatwaveEmitter.multiplier
        lifeSpan: 5000
        lifeSpanVariation: 0
        particleRotationVariation.x: 0
        particleRotationVelocityVariation.x: 0
        particleRotationVelocityVariation.z: 0
        particleRotationVelocityVariation.y: 0
        shape: heatwaveArea
        particleRotationVariation.z: 0
        particleRotationVariation.y: 360

        ModelParticle3D {
            id: heatwaveParticle
            maxAmount: 1000 * root.intensity * heatwaveEmitter.multiplier
            color: "#ffffff"
            fadeInDuration: 2000
            fadeOutDuration: 2000
            unifiedColorVariation: true
            hasTransparency: true
            sortMode: Particle3D.SortDistance
            colorVariation.w: 0
            colorVariation.z: 0
            colorVariation.y: 0
            colorVariation.x: 0
        }

        ParticleShape3D {
            id: heatwaveArea
            extents: root.volume
        }
    }

    Gravity3D {
        id: heatwaveGravity
        particles: heatwaveParticle
        system: root
        magnitude: 20
        direction.y: 1
    }

    Model {
        source: "#Sphere"
        castsReflections: true
        receivesReflections: true
        receivesShadows: true
        castsShadows: true
        materials: heatwaveMat
        scale.z: 1
        scale.y: 1
        scale.x: 1
        instancing: heatwaveParticle.instanceTable
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: heatwaveMat
            cullMode: Material.BackFaceCulling
            property color baseColor: root.color
            property real opacity: root.opacity
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            fragmentShader: "shaders/heatwave.frag"
            sourceBlend: CustomMaterial.SrcAlpha
            shadingMode: CustomMaterial.Shaded
            vertexShader: "shaders/heatwave.vert"
            depthDrawMode: Material.NeverDepthDraw
            objectName: "New Material"
        }
    }
}

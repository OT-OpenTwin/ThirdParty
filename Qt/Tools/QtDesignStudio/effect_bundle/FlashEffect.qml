import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(30, 30, 30)
    property color color: "#ffffff"
    running: root.visible
    ParticleEmitter3D {
        id: flashEmitter
        velocity: flashDirection
        particle: flashParticle
        particleScale: 0
        particleEndScale: 1

        enabled: root.visible
        lifeSpan: 1000
        emitBursts: flashBurst
        ModelParticle3D {
            id: flashParticle
            sortMode: Particle3D.SortDistance
            fadeInDuration: flashEmitter.lifeSpan / 4
            fadeOutDuration: flashParticle.fadeInDuration * 3
        }

        VectorDirection3D {
            id: flashDirection
            directionVariation.x: 0
            directionVariation.z: 0
            direction.y: 0
            directionVariation.y: 0
        }

        EmitBurst3D {
            id: flashBurst
            duration: 100
            amount: 1
            time: 0
        }

        Model {
            source: "#Sphere"
            materials: flashMat
            scale.y: root.volume.y
            instancing: flashParticle.instanceTable
            scale.z: root.volume.z
            scale.x: root.volume.x
        }
        emitRate: 1
        particleEndScaleVariation: 0
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: flashMat
            fragmentShader: "shaders/flash.frag"
            depthDrawMode: Material.NeverDepthDraw
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.One
            cullMode: Material.NoCulling
            property color baseColor: root.color
            property real opacity: root.opacity
            sourceBlend: CustomMaterial.One
            vertexShader: "shaders/flash.vert"
            objectName: "Flash Material"
        }
    }
}

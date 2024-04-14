import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property vector3d volume: Qt.vector3d(500, 500, 500)
    property real intensity: 0.5
    property real size: 1.0

    property color color: "#ffffff"
    startTime: 3000

    running: root.visible
    ParticleEmitter3D {

        property real multiplier: (root.volume.x / 500.0) * (root.volume.y / 500.0)
                                  * (root.volume.z / 500.0)
        enabled: root.visible
        id: rainEmitter
        y: root.volume.y
        velocity: rainDirection
        particleScale: root.size
        particleScaleVariation: root.size
        particleEndScale: root.size
        system: root
        ModelParticle3D {
            id: rainParticle
            color: "#ffffff"
            alignMode: Particle3D.AlignNone
            maxAmount: 5000 * root.intensity * rainEmitter.multiplier
            hasTransparency: true
            fadeOutDuration: 100
            unifiedColorVariation: true
            sortMode: Particle3D.SortDistance
            fadeInDuration: 500 //rain.life / 3
        }

        ParticleShape3D {
            id: rainArea
            extents.x: root.volume.x
            extents.z: root.volume.z
            extents.y: 1
        }

        VectorDirection3D {
            id: rainDirection
            direction.y: -890
        }
        shape: rainArea
        particleRotationVariation.y: 360
        particle: rainParticle
        emitRate: 500 * root.intensity * rainEmitter.multiplier
        lifeSpan: 1.5 * root.volume.y
        particleEndScaleVariation: root.size
    }

    Model {
        source: "#Cube"
        castsReflections: true
        receivesShadows: true
        materials: rainMat
        instancing: rainParticle.instanceTable
        castsShadows: true
        receivesReflections: true
    }

    ParticleSystem3D {
        id: ripples
        y: 0
        ParticleEmitter3D {
            id: rippleEmitter
            lifeSpanVariation: 250

            enabled: root.visible
            particleScale: 0
            lifeSpan: 250
            system: ripples
            ModelParticle3D {
                id: rippleParticle
                color: root.color
                alignMode: Particle3D.AlignNone
                maxAmount: 5000 * root.intensity * rainEmitter.multiplier
                colorVariation.y: 0
                sortMode: Particle3D.SortDistance
                fadeInDuration: 20
                fadeOutDuration: 80
                unifiedColorVariation: true
                colorVariation.w: 0
                hasTransparency: true
                colorVariation.x: 0
                colorVariation.z: 0
            }

            ParticleShape3D {
                id: rippleArea
                extents.x: root.volume.x
                extents.z: root.volume.z
                extents.y: 0.1
            }
            particle: rippleParticle
            particleRotationVelocityVariation.y: 0
            particleScaleVariation: 0
            particleRotationVelocityVariation.z: 0
            shape: rippleArea
            particleEndScale: 0.25 * root.size
            emitRate: 5000 * root.intensity * rainEmitter.multiplier
            particleRotationVariation.x: 360
            particleRotationVariation.z: 360
            particleEndScaleVariation: 0.25 * root.size
            particleRotationVelocityVariation.x: 0
            particleRotationVariation.y: 360
        }

        Model {
            source: "#Sphere"
            castsReflections: true
            scale.x: 1
            scale.y: 1
            instancing: rippleParticle.instanceTable
            materials: splashMat
            receivesReflections: true
            castsShadows: true
            scale.z: 1
            receivesShadows: true
        }
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: rainMat
            fragmentShader: "shaders/raindrop.frag"
            objectName: "New Material"
            property color baseColor: root.color
            property real opacity: root.opacity
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            sourceBlend: CustomMaterial.SrcAlpha
            vertexShader: "shaders/raindrop.vert"
            depthDrawMode: Material.NeverDepthDraw
            cullMode: Material.BackFaceCulling
            property TextureInput rainmap: texture_rain
            TextureInput {
                id: texture_rain
                texture: raintex
                enabled: true
            }

            Texture {
                id: raintex
                source: "images/raindrops_multi.tga"
                scaleV: 3
                scaleU: 3
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
        }

        CustomMaterial {
            id: splashMat
            fragmentShader: "shaders/rainsplash.frag"
            objectName: "New Material"
            property color baseColor: "white"
            shadingMode: CustomMaterial.Shaded
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            sourceBlend: CustomMaterial.SrcAlpha
            vertexShader: "shaders/raindrop.vert"
            depthDrawMode: Material.NeverDepthDraw
            cullMode: Material.BackFaceCulling
            property TextureInput rainmap: texture_splash
            TextureInput {
                id: texture_splash
                texture: splashtex
                enabled: true
            }

            Texture {
                id: splashtex
                source: "images/rainsplash.png"
                scaleV: 3
                scaleU: 3
                generateMipmaps: true
                mipFilter: Texture.Linear
            }
        }
    }
}

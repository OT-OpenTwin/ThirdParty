import QtQuick
import QtQuick3D
import QtQuick3D.Particles3D
import QtQuick3D.Helpers

ParticleSystem3D {
    id: root

    property color color: "#ffffff"

    running: root.visible
    ParticleEmitter3D {
        id: steamEmitter

        enabled: root.visible
        x: 0
        particleScale: 0
        velocity: steamDirection
        system: root
        lifeSpan: 500
        particleRotation.y: 0
        ModelParticle3D {
            id: steamParticle
            color: root.color
            alignMode: Particle3D.AlignTowardsStartVelocity
            maxAmount: 1500
            sortMode: Particle3D.SortNone
            fadeInDuration: 250
            fadeOutDuration: 250
            unifiedColorVariation: true
            colorVariation.w: 1
            hasTransparency: true
        }
        particleRotation.z: 0
        particle: steamParticle
        particleRotationVelocity.x: 0
        particleRotationVelocityVariation.y: 0
        particleScaleVariation: 0
        particleRotationVelocityVariation.z: 0
        particleEndScale: 10
        emitRate: 75
        particleRotation.x: 0
        particleRotationVariation.x: 0
        particleRotationVelocity.z: 0
        particleRotationVelocity.y: 0
        particleRotationVariation.z: 0
        particleEndScaleVariation: 10
        lifeSpanVariation: 500
        particleRotationVelocityVariation.x: 0
        particleRotationVariation.y: 0
    }

    Model {
        source: "#Sphere"
        castsReflections: true
        scale.x: 0.01
        scale.y: 0.01
        instancing: steamParticle.instanceTable
        materials: steamMat
        receivesReflections: true
        castsShadows: true
        scale.z: 0.1
        receivesShadows: true
    }

    Wander3D {
        id: steamWander
        globalAmount.y: 5
        uniqueAmount.y: 10
        system: root
        uniquePaceVariation: 1
        particles: steamParticle
        uniquePace.z: 0.1
        globalPaceStart.x: 0.1
        globalAmount.x: 5
        uniquePace.x: 0.1
        globalPace.x: 0.1
        uniqueAmount.z: 10
        uniqueAmount.x: 10
        uniquePace.y: 0.1
        uniqueAmountVariation: 1
        globalPaceStart.z: 0.1
        globalAmount.z: 5
        globalPace.z: 0.1
        globalPace.y: 0.1
        globalPaceStart.y: 0.1
    }

    VectorDirection3D {
        id: steamDirection
        directionVariation.z: 10
        directionVariation.y: 50
        directionVariation.x: 10
        direction.z: 0
        direction.y: 100
    }
    staticFlags: 0

    ParticleSystem3D {
        id: steamJet_thick
        y: 25
        ParticleEmitter3D {
            id: steamJetThickEmitter
            x: 0

            enabled: root.visible
            particleScale: 2.5
            system: steamJet_thick
            lifeSpan: 5000
            particleRotation.y: 0
            ModelParticle3D {
                id: steamJetThickParticle
                color: root.color
                alignMode: Particle3D.AlignTowardsStartVelocity
                maxAmount: 1500
                colorVariation.y: 0
                sortMode: Particle3D.SortNone
                fadeInDuration: 2500
                fadeOutDuration: 2500
                unifiedColorVariation: true
                colorVariation.w: 1
                colorVariation.z: 0
                colorVariation.x: 0
                hasTransparency: true
            }
            particleRotation.z: 0
            z: -5.27116
            particle: steamJetThickParticle
            velocity: steamJetThickDirection
            particleRotationVelocity.x: 0
            particleRotationVelocityVariation.y: 15
            particleScaleVariation: 2.5
            particleRotationVelocityVariation.z: 15
            particleEndScale: 10
            emitRate: 50
            particleRotation.x: 0
            particleRotationVariation.x: 0
            particleRotationVelocity.z: 0
            particleRotationVelocity.y: 0
            particleRotationVariation.z: 0
            particleEndScaleVariation: 5
            lifeSpanVariation: 5000
            particleRotationVelocityVariation.x: 15
            particleRotationVariation.y: 0
        }

        Model {
            source: "#Sphere"
            castsReflections: true
            scale.x: 0.1
            scale.y: 0.1
            instancing: steamJetThickParticle.instanceTable
            materials: steamMat
            receivesReflections: true
            castsShadows: true
            scale.z: 0.1
            receivesShadows: true
        }

        Wander3D {
            id: steamJetThickWander
            uniqueAmount.y: 10
            globalAmount.y: 5
            system: steamJet_thick
            uniquePaceVariation: 1
            particles: steamJetThickParticle
            globalAmount.x: 5
            globalPaceStart.x: 0.1
            uniquePace.z: 0.1
            globalPace.x: 0.1
            uniquePace.x: 0.1
            uniqueAmount.z: 10
            uniqueAmount.x: 10
            uniquePace.y: 0.1
            uniqueAmountVariation: 1
            globalAmount.z: 5
            globalPaceStart.z: 0.1
            globalPace.z: 0.1
            globalPace.y: 0.1
            globalPaceStart.y: 0.1
        }

        VectorDirection3D {
            id: steamJetThickDirection
            directionVariation.x: 5
            direction.y: 75
            direction.z: 0
            directionVariation.z: 5
            directionVariation.y: 25
        }

        Gravity3D {
            id: steamJetThickGravity
            particles: steamJetThickParticle
            system: steamJet_thick
            magnitude: 1
            direction.y: -8.9
        }
        staticFlags: 0
    }

    ParticleSystem3D {
        id: steamCloud
        y: 50
        ParticleEmitter3D {
            id: steamCloudEmitter

            enabled: root.visible
            x: 0
            velocity: steamCloudDirection
            particleScale: 5
            system: steamCloud
            lifeSpan: 10000
            particleRotation.y: 360
            ModelParticle3D {
                id: steamCloudParticle
                color: root.color
                maxAmount: 1500
                sortMode: Particle3D.SortNone
                fadeInDuration: 5000
                fadeOutDuration: 5000
                unifiedColorVariation: true
                colorVariation.w: 1
                hasTransparency: true
            }
            particleRotation.z: 360
            particle: steamCloudParticle
            particleRotationVelocity.x: 0
            particleRotationVelocityVariation.y: 30
            particleScaleVariation: 5
            particleRotationVelocityVariation.z: 30
            particleEndScale: 20
            emitRate: 25
            particleRotation.x: 360
            particleRotationVariation.x: 360
            particleRotationVelocity.z: 0
            particleRotationVelocity.y: 0
            particleRotationVariation.z: 360
            particleEndScaleVariation: 10
            lifeSpanVariation: 10000
            particleRotationVelocityVariation.x: 30
            particleRotationVariation.y: 360
        }

        Gravity3D {
            id: steamCloudGravity
            particles: steamCloudParticle
            system: steamCloud
            magnitude: 1
            direction.y: -8.9
        }

        Model {
            source: "#Sphere"
            castsReflections: true
            scale.x: 0.1
            scale.y: 0.1
            instancing: steamCloudParticle.instanceTable
            materials: steamMat
            receivesReflections: true
            castsShadows: true
            scale.z: 0.1
            receivesShadows: true
        }

        Wander3D {
            id: steamCloudWander
            globalAmount.y: 1
            uniqueAmount.y: 10
            system: steamCloud
            uniquePaceVariation: 1
            particles: steamCloudParticle
            globalAmount.x: 0
            globalPaceStart.x: 0.1
            uniquePace.z: 0.1
            globalPace.x: 0.1
            uniquePace.x: 0.1
            uniqueAmount.z: 10
            uniqueAmount.x: 10
            uniquePace.y: 0.1
            uniqueAmountVariation: 1
            globalAmount.z: 0
            globalPaceStart.z: 0.1
            globalPace.z: 0.1
            globalPace.y: 0.1
            globalPaceStart.y: 0.1
        }

        VectorDirection3D {
            id: steamCloudDirection
            directionVariation.x: 10
            direction.y: 50
            direction.z: 0
            directionVariation.z: 10
            directionVariation.y: 50
        }
    }

    Node {
        id: __materialLibrary__

        CustomMaterial {
            id: steamMat
            fragmentShader: "shaders/steam.frag"
            TextureInput {
                id: steamtexinput
                texture: steamtex
                enabled: true
            }

            Texture {
                id: steamtex
                source: "images/steam.png"
                mipFilter: Texture.Linear
                generateMipmaps: true
            }
            objectName: "Steam Material"
            sourceBlend: CustomMaterial.SrcAlpha
            depthDrawMode: Material.NeverDepthDraw
            destinationBlend: CustomMaterial.OneMinusSrcAlpha
            property color baseColor: root.color
            property real opacity: root.opacity
            property TextureInput dfMask: steamtexinput
            cullMode: Material.BackFaceCulling
            shadingMode: CustomMaterial.Shaded
            vertexShader: "shaders/steam.vert"
        }
    }
}

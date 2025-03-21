// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

import QtQuick
import QtQuick3D

Item {
    id: root
    required property Node origin
    required property Camera camera

    property real xSpeed: 0.1
    property real ySpeed: 0.1

    property bool xInvert: false
    property bool yInvert: true

    property bool mouseEnabled: true
    property bool panEnabled: true

    readonly property bool inputsNeedProcessing: status.useMouse || status.isPanning

    implicitWidth: parent.width
    implicitHeight: parent.height

    Connections {
        target: camera
        function onZChanged() {
            // Adjust near/far values based on distance
            let distance = camera.z
            if (distance < 1) {
                camera.clipNear = 0.01
                camera.clipFar = 100
                if (camera.z === 0) {
                    console.warn("camera z set to 0, setting it to near clip")
                    camera.z = camera.clipNear
                    }
            } else if (distance < 100) {
                camera.clipNear = 0.1
                camera.clipFar = 1000
            } else {
                camera.clipNear = 1
                camera.clipFar = 10000
            }
        }
    }

    DragHandler {
        id: dragHandler
        target: null
        enabled: mouseEnabled
        acceptedModifiers: Qt.NoModifier
        onCentroidChanged: {
            mouseMoved(Qt.vector2d(centroid.position.x, centroid.position.y), false);
        }

        onActiveChanged: {
            if (active)
                mousePressed(Qt.vector2d(centroid.position.x, centroid.position.y));
            else
                mouseReleased(Qt.vector2d(centroid.position.x, centroid.position.y));
        }
    }

    DragHandler {
        id: ctrlDragHandler
        target: null
        enabled: mouseEnabled && panEnabled
        acceptedModifiers: Qt.ControlModifier
        onCentroidChanged: {
            panEvent(Qt.vector2d(centroid.position.x, centroid.position.y));
        }

        onActiveChanged: {
            if (active)
                startPan(Qt.vector2d(centroid.position.x, centroid.position.y));
            else
                endPan();
        }
    }

    PinchHandler {
        id: pinchHandler
        target: null
        enabled: mouseEnabled

        property real distance: 0.0
        onCentroidChanged: {
            panEvent(Qt.vector2d(centroid.position.x, centroid.position.y))
        }

        onActiveChanged: {
            if (active) {
                startPan(Qt.vector2d(centroid.position.x, centroid.position.y))
                distance = root.camera.z
            } else {
                endPan()
                distance = 0.0
            }
        }
        onScaleChanged: {
            camera.z = distance * (1 / scale)
        }
    }

    TapHandler {
        onTapped: root.forceActiveFocus()
    }

    WheelHandler {
        id: wheelHandler
        orientation: Qt.Vertical
        target: null
        enabled: mouseEnabled
        acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
        onWheel: event => {
            let delta = -event.angleDelta.y * 0.01;
            camera.z += camera.z * 0.1 * delta
        }
    }

    function mousePressed(newPos) {
        root.forceActiveFocus()
        status.currentPos = newPos
        status.lastPos = newPos
        status.useMouse = true;
    }

    function mouseReleased(newPos) {
        status.useMouse = false;
    }

    function mouseMoved(newPos: vector2d) {
        status.currentPos = newPos;
    }

    function startPan(pos: vector2d) {
        status.isPanning = true;
        status.currentPanPos = pos;
        status.lastPanPos = pos;
    }

    function endPan() {
        status.isPanning = false;
    }

    function panEvent(newPos: vector2d) {
        status.currentPanPos = newPos;
    }

    FrameAnimation {
        id: updateTimer
        running: root.inputsNeedProcessing
        onTriggered: status.processInput(frameTime * 100)
    }

    QtObject {
        id: status

        property bool useMouse: false
        property bool isPanning: false

        property vector2d lastPos: Qt.vector2d(0, 0)
        property vector2d lastPanPos: Qt.vector2d(0, 0)
        property vector2d currentPos: Qt.vector2d(0, 0)
        property vector2d currentPanPos: Qt.vector2d(0, 0)

        function negate(vector) {
            return Qt.vector3d(-vector.x, -vector.y, -vector.z)
        }

        function processInput(frameDelta) {
            if (useMouse) {
                // Get the delta
                var rotationVector = origin.eulerRotation;
                var delta = Qt.vector2d(lastPos.x - currentPos.x,
                                        lastPos.y - currentPos.y);
                // rotate x
                var rotateX = delta.x * xSpeed * frameDelta
                if (xInvert)
                    rotateX = -rotateX;
                rotationVector.y += rotateX;

                // rotate y
                var rotateY = delta.y * -ySpeed * frameDelta
                if (yInvert)
                    rotateY = -rotateY;
                rotationVector.x += rotateY;
                origin.setEulerRotation(rotationVector);
                lastPos = currentPos;
            }
            if (isPanning) {
                let delta = currentPanPos.minus(lastPanPos);
                delta.x = -delta.x

                delta.x = (delta.x / root.width) * camera.z * frameDelta
                delta.y = (delta.y / root.height) * camera.z * frameDelta

                let velocity = Qt.vector3d(0, 0, 0)
                // X Movement
                let xDirection = origin.right
                velocity = velocity.plus(Qt.vector3d(xDirection.x * delta.x,
                                                     xDirection.y * delta.x,
                                                     xDirection.z * delta.x));
                // Y Movement
                let yDirection = origin.up
                velocity = velocity.plus(Qt.vector3d(yDirection.x * delta.y,
                                                     yDirection.y * delta.y,
                                                     yDirection.z * delta.y));

                origin.position = origin.position.plus(velocity)

                lastPanPos = currentPanPos
            }
        }
    }

}

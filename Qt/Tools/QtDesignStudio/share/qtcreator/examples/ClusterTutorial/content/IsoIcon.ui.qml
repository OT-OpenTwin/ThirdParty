import QtQuick 2.8
import QtQuick.Layouts 1.0
import QtQuick.Studio.Components 1.0

Item {
    id: isoIcon
    property alias engineIconOffSource: engineIconOff.source
    property alias engineIconOnSource: engineIconOn.source
    width: 92
    height: 64
    property bool active: false
    state: "normal"
    Image {
        id: engineIconOff
        anchors.verticalCenter: parent.verticalCenter
        source: "icons/engineIconOff.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: engineIconOn
        x: 0
        y: 0
        anchors.verticalCenter: parent.verticalCenter
        source: "icons/engineIconOn.png"
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }
    states: [
        State {
            name: "normal"
            when: !isoIcon.active

            PropertyChanges {
                target: engineIconOn
                visible: false
            }

            PropertyChanges {
                target: engineIconOff
                visible: true
            }

            PropertyChanges {
                target: isoIcon
                visible: true
            }
        },
        State {
            name: "active"
            when: isoIcon.active

            PropertyChanges {
                target: engineIconOff
                visible: false
            }

            PropertyChanges {
                target: engineIconOn
                visible: true
            }

            PropertyChanges {
                target: isoIcon
                visible: true
            }
        }
    ]
}

/*##^## Designer {
    D{i:0;height:61.1875;width:61.1875}
}
 ##^##*/

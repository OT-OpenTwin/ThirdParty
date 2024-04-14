pragma Singleton
import QtQuick 2.10

QtObject {
    readonly property int width: 1280
    readonly property int height: 800

    /* Edit this comment to add your custom font */
    readonly property FontLoader myCustomFont: FontLoader { source: "Teko-Medium.ttf" }    
    readonly property color backgroundColor: "#c2c2c2"
}

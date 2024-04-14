/****************************************************************************
**
** Copyright (C) 2022 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt Safe Renderer module
**
** $QT_BEGIN_LICENSE:COMM$
**
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** $QT_END_LICENSE$
**
**
**
**
**
**
**
**
****************************************************************************/
import QtQuick
import Qt.SafeRenderer

/*!
    \qmltype SafeText
    \inqmlmodule Qt.SafeRenderer 2.0
    \brief Provides a QML text type which can be rendered in the Qt Safe Renderer runtime.

    The \l {text} can be changed on runtime if \l {runtimeEditable} is set to
    \c{true}.
    The SafeText object communicates the scene position changes to the Safe Renderer runtime.
    For that purpose, a unique \l {objectName} property must be set.

    \note SafeText is not rendered properly if the font size is longer than 175.

    The following code provides an example of the SafeText type:

    \code
    SafeText {
        id: safeText
        objectName: "safeText"
        x: 256
        y: 8
        text: "Safe text.."
        color: "black"
        fillColor: "white"  // optional, but recommended to use fillColor for controlled background color
        font.pixelSize: 12
    }
    \endcode
*/

QQuickSafeText {
     id: textObject
     width: 128
     height: 64
     font.family: "Times New Roman"
     font.pixelSize: 16
     runtimeEditable: false
     onPositionChanged : {
         QSafeMessageSender.moveItem(textObject.objectName, pos)
     }
     onTextChanged: {
         if (runtimeEditable && objectName) {
            QSafeMessageSender.setText(textObject.objectName, text)
         }
     }

     onColorChanged: {
         if (runtimeEditable && objectName) {
             QSafeMessageSender.setColor(textObject.objectName, color)
         }
     }

     Component.onCompleted: {
         if (runtimeEditable && objectName) {
             QSafeMessageSender.setColor(textObject.objectName, color)
             QSafeMessageSender.setText(textObject.objectName, text)
         }
     }
}

/****************************************************************************
**
** Copyright (C) 2021 The Qt Company Ltd.
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
    \qmltype SafePicture
    \inqmlmodule Qt.SafeRenderer 2.0
    \brief Provides a QML Picture type which can be rendered in the Qt Safe Renderer runtime.

    SafePicture is an indicator that displays the colorized scalable vector QPicture
    in the Safe Renderer runtime.

    The following code provides an example how to use the SafePicture type:

    \code
    SafePicture {
        id: iconCoolant
        objectName: "iconCoolant"
        width: 30
        height: 30
        color: "#e41e25"
        fillColor: "white"  // optional, but recommended to use fillColor for controlled background color
        source: "qrc:/iso-icons/iso_grs_7000_4_2426.dat"
    }
    \endcode
*/

QQuickSafePicture {
     id: picture
     width: 64
     height: 64
}


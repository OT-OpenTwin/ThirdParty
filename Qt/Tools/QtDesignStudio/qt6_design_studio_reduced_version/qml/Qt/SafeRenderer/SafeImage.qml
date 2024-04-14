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
    \qmltype SafeImage
    \inqmlmodule Qt.SafeRenderer 2.0
    \brief Provides a QML Image type which can be rendered in the Qt Safe Renderer runtime.

    On build time, SafeImage objects are prerendered to Safe Renderer image format.

    SafeImage supports the same image formats as QImage. For more information,
    see \l{Reading and Writing Image Files}.

    The following code provides an example how to use the SafeImage type:

    \code
    SafeImage {
        id: safeImage1
        objectName: "safeImage1"
        source: "indicator1.png"
        fillColor: "black"  // optionally partially transparent image can be blended over a solid background
        width: 64
        height: 64
        x: 321
        y: 123
    }
    \endcode
*/

QQuickSafeImage {
     id: image
     width: 64
     height: 64
}

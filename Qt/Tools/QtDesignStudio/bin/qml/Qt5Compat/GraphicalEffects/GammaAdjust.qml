// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial
import QtQuick
import Qt5Compat.GraphicalEffects.private

/*!
    \qmltype GammaAdjust
    \inqmlmodule Qt5Compat.GraphicalEffects
    \since QtGraphicalEffects 1.0
    \inherits QtQuick2::Item
    \ingroup qtgraphicaleffects-color
    \brief Alters the luminance of the source item.

    GammaAdjust is applied to each pixel according to the curve which is
    pre-defined as a power-law expression, where the property gamma is used as the
    reciprocal scaling exponent. Refer to the property documentation of \l{GammaAdjust::gamma}{gamma}
    for more details.

    \table
    \header
        \li Source
        \li Effect applied
    \row
        \li \image Original_bug.png
        \li \image GammaAdjust_bug.png
    \endtable

    \section1 Example

    The following example shows how to apply the effect.
    \snippet GammaAdjust-example.qml example

*/
Item {
    id: rootItem

    /*!
        This property defines the source item for which the luminance is going to be
        adjusted.

        \note It is not supported to let the effect include itself, for
        instance by setting source to the effect's parent.
    */
    property variant source

    /*!
        This property defines the change factor for how the luminance of each pixel
        is altered according to the equation:

        \code
luminance = pow(original_luminance, 1.0 / gamma); // The luminance is assumed to be between 0.0 and 1.0
        \endcode

        Setting the gamma values under 1.0 makes the image darker, the values
        above 1.0 lighten it.

        The value ranges from 0.0 (darkest) to inf (lightest). By default, the
        property is set to \c 1.0 (no change).

        \table
        \header
        \li Output examples with different gamma values
        \li
        \li
        \row
            \li \image GammaAdjust_gamma1.png
            \li \image GammaAdjust_gamma2.png
            \li \image GammaAdjust_gamma3.png
        \row
            \li \b { gamma: 0.5 }
            \li \b { gamma: 1.0 }
            \li \b { gamma: 2.0 }
        \endtable

        \table
        \header
            \li Pixel luminance curves of the above images.
            \li
            \li
        \row
            \li \image GammaAdjust_gamma1_graph.png
            \li \image GammaAdjust_gamma2_graph.png
            \li \image GammaAdjust_gamma3_graph.png
        \row
            \li Red curve: default gamma (1.0)
            \li
            \li
        \row
            \li Yellow curve: effect applied
            \li
            \li
        \row
            \li X-axis: pixel original luminance
            \li
            \li
        \row
            \li Y-axis: pixel luminance with effect applied
            \li
            \li
        \endtable

    */
    property real gamma: 1.0

    /*!
        This property allows the effect output pixels to be cached in order to
        improve the rendering performance.

        Every time the source or effect properties are changed, the pixels in
        the cache must be updated. Memory consumption is increased, because an
        extra buffer of memory is required for storing the effect output.

        It is recommended to disable the cache when the source or the effect
        properties are animated.

        By default, the property is set to \c false.
    */
    property bool cached: false

    SourceProxy {
        id: sourceProxy
        input: rootItem.source
        interpolation: input && input.smooth ? SourceProxy.LinearInterpolation : SourceProxy.NearestInterpolation
    }

    ShaderEffectSource {
        id: cacheItem
        anchors.fill: parent
        visible: rootItem.cached
        smooth: true
        sourceItem: shaderItem
        live: true
        hideSource: visible
    }

    ShaderEffect {
        id: shaderItem
        property variant source: sourceProxy.output
        property real gamma: 1.0 / Math.max(rootItem.gamma, 0.0001)

        anchors.fill: parent

        fragmentShader: "qrc:/qt-project.org/imports/Qt5Compat/GraphicalEffects/shaders_ng/gammaadjust.frag.qsb"
    }
}

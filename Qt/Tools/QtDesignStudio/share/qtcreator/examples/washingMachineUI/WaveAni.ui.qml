/****************************************************************************
**
** Copyright (C) 2021 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Design Studio.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick 2.8
import QtQuick.Timeline 1.0

Item {
    id: waveAni
    width: 400
    height: 241

    Image {
        id: wave3
        x: 40
        y: 47
        source: "assets/wave3.png"
    }

    Image {
        id: wave2
        x: -25
        y: 75
        source: "assets/wave2.png"
    }

    Image {
        id: wave1
        x: 8
        y: 105
        source: "assets/wave1.png"
    }

    Image {
        id: wave0
        x: -36
        y: 98
        width: 387
        height: 228
        source: "assets/wave0.png"
    }

    Timeline {
        id: timeline
        animations: [
            TimelineAnimation {
                id: timelineAnimation
                running: true
                loops: -1
                duration: 5000
                to: 5000
                from: 0
            }
        ]
        enabled: true
        endFrame: 5000
        startFrame: 0

        KeyframeGroup {
            target: wave0
            property: "x"
            Keyframe {
                value: 94
                frame: 0
            }

            Keyframe {
                value: -107
                frame: 5001
            }

            Keyframe {
                value: -36
                frame: 5000
            }
        }

        KeyframeGroup {
            target: wave1
            property: "x"
            Keyframe {
                value: -79
                frame: 0
            }

            Keyframe {
                value: 51
                frame: 5000
            }
        }

        KeyframeGroup {
            target: wave2
            property: "x"
            Keyframe {
                value: 107
                frame: 0
            }

            Keyframe {
                value: -25
                frame: 5000
            }
        }

        KeyframeGroup {
            target: wave3
            property: "x"
            Keyframe {
                value: -135
                frame: 0
            }

            Keyframe {
                value: 122
                frame: 5000
            }
        }
    }
}


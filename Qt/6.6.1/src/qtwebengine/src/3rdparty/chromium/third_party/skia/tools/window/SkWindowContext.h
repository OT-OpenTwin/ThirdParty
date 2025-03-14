/*
 * Copyright 2023 Google LLC
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */
#ifndef SkWindowContext_DEFINED
#define SkWindowContext_DEFINED

#include "include/core/SkRefCnt.h"
#include "include/core/SkSurfaceProps.h"
#include "include/gpu/GrTypes.h"
#include "tools/window/SkDisplayParams.h"

class GrDirectContext;
class SkSurface;
#ifdef SK_GRAPHITE_ENABLED
namespace skgpu::graphite {
class Context;
class Recorder;
}
#endif

class SkWindowContext {
public:
    SkWindowContext(const SkDisplayParams&);

    virtual ~SkWindowContext();

    virtual sk_sp<SkSurface> getBackbufferSurface() = 0;

    virtual void swapBuffers() = 0;

    virtual bool isValid() = 0;

    virtual void resize(int w, int h) = 0;

    virtual void activate(bool isActive) {}

    const SkDisplayParams& getDisplayParams() { return fDisplayParams; }
    virtual void setDisplayParams(const SkDisplayParams& params) = 0;

    GrDirectContext* directContext() const { return fContext.get(); }
#ifdef SK_GRAPHITE_ENABLED
    skgpu::graphite::Context* graphiteContext() const { return fGraphiteContext.get(); }
    skgpu::graphite::Recorder* graphiteRecorder() const { return fGraphiteRecorder.get(); }
#endif

    int width() const { return fWidth; }
    int height() const { return fHeight; }
    SkISize dimensions() const { return {fWidth, fHeight}; }
    int sampleCount() const { return fSampleCount; }
    int stencilBits() const { return fStencilBits; }

protected:
    virtual bool isGpuContext() { return true;  }

    sk_sp<GrDirectContext> fContext;
#if defined(SK_GRAPHITE_ENABLED)
    std::unique_ptr<skgpu::graphite::Context> fGraphiteContext;
    std::unique_ptr<skgpu::graphite::Recorder> fGraphiteRecorder;
#endif

    int               fWidth;
    int               fHeight;
    SkDisplayParams   fDisplayParams;

    // parameters obtained from the native window
    // Note that the platform .cpp file is responsible for
    // initializing fSampleCount and fStencilBits!
    int               fSampleCount = 1;
    int               fStencilBits = 0;
};

#endif

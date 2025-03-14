// Copyright 2023 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef CONTENT_BROWSER_WEB_CONTENTS_WEB_CONTENTS_VIEW_IOS_H_
#define CONTENT_BROWSER_WEB_CONTENTS_WEB_CONTENTS_VIEW_IOS_H_

#include "base/memory/raw_ptr.h"

#include "content/browser/renderer_host/render_view_host_delegate_view.h"
#include "content/browser/web_contents/web_contents_view.h"
#include "content/common/content_export.h"
#include "content/public/browser/visibility.h"
#include "ui/gfx/geometry/size.h"

namespace content {

class RenderWidgetHostViewIOS;
class WebContentsImpl;
class WebContentsViewDelegate;
class WebContentsUIViewHolder;

// iOS-specific implementation of the WebContentsView. It owns an UIView that
// contains all of the contents of the tab and associated child views.
class WebContentsViewIOS : public WebContentsView,
                           public RenderViewHostDelegateView {
 public:
  // The corresponding WebContentsImpl is passed in the constructor, and manages
  // our lifetime. This doesn't need to be the case, but is this way currently
  // because that's what was easiest when they were split.
  WebContentsViewIOS(WebContentsImpl* web_contents,
                     std::unique_ptr<WebContentsViewDelegate> delegate);

  WebContentsViewIOS(const WebContentsViewIOS&) = delete;
  WebContentsViewIOS& operator=(const WebContentsViewIOS&) = delete;

  ~WebContentsViewIOS() override;

  // WebContentsView implementation --------------------------------------------
  gfx::NativeView GetNativeView() const override;
  gfx::NativeView GetContentNativeView() const override;
  gfx::NativeWindow GetTopLevelNativeWindow() const override;
  gfx::Rect GetContainerBounds() const override;
  void Focus() override;
  void SetInitialFocus() override;
  void StoreFocus() override;
  void RestoreFocus() override;
  void FocusThroughTabTraversal(bool reverse) override;
  DropData* GetDropData() const override;
  gfx::Rect GetViewBounds() const override;
  void CreateView(gfx::NativeView context) override;
  RenderWidgetHostViewBase* CreateViewForWidget(
      RenderWidgetHost* render_widget_host) override;
  RenderWidgetHostViewBase* CreateViewForChildWidget(
      RenderWidgetHost* render_widget_host) override;
  void SetPageTitle(const std::u16string& title) override;
  void RenderViewReady() override;
  void RenderViewHostChanged(RenderViewHost* old_host,
                             RenderViewHost* new_host) override;
  void SetOverscrollControllerEnabled(bool enabled) override;
  void OnCapturerCountChanged() override;
  void FullscreenStateChanged(bool is_fullscreen) override;
  void UpdateWindowControlsOverlay(const gfx::Rect& bounding_rect) override;

  using RenderWidgetHostViewCreateFunction =
      RenderWidgetHostViewIOS* (*)(RenderWidgetHost*);

  // Used to override the creation of RenderWidgetHostViews in tests.
  CONTENT_EXPORT static void InstallCreateHookForTests(
      RenderWidgetHostViewCreateFunction create_render_widget_host_view);

 private:
  // The WebContentsImpl whose contents we display.
  raw_ptr<WebContentsImpl> web_contents_;
  std::unique_ptr<WebContentsUIViewHolder> ui_view_;
};

}  // namespace content

#endif  // CONTENT_BROWSER_WEB_CONTENTS_WEB_CONTENTS_VIEW_IOS_H_

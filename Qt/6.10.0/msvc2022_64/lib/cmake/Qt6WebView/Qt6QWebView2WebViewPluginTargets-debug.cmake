#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QWebView2WebViewPlugin" for configuration "Debug"
set_property(TARGET Qt6::QWebView2WebViewPlugin APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(Qt6::QWebView2WebViewPlugin PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_DEBUG ""
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/plugins/webview/qtwebview_webview2d.dll"
  )

list(APPEND _cmake_import_check_targets Qt6::QWebView2WebViewPlugin )
list(APPEND _cmake_import_check_files_for_Qt6::QWebView2WebViewPlugin "${_IMPORT_PREFIX}/plugins/webview/qtwebview_webview2d.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

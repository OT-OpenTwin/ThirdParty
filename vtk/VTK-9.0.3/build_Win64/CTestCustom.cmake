list(APPEND CTEST_CUSTOM_MEMCHECK_IGNORE
  # Issues in third party glut library
  VTK::RenderingExternalCxx-TestGLUTRenderWindow
  VTK::IOVPICCxx-TestVPICReader
  VTK::RenderingFreeTypeFontConfigCxx-TestSystemFontRendering
  VTK::GeovisGDALCxx-TestRasterReprojectionFilter

  # The PLY code does out of range ops but that is just how
  # it is architected currently. It stores every value into
  # uint, int, and double but typically only uses the
  # value that makes sense for the type read in. Code needs
  # to be reworked eventually but the out of range values
  # are likely not being used.
  VTK::IOPLYCxx-TestPLYWriter
  VTK::IOPLYCxx-TestPLYWriterString
  VTK::IOPLYCxx-TestPLYReaderTextureUVPoints
  VTK::IOPLYCxx-TestPLYReaderTextureUVFaces

  # TestLinePlotDouble intentionally uses very large doubles
  # even though the implementation of the class is largely
  # float. Fixing this requires reworking a few classes to
  # use doubles everywhere (which they generally should)
  # when that is done this can be removed.
  # The key classes impacted are vtkPlotPoints and the
  # Draw calls in Context2D
  VTK::ChartsCoreCxx-TestLinePlotDouble
)

list(APPEND CTEST_CUSTOM_WARNING_MATCH
  "{standard input}:[0-9][0-9]*: Warning: ")

list(APPEND CTEST_CUSTOM_WARNING_EXCEPTION
  # classes that have been marked deprecated
  # and will be removed in the future
  # To be remove din VTK 9.0
  "vtkTemporalStreamTracer"

  # Java compilation warnings that don't matter.
  "^1 warning$"
  "bootstrap class path not set in conjunction with -source"

  # OSX has deprecated openGL but we still use it
  # and probably will not update the code but replace it
  # with vulklan/moltenVK in the future
  "Cocoa.*deprecated"
  "NSOpenGL.*deprecated"

  # C4275 carries with it a note that we don't care about. std::exception is
  # the main culprit here.
  "vcruntime_exception.h.*: note: see declaration of 'std::exception'"

  # GetVersion is deprecated, but its use is OK.
  "sysinfoapi.h.*: note: see declaration of 'GetVersion'"

  # Suppress notes from template instantiation backtraces.
  "note: see reference to (class|function) template instantiation"
  "note: while compiling class template member function"

  # This is secondary output from clang, not indicating the warning per se.
  "[0-9]* warnings? generated"
  "note: \\(skipping [0-9]* expansions in backtrace"
  "note: expanded from (here|macro)"

  # This is secondary output from MSVC, not indicate the warning per se.
  "note: see declaration of"
  "note: see previous definition of"

  # function cast in vtkLogger/loguru
  "vtkLogger.cxx.*: warning: cast between incompatible function types"

  # Qt headers cause C4127 warnings with MSVC. Nothing we can do to fix them.
  "[Qq]t([Cc]ore|[Gg]ui|[Tt]est|[Ww]idgets).*(warning|note)"
  # Qt has some functions marked as `__forceinline` which MSVC refuses to inline.
  "[Qq]t.*warning C4714"
  "[Qq]t.*note: see declaration of"

  # Ignore moc-generated code (and rcc and uic).
  "\\.dir[/\\\\][^/\\\\]*_autogen"

  # Ignore diy2 warnings
  "vtkdiy2"

  # Intel compilers warn about large functions, but we don't usually care.
  "remark #11074: Inlining inhibited by limit (max-total-size|max-size)"
  # Ignore the suggestion line for more information too.
  "remark #11076: To get full report use"
  )

set(cdash_show_third_party_warnings "OFF")
if (NOT cdash_show_third_party_warnings)
  list(APPEND CTEST_CUSTOM_WARNING_EXCEPTION
    # HDF5 lex/yacc sources compilation lacks the "ThirdParty" part of the path.
    "hl/src/H5LT(parse|analyze)"

    # Suppress ThirdParty source code from displaying warnings.
    "[Tt]hird[Pp]arty"

    # clang will often give multiline warnings from macro expansions,
    # where the first part has "warning:" and subsequent parts have "note:"
    # and those will sometimes expand into systems headers. When this occurs
    # for ThirdParty code, we want it suppressed too. Do so here for headers within Xcode.
    "Xcode\\.app/Contents/Developer.+note:"

    # Suppress Remote module source code from displaying warnings.
    # Suppress modules individually as just "Remote" is a common pattern
    "[Rr]emote.[Mm]oment[Ii]nvariants"
    "[Rr]emote.[Pp]oisson[Rr]econstruction"
    "[Rr]emote.[Pp]owercrust"

    # sometimes we use system third party headers with issues
    # in this case liblas
    "include/liblas"

    # in this case a redefinition of strndup between netcdf and
    # /usr/include/x86_64-linux-gnu/bits/string2.h  but the warning
    # does not include ThirdParty in the line
    "bits/string2\\.h"

    # some windows link warnings related to hdf5 that do not include
    # ThirdParty in the message
    "H5.*\\.c\\.obj : warning LNK4221"

    # ThirdParty xdmf2 uses sbrk which has been marked deprecated but
    # produces a warning without ThirdParty ala
    # /usr/include/unistd.h:587:7: note: 'sbrk' has been explicitly marked deprecated here
    "note: 'sbrk' has been explicitly marked deprecated here"

    # libproj source code includes the line
    # return 0;       /* suppresses a warning */
    # which is listed as context for another warning
    # and causes a match due to the work warning in it
    "return 0;       /\\* suppresses a warning \\*/"

    # boost graph lib causes a warning on gcc with code that
    # boost uses internally. An example for you template fans is
    # /source/Infovis/BoostGraphAlgorithms/Testing/Cxx/TestBoostAdapter.cxx:221:47: warning: '*((void*)(& ei)+32).__gnu_cxx::__normal_iterator<boost::detail::stored_edge_property<long unsigned int, boost::property<boost::edge_index_t, unsigned int> >*, std::vector<boost::detail::stored_edge_property<long unsigned int, boost::property<boost::edge_index_t, unsigned int> >, std::allocator<boost::detail::stored_edge_property<long unsigned int, boost::property<boost::edge_index_t, unsigned int> > > > >::_M_current' may be used uninitialized in this function [-Wmaybe-uninitialized]
    "[Bb]oost[Gg]raph.*edge_property.*may be used uninitialized"

    # Warnings due to DIY
    "xmemory.*: warning C4996:.*Default Bounds constructor"

    # vtkm related warnings, someone working on vtkm shoudl fix these and once fixed
    # remove these suppressions
    "struct VTKM_DEPRECATED"
    "vtkm::filter"

    # eigen uses this internal header from CUDA that should not be used.
    # [-Wcpp]
    "host_defines.h is an internal header file and must not be used directly.  This file will be removed in a future CUDA release.  Please use cuda_runtime_api.h or cuda_runtime.h instead"

    # warnings from moc generated code such as
    # GUISupport/Qt/GUISupportQt_autogen/EWIEGA46WW/moc_QVTKInteractorInternal.cpp:73:55: warning: redundant parentheses surrounding declarator [-Wredundant-parens]
    "autogen.*moc.*redundant parentheses"

    # third party hdf5
    # if(NULL == (*full_name = (char *)H5MM_malloc(path1_len + path2_len + 2 + 2))) /* Extra "+2" to quiet GCC warning - 2019/07/05, QAK */
    "H5MM.*quiet GCC warning"

    # missing overrides may be suppressed, but the superclass shows up as a match on some systems
    # it makes no sense to suppress the offending class but report the superclass
    # vtkPolyDataAlgorithm.h:91:3: note: overridden virtual function is here
    "note: overridden virtual function is here"
  )
endif ()

list(APPEND CTEST_CUSTOM_COVERAGE_EXCLUDE
  "vtk[^\\.]+(Java|Python).cxx"
  ".*Testing.Cxx.*cxx"
  ".*Testing.Cxx.*h"
  ".*moc_.*cxx"

  # Exclude files from the Utilities directories
  ".*/Utilities/.*"
  ".*/ThirdParty/.*")

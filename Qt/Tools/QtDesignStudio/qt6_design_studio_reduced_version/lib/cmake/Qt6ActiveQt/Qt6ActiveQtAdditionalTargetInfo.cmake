# Additional target information for Qt6ActiveQt
if(NOT DEFINED QT_DEFAULT_IMPORT_CONFIGURATION)
    set(QT_DEFAULT_IMPORT_CONFIGURATION RELWITHDEBINFO)
endif()
__qt_internal_promote_target_to_global_checked(Qt6::ActiveQt)
__qt_internal_promote_target_to_global_checked(Qt6::ActiveQtPrivate)


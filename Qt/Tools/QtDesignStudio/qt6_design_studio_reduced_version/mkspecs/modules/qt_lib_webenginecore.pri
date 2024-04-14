QT.webenginecore.VERSION = 6.6.2
QT.webenginecore.name = QtWebEngineCore
QT.webenginecore.module = Qt6WebEngineCore
QT.webenginecore.libs = $$QT_MODULE_LIB_BASE
QT.webenginecore.ldflags = 
QT.webenginecore.includes = $$QT_MODULE_INCLUDE_BASE $$QT_MODULE_INCLUDE_BASE/QtWebEngineCore
QT.webenginecore.frameworks = 
QT.webenginecore.bins = $$QT_MODULE_BIN_BASE
QT.webenginecore.depends =  core gui network quick webchannel positioning
QT.webenginecore.uses = 
QT.webenginecore.module_config = v2
QT.webenginecore.DEFINES = QT_WEBENGINECORE_LIB
QT.webenginecore.enabled_features = webengine-geolocation webengine-webchannel webengine-spellchecker webengine-extensions
QT.webenginecore.disabled_features = webengine-native-spellchecker
QT_CONFIG += webengine-geolocation webengine-webchannel webengine-spellchecker webengine-extensions
QT_MODULES += webenginecore


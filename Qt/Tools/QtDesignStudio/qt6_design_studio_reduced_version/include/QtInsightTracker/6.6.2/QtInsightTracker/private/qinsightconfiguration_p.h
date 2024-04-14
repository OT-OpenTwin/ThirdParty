// Copyright (C) 2023 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

#ifndef QINSIGHTCONFIGURATION_P_H
#define QINSIGHTCONFIGURATION_P_H

//
//  W A R N I N G
//  -------------
//
// This file is not part of the Qt API.  It exists purely as an
// implementation detail.  This header file may change from version to
// version without notice, or even be removed.
//
// We mean it.
//

#include <QtInsightTracker/qtinsighttracker_global.h>
#include <QtInsightTracker/QInsightConfiguration>
#include <QtCore/QObject>
#include <QtCore/QFile>

QT_BEGIN_NAMESPACE

class QSettings;

class Q_INSIGHTTRACKER_EXPORT QInsightConfigurationPrivate : public QInsightConfiguration
{
    Q_OBJECT
public:
    explicit QInsightConfigurationPrivate(QObject *parent = nullptr);
    ~QInsightConfigurationPrivate() = default;

    bool loadConfig();
    bool applyConfig(const QByteArray &data);

    QDateTime lastSync() const;
    void setLastSync(const QDateTime &time);
    bool lastShutdown() const;
    void setLastShutdown(bool shutdown);

    bool isValid() override;

    QString server() const override;
    void setServer(const QString &server) override;
    QString token() const override;
    void setToken(const QString &token) override;
    QString deviceModel() const override;
    void setDeviceModel(const QString &deviceModel) override;
    QString deviceVariant() const override;
    void setDeviceVariant(const QString &deviceVariant) override;
    QString deviceScreenType() const override;
    void setDeviceScreenType(const QString &deviceScreenType) override;
    QString appBuild() const override;
    void setAppBuild(const QString &appBuild) override;
    QString platform() const override;
    void setPlatform(const QString &platform) override;
    QString storageType() const override;
    void setStorageType(const QString &storageType) override;
    QString storagePath() const override;
    void setStoragePath(const QString &storagePath) override;
    int storageSize() const override;
    void setStorageSize(int storageSize) override;
    int syncInterval() const override;
    void setSyncInterval(int syncInterval) override;
    int batchSize() const override;
    void setBatchSize(int batchSize) override;
    QStringList categories() override;
    void setCategories(const QStringList &categories) override;
    QStringList events() override;
    void setEvents(const QStringList &events) override;
    QString userId() override;
    void setUserId(const QString &userId) override;
    bool remoteConfig() const override;
    void setRemoteConfig(bool enabled) override;
    int remoteConfigInterval() const override;
    void setRemoteConfigInterval(int syncInterval) override;

private:
    void reset();
    bool parseConfig(const QByteArray &data);

    QSettings *m_settings;
    QByteArray m_hash;
    QFile m_remoteConfigs;

private:
    QString m_server;
    QString m_token;
    QString m_deviceModel;
    QString m_deviceVariant;
    QString m_deviceScreenType;
    QString m_appBuild;
    QString m_platform;
    QString m_storageType;
    QString m_storagePath;
    int m_storageSize;
    int m_syncInterval;
    int m_batchSize;
    QStringList m_categories;
    QStringList m_events;
    QString m_userId;
    bool m_remoteConfig;
    int m_remoteConfigInterval;
};

QT_END_NAMESPACE

#endif // QINSIGHTCONFIGURATION_P_H

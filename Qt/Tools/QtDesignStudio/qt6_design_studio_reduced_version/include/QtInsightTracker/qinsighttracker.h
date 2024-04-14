// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial

#ifndef QINSIGHTTRACKER_H
#define QINSIGHTTRACKER_H

#include <QtInsightTracker/qtinsighttracker_global.h>
#include <QtInsightTracker/QInsightConfiguration>
#include <QtCore/QObject>

QT_BEGIN_NAMESPACE

class Q_INSIGHTTRACKER_EXPORT QInsightTracker : public QObject
{
    Q_OBJECT
public:
    QInsightTracker();

    void interaction(const QString &name, const QString &category = QString()) const;
    void interaction(const QString &name, const QString &contextKey, double contextValue,
                     const QString &category = QString()) const;
    void transition(const QString &name) const;
    void transition(const QString &name, const QString &contextKey, double contextValue) const;

    QT_DEPRECATED
    void sendScreenView(const QString &name) const;
    QT_DEPRECATED
    void sendScreenView(const QString &name,
                        const QString &contextKey, double contextValue) const;

    QT_DEPRECATED
    void sendClickEvent(const QString &name, const QString &category, int x, int y) const;
    QT_DEPRECATED
    void sendClickEvent(const QString &name, const QString &category, int x, int y,
                        const QString &contextKey, double contextValue) const;

    void clearCache();
    void startNewSession();

    bool isEnabled() const;
    void setEnabled(bool enabled);

    QInsightConfiguration *configuration() const;
};

QT_END_NAMESPACE

#endif // QINSIGHTTRACKER_H

/*
    TabToolbar - a small utility library for Qt, providing tabbed toolbars
	Copyright (C) 2018 Oleksii Sierov
	
    TabToolbar is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TabToolbar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with TabToolbar.  If not, see <http://www.gnu.org/licenses/>.
*/
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QLabel>
#include <QToolButton>
#include <QMenu>
#include <QAction>
#include <QSize>
#include <QApplication>
#include <QStyle>
#include <QPainter>
#include <QProxyStyle>
#include <QStyleOptionToolButton>
#include <TabToolbar/Group.h>
#include <TabToolbar/SubGroup.h>
#include <TabToolbar/TabToolbar.h>
#include "CompactToolButton.h"
#include "ToolButtonStyle.h"

using namespace tt;

Group::Group(const QString& name, QWidget* parent) : QFrame(parent)
{
    setFrameShape(NoFrame);
    setLineWidth(0);
    setContentsMargins(0, 0, 0, 0);
    setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Fixed);

    QHBoxLayout* separatorLayout = new QHBoxLayout(this);
    separatorLayout->setContentsMargins(0, 0, 0, 0);
    separatorLayout->setSpacing(0);
    separatorLayout->setDirection(QBoxLayout::LeftToRight);
    setLayout(separatorLayout);

    QVBoxLayout* outerLayout = new QVBoxLayout();
    outerLayout->setContentsMargins(0, 0, 0, 0);
    outerLayout->setSpacing(0);
    outerLayout->setDirection(QBoxLayout::TopToBottom);
    separatorLayout->addLayout(outerLayout);
    separatorLayout->addWidget(CreateSeparator());

    QFrame* innerFrame = new QFrame(this);
    innerFrame->setFrameShape(NoFrame);
    innerFrame->setLineWidth(0);
    innerFrame->setContentsMargins(0, 0, 0, 0);
    innerFrame->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Minimum);

    innerLayout = new QHBoxLayout(innerFrame);
    innerLayout->setContentsMargins(2, 4, 2, 0);
    innerLayout->setSpacing(4);
    innerLayout->setDirection(QBoxLayout::LeftToRight);
    innerFrame->setLayout(innerLayout);

    outerLayout->addWidget(innerFrame);

    QLabel* groupName = new QLabel(name, this);
    groupName->setProperty("TTGroupName", QVariant(true));
    groupName->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Maximum);
    groupName->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    groupName->adjustSize();

    outerLayout->addWidget(groupName);

    unsigned groupMaxHeight;
    unsigned rowCount;
    bool found = false;
    QObject* par = this;
    do
    {
        par = par->parent();
        const TabToolbar* tt = dynamic_cast<TabToolbar*>(par);
        if(tt)
        {
            groupMaxHeight = tt->GroupMaxHeight();
            rowCount = tt->RowCount();
            found = true;
        }
    } while(par && !found);
    if(!found)
        throw std::runtime_error("Group should be constructed inside TabToolbar!");
    const unsigned height = groupMaxHeight + groupName->height() + rowCount - 1;
    setMinimumHeight(height);
    setMaximumHeight(height);
}

SubGroup* Group::AddSubGroup(SubGroup::Align align)
{
    SubGroup* sgrp = new SubGroup(align, this);
    innerLayout->addWidget(sgrp);
    return sgrp;
}

// Modified by Alexander Kuester
QFrame* Group::CreateSeparator()
{
    QFrame* separator = new QFrame(this);
	separator->setObjectName("TabToolBarGroupSeperatorLine");	// Added by Alexander Kuester
    separator->setProperty("TTSeparator", QVariant(true));
    separator->setAutoFillBackground(false);
    separator->setFrameShadow(QFrame::Plain);
    separator->setLineWidth(1);
    separator->setMidLineWidth(0);
    separator->setFrameShape(QFrame::VLine);
	my_separators.push_back(separator);
    return separator;
}

void Group::AddSeparator()
{
    innerLayout->addWidget(CreateSeparator());
}

void Group::AddAction(QToolButton::ToolButtonPopupMode type, QAction* action, QMenu* menu)
{
    if(type == QToolButton::MenuButtonPopup)
    {
        innerLayout->addWidget(new CompactToolButton(action, menu, this));
    }
    else
    {
        const int iconSize = QApplication::style()->pixelMetric(QStyle::PM_LargeIconSize);
        QToolButton* btn = new QToolButton(this);
        btn->setProperty("TTInternal", QVariant(true));
        btn->setAutoRaise(true);
        btn->setDefaultAction(action);
        btn->setIconSize(QSize(iconSize, iconSize));
        btn->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Minimum);
        btn->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
        btn->setPopupMode(type);
        btn->setStyle(new TTToolButtonStyle());
        if(menu)
            btn->setMenu(menu);
        innerLayout->addWidget(btn);
		actionButtonMap.insert_or_assign(action, btn);		// Added by Alexander Kuester
    }
}

// Added by Alexander Kuester
void Group::RemoveAction(QAction* action) {
	actionButtonMapIterator btn = actionButtonMap.find(action);
	assert(btn != actionButtonMap.end());	// Action was not added
	assert(btn->second);	// Nullptr stored
	innerLayout->removeWidget(btn->second);
	actionButtonMap.erase(action);
}

void Group::AddWidget(QWidget* widget)
{
    widget->setParent(this);
    widget->setProperty("TTInternal", QVariant(true));
    innerLayout->addWidget(widget);
}

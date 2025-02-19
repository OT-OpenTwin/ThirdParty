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
#include <QScrollArea>
#include <QSpacerItem>
#include <QFrame>
#include <QVariant>
#include <QWheelEvent>
#include <QScrollBar>
#include <QEvent>
#include <TabToolbar/TabToolbar.h>
#include <TabToolbar/Page.h>
#include <TabToolbar/Group.h>

using namespace tt;

namespace
{
class TTScroller : public QObject
{
public:
    TTScroller(QObject* parent) : QObject(parent) {}

protected:
    bool eventFilter(QObject* watched, QEvent* event) override
    {
        if(event->type() == QEvent::Wheel)
        {
            QScrollArea* scroll = static_cast<QScrollArea*>(watched);
            QWheelEvent* wheel = static_cast<QWheelEvent*>(event);
            QScrollBar* scrollbar = scroll->horizontalScrollBar();
            scrollbar->setValue(scrollbar->value() - wheel->angleDelta().y()/5);
            return true;
        }
        return QObject::eventFilter(watched, event);
    }
};
}

// Modified by Alexander Kuester
Page::Page(int index, const QString& pageName, QWidget* parent)
    : QWidget(parent),
      myIndex(index)
{
    setObjectName(pageName);
    setSizePolicy(QSizePolicy::Maximum, QSizePolicy::MinimumExpanding);
    setContentsMargins(0, 0, 0, 0);
    QHBoxLayout* l = new QHBoxLayout(this);
    l->setContentsMargins(0, 0, 0, 0);
    l->setSpacing(0);
    setLayout(l);

    QScrollArea* scrollArea = new QScrollArea(this);
    scrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    scrollArea->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    scrollArea->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::MinimumExpanding);
    scrollArea->setFrameShape(QFrame::NoFrame);
    scrollArea->setFrameShadow(QFrame::Plain);
    scrollArea->setLineWidth(0);
    scrollArea->setWidgetResizable(true);
    scrollArea->installEventFilter(new TTScroller(scrollArea));
    innerArea = new QWidget();
    innerArea->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Ignored);
    innerArea->setProperty("TTPage", QVariant(true));
    innerLayout = new QHBoxLayout(innerArea);
    innerLayout->setContentsMargins(0, 0, 0, 0);
    innerLayout->setSpacing(1);	// Changed to 1 by Alexander Kuester

    QSpacerItem* spacer = new QSpacerItem(1, 0, QSizePolicy::Expanding, QSizePolicy::Minimum);
    innerLayout->addItem(spacer);

    scrollArea->setWidget(innerArea);
    l->addWidget(scrollArea);
}

Group* Page::AddGroup(const QString& name)
{
    Group* grp = new Group(name, innerArea);
    innerLayout->insertWidget(innerLayout->count()-1, grp);
    QObject* parent = this;
    TabToolbar* tt = nullptr;
    do
    {
        parent = parent->parent();
        tt = dynamic_cast<TabToolbar*>(parent);
    } while(tt == nullptr);
    tt->AdjustVerticalSize(grp->height());
    return grp;
}

int Page::getIndex(void) const { return myIndex; }

void Page::setIndex(int index) { myIndex = index; }

void Page::hide()
{
    emit Hiding(myIndex);
}

void Page::show()
{
    emit Showing(myIndex);
}

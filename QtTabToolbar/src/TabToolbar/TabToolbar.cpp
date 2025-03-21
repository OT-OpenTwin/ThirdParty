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
#include <QPlainTextEdit>
#include <QHBoxLayout>
#include <QTabBar>
#include <QVariant>
#include <QToolButton>
#include <QSignalBlocker>
#include <QApplication>
#include <QFrame>
#include <QTimer>
#include <TabToolbar/TabToolbar.h>
#include <TabToolbar/Page.h>
#include <cassert>

using namespace tt;

TabToolbar::TabToolbar(QWidget* parent, unsigned _groupMaxHeight, unsigned _groupRowCount) :
    QToolBar(parent),
    groupRowCount(_groupRowCount),
    groupMaxHeight(_groupMaxHeight)
{
    setObjectName("TabToolbar");
    tempShowTimer.setSingleShot(true);
    tempShowTimer.setInterval(QApplication::doubleClickInterval());

    setProperty("TabToolbar", QVariant(true));
    setContentsMargins(0, 0, 0, 0);
    layout()->setContentsMargins(0, 0, 0, 0);
    layout()->setSpacing(0);
    setContentsMargins(0, 0, 0, 0);
    setFloatable(false);
    setMovable(false);
    setAllowedAreas(Qt::TopToolBarArea);
    tabBar = new QTabWidget(this);
    tabBar->setObjectName("TTTabWidget"); // Changed by Alexander Kuester
	tabBar->setContextMenuPolicy(Qt::ContextMenuPolicy::NoContextMenu);
    tabBar->setProperty("TTWidget", QVariant(true));
    tabBar->setProperty("TTBHidden", false); // Changed by Alexander Kuester
    tabBar->tabBar()->setProperty("TTTab", QVariant(true));
    tabBarHandle = addWidget(tabBar);
    tabBar->setUsesScrollButtons(true);

    cornerActions = new QFrame(this);
    cornerActions->setFrameShape(QFrame::NoFrame);
    cornerActions->setLineWidth(0);
    cornerActions->setContentsMargins(0, 0, 0, 0);
    cornerActions->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Minimum);
    QHBoxLayout* cornerLayout = new QHBoxLayout(cornerActions);
    cornerLayout->setContentsMargins(0, 0, 0, 0);
    cornerLayout->setSpacing(0);
    cornerLayout->setDirection(QBoxLayout::LeftToRight);
    cornerActions->setLayout(cornerLayout);

    hideAction = new QAction(this);
    hideAction->setCheckable(true);
    hideAction->setText("▲");
    hideButton = new QToolButton(tabBar);
    hideButton->setProperty("TTHide", QVariant(true));
    hideButton->setToolButtonStyle(Qt::ToolButtonTextOnly);
    hideButton->setDefaultAction(hideAction);
    hideButton->setAutoRaise(true);
    hideButton->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    hideButton->setToolTip("");
    hideButton->setToolTipDuration(0);
    QObject::connect(hideAction, &QAction::triggered, [this]()
    {
        tempShowTimer.start();
        isMinimized = hideAction->isChecked();
        hideAction->setText(isMinimized ? "▼" : "▲");
        HideAt(tabBar->currentIndex());
        if (isMinimized) {
            emit Minimized();
        }
        else {
            emit Maximized();
        }
    });
	// Changed by Alexander Kuester
    //QObject::connect(tabBar, &QTabWidget::tabBarDoubleClicked, hideAction, &QAction::trigger);
	QObject::connect(tabBar, &QTabWidget::tabBarDoubleClicked, this, &TabToolbar::TabDoubleClicked);
    QObject::connect(tabBar, &QTabWidget::tabBarClicked, this, &TabToolbar::TabClicked);
    QObject::connect(tabBar, &QTabWidget::currentChanged, this, &TabToolbar::CurrentTabChanged);
    QObject::connect((QApplication*)QApplication::instance(), &QApplication::focusChanged, this, &TabToolbar::FocusChanged);
    cornerLayout->addWidget(hideButton);
    tabBar->setCornerWidget(cornerActions);
}

TabToolbar::~TabToolbar()
{
}

// Changed by Alexander Kuester
bool TabToolbar::event(QEvent* event)
{
    return QToolBar::event(event);
}

void TabToolbar::FocusChanged(QWidget* old, QWidget* now)
{
    (void)old;
    if(now && now != this)
    {
        if(isMinimized && isShown)
        {
            QObject* parent = now;
            do
            {
                parent = parent->parent();
                if(parent == this)
                    return;
            } while(parent);

            HideAt(currentIndex);
        }
    }
}

unsigned TabToolbar::RowCount() const
{
    return groupRowCount;
}

unsigned TabToolbar::GroupMaxHeight() const
{
    return groupMaxHeight;
}

void TabToolbar::AddCornerAction(QAction* action)
{
    QToolButton* actionButton = new QToolButton(tabBar);
    actionButton->setProperty("TTInternal", QVariant(true));
    actionButton->setToolButtonStyle(Qt::ToolButtonIconOnly);
    actionButton->setDefaultAction(action);
    actionButton->setAutoRaise(true);
    actionButton->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    cornerActions->layout()->addWidget(actionButton);
}

void TabToolbar::SetSpecialTabEnabled(bool enabled)
{
    hasSpecialTab = enabled;
    tabBar->tabBar()->setProperty("TTSpecial", QVariant(enabled));
    if(enabled && tabBar->count() > 0)
    {
        tabBar->setCurrentIndex(1);
    }
}

QAction* TabToolbar::HideAction()
{
    return hideAction;
}

// Changed by Alexander Kuester
void TabToolbar::TabClicked(int index)
{
    if(tempShowTimer.isActive() || (index == 0 && hasSpecialTab))
        return;

    if(isMinimized)
    {
        if(isShown && index != currentIndex)
            return; //dont hide tab bar if just switching tabs
        isMinimized = isShown;
        HideAt(index);
        isMinimized = true;
    }

	emit tabClicked(index);
}

void TabToolbar::TabDoubleClicked(int index) {
	if (allowDoubleClickOnTab) hideAction->trigger();
}

// Changed by Alexander Kuester
void TabToolbar::CurrentTabChanged(int index)
{
    QSignalBlocker blocker(tabBar);
    if(index == 0 && hasSpecialTab)
    {
        tabBar->setCurrentIndex(currentIndex);
        emit SpecialTabClicked();
    }
    else
    {
        currentIndex = index;
		emit currentTabChanged(index);
    }
}

int TabToolbar::CurrentTab() const
{
    return currentIndex;
}

// Created by Alexander Kuester
int TabToolbar::TabCount() const { return tabBar->count(); }

void TabToolbar::SetCurrentTab(int index)
{
    tabBar->setCurrentIndex(index);
}

void TabToolbar::SetAllowDoubleClickOnTab(bool allow) {
	allowDoubleClickOnTab = allow;
}

void TabToolbar::HideAt(int index)
{
    if(isMinimized)
    {
        tabBar->setProperty("TTBHidden", true); // Changed by Alexander Kuester
        const int minHeight = tabBar->tabBar()->height() + 1;
        tabBar->setMaximumHeight(minHeight);
        tabBar->setMinimumHeight(minHeight);
        setMaximumHeight(minHeight);
        setMinimumHeight(minHeight);
        isShown = false;
    } else {
        tabBar->setProperty("TTBHidden", false); // Changed by Alexander Kuester
        tabBar->setCurrentIndex(index);
        if(!isShown)
        {
            tabBar->setMaximumHeight(maxHeight);
            tabBar->setMinimumHeight(maxHeight);
            setMaximumHeight(maxHeight);
            setMinimumHeight(maxHeight);
            tabBar->adjustSize();
        }
        setFocus();
        isShown = true;
    }
}

void TabToolbar::HideTab(int index)
{
    (void)index;
    Page* page = static_cast<Page*>(sender());
    QSignalBlocker blocker(page);
    for(int i=0; i<tabBar->count(); i++)
    {
        if(tabBar->widget(i) == page)
        {
            tabBar->removeTab(i);
            return;
        }
    }
    currentIndex = tabBar->currentIndex();
}

void TabToolbar::AdjustVerticalSize(unsigned vSize)
{
    QTimer::singleShot(0, this, [this, vSize]()
    {
		maxHeight = vSize + tabBar->tabBar()->height() + 6;
        setMaximumHeight(maxHeight);
        setMinimumHeight(maxHeight);
    });
}

void TabToolbar::ShowTab(int index)
{
    Page* page = static_cast<Page*>(sender());
    QSignalBlocker blocker(page);
    tabBar->insertTab(index, page, page->objectName());
    currentIndex = tabBar->currentIndex();
}

Page* TabToolbar::AddPage(const QString& pageName)
{
    Page* page = new Page(tabBar->count(), pageName);
    QSignalBlocker blocker(page);
    QObject::connect(page, &Page::Hiding, this, &TabToolbar::HideTab);
    QObject::connect(page, &Page::Showing, this, &TabToolbar::ShowTab);
    tabBar->addTab(page, pageName);
	pages.push_back(page);
    return page;
}

// Created by Alexander Kuester
void TabToolbar::DestroyPage(int index) {
	assert(index >= 0 && index < pages.size());	// Index out of range
	pages.erase(pages.begin() + index);
	for (int i = index; i < pages.size(); i++) { pages.at(i)->setIndex(i); }
	tabBar->removeTab(index);
}

// Created by Alexander Kuester
void TabToolbar::DestroyPage(Page * page) {
	assert(page != nullptr); // Nullptr provided
	DestroyPage(page->getIndex());
}
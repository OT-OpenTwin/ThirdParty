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
#ifndef TAB_TOOLBAR_H
#define TAB_TOOLBAR_H
#include <QTabWidget>
#include <QToolBar>
#include <QList>
#include <QTimer>
#include <memory>
#include <TabToolbar/API.h>

class QToolButton;
class QFrame;
class QMenu;

namespace tt
{
class Page;

class TT_API TabToolbar : public QToolBar
{
    Q_OBJECT
public:
    explicit TabToolbar(QWidget* parent = nullptr, unsigned _groupMaxHeight = 75, unsigned _groupRowCount = 3);
    virtual ~TabToolbar();

    void     SetSpecialTabEnabled(bool enabled);
    Page*    AddPage(const QString& pageName);						// Changed by Alexander Kuester (uiCore)
    QAction* HideAction();
    void     AddCornerAction(QAction* action);
    // QString  GetStyle() const; // Removed by Alexander Kuester (uiCore)
    unsigned RowCount() const;
    unsigned GroupMaxHeight() const;
    int      CurrentTab() const;
	int      TabCount() const;										// Created by Alexander Kuester (uiCore)
    void     SetCurrentTab(int index);
	void     SetAllowDoubleClickOnTab(bool allow);					// Created by Alexander Kuester (uiCore)
	void	 DestroyPage(int index);								// Created by Alexander Kuester (uiCore)
	void	 DestroyPage(Page * page);								// Created by Alexander Kuester (uiCore)
	QTabWidget *	tabWidget(void) const { return tabBar; }		// Created by Alexander Kuester (uiCore)
signals:
    void     Minimized();
    void     Maximized();
    void     SpecialTabClicked();
    void     StyleChanged();
	void	 tabClicked(int index);									// Created by Alexander Kuester (uiCore)
	void	 currentTabChanged(int index);							// Created by Alexander Kuester (uiCore)

private slots:
    void     FocusChanged(QWidget* old, QWidget* now);
    void     TabClicked(int index);									// Changed by Alexander Kuester (uiCore)
	void     TabDoubleClicked(int index);							// Created by Alexander Kuester (uiCore)
    void     CurrentTabChanged(int index);							// Changed by Alexander Kuester (uiCore)
    void     HideAt(int index = -1);
    void     HideTab(int index);
    void     ShowTab(int index);

protected:
    bool     event(QEvent* event) override;							// Changed by Alexander Kuester (uiCore)

private:
    void     AdjustVerticalSize(unsigned vSize);

	bool           allowDoubleClickOnTab = true;					// Added by Alexander Kuester (uiCore)
    const unsigned groupRowCount;
    const unsigned groupMaxHeight;
    bool           hasSpecialTab = false;
    int            currentIndex = 0;
    unsigned       maxHeight = QWIDGETSIZE_MAX;
    QFrame*        cornerActions = nullptr;
    QAction*       hideAction = nullptr;
    QToolButton*   hideButton = nullptr;
    QAction*       tabBarHandle = nullptr;
    QTabWidget*    tabBar = nullptr;
    bool           ignoreStyleEvent = false;
    bool           isMinimized = false;
    bool           isShown = true;
    QTimer         tempShowTimer;
    
	std::vector<Page *>	pages;

    friend class Page;
};

}
#endif

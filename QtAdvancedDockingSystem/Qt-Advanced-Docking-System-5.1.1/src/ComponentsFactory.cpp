//============================================================================
/// \file   ComponentsFactory.cpp
/// \author Alexander Kuester
/// \date   03.09.2026
/// \brief  Implementation of ComponentsFactory
//============================================================================

#include "ComponentsFactory.h"

#include <memory>

#include "FloatingDockContainer.h"
#include "DockWidgetTab.h"
#include "DockAreaTabBar.h"
#include "DockAreaTitleBar.h"
#include "DockWidget.h"
#include "DockAreaWidget.h"

namespace ads
{
static std::unique_ptr<CComponentsFactory> DefaultFactory(
    new CComponentsFactory());

//============================================================================

CFloatingDockContainer* CComponentsFactory::createFloatingDockContainer(
    CDockManager* DockManager) const
{
    return new CFloatingDockContainer(DockManager);
}

CFloatingDockContainer* CComponentsFactory::createFloatingDockContainer(
    CDockAreaWidget* DockArea) const
{
    return new CFloatingDockContainer(DockArea);
}

CFloatingDockContainer* CComponentsFactory::createFloatingDockContainer(
    CDockWidget* DockWidget) const
{
    return new CFloatingDockContainer(DockWidget);
}

//============================================================================
const CComponentsFactory* CComponentsFactory::factory()
{
    return DefaultFactory.get();
}

//============================================================================
void CComponentsFactory::setFactory(CComponentsFactory* Factory)
{
    DefaultFactory.reset(Factory);
}

//============================================================================
void CComponentsFactory::resetDefaultFactory()
{
    DefaultFactory.reset(new CComponentsFactory());
}

}  // namespace ads

//---------------------------------------------------------------------------
// EOF ComponentsFactory.cpp

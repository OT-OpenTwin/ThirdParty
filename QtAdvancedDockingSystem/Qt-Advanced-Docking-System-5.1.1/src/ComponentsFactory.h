#ifndef ComponentsFactoryH
#    define ComponentsFactoryH
//============================================================================
/// \file   DockComponentsFactory.h
/// \author Alexander Kuester
/// \date   03.09.2026
/// \brief  Declaration of ComponentsFactory
//============================================================================

//============================================================================
//                                   INCLUDES
//============================================================================
#    include "ads_globals.h"

namespace ads
{
class CDockWidget;
class CDockManager;
class CDockAreaWidget;
class CFloatingDockContainer;

/**
 * Factory for creation of certain elements for the docking framework.
 * A default unique instance provided by CComponentsFactory is used for
 * creation of all supported components. To inject your custom components,
 * you can create your own derived components factory and register
 * it via setDefaultFactory() function.
 * \code
 * CComponentsFactory::setDefaultFactory(new MyComponentsFactory()));
 * \endcode
 */
class ADS_EXPORT CComponentsFactory
{
public:
    /**
     * Force virtual destructor
     */
    virtual ~CComponentsFactory() {}

    /**
     * This default implementation just creates a floating dock container
     * with new CFloatingDockContainer(DockManager).
     */
    virtual CFloatingDockContainer* createFloatingDockContainer(
        CDockManager* DockManager) const;

    /**
     * This default implementation just creates a floating dock container
     * with new CFloatingDockContainer(DockArea).
     */
    virtual CFloatingDockContainer* createFloatingDockContainer(
        CDockAreaWidget* DockArea) const;

    /**
     * This default implementation just creates a floating dock container
     * with new CFloatingDockContainer(DockWidget).
     */
    virtual CFloatingDockContainer* createFloatingDockContainer(
        CDockWidget* DockWidget) const;

    /**
     * Returns the default components factory
     */
    static const CComponentsFactory* factory();

    /**
     * Sets a new default factory for creation of GUI elements.
     * This function takes ownership of the given Factory.
     */
    static void setFactory(CComponentsFactory* Factory);

    /**
     * Resets the current factory to the default factory.
     */
    static void resetDefaultFactory();
};

}  // namespace ads

//---------------------------------------------------------------------------
#endif  // ComponentsFactoryH

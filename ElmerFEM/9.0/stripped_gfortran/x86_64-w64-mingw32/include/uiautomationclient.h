/*** Autogenerated by WIDL 6.3 from include/uiautomationclient.idl - Do not edit ***/

#ifdef _WIN32
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif
#include <rpc.h>
#include <rpcndr.h>
#endif

#ifndef COM_NO_WINDOWS_H
#include <windows.h>
#include <ole2.h>
#endif

#ifndef __uiautomationclient_h__
#define __uiautomationclient_h__

/* Forward declarations */

/* Headers for imported files */

#include <uiautomationcore.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifndef __UIAutomationClient_LIBRARY_DEFINED__
#define __UIAutomationClient_LIBRARY_DEFINED__

DEFINE_GUID(LIBID_UIAutomationClient, 0x944de083, 0x8fb8, 0x45cf, 0xbc,0xb7, 0xc4,0x77,0xac,0xb2,0xf8,0x97);

#define UIA_RuntimeIdPropertyId (30000)

#define UIA_BoundingRectanglePropertyId (30001)

#define UIA_ProcessIdPropertyId (30002)

#define UIA_ControlTypePropertyId (30003)

#define UIA_LocalizedControlTypePropertyId (30004)

#define UIA_NamePropertyId (30005)

#define UIA_AcceleratorKeyPropertyId (30006)

#define UIA_AccessKeyPropertyId (30007)

#define UIA_HasKeyboardFocusPropertyId (30008)

#define UIA_IsKeyboardFocusablePropertyId (30009)

#define UIA_IsEnabledPropertyId (30010)

#define UIA_AutomationIdPropertyId (30011)

#define UIA_ClassNamePropertyId (30012)

#define UIA_HelpTextPropertyId (30013)

#define UIA_ClickablePointPropertyId (30014)

#define UIA_CulturePropertyId (30015)

#define UIA_IsControlElementPropertyId (30016)

#define UIA_IsContentElementPropertyId (30017)

#define UIA_LabeledByPropertyId (30018)

#define UIA_IsPasswordPropertyId (30019)

#define UIA_NativeWindowHandlePropertyId (30020)

#define UIA_ItemTypePropertyId (30021)

#define UIA_IsOffscreenPropertyId (30022)

#define UIA_OrientationPropertyId (30023)

#define UIA_FrameworkIdPropertyId (30024)

#define UIA_IsRequiredForFormPropertyId (30025)

#define UIA_ItemStatusPropertyId (30026)

#define UIA_IsDockPatternAvailablePropertyId (30027)

#define UIA_IsExpandCollapsePatternAvailablePropertyId (30028)

#define UIA_IsGridItemPatternAvailablePropertyId (30029)

#define UIA_IsGridPatternAvailablePropertyId (30030)

#define UIA_IsInvokePatternAvailablePropertyId (30031)

#define UIA_IsMultipleViewPatternAvailablePropertyId (30032)

#define UIA_IsRangeValuePatternAvailablePropertyId (30033)

#define UIA_IsScrollPatternAvailablePropertyId (30034)

#define UIA_IsScrollItemPatternAvailablePropertyId (30035)

#define UIA_IsSelectionItemPatternAvailablePropertyId (30036)

#define UIA_IsSelectionPatternAvailablePropertyId (30037)

#define UIA_IsTablePatternAvailablePropertyId (30038)

#define UIA_IsTableItemPatternAvailablePropertyId (30039)

#define UIA_IsTextPatternAvailablePropertyId (30040)

#define UIA_IsTogglePatternAvailablePropertyId (30041)

#define UIA_IsTransformPatternAvailablePropertyId (30042)

#define UIA_IsValuePatternAvailablePropertyId (30043)

#define UIA_IsWindowPatternAvailablePropertyId (30044)

#define UIA_ValueValuePropertyId (30045)

#define UIA_ValueIsReadOnlyPropertyId (30046)

#define UIA_RangeValueValuePropertyId (30047)

#define UIA_RangeValueIsReadOnlyPropertyId (30048)

#define UIA_RangeValueMinimumPropertyId (30049)

#define UIA_RangeValueMaximumPropertyId (30050)

#define UIA_RangeValueLargeChangePropertyId (30051)

#define UIA_RangeValueSmallChangePropertyId (30052)

#define UIA_ScrollHorizontalScrollPercentPropertyId (30053)

#define UIA_ScrollHorizontalViewSizePropertyId (30054)

#define UIA_ScrollVerticalScrollPercentPropertyId (30055)

#define UIA_ScrollVerticalViewSizePropertyId (30056)

#define UIA_ScrollHorizontallyScrollablePropertyId (30057)

#define UIA_ScrollVerticallyScrollablePropertyId (30058)

#define UIA_SelectionSelectionPropertyId (30059)

#define UIA_SelectionCanSelectMultiplePropertyId (30060)

#define UIA_SelectionIsSelectionRequiredPropertyId (30061)

#define UIA_GridRowCountPropertyId (30062)

#define UIA_GridColumnCountPropertyId (30063)

#define UIA_GridItemRowPropertyId (30064)

#define UIA_GridItemColumnPropertyId (30065)

#define UIA_GridItemRowSpanPropertyId (30066)

#define UIA_GridItemColumnSpanPropertyId (30067)

#define UIA_GridItemContainingGridPropertyId (30068)

#define UIA_DockDockPositionPropertyId (30069)

#define UIA_ExpandCollapseExpandCollapseStatePropertyId (30070)

#define UIA_MultipleViewCurrentViewPropertyId (30071)

#define UIA_MultipleViewSupportedViewsPropertyId (30072)

#define UIA_WindowCanMaximizePropertyId (30073)

#define UIA_WindowCanMinimizePropertyId (30074)

#define UIA_WindowWindowVisualStatePropertyId (30075)

#define UIA_WindowWindowInteractionStatePropertyId (30076)

#define UIA_WindowIsModalPropertyId (30077)

#define UIA_WindowIsTopmostPropertyId (30078)

#define UIA_SelectionItemIsSelectedPropertyId (30079)

#define UIA_SelectionItemSelectionContainerPropertyId (30080)

#define UIA_TableRowHeadersPropertyId (30081)

#define UIA_TableColumnHeadersPropertyId (30082)

#define UIA_TableRowOrColumnMajorPropertyId (30083)

#define UIA_TableItemRowHeaderItemsPropertyId (30084)

#define UIA_TableItemColumnHeaderItemsPropertyId (30085)

#define UIA_ToggleToggleStatePropertyId (30086)

#define UIA_TransformCanMovePropertyId (30087)

#define UIA_TransformCanResizePropertyId (30088)

#define UIA_TransformCanRotatePropertyId (30089)

#define UIA_IsLegacyIAccessiblePatternAvailablePropertyId (30090)

#define UIA_LegacyIAccessibleChildIdPropertyId (30091)

#define UIA_LegacyIAccessibleNamePropertyId (30092)

#define UIA_LegacyIAccessibleValuePropertyId (30093)

#define UIA_LegacyIAccessibleDescriptionPropertyId (30094)

#define UIA_LegacyIAccessibleRolePropertyId (30095)

#define UIA_LegacyIAccessibleStatePropertyId (30096)

#define UIA_LegacyIAccessibleHelpPropertyId (30097)

#define UIA_LegacyIAccessibleKeyboardShortcutPropertyId (30098)

#define UIA_LegacyIAccessibleSelectionPropertyId (30099)

#define UIA_LegacyIAccessibleDefaultActionPropertyId (30100)

#define UIA_AriaRolePropertyId (30101)

#define UIA_AriaPropertiesPropertyId (30102)

#define UIA_IsDataValidForFormPropertyId (30103)

#define UIA_ControllerForPropertyId (30104)

#define UIA_DescribedByPropertyId (30105)

#define UIA_FlowsToPropertyId (30106)

#define UIA_ProviderDescriptionPropertyId (30107)

#define UIA_IsItemContainerPatternAvailablePropertyId (30108)

#define UIA_IsVirtualizedItemPatternAvailablePropertyId (30109)

#define UIA_IsSynchronizedInputPatternAvailablePropertyId (30110)

#endif /* __UIAutomationClient_LIBRARY_DEFINED__ */
/* Begin additional prototypes for all interfaces */


/* End additional prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __uiautomationclient_h__ */

# framework.ui - Backend Layer Requirements

## 1. Overview

Brief purpose within the application for the backend layer.

## 2. Components

### Component Type: dto

- framework.ui/src/main/java/at/a1ta/framework/ui/client/dto/RpcStatus.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/dto/ApplicationInitData.java (java)

### Component Type: service_layer

- framework.ui/src/main/java/at/a1ta/framework/ui/client/ServiceProxy.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/RPCService.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/RPCServiceAsync.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/ServiceLocator.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/ApplicationInitDataServletAsync.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/SystemMessageServletAsync.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/ApplicationInitDataServlet.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/SystemMessageServlet.java (java)

### Component Type: servlet

- framework.ui/src/main/java/at/a1ta/framework/ui/server/RPCServletImpl.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/ApplicationInitDataServletImpl.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/SystemMessageServletImpl.java (java)

### Component Type: unknown

- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/SessionAwareActionHandler.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/SpringSessionAwareDispatch.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/ActionHandlerRegistryBean.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/SimpleSessionAwareDispatch.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/AbstractActionHandler.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/AbstractSessionAwareDispatch.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/shared/RPCString.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/shared/RPCVoid.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/shared/RPCArrayList.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/EventQueue.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ErrorHandler.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/TextWidget.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ExtendedGrid.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/WaitingWidget.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/TooltipListener.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/LimitTextArea.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/AbstractPortlet.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/DoubleClickListener.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/StyledLabel.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/SuggestBoxFix.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/PkbListBox.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/PortletPopupPanel.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/PortletHeader.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ModelDataCombo.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ClickListener.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ModelDataSuggestBox.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ModelData.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ErrorWidgetHolder.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/EditableListBox.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/WaitingPopup.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/HasTableDataStore.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/DialogPanel.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/CloseableComponent.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/PopupCloseListener.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/DialogComponent.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/DataTableFilter.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/TableDataComparator.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/StoreChangedHandler.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/TableDataStore.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/tinymce/TinyMCE.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/util/HtmlUtils.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/util/Validator.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/util/PrintHelper.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/bundle/FrameworkUI.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/bundle/AdminImageResources.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/bundle/AdminStyleResources.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/binding/FillComboAsyncCallback.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/action/HasUserAction.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/BaseHasUserAction.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/BaseAction.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/BaseAsyncCallback.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEventType.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/Observable.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/GenericEvent.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEvent.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEventManager.java (java)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEventListener.java (java)


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** n/a
- **Design Patterns (top):** n/a
- **Inputs/Outputs:** API exposure 0, API consumers 0, DB interactions 0.
- **Key Methods/Functions:** [To be derived in advanced analysis]

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]

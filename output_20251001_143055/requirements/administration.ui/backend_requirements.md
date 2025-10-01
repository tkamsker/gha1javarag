# administration.ui - Backend Layer Requirements

## 1. Overview

Brief purpose within the application for the backend layer.

## 2. Components

### Component Type: dto

- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/dto/RTCodeModel.java (java)

### Component Type: service_layer

- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ServiceImageRenderer.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectServiceDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditServiceDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditServiceDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectServiceDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/ServicePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/GwtServicePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServicePanel.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServiceManagementPanel.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/SettingsServiceLocator.java (java) [consumes_api, db]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingException.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServletAsync.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServletAsync.java (java) [consumes_api, db]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServlet.java (java) [consumes_api, db]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServletAsync.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServletAsync.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServletAsync.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServletAsync.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/ServiceServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/dto/ServiceModel.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UnknownAreaCodeServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/SystemTrackingServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CCTOrgStructureElementServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CommonServiceLocator.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/VIPHistoryServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/VIPHistoryServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserShopAssignmentServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserShopAssignmentServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserRoleServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UnknownAreaCodeServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/SystemTrackingServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/ServiceServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/ServiceServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserRoleServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CCTOrgStructureElementServletAsync.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddServicesEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/RemoveServicesEvent.java (java)

### Component Type: servlet

- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/AuthServletImpl.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/PastExportServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/UploadFileServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/IbatisServletImpl.java (java) [consumes_api, db]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/CreditTypeServletImpl.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ReportingServletImpl.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/TeamServletImpl.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ChargingTypeServletImpl.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/FileContentServlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UsageStatisticsServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureElementUploadServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserRoleServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/SystemTrackingServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentUploadServlet.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UnknownAreaCodeServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureElementServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/VIPHistoryServletImpl.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentDownloadServlet.java (java)

### Component Type: unknown

- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/util/FileUtil.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessagesGrid.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/IconButtonRenderer.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ReportingWidget.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/MarkableCheckbox.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessageGrid.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ImageRenderer.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SettingsCell.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreasCodeDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectTeamMemberDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUserDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupManagementDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypeDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditMessageDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditMessageDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectTeamMemberDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamsDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectRolesDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreaCodeDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectRolesDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypesDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupDialog.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CheckUsagePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupManagementPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/IbatisPortlet.java (java) [consumes_api, db]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserManagementPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/AllMessagesPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserShopAssignmentPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CuCoSettBasePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/ReportingPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CCTOrgStructureElementPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupsManagementPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchComponent.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamManagementPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypesPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamPortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreasCodePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreaCodePortlet.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamPanel.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberPanel.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberManagementPanel.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamManagementPanel.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureErrorExport.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/PortletHelper.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/LocalPagingDetails.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/ImageRenderer.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/BooleanRenderer.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/SystemMessagePreviewComponent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/AdminCommonTextPool.java (java) [db]
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/AdminUI.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddCreditTypeEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/SelectRolesEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamMemberEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddUnknownAreaCodeEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/GwtAddTeamMembersEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/CuCoEventType.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamMembersEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/RoleEvent.java (java)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/ProductgroupEvent.java (java) domain:product
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplExtended.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/Util.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplMozillaExtended.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PagingGridContainer.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilterField.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ButtonRenderer.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilter.java (java) [consumes_api]
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/NumberFieldFixed.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/DetailsDialog.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/FilterablePagingMemoryProxy.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/BaseFilterableMemoryProxy.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/LinkCellRenderer.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/GridContainer.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/FilterableMemoryProxy.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ComboBoxFix.java (java)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplIE6Extended.java (java)


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** spring_framework, mybatis
- **Design Patterns (top):** n/a
- **Inputs/Outputs:** API exposure 0, API consumers 79, DB interactions 6.
- **Key Methods/Functions:** [To be derived in advanced analysis]

### API Endpoints Summary

- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/AuthServletImpl.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/PastExportServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/UploadFileServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/IbatisServletImpl.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/CreditTypeServletImpl.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ReportingServletImpl.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/TeamServletImpl.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ChargingTypeServletImpl.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/FileContentServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/util/FileUtil.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessagesGrid.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/IconButtonRenderer.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ReportingWidget.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/MarkableCheckbox.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessageGrid.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ServiceImageRenderer.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ImageRenderer.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SettingsCell.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreasCodeDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectServiceDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditServiceDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditServiceDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectTeamMemberDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUserDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupManagementDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypeDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditMessageDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditMessageDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectTeamMemberDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamsDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectRolesDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreaCodeDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectRolesDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectServiceDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypesDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupDialog.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CheckUsagePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupManagementPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/IbatisPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserManagementPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/AllMessagesPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserShopAssignmentPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CuCoSettBasePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/ReportingPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CCTOrgStructureElementPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupsManagementPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchComponent.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamManagementPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/ServicePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypesPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamPortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreasCodePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/GwtServicePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreaCodePortlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamPanel.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberPanel.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServicePanel.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberManagementPanel.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServiceManagementPanel.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamManagementPanel.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/SettingsServiceLocator.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingException.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServletAsync.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServletAsync.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServletAsync.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServletAsync.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServletAsync.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServlet.java (consumes)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServletAsync.java (consumes)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilterField.java (consumes)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilter.java (consumes)

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]

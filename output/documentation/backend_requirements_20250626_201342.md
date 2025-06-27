# Requirements Document: Backend Layer

## 1. Overview
Analysis of backend layer components and functionality

## 2. Components
- cuco/src/main/java/at/a1ta/cuco/cacheControl/GWTCacheControlFilter.java (Java source file)
  - Purpose: Servlet filter implementation to manage cache control headers for GWT application resources
- cuco/src/main/java/at/a1ta/cuco/cacheControl/app/starter/client/AppStarter.java (Java source file)
  - Purpose: Client-side application starter class for cache control functionality
- cuco/src/main/java/at/a1ta/cuco/admin/starter/client/AdminStarter.java (Java source file)
  - Purpose: Administrative interface entry point for the cache control system
- cuco/src/main/java/at/a1ta/cuco/mycuco/starter/client/MyCuCoStarter.java (Java source file)
  - Purpose: Starter class for initializing and configuring the MyCuCo client application
- cuco/src/main/java/at/a1ta/pkb/starter/client/PkbStarter.java (Java source file)
  - Purpose: Starter class for initializing and configuring the PKB (Probably Knowledge Base) client application
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/AuthServletImpl.java (Java source file)
  - Purpose: Authentication servlet implementation that handles user authorization and security-related operations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/PastExportServlet.java (Java source file)
  - Purpose: Servlet implementation for handling past export operations and requests
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/UploadFileServlet.java (Java source file)
  - Purpose: Handles file upload functionality in the web application
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/IbatisServletImpl.java (Java source file)
  - Purpose: Implements database operations using iBatis ORM framework
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/CreditTypeServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling credit type related operations in the CUCO settlement system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ReportingServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling reporting functionality in the CUCO settlement system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/TeamServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling team-related operations in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ChargingTypeServletImpl.java (Java source file)
  - Purpose: Servlet implementation for managing charging types in the system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/FileContentServlet.java (Java source file)
  - Purpose: Servlet for handling file content requests and responses in the web application
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/util/FileUtil.java (Java source file)
  - Purpose: Utility class for file operations in the A1 Telekom Austria web client application
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessagesGrid.java (Java source file)
  - Purpose: Implements a grid UI component for displaying and managing system messages in the administration interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/IconButtonRenderer.java (Java source file)
  - Purpose: Provides custom button rendering functionality with icons for grid components
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ReportingWidget.java (Java source file)
  - Purpose: A GWT UI widget for handling reporting functionality in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/MarkableCheckbox.java (Java source file)
  - Purpose: A generic checkbox widget that can be associated with a marker object
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessageGrid.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ServiceImageRenderer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ImageRenderer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SettingsCell.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreasCodeDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectServiceDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditServiceDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditServiceDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectTeamMemberDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUserDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupManagementDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypeDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditMessageDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditMessageDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectTeamMemberDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamsDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectRolesDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreaCodeDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectRolesDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectServiceDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypesDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CheckUsagePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupManagementPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/IbatisPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserManagementPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/AllMessagesPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserShopAssignmentPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CuCoSettBasePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/ReportingPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CCTOrgStructureElementPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupsManagementPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchComponent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamManagementPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/ServicePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypesPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamPortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreasCodePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/GwtServicePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreaCodePortlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamPanel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberPanel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServicePanel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberManagementPanel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServiceManagementPanel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamManagementPanel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/SettingsServiceLocator.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingException.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UsageStatisticsServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureElementUploadServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserRoleServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureErrorExport.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/SystemTrackingServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentUploadServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UnknownAreaCodeServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureElementServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/ServiceServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/VIPHistoryServletImpl.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentDownloadServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/dto/ServiceModel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/dto/RTCodeModel.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/PortletHelper.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/LocalPagingDetails.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/ImageRenderer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/BooleanRenderer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/SystemMessagePreviewComponent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/AdminCommonTextPool.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/AdminUI.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/configuration/SettingsManager.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/configuration/CuCoConfiguration.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UnknownAreaCodeServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/SystemTrackingServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CCTOrgStructureElementServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CommonServiceLocator.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/VIPHistoryServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/VIPHistoryServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserShopAssignmentServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserShopAssignmentServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserRoleServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UnknownAreaCodeServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/SystemTrackingServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/ServiceServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/ServiceServlet.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserRoleServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CCTOrgStructureElementServletAsync.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddCreditTypeEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/SelectRolesEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamMemberEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddUnknownAreaCodeEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/GwtAddTeamMembersEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/CuCoEventType.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddServicesEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/RemoveServicesEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamMembersEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/RoleEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/ProductgroupEvent.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplExtended.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/Util.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplMozillaExtended.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PagingGridContainer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilterField.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ButtonRenderer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilter.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/NumberFieldFixed.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/DetailsDialog.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/FilterablePagingMemoryProxy.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/BaseFilterableMemoryProxy.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/LinkCellRenderer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/GridContainer.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/FilterableMemoryProxy.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ComboBoxFix.java (Java source file)
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplIE6Extended.java (Java source file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/tiny_mce_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/tiny_mce_popup.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/tiny_mce.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/directionality/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/directionality/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/legacyoutput/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/legacyoutput/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/example/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/example/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/example/js/dialog.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/example/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/example/langs/en.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/iespell/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/iespell/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advimage/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advimage/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advimage/js/image.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advimage/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advimage/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/template/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/template/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/template/js/template.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/template/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/template/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/searchreplace/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/searchreplace/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/searchreplace/js/searchreplace.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/searchreplace/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/searchreplace/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/contextmenu/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/contextmenu/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/inlinepopups/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/inlinepopups/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/style/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/style/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/style/js/props.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/style/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/style/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/ins.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/abbr.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/cite.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/del.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/element_common.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/attributes.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/js/acronym.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/xhtmlxtras/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/nonbreaking/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/nonbreaking/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/print/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/print/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/autoresize/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/autoresize/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/autosave/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/autosave/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/autosave/langs/en.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/tabfocus/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/tabfocus/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/insertdatetime/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/insertdatetime/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/layer/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/layer/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/js/cell.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/js/merge_cells.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/js/row.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/js/table.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/table/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullpage/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullpage/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullpage/js/fullpage.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullpage/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullpage/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlist/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlist/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/preview/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/preview/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/preview/jscripts/embed.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/pagebreak/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/pagebreak/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullscreen/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/fullscreen/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/visualchars/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/visualchars/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/save/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/save/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/noneditable/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/noneditable/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlink/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlink/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlink/js/advlink.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlink/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advlink/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/bbcode/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/bbcode/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/paste/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/paste/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/paste/js/pastetext.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/paste/js/pasteword.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/paste/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/paste/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/js/media.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/js/embed.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/media/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/emotions/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/emotions/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/emotions/js/emotions.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/emotions/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/emotions/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advhr/editor_plugin.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advhr/editor_plugin_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advhr/js/rule.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advhr/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/plugins/advhr/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/utils/editable_selects.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/utils/mctabs.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/utils/form_utils.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/utils/validate.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/langs/de.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/langs/en.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/editor_template.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/editor_template_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/about.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/link.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/anchor.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/source_editor.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/charmap.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/image.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/js/color_picker.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/langs/en_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/langs/de_dlg.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/langs/de.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/advanced/langs/en.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/simple/editor_template.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/simple/editor_template_src.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/simple/langs/de.js (JavaScript file)
- framework.ui/src/main/resources/at/a1ta/framework/ui/public/tiny_mce/themes/simple/langs/en.js (JavaScript file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/RPCServletImpl.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/ApplicationInitDataServletImpl.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/SystemMessageServletImpl.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/SessionAwareActionHandler.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/SpringSessionAwareDispatch.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/ActionHandlerRegistryBean.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/SimpleSessionAwareDispatch.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/AbstractActionHandler.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/server/dispatch/AbstractSessionAwareDispatch.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/shared/RPCString.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/shared/RPCVoid.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/shared/RPCArrayList.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/EventQueue.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ErrorHandler.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ServiceProxy.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/dto/RpcStatus.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/dto/ApplicationInitData.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/TextWidget.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ExtendedGrid.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/WaitingWidget.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/TooltipListener.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/LimitTextArea.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/AbstractPortlet.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/DoubleClickListener.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/StyledLabel.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/SuggestBoxFix.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/PkbListBox.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/PortletPopupPanel.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/PortletHeader.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ModelDataCombo.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ClickListener.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ModelDataSuggestBox.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ModelData.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/ErrorWidgetHolder.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/EditableListBox.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/WaitingPopup.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/HasTableDataStore.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/DialogPanel.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/CloseableComponent.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/PopupCloseListener.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/dialog/DialogComponent.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/DataTableFilter.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/TableDataComparator.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/StoreChangedHandler.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/ui/table/TableDataStore.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/tinymce/DefaultTinyMCEConfiguration.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/tinymce/CuCoTinyMCEConfiguration.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/tinymce/TinyMCE.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/util/HtmlUtils.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/util/Validator.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/util/PrintHelper.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/bundle/FrameworkUI.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/bundle/AdminImageResources.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/bundle/AdminStyleResources.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/binding/FillComboAsyncCallback.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/action/HasUserAction.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/BaseHasUserAction.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/BaseAction.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/RPCService.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/RPCServiceAsync.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/command/BaseAsyncCallback.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/ServiceLocator.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/ApplicationInitDataServletAsync.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/SystemMessageServletAsync.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/ApplicationInitDataServlet.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/service/SystemMessageServlet.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEventType.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/Observable.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/GenericEvent.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEvent.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEventManager.java (Java source file)
- framework.ui/src/main/java/at/a1ta/framework/ui/client/event/PortletEventListener.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/util/CCTClearanceXSLTTester.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/util/ReflectionUtilTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/util/ConfigDataGenerator.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/MobileSubscriptionCategory.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/FixedLineTelephoneSet.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/MobileSubscription.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/FixedLineTelephoneSetConfiguration.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1cml/v2/shared/A1CMLV2DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1cml/v2/shared/A1CMLV2ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bfw1/v1/shared/BFWV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bfw1/v1/shared/BFWV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v12/shared/ETGTV12ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v12/shared/ETGTV12DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v11/shared/ETGTV11DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v11/shared/ETGTV11ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v10/shared/ETGTV10ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v10/shared/ETGTV10DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/marketplace/v1/shared/MarketplaceProductGenerator.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/marketplace/v1/shared/MarketplaceV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/marketplace/v1/shared/MarketplaceV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v6/shared/BpbV6DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v6/shared/BpbV6ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v1/shared/BpbV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v1/shared/BpbV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v7/shared/BpbV7ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v7/shared/BpbV7DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/daas/v1/shared/DaaSV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/daas/v1/shared/DaaSV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v1/shared/A1bnV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v1/shared/A1BNV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v8/shared/A1BNV8DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v8/shared/A1BNV8ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v9/shared/A1BNV9DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v9/shared/A1BNV9ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v2/shared/A1BNV2DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v2/shared/A1bnV2ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v11/shared/A1BNV11DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v11/shared/A1BNV11ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v10/shared/A1BNV10ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v10/shared/A1BNV10DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v6/shared/A1BIV6DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v6/shared/A1BIV6ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v5/shared/A1BIV5DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v5/shared/A1BIV5ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v4/shared/A1BIV4ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v4/shared/A1BIV4DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v3/shared/A1BIV3DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v3/shared/A1BIV3ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v5/shared/PSHCV5ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v5/shared/PSHCV5DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v4/shared/PSHCV4ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v4/shared/PSHCV4DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v1/shared/FibV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v1/shared/FibV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v7/shared/FibV7DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v7/shared/FibV7ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v1/shared/A1PSV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v1/shared/A1PSV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v2/shared/A1PSV2DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v2/shared/A1PSV2ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v1/shared/BizkoV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v1/shared/BizkoV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v9/shared/BizkoV9DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v9/shared/BizkoV9ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1voip/v1/shared/A1VOIPV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1voip/v1/shared/A1VOIPV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bip/v1/shared/A1BIPV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bip/v1/shared/A1BIPV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1tvres/v1/shared/A1TVRESV1DefaultConfigurationTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1tvres/v1/shared/A1TVRESV1ConfigurationSmokeTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/XsltTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/QuoteServiceImplTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/IQuoteDaoTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/DefaultConfigParserTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/ICuscoServiceImplTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/IOpportunityServiceImplTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/IQuoteServiceImplTest.java (Java source file)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/ICuscoCustomerContactServiceImplTest.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/XMLUtil.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/ReflectionUtil.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/JaxbDateAdapter.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/NonMappableCharacterReplacer.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/QuoteDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/SalesstageDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/POVDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/ProductOfferingDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/QuoteClearanceDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/QuoteFlashInfoDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/POVConfigurationDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/OpportunityDao.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/ProductOfferingTypeHandler.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/ProductOfferingDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/POVConfigurationDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/SalesstageDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/OpportunityDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/QuoteDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/POVDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/QuoteClearanceDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/QuoteFlashInfoDaoImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/XMLTypeHandlerCallback.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/Pair.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/ConfigurableListSelectorRuntimeConfigurationHelper.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/TariffSocMappings.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/CctAttributeList.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Totals.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/ProductInstance.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/ApproverUserInfo.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/POVHistory.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/RuntimeConfigurable.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Configurable.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/POV.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/CctAttribute.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Quote.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Copyable.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/QuoteForFlash.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Opportunity.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/SalesInformation.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Priceable.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/CCTClearanceRule.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Role.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/SaveInfo.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/QuoteFlashInfo.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/POVConfiguration.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/MobileSubscriptionBase.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/QuoteFlashInfoService.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/QuoteClearanceService.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/QuoteService.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/OpportunityService.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/OpportunityServiceImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/QuoteClearanceServiceImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/QuoteFlashInfoServiceImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/QuoteServiceImpl.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/configurationtool/CacheMBean.java (Java source file)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/configurationtool/CacheManager.java (Java source file)

## 3. Functionality
### Main Features
- Servlet implementation for handling team-related operations in the web client
- Handles file upload functionality in the web application
- Starter class for initializing and configuring the MyCuCo client application
- A generic checkbox widget that can be associated with a marker object
- Starter class for initializing and configuring the PKB (Probably Knowledge Base) client application
- Servlet implementation for managing charging types in the system
- Administrative interface entry point for the cache control system
- Implements database operations using iBatis ORM framework
- Utility class for file operations in the A1 Telekom Austria web client application
- A GWT UI widget for handling reporting functionality in the web client
- Provides custom button rendering functionality with icons for grid components
- Authentication servlet implementation that handles user authorization and security-related operations
- Servlet implementation for handling credit type related operations in the CUCO settlement system
- Servlet for handling file content requests and responses in the web application
- Servlet filter implementation to manage cache control headers for GWT application resources
- Servlet implementation for handling past export operations and requests
- Servlet implementation for handling reporting functionality in the CUCO settlement system
- Client-side application starter class for cache control functionality
- Implements a grid UI component for displaying and managing system messages in the administration interface

### Data Structures
#### Filter
Fields:
- FilterConfig
Relationships:
- implements javax.servlet.Filter
#### SystemMessagePool
Fields:
- messages
- settings
Relationships:
- extends TextPool
#### SettingPool
Fields:
- settings
- localSettings
Relationships:
- associated with LocalSettingPool
#### LocalSettingPool
Fields:
- settings
- configurations
Relationships:
- extends SettingPool
#### TextPool
Fields:
- text resources
- translations
Relationships:
- used by MyCuCoStarter
#### LocalSettingPool
Fields:
- settings
- configurations
Relationships:
- extends SettingPool
#### SystemMessage
Fields:
- message content
- message type
Relationships:
- used by PkbStarter
#### Authority
Fields:
- authority details
Relationships:
- Used by AuthorityService
#### HttpServletRequest
Fields:
- request parameters
Relationships:
- Processed by PastExportServlet
#### HttpServletResponse
Fields:
- response data
Relationships:
- Generated by PastExportServlet
#### FileItem
Fields:
- name
- content
- size
Relationships:
- Apache Commons FileUpload
#### SqlMapClientDaoSupport
Fields:
- sqlMapClient
Relationships:
- Spring Framework
- iBatis
#### ArrayList
Fields:
- Generic collection
Relationships:
- Used for returning credit type data
#### ArrayList
Fields:
- Generic collection
Relationships:
- Used for report data collection
#### HashMap
Fields:
- Key-value pairs
Relationships:
- Used for report parameters/configuration
#### BiteUser
Fields:
- user details
Relationships:
- Used for team member management
#### ChargingType
Fields:
- charging type details
Relationships:
- Managed by ChargingTypeService
#### HttpServletRequest
Fields:
- request parameters
- headers
Relationships:
- Extends HttpServlet
#### File operations utilities
Fields:
- file handling methods
Relationships:
- Used by other components requiring file operations
#### SystemMessage
Fields:
- id
- message
- status
Relationships:
- Displayed in grid rows
#### ModelData
Fields:
- button properties
- icon properties
Relationships:
- Used by ListStore
#### HashMap
Fields:
- unknown - full implementation not visible
Relationships:
- Used for storing report-related data
#### MarkableCheckbox<B>
Fields:
- marker: B
Relationships:
- Extends CheckBox
- Contains generic type B

### Key Methods/Functions
#### GWTCacheControlFilter
Description: Implements Filter interface to intercept and modify HTTP responses with cache control headers
#### AppStarter
Description: Entry point for the cache control application client interface
#### AdminStarter
Description: Entry point for the administrative interface with extended functionality
#### MyCuCoStarter
Description: Main starter class that handles initialization of client-side configuration and settings
#### PkbStarter
Description: Main starter class that handles initialization of PKB client-side configuration and system messages
#### AuthServletImpl
Description: Web servlet handling authentication and authorization requests
#### PastExportServlet
Description: Handles HTTP requests for exporting historical data
#### UploadFileServlet
Description: Processes multipart file upload requests and manages file storage
#### IbatisServletImpl
Description: Handles database operations through iBatis SqlMap interface
#### CreditTypeServletImpl
Description: Spring-enabled servlet that processes credit type operations and interfaces with CreditTypeService
#### ReportingServletImpl
Description: Spring-enabled servlet that handles report generation and processing
#### TeamServletImpl
Description: Spring Remote Service Servlet handling team management operations
#### ChargingTypeServletImpl
Description: Spring Remote Service Servlet handling charging type operations
#### FileContentServlet
Description: Handles HTTP requests for file content operations
#### FileUtil
Description: Provides helper methods for file operations
#### SystemMessagesGrid
Description: Grid widget that displays system messages with selection and click handling capabilities
#### IconButtonRenderer
Description: Renders buttons with icons in grid cells
#### ReportingWidget
Description: Provides reporting interface elements including horizontal panel and image handling
#### MarkableCheckbox
Description: Custom checkbox that maintains a reference to a marker object of generic type

## 4. Dependencies
- java.util.Date
- com.google.gwt.event.dom.client
- java.util.List
- com.extjs.gxt.ui.client.data
- at.a1ta.bite.core.shared.dto.TextPool
- com.google.gwt.event.logical.shared
- javax.servlet
- A1 Telekom Austria proprietary libraries
- at.a1ta.bite.core.shared.dto.LocalSettingPool
- at.a1ta.bite.ui.client.BiteEntryPoint
- com.google.gwt.event.dom.client.ClickEvent
- java.util.ArrayList
- javax.servlet.http.HttpServlet
- javax.servlet.http.HttpServletRequest
- at.a1ta.bite.core.shared.dto.SettingPool
- org.springframework
- at.a1ta.bite.ui
- com.google.gwt.user.client.ui.CheckBox
- at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet
- org.springframework.orm.ibatis
- org.springframework.beans.factory
- java.io
- org.springframework.web.context
- at.a1ta.bite.core.shared.dto
- javax.servlet.HttpServlet
- javax.servlet.annotation.WebServlet
- at.a1ta.cuco.core.service.ChargingTypeService
- com.google.gwt.user.client.ui.HorizontalPanel
- javax.servlet.Filter
- at.a1ta.bite.core.shared.dto.systemmessage.SystemMessagePool
- javax.servlet.ServletException
- at.a1ta.bite.core.shared.dto.security.Authority
- javax.servlet.http.HttpServletResponse
- com.extjs.gxt.ui.client.store
- at.a1ta.bite.core.server.service.AuthorityService
- javax.servlet.ServletRequest
- at.a1ta.cuco.core.service.CreditTypeService
- at.a1ta.bite.core.shared.dto.StartupConfiguration
- org.apache.commons.fileupload
- com.google.gwt.user.client.ui.Image
- javax.servlet.FilterChain
- at.a1ta.bite.ui.server.servlet
- com.extjs.gxt.ui.client.widget.button
- java.io.IOException
- java.io packages
- com.google.gwt.event.dom.client.ClickHandler
- javax.servlet.FilterConfig
- javax.servlet.ServletResponse
- com.extjs.gxt.ui.client.event
- org.apache.commons.lang3
- at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage

## 5. Business Rules
- Must implement standard servlet filter lifecycle methods (init, doFilter, destroy)
- Must handle HTTP request/response processing for cache control
- Initialize application settings and message pools
- Initialize administrative interface with appropriate access levels
- Client initialization must load local settings before startup
- System must initialize with local settings and handle system messages
- Must authenticate users and manage their authorities
- Must handle export requests and generate appropriate responses
- Handle multipart file upload requests
- Validate and process uploaded files
- Database access and operations using iBatis mappings
- Spring context integration
- Must authenticate and authorize credit type operations
- Must handle and log exceptions during report generation
- Team management operations must be handled through Spring Remote Service
- Charging type operations must be processed through ChargingTypeService
- Process HTTP requests for file content operations
- File operations must comply with A1 Telekom Austria's security and handling policies
- Handle selection events for system messages
- Manage click interactions on grid elements
- Button rendering with icon integration
- Handle button selection events
- Handles click events for reporting actions
- Checkbox label is set to marker's string representation
- Marker object must be maintained and accessible


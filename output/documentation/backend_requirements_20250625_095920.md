# Requirements Document: Backend Layer

## 1. Overview
Analysis of backend layer components and functionality

## 2. Components
- cuco/src/main/java/at/a1ta/cuco/cacheControl/GWTCacheControlFilter.java (Java source file)
  - Purpose: Implements a servlet filter to control caching behavior for GWT application resources
- cuco/src/main/java/at/a1ta/cuco/cacheControl/app/starter/client/AppStarter.java (Java source file)
  - Purpose: Entry point for the main application module that initializes core application components
- cuco/src/main/java/at/a1ta/cuco/admin/starter/client/AdminStarter.java (Java source file)
  - Purpose: Entry point for the admin module that initializes administration interface components
- cuco/src/main/java/at/a1ta/cuco/mycuco/starter/client/MyCuCoStarter.java (Java source file)
  - Purpose: Application starter class for the MyCuCo client application that initializes configuration and resources
- cuco/src/main/java/at/a1ta/pkb/starter/client/PkbStarter.java (Java source file)
  - Purpose: Application starter class for the PKB (Personal Knowledge Base) client application
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/AuthServletImpl.java (Java source file)
  - Purpose: Authentication servlet implementation for handling authorization requests
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/PastExportServlet.java (Java source file)
  - Purpose: Servlet for handling past export operations and generating export data in a specific format
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/UploadFileServlet.java (Java source file)
  - Purpose: Handles file upload functionality through HTTP requests
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/IbatisServletImpl.java (Java source file)
  - Purpose: Spring-enabled servlet implementation for iBATIS database operations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/CreditTypeServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling credit type related operations in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ReportingServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling reporting functionality in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/TeamServletImpl.java (Java source file)
  - Purpose: Servlet implementation for team management operations in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/ChargingTypeServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling charging type related operations through web services
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/FileContentServlet.java (Java source file)
  - Purpose: Handles file upload operations through HTTP servlet
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/server/util/FileUtil.java (Java source file)
  - Purpose: Utility class for file operations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessagesGrid.java (Java source file)
  - Purpose: Implements a grid component for displaying system messages with date formatting and selection handling
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/IconButtonRenderer.java (Java source file)
  - Purpose: Custom renderer for grid columns that display interactive buttons with icons
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ReportingWidget.java (Java source file)
  - Purpose: Implements a reporting interface widget with data table functionality
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/MarkableCheckbox.java (Java source file)
  - Purpose: A custom checkbox widget that can be associated with a generic marker object
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SystemMessageGrid.java (Java source file)
  - Purpose: Grid component for displaying system messages with paging functionality
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ServiceImageRenderer.java (Java source file)
  - Purpose: Custom renderer for displaying service images in a grid
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/ImageRenderer.java (Java source file)
  - Purpose: Renders images in a grid component for the web client UI
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/ui/SettingsCell.java (Java source file)
  - Purpose: Represents a settings cell container for segment and category data
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreasCodeDialog.java (Java source file)
  - Purpose: Dialog interface for editing unknown areas codes
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectServiceDialog.java (Java source file)
  - Purpose: GWT-based dialog for selecting services in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditServiceDialog.java (Java source file)
  - Purpose: GWT-based dialog for editing service properties
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditServiceDialog.java (Java source file)
  - Purpose: ExtJS-based dialog for editing service properties
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectTeamMemberDialog.java (Java source file)
  - Purpose: Dialog component for selecting team members using GWT UI framework
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamDialog.java (Java source file)
  - Purpose: Dialog for creating and editing team information
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUserDialog.java (Java source file)
  - Purpose: Dialog for editing user information and settings
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupManagementDialog.java (Java source file)
  - Purpose: Dialog interface for editing role group management settings in the administration system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypeDialog.java (Java source file)
  - Purpose: Dialog interface for creating and editing credit types in the system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtEditMessageDialog.java (Java source file)
  - Purpose: Dialog interface for editing system messages or notifications
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditMessageDialog.java (Java source file)
  - Purpose: Dialog interface for editing messages in the system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectTeamMemberDialog.java (Java source file)
  - Purpose: Dialog interface for selecting team members with pagination support
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditTeamsDialog.java (Java source file)
  - Purpose: Dialog interface for editing team information using UiBinder
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectRolesDialog.java (Java source file)
  - Purpose: Dialog component for selecting user roles in the application
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreaCodeDialog.java (Java source file)
  - Purpose: Dialog for editing unknown area codes in the system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/GwtSelectRolesDialog.java (Java source file)
  - Purpose: GWT-specific implementation of role selection dialog
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/SelectServiceDialog.java (Java source file)
  - Purpose: Dialog component for selecting services with pagination support
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypesDialog.java (Java source file)
  - Purpose: Dialog for editing credit type configurations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupDialog.java (Java source file)
  - Purpose: Dialog for managing role group assignments and configurations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CheckUsagePortlet.java (Java source file)
  - Purpose: A GWT portlet for checking usage statistics or metrics with date-based filtering
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupManagementPortlet.java (Java source file)
  - Purpose: Manages role groups with paging support using GXT framework
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/IbatisPortlet.java (Java source file)
  - Purpose: Interface for iBatis database operations through a GXT-based UI
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserManagementPortlet.java (Java source file)
  - Purpose: Portlet for managing user accounts and permissions in the administration interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/AllMessagesPortlet.java (Java source file)
  - Purpose: Portlet for displaying and managing system messages across the platform
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/UserShopAssignmentPortlet.java (Java source file)
  - Purpose: Portlet for managing user assignments to shops/stores
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CuCoSettBasePortlet.java (Java source file)
  - Purpose: Base abstract portlet class for Customer Communication Settings functionality
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/ReportingPortlet.java (Java source file)
  - Purpose: Implements reporting functionality for the Customer Communication Settings system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/CCTOrgStructureElementPortlet.java (Java source file)
  - Purpose: Manages organizational structure elements in the Customer Communication Settings system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/RoleGroupsManagementPortlet.java (Java source file)
  - Purpose: Manages role groups in a web client portlet interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchPortlet.java (Java source file)
  - Purpose: Implements VIP search functionality as a portlet
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchComponent.java (Java source file)
  - Purpose: Implements the UI component for VIP search functionality
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamManagementPortlet.java (Java source file)
  - Purpose: Portlet for managing team configurations in the web client interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/ServicePortlet.java (Java source file)
  - Purpose: Portlet for managing service-related configurations with paging support
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypesPortlet.java (Java source file)
  - Purpose: Portlet for managing credit types with clickable interface elements
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/CreditTypePortlet.java (Java source file)
  - Purpose: Portlet component for managing credit type configurations in the administration interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/TeamPortlet.java (Java source file)
  - Purpose: Portlet component for team management functionality
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreasCodePortlet.java (Java source file)
  - Purpose: Portlet for handling and displaying unknown area codes in the system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/GwtServicePortlet.java (Java source file)
  - Purpose: GWT-based portlet implementation for handling service-related functionality in the CUCOSETT web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/UnknownAreaCodePortlet.java (Java source file)
  - Purpose: Portlet for managing and displaying unknown area codes using ExtJS/GXT grid components
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamPanel.java (Java source file)
  - Purpose: Panel component for displaying and managing team-related information
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberPanel.java (Java source file)
  - Purpose: Manages the display and interaction with team member data in a panel format using GXT UI components
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServicePanel.java (Java source file)
  - Purpose: Manages team service-related functionality in a panel interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamMemberManagementPanel.java (Java source file)
  - Purpose: Provides comprehensive team member management functionality including selection and click handling
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamServiceManagementPanel.java (Java source file)
  - Purpose: Manages team service-related operations in a GWT panel interface
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/portlet/past/widget/TeamManagementPanel.java (Java source file)
  - Purpose: Provides UI panel for team management operations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/SettingsServiceLocator.java (Java source file)
  - Purpose: Service locator pattern implementation for various settings-related services
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServlet.java (Java source file)
  - Purpose: Remote service interface for managing charging types in the system
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServlet.java (Java source file)
  - Purpose: Remote service interface for handling reporting functionality
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingException.java (Java source file)
  - Purpose: Custom exception class for reporting-related errors
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ChargingTypeServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for retrieving charging type data in GWT client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for iBATIS DAO operations in GWT client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/IbatisServlet.java (Java source file)
  - Purpose: Synchronous service interface for iBATIS DAO operations in GWT server
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for credit type management operations in GWT client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for team management operations in GWT client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/TeamServlet.java (Java source file)
  - Purpose: Synchronous service interface for team management operations in GWT
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/ReportingServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for handling reporting operations in the web client
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/CreditTypeServlet.java (Java source file)
  - Purpose: Remote service interface for managing credit type operations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServlet.java (Java source file)
  - Purpose: Remote service interface for handling authentication and authorization operations
- administration.ui/src/main/java/at/a1ta/webclient/cucosett/client/service/AuthServletAsync.java (Java source file)
  - Purpose: Asynchronous interface for authentication-related service calls in GWT client
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UsageStatisticsServlet.java (Java source file)
  - Purpose: Servlet handling usage statistics for A1 Telekom Austria system
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureElementUploadServlet.java (Java source file)
  - Purpose: Servlet handling organizational structure element uploads
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserRoleServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling user role management operations
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureErrorExport.java (Java source file)
  - Purpose: Exports organization structure errors to Excel format
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/SystemTrackingServletImpl.java (Java source file)
  - Purpose: Implementation of system tracking functionality via servlet
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentUploadServlet.java (Java source file)
  - Purpose: Handles file uploads for user-shop assignments through HTTP servlet
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UnknownAreaCodeServletImpl.java (Java source file)
  - Purpose: Implements servlet handling unknown area code operations
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentServletImpl.java (Java source file)
  - Purpose: Implements servlet for managing user-shop assignments
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/CCTOrgStructureElementServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling organizational structure element operations in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/ServiceServletImpl.java (Java source file)
  - Purpose: Implementation of service-related operations servlet in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/VIPHistoryServletImpl.java (Java source file)
  - Purpose: Servlet implementation for handling VIP history data and operations
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/server/UserShopAssignmentDownloadServlet.java (Java source file)
  - Purpose: Servlet for handling user shop assignment downloads
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/dto/ServiceModel.java (Java source file)
  - Purpose: Data model class for service information in the admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/dto/RTCodeModel.java (Java source file)
  - Purpose: Data model class for RT code information in the admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/PortletHelper.java (Java source file)
  - Purpose: Utility class for creating and managing portlet-style UI components with tooltips and icons
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/LocalPagingDetails.java (Java source file)
  - Purpose: Handles local pagination functionality for data grids and lists
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/ImageRenderer.java (Java source file)
  - Purpose: Handles image rendering and display functionality for the UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/BooleanRenderer.java (Java source file)
  - Purpose: Renders boolean values as Yes/No text in grid cells using localized strings
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/ui/SystemMessagePreviewComponent.java (Java source file)
  - Purpose: Provides UI component for previewing system messages
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/AdminCommonTextPool.java (Java source file)
  - Purpose: Defines interface for accessing localized text strings used in admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/AdminUI.java (Java source file)
  - Purpose: Central access point for common UI resources and configuration in the admin interface
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/configuration/SettingsManager.java (Java source file)
  - Purpose: Base settings management class that handles key-value configuration storage and retrieval
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/bundle/configuration/CuCoConfiguration.java (Java source file)
  - Purpose: Application-specific configuration manager extending base settings functionality
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UnknownAreaCodeServlet.java (Java source file)
  - Purpose: Remote service interface for handling unknown area code operations in the CUCO admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/SystemTrackingServlet.java (Java source file)
  - Purpose: Remote service interface for system tracking functionality in the CUCO admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CCTOrgStructureElementServlet.java (Java source file)
  - Purpose: Remote service interface for managing CCT organizational structure elements
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CommonServiceLocator.java (Java source file)
  - Purpose: Service locator pattern implementation for managing GWT service instances in the admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/VIPHistoryServlet.java (Java source file)
  - Purpose: Remote service interface definition for VIP history operations
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/VIPHistoryServletAsync.java (Java source file)
  - Purpose: Asynchronous interface for VIP history operations in GWT client code
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserShopAssignmentServlet.java (Java source file)
  - Purpose: Remote service interface for managing user-shop assignments in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserShopAssignmentServletAsync.java (Java source file)
  - Purpose: Asynchronous interface for user-shop assignment operations in GWT client code
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserRoleServlet.java (Java source file)
  - Purpose: Remote service interface for managing user roles and permissions
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UnknownAreaCodeServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for managing unknown area codes in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/SystemTrackingServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for system tracking and analysis operations
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/ServiceServletAsync.java (Java source file)
  - Purpose: Asynchronous service interface for managing services in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/ServiceServlet.java (Java source file)
  - Purpose: Remote service interface for handling service-related operations in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/UserRoleServletAsync.java (Java source file)
  - Purpose: Asynchronous interface for user and role management operations
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/service/CCTOrgStructureElementServletAsync.java (Java source file)
  - Purpose: Asynchronous interface for managing organizational structure elements
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddCreditTypeEvent.java (Java source file)
  - Purpose: Event class for handling credit type addition operations in the admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/SelectRolesEvent.java (Java source file)
  - Purpose: Event class for handling role selection operations in the admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamMemberEvent.java (Java source file)
  - Purpose: Event class for handling team member addition operations in the admin UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddUnknownAreaCodeEvent.java (Java source file)
  - Purpose: Event handler class for adding unknown area codes in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/GwtAddTeamMembersEvent.java (Java source file)
  - Purpose: Event handler class for adding team members in the GWT-based administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamEvent.java (Java source file)
  - Purpose: Event handler class for adding teams in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/CuCoEventType.java (Java source file)
  - Purpose: Defines event types for the CuCo administration UI system as an enumeration
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddServicesEvent.java (Java source file)
  - Purpose: Represents an event for adding services in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/RemoveServicesEvent.java (Java source file)
  - Purpose: Represents an event for removing services in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/AddTeamMembersEvent.java (Java source file)
  - Purpose: Event class for handling the addition of team members in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/RoleEvent.java (Java source file)
  - Purpose: Event class for handling role-related operations in the administration UI
- administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/ProductgroupEvent.java (Java source file)
  - Purpose: Event class for handling product group operations in the administration UI
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplExtended.java (Java source file)
  - Purpose: Extends GWT's PopupImpl to provide custom z-index handling for popup elements
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/Util.java (Java source file)
  - Purpose: Provides utility functions and fixes for GXT framework components
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplMozillaExtended.java (Java source file)
  - Purpose: Extends Mozilla-specific popup implementation to provide custom z-index handling
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PagingGridContainer.java (Java source file)
  - Purpose: Extends GridContainer to provide pagination functionality for grid displays
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilterField.java (Java source file)
  - Purpose: Provides filtering functionality for memory-based data proxies
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ButtonRenderer.java (Java source file)
  - Purpose: Renders buttons within grid cells with associated actions
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ProxyFilter.java (Java source file)
  - Purpose: Defines an interface for proxy filters that can be bound to data loaders in a GXT UI framework
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/NumberFieldFixed.java (Java source file)
  - Purpose: Provides a workaround implementation for number field issues in GWT 2.1 with GXT 2.1.2
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/DetailsDialog.java (Java source file)
  - Purpose: Implements a dialog component for displaying details in a GXT-based UI
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/FilterablePagingMemoryProxy.java (Java source file)
  - Purpose: Implements a paging proxy for in-memory data with filtering capabilities for GXT grid components
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/BaseFilterableMemoryProxy.java (Java source file)
  - Purpose: Provides base functionality for filtering in-memory data in GXT components
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/LinkCellRenderer.java (Java source file)
  - Purpose: Renders clickable links in GXT grid cells
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/GridContainer.java (Java source file)
  - Purpose: A container component that extends ContentPanel to provide grid functionality with selection and filtering capabilities
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/FilterableMemoryProxy.java (Java source file)
  - Purpose: Interface defining filtering capability for memory-based data proxies
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/ComboBoxFix.java (Java source file)
  - Purpose: Extension of GXT ComboBox that handles expansion errors gracefully
- administration.ui/src/main/java/at/a1ta/framework/gxt/ui/PopupImplIE6Extended.java (Java source file)
  - Purpose: Extends IE6 popup implementation to ensure proper z-index handling for popup elements
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/EsbBrianDaoBeanConverterTest.java (Java source file)
  - Purpose: Test class for validating conversions between PayableTicket and credit request objects
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/ITestESBLocationService.java (Java source file)
  - Purpose: Integration test class for ESB Location Service functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/AbstractParametrizedESBDaoTest.java (Java source file)
  - Purpose: Abstract base test class for ESB DAO implementations that require parameters
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/CustomerInventoryTest.java (Java source file)
  - Purpose: Test class for customer inventory ESB operations
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/EsbBrianDaoTest.java (Java source file)
  - Purpose: Test class for Brian ESB DAO implementation
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/ITestDefaultPartnerCenterLandingPageDao.java (Java source file)
  - Purpose: Integration test class for testing Partner Center landing page DAO functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/ITestESBPartyService.java (Java source file)
  - Purpose: Integration test class for ESB Party Service implementation
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/esb/ITestProductBrowser.java (Java source file)
  - Purpose: Integration test class for Product Browser functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/util/PhoneNumberParserTest.java (Java source file)
  - Purpose: Unit test class for validating phone number parsing functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/cusco/impl/HttpPostCusCoDaoTest.java (Java source file)
  - Purpose: Test class for CusCo DAO HTTP POST operations
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/solr/SolrPartyQueryHelperTest.java (Java source file)
  - Purpose: Test class for Solr query construction for party searches
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/solr/SolrPartyRepositoryWithPhoneNumbersTest.java (Java source file)
  - Purpose: Unit test class for testing Solr repository functionality related to party entities with phone numbers
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/solr/SolrPartyRepositoryTest.java (Java source file)
  - Purpose: Unit test class for testing basic Solr repository operations for party entities
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/solr/AbstractSolrRepositoryTest.java (Java source file)
  - Purpose: Abstract base class for Solr repository test classes providing common test infrastructure
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/db/impl/SalesInfoDaoImplTest.java (Java source file)
  - Purpose: Unit test class for SalesInfoDaoImpl to verify sales information data access operations
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/db/impl/MyNotesDaoImplTest.java (Java source file)
  - Purpose: Unit test class for MyNotesDaoImpl to verify user notes data access operations
- cuco-core/src/test/java/at/a1ta/cuco/core/dao/db/impl/CustomerUnlockRequestDaoImplTest.java (Java source file)
  - Purpose: Unit test class for CustomerUnlockRequestDaoImpl to verify customer unlock request operations
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/dto/IndexationStatusTest.java (Java source file)
  - Purpose: Unit test class to verify the functionality of IndexationStatus enum conversion methods
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/HousenumberValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for house numbers
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/CityValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for city names
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/FirstnameValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for first names
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/ZipCodeValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for postal/ZIP codes
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/AONNumberValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for AON numbers
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/StreetValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for street addresses
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/PartyIdValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for party identifiers
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/LastnameValidatorTest.java (Java source file)
  - Purpose: Unit test class to verify the validation logic for last names
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/PhonenumberValidatorTest.java (Java source file)
  - Purpose: Unit test class for validating phone number formats
- cuco-core/src/test/java/at/a1ta/cuco/core/shared/validator/BANValidatorTest.java (Java source file)
  - Purpose: Unit test class for validating Bank Account Numbers (BAN)
- cuco-core/src/test/java/at/a1ta/cuco/core/service/FlashInfoServiceTest.java (Java source file)
  - Purpose: Unit test class for Flash Info Service functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/InvoiceServiceTest.java (Java source file)
  - Purpose: Unit test suite for the InvoiceService class to verify invoice processing functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/CustomerAssignmentServiceTest.java (Java source file)
  - Purpose: Unit test suite for CustomerAssignmentService to verify customer contract assignment functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/IMailServiceTest.java (Java source file)
  - Purpose: Integration test suite for mail service implementation
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/AccessTokenServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for AccessTokenService implementation that handles authentication token management
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/UnknownAreaCodeServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for service handling unknown area codes in telecommunications context
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/KumsCustomerServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for KUMS customer service implementation handling customer data
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/CustomerUnlockServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for the CustomerUnlockService implementation that handles customer account unlocking functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/PayableTicketServiceImplTest.java (Java source file)
  - Purpose: Test suite for PayableTicketService implementation that handles ticket payment processing
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/IAutoVvlServiceImplTest.java (Java source file)
  - Purpose: Test implementation for AutoVvlService that handles automated VVL (likely contract extension) operations
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/GamificationHttpServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for GamificationHttpService implementation that tests gamification-related HTTP service functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/ProductBrowserServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for ProductBrowserService implementation that validates product browsing functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/BillingCycleServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for BillingCycleService implementation that validates billing cycle operations
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/CustomerInteractionServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for CustomerInteractionService implementation
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/LocationServiceImplTests.java (Java source file)
  - Purpose: Unit test suite for LocationService implementation
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/ClearingAccountServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for ClearingAccountService implementation
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/ContactPersonServiceImplTest.java (Java source file)
  - Purpose: Unit test suite for ContactPersonServiceImpl class that verifies contact person management functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/PartyServiceTest.java (Java source file)
  - Purpose: Unit test suite for PartyService implementation to verify party management functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/impl/IAttributeServiceImplTest.java (Java source file)
  - Purpose: Integration test suite for AttributeService implementation using Spring context
- cuco-core/src/test/java/at/a1ta/cuco/core/service/visitreport/VisitReportServiceImplTest.java (Java source file)
  - Purpose: Unit tests for VisitReportService implementation, focusing on digital selling functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/customerequipment/CustomerEquipmentHelperTest.java (Java source file)
  - Purpose: Unit tests for CustomerEquipmentHelper utility class
- cuco-core/src/test/java/at/a1ta/cuco/core/service/report/ITestUserActionStatistics.java (Java source file)
  - Purpose: Integration test class for user action statistics functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/report/DepartmentActionStatisticsTest.java (Java source file)
  - Purpose: Test class for validating department-level action statistics reporting functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/report/UserActionStatisticsTest.java (Java source file)
  - Purpose: Test class for validating user-level action statistics reporting functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/report/UserActionStatisticsTestBase.java (Java source file)
  - Purpose: Base test class providing common functionality for action statistics testing
- cuco-core/src/test/java/at/a1ta/cuco/core/service/cron/DataTheftRapidAlertJobTest.java (Java source file)
  - Purpose: Test class for validating the DataTheftRapidAlert job functionality
- cuco-core/src/test/java/at/a1ta/cuco/core/service/cron/IKumsSkzShopSynchronizationJobTest.java (Java source file)
  - Purpose: Test class for validating shop synchronization job functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/configuration/MetricsConfiguration.java (Java source file)
  - Purpose: Configuration class for metrics collection and monitoring setup
- cuco-core/src/main/java/at/a1ta/cuco/core/bean/Reporting.java (Java source file)
  - Purpose: Represents a reporting entity that contains query and metadata information for generating reports
- cuco-core/src/main/java/at/a1ta/cuco/core/bean/KeyableBean.java (Java source file)
  - Purpose: Defines contract for beans that have a unique identifier
- cuco-core/src/main/java/at/a1ta/cuco/core/bean/File.java (Java source file)
  - Purpose: Represents a file entity with MIME type support for various file formats
- cuco-core/src/main/java/at/a1ta/cuco/core/bean/ReportingWhitelist.java (Java source file)
  - Purpose: Provides GWT RPC whitelisting functionality for report-related classes that need to be serialized
- cuco-core/src/main/java/at/a1ta/cuco/core/bean/PWUTokenResponse.java (Java source file)
  - Purpose: Data transfer object for PWU (presumably Payment Web Unit) token response information
- cuco-core/src/main/java/at/a1ta/cuco/core/healthcheck/SolrHealthCheck.java (Java source file)
  - Purpose: Health check implementation for Solr service monitoring
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/billingcycle/DefaultBillingCycleDao.java (Java source file)
  - Purpose: Implementation of billing cycle data access operations extending AbstractDao
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/billingcycle/BillingCycleDao.java (Java source file)
  - Purpose: Interface defining billing cycle data access operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianCeeQueryOrderDaoImpl.java (Java source file)
  - Purpose: Implementation of ESB query order operations for BrianCee system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/MobilPointsDaoImpl.java (Java source file)
  - Purpose: Implementation of data access layer for handling MobilPoints service interactions through ESB
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianDao.java (Java source file)
  - Purpose: Interface defining data access operations for Brian service
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianDaoImpl.java (Java source file)
  - Purpose: Implementation of Brian service data access operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/EsbPartyDao.java (Java source file)
  - Purpose: Interface defining data access operations for ESB party-related functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/CustomerAssignmentDaoImpl.java (Java source file)
  - Purpose: Implementation of customer assignment data access operations for ESB integration
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BusinessHardwareReplacementDaoImpl.java (Java source file)
  - Purpose: Implementation of business hardware replacement operations through ESB
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/MobilPointsDao.java (Java source file)
  - Purpose: Data access interface for retrieving mobile points information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/KUMSCommonDao.java (Java source file)
  - Purpose: Data access interface for retrieving point of sale information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/EsbPartyDaoImpl.java (Java source file)
  - Purpose: Implementation of ESB party data access operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/CustomerAssignmentDao.java (Java source file)
  - Purpose: Interface defining data access operations for customer contract assignments
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/KUMSCommonDaoImpl.java (Java source file)
  - Purpose: Implementation class for ESB-based data access operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/PartnerCenterLandingPageDao.java (Java source file)
  - Purpose: Interface for partner center landing page authentication and access operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianCeeQueryOrderDao.java (Java source file)
  - Purpose: Interface for querying order information from Brian Cee system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BusinessHardwareReplacementDao.java (Java source file)
  - Purpose: Interface for retrieving business hardware replacement information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/PartnerCenterLandingPageDaoImpl.java (Java source file)
  - Purpose: Implementation of partner center landing page data access
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/OracleArrayTypeHandler.java (Java source file)
  - Purpose: Handles conversion between Java List objects and Oracle Array types for iBatis database operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/ListStringTypeHandler.java (Java source file)
  - Purpose: Handles conversion between Java List<String> objects and delimited string values for iBatis database operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/YNNullableBooleanTypeHandler.java (Java source file)
  - Purpose: Handles conversion between Java Boolean objects and Y/N character values in database, supporting null values
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/YNBooleanTypeHandler.java (Java source file)
  - Purpose: Custom iBATIS type handler to convert between Java Boolean values and Y/N database representations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/IdxStatusDBMappingHandler.java (Java source file)
  - Purpose: Custom iBATIS type handler for mapping IndexationStatus enum values to database representations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/BooleanTypeHandler.java (Java source file)
  - Purpose: Custom iBATIS type handler to convert between Java Boolean values and 1/0 database representations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/VIPStatusHandler.java (Java source file)
  - Purpose: Custom type handler for mapping VIP status values between database and Java objects in iBatis
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/BrianCeeQueryOrderStub.java (Java source file)
  - Purpose: Stub class for handling Brian CEE query order web service interactions
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/PhoneNumberParser.java (Java source file)
  - Purpose: Utility class for parsing and validating phone numbers
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/cusco/CusCoResponse.java (Java source file)
  - Purpose: Represents the response structure for customer communication operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/cusco/CusCoDao.java (Java source file)
  - Purpose: Data Access Object interface for customer communication operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/cusco/impl/HttpPostCusCoDao.java (Java source file)
  - Purpose: HTTP POST implementation of the CusCoDao interface
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyRepository.java (Java source file)
  - Purpose: Interface defining repository operations for Party entities in Solr search
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyQueryHelper.java (Java source file)
  - Purpose: Helper class to build Solr queries for Party entity searches
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyRepositoryWithPhoneNumbers.java (Java source file)
  - Purpose: Extended repository implementation for Party entities with phone number handling
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyQuery.java (Java source file)
  - Purpose: Defines search query fields and functionality for party/customer data in Solr search engine
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CustomerUnlockRequestDao.java (Java source file)
  - Purpose: Data access interface for managing customer unlock requests
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/InventoryDao.java (Java source file)
  - Purpose: Data access interface for managing customer inventory and bindings
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SingleTurnaroundDao.java (Java source file)
  - Purpose: Data access interface for managing single turnaround operations in the clearing and settlement system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ChargingTypeDao.java (Java source file)
  - Purpose: Data access interface for managing charging types in the billing system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ClearingAccountDao.java (Java source file)
  - Purpose: Data access interface for managing clearing accounts in the settlement system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyToDoNotesDao.java (Java source file)
  - Purpose: Data Access Object interface for managing to-do notes in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UnknownAreaCodeDao.java (Java source file)
  - Purpose: Data Access Object interface for handling unknown area codes
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CreditTypeDao.java (Java source file)
  - Purpose: Data Access Object interface for managing credit types
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/PartyDao.java (Java source file)
  - Purpose: Data access interface for managing party/customer related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UITextsEditorDAO.java (Java source file)
  - Purpose: Data access interface for managing UI text content
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ReportingDao.java (Java source file)
  - Purpose: Data access interface for handling reporting functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MKInteractionDao.java (Java source file)
  - Purpose: Data access interface for managing marketing interactions
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyQuoteDao.java (Java source file)
  - Purpose: Data access interface for managing opportunities and quotes
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/StandardAddressDao.java (Java source file)
  - Purpose: Data access interface for managing standard addresses
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/InventoryProductGroupDao.java (Java source file)
  - Purpose: Data access interface for managing inventory product group operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UserShopAssignmentDao.java (Java source file)
  - Purpose: Data access interface for managing user-shop assignments and their audit logs
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ServiceDao.java (Java source file)
  - Purpose: Data access interface for service-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ImageSizeDao.java (Java source file)
  - Purpose: Data access interface for managing image size configurations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ProductHierarchyDao.java (Java source file)
  - Purpose: Data access interface for retrieving product hierarchy information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CucoLogsDao.java (Java source file)
  - Purpose: Data access interface for system logging operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/LocationDao.java (Java source file)
  - Purpose: Data access interface for managing location-related data in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/InvoiceDao.java (Java source file)
  - Purpose: Data access interface for managing invoice-related operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/PhoneNumberDao.java (Java source file)
  - Purpose: Data access interface for managing phone number related operations and queries
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/LinksPortletDao.java (Java source file)
  - Purpose: Data access object for managing links portlet data in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SalesInfoDao.java (Java source file)
  - Purpose: Data access object for managing sales information and notes in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/FlashInfoDao.java (Java source file)
  - Purpose: Data access object for managing flash information/notifications in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/AttributeDao.java (Java source file)
  - Purpose: Data access interface for managing attribute configurations and history
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CustomerBlockDao.java (Java source file)
  - Purpose: Data access interface for managing customer blocking functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ContactPersonDao.java (Java source file)
  - Purpose: Data access interface for managing contact person information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ImageDao.java (Java source file)
  - Purpose: Data access object interface for handling image-related database operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/PayableTicketDao.java (Java source file)
  - Purpose: Data access object interface for managing payable tickets in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/GamificationLocalDAO.java (Java source file)
  - Purpose: Data access interface for managing local gamification data and messages
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/VbmProductsDao.java (Java source file)
  - Purpose: Data access interface for managing VBM (Value Based Management) products and related information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/TurnoverDao.java (Java source file)
  - Purpose: Data access interface for retrieving turnover information for parties
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyNotesDao.java (Java source file)
  - Purpose: Data access interface for managing sales information notes with filtering capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CCTOrgStructureElementDao.java (Java source file)
  - Purpose: Data access interface for managing organizational structure elements in CCT system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UserInfoStatisticsDao.java (Java source file)
  - Purpose: Data access interface for user statistics information
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/TeamDao.java (Java source file)
  - Purpose: Data access interface for team management operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/VIPHistoryDao.java (Java source file)
  - Purpose: Data access interface for managing VIP customer history records
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UsageDataDao.java (Java source file)
  - Purpose: Data access interface for retrieving customer usage data across different services
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CategoryDao.java (Java source file)
  - Purpose: Data access interface for managing customer categories or classifications
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CmDBICTServiceDao.java (Java source file)
  - Purpose: Data access interface for retrieving ICT services associated with a party/customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SettingsEditorDAO.java (Java source file)
  - Purpose: Data access interface for managing system settings
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SegmentDao.java (Java source file)
  - Purpose: Data access interface for segment-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ClearingAccountDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing clearing account operations in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/TeamDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing team-related operations in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CmDBICTServiceDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing ICT service information from CmDB
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/StandardAddressDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing standard addresses in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ProductHierarchyDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing product hierarchy data
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/PartyDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing party-related data
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CategoryDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing category entities
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MyQuoteDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing quote-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ImageDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing image entities
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MKInteractionDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing customer interactions in the MK system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/PayableTicketDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing payable tickets
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MyToDoNotesDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing to-do notes
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ServiceDaoImpl.java (Java source file)
  - Purpose: Data access implementation for Service entities in the CUCO core system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/InventoryDaoImpl.java (Java source file)
  - Purpose: Data access implementation for inventory management in the CUCO core system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UsageDataDaoImpl.java (Java source file)
  - Purpose: Data access implementation for usage data tracking in the CUCO core system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/PhoneNumberDaoImpl.java (Java source file)
  - Purpose: Data access implementation for phone number related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/InventoryProductGroupDaoImpl.java (Java source file)
  - Purpose: Data access implementation for inventory product group management
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CreditTypeDaoImpl.java (Java source file)
  - Purpose: Data access implementation for credit type management
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/TurnoverDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing turnover records in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/LocationDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing location data in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/InvoiceDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing invoice records in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SegmentDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing Segment entities in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ContactPersonDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing ContactPerson entities in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CCTOrgStructureElementDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing CCT organizational structure elements in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ReportingDaoImpl.java (Java source file)
  - Purpose: Data access implementation for handling reporting data operations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UserInfoStatisticsDaoImpl.java (Java source file)
  - Purpose: Data access implementation for user information statistics
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ChargingTypeDaoImpl.java (Java source file)
  - Purpose: Data access implementation for charging types management
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CustomerBlockDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing customer blocks related to flash info
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/FlashInfoDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing flash info entities with batch processing capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SettingsEditorDAOImpl.java (Java source file)
  - Purpose: Data access implementation for managing application settings
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SalesInfoDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing sales-related information including appointments, competitor notes, and other sales data
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ImageSizeDaoImpl.java (Java source file)
  - Purpose: Data access implementation for retrieving image size configurations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/GamificationLocalDAOImpl.java (Java source file)
  - Purpose: Data access implementation for handling gamification-related data operations locally
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UITextsEditorDAOImpl.java (Java source file)
  - Purpose: Data access implementation for managing UI text content in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/LinksPortletDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing link portlet data in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UnknownAreaCodeDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing unknown area codes in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SingleTurnaroundDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing single turnaround operations in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/VbmProductsDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing VBM (Value Based Management) products and decline reasons
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MyNotesDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing user notes with search functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CucoLogsDaoImpl.java (Java source file)
  - Purpose: Data access implementation for handling CUCO system logs
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/AttributeDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing customer attributes
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CustomerUnlockRequestDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing customer unlock requests
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UserShopAssignmentDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing user-shop assignments in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/VIPHistoryDaoImpl.java (Java source file)
  - Purpose: Data access implementation for managing VIP history records in the database
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/SetupTypeSetTypeHandler.java (Java source file)
  - Purpose: Custom type handler for converting SetupType sets between Java and database representations
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/VisitReportDaoImpl.java (Java source file)
  - Purpose: Implementation of data access operations for visit reports in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/ToDoGroupStatusHandler.java (Java source file)
  - Purpose: Handles conversion between database and application representations of ToDo group statuses
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/VisitReportDao.java (Java source file)
  - Purpose: Interface defining data access operations for visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/LinksPortlet.java (Java source file)
  - Purpose: Represents a portlet containing link information with authentication requirements
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductOfferingTypeHandler.java (Java source file)
  - Purpose: Custom type handler for ProductOffering objects in iBatis SQL mapping
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AttributeHistory.java (Java source file)
  - Purpose: Tracks historical changes to attributes with various value types
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ContactPerson.java (Java source file)
  - Purpose: Represents a contact person entity associated with a customer in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Message.java (Java source file)
  - Purpose: Represents a message entity in the system with copyright information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Granularity.java (Java source file)
  - Purpose: Defines time-based granularity levels for data analysis or reporting
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/GamificationRequest.java (Java source file)
  - Purpose: Data transfer object for gamification-related requests
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AggregatedInventoryProductGroupUsage.java (Java source file)
  - Purpose: Represents aggregated usage data for inventory product groups with associated parties
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/BillingCycleEntry.java (Java source file)
  - Purpose: Represents a billing cycle period with associated metadata
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InventoryProductGroupAssignable.java (Java source file)
  - Purpose: Defines an interface for objects that can be assigned to inventory product groups
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/NotesFilter.java (Java source file)
  - Purpose: Provides filtering capabilities for sales information notes and todo items
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CreditType.java (Java source file)
  - Purpose: Represents a type of credit in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SingleTurnaround.java (Java source file)
  - Purpose: Represents a single financial transaction or turnaround event for a customer
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Salesstage.java (Java source file)
  - Purpose: Manages the lifecycle and status of a sales process
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Party.java (Java source file)
  - Purpose: Represents a party entity that extends customer functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/LocationPlaceholder.java (Java source file)
  - Purpose: Represents a placeholder location object with default invalid ID values
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Tupel.java (Java source file)
  - Purpose: Generic tuple implementation for storing two values of different types
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Team.java (Java source file)
  - Purpose: Represents a team entity with members and metadata
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Image.java (Java source file)
  - Purpose: Data transfer object for representing image metadata in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/MyOpportunity.java (Java source file)
  - Purpose: Data transfer object for business opportunities or leads
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/StandardAddress.java (Java source file)
  - Purpose: Data transfer object for standardized address information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SalesConvEmailData.java (Java source file)
  - Purpose: Data transfer object for email communication data in sales conversations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PointOfSaleInfo.java (Java source file)
  - Purpose: Data transfer object representing point of sale information for dealers
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PhoneNumberStructure.java (Java source file)
  - Purpose: Data transfer object for structured phone number representation
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Product.java (Java source file)
  - Purpose: Represents a product entity with hierarchical structure and inventory group assignment capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/EsbParty.java (Java source file)
  - Purpose: Represents a party entity in the ESB (Enterprise Service Bus) system with address information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/BANCollection.java (Java source file)
  - Purpose: Manages a collection of Billing Account Numbers (BANs) associated with a party
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/MobileChurnLikeliness.java (Java source file)
  - Purpose: Data transfer object for representing mobile customer churn likelihood information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Customer.java (Java source file)
  - Purpose: Data transfer object representing customer information with business and personal details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/IndexationStatus.java (Java source file)
  - Purpose: Enumeration defining possible states for product indexation status
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Inventory.java (Java source file)
  - Purpose: Represents inventory data for customer assets and contracts in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Segment.java (Java source file)
  - Purpose: Defines segments for categorizing or grouping data in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Invoice.java (Java source file)
  - Purpose: Manages invoice data and provides invoice comparison functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Auth.java (Java source file)
  - Purpose: Defines authorization/permission constants for the application
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/BillingAccountNumber.java (Java source file)
  - Purpose: Represents a billing account with associated brands and phone numbers
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ToDoNotesFilter.java (Java source file)
  - Purpose: Defines filtering criteria for TODO notes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ContractOwnerAssignment.java (Java source file)
  - Purpose: Represents the assignment of billing accounts to a party/contract owner
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyCustomerLoyaltyInfo.java (Java source file)
  - Purpose: Manages customer loyalty information status for a party
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyProfileNPSInfo.java (Java source file)
  - Purpose: Stores Net Promoter Score (NPS) information for a party profile
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Category.java (Java source file)
  - Purpose: Data transfer object representing a category entity with basic metadata
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ClearingAccount.java (Java source file)
  - Purpose: DTO representing a clearing account for invoice and payment processing
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SelectedProductOffering.java (Java source file)
  - Purpose: Wrapper class for product offerings with selection state
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InsuranceBrokerInfo.java (Java source file)
  - Purpose: Represents information about an insurance broker with status tracking capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CustomerFilter.java (Java source file)
  - Purpose: Defines filtering criteria for customer data queries
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductGroup.java (Java source file)
  - Purpose: Represents a group of products with metadata and tracking information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AttributeConfig.java (Java source file)
  - Purpose: Data transfer object for storing attribute configuration settings
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CustomerBlock.java (Java source file)
  - Purpose: Data transfer object representing a customer block entity
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SearchResultComparator.java (Java source file)
  - Purpose: Comparator implementation for sorting Party objects in search results
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartySearch.java (Java source file)
  - Purpose: Data transfer object for searching party/customer information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyAdditionalInfo.java (Java source file)
  - Purpose: Container for various party/customer related information components
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyDeclarationOfConsentInfo.java (Java source file)
  - Purpose: Manages information about customer consent status
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/OverviewStatus.java (Java source file)
  - Purpose: Defines possible status values for overview displays in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/VipExport.java (Java source file)
  - Purpose: Defines constants and configuration for VIP data export functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/BindingsFilter.java (Java source file)
  - Purpose: Defines filtering criteria for contract bindings
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductDetailFilter.java (Java source file)
  - Purpose: Defines a filter structure for querying product details with various search criteria
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CucoLogs.java (Java source file)
  - Purpose: Represents logging data structure for customer-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductFeasibilityStatus.java (Java source file)
  - Purpose: Defines possible states for product installation feasibility
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UIText.java (Java source file)
  - Purpose: Represents a key-value pair for UI text elements, likely used for internationalization or dynamic text content
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InsuranceBrokerContractInfo.java (Java source file)
  - Purpose: Stores information about insurance broker contracts related to devices
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InventoryProductGroupAssignation.java (Java source file)
  - Purpose: Manages the association between inventory product groups and products
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CrmAuthenticationInfo.java (Java source file)
  - Purpose: Manages CRM authentication state and credentials information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductOffering.java (Java source file)
  - Purpose: Defines available product offerings with associated IDs and codes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AccessToken.java (Java source file)
  - Purpose: Manages access token information for target systems
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ServiceClassInfo.java (Java source file)
  - Purpose: Represents service class information with status indicators and descriptive text
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/BusinessOffer.java (Java source file)
  - Purpose: Represents a business offer with customer and product information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InventoryProductGroupUsage.java (Java source file)
  - Purpose: Tracks usage information for inventory product groups
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UnknownAreaCode.java (Java source file)
  - Purpose: Exception class to handle unknown area code scenarios
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Turnover.java (Java source file)
  - Purpose: Data transfer object for representing turnover/revenue information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Person.java (Java source file)
  - Purpose: Data transfer object for representing person information with Solr integration
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/QuoteClearanceConfigurationHolder.java (Java source file)
  - Purpose: Holds configuration data for quote clearance including product offerings and roles
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyProfileInfo.java (Java source file)
  - Purpose: Manages party profile information with status tracking capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ReadOnlyStatusBasedOnCategory.java (Java source file)
  - Purpose: Defines enumeration for edit permissions based on category
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/GamificationMessageComparator.java (Java source file)
  - Purpose: Provides comparison functionality for GamificationMessage objects based on timestamps
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/MatrixPosition.java (Java source file)
  - Purpose: Represents a position in a matrix structure with generic type support
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Service.java (Java source file)
  - Purpose: Represents a service entity with associated properties and validity period
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/GamificationData.java (Java source file)
  - Purpose: Data transfer object for gamification-related data in the CuCo system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/GamificationResponse.java (Java source file)
  - Purpose: Response object for gamification-related operations containing status and data
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ChargingType.java (Java source file)
  - Purpose: Represents charging type configuration for mobile services
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyProfileSolvency.java (Java source file)
  - Purpose: Represents solvency/credit information for a party profile in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InventoryProductGroup.java (Java source file)
  - Purpose: Represents a grouping of inventory products with visibility and ordering properties
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartySummaryPrintModel.java (Java source file)
  - Purpose: Models printable summary information for a party
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UserInfoStatistics.java (Java source file)
  - Purpose: Data transfer object for aggregating user-related statistics and metrics
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SupportingUnit.java (Java source file)
  - Purpose: Represents a supporting organizational unit with status tracking capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CMBuddyLogin.java (Java source file)
  - Purpose: Data transfer object for handling login credentials
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/MyFlashInfo.java (Java source file)
  - Purpose: Data transfer object for flash message information with party/creator details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/VipStatus.java (Java source file)
  - Purpose: Represents VIP status information with state and numeric value
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductLevel.java (Java source file)
  - Purpose: Represents hierarchical product level structure with inventory group assignment capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/FlashInfo.java (Java source file)
  - Purpose: Represents flash information/notification data structure with time bounds and customer blocks
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Recipient.java (Java source file)
  - Purpose: Defines a recipient entity for message or notification delivery
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/VIPHistoryEntry.java (Java source file)
  - Purpose: Tracks historical changes to VIP customer status
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartnerCenterAccessTokenRequest.java (Java source file)
  - Purpose: Represents a request object for obtaining access tokens specific to Partner Center authentication
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/RTCode.java (Java source file)
  - Purpose: Represents a rate/tariff code entity with product and sales information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/GamificationCuCoMessages.java (Java source file)
  - Purpose: Manages gamification-related messages for customer care operations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CustomerBinding.java (Java source file)
  - Purpose: Represents a binding between a customer and their product/service contracts
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Attribute.java (Java source file)
  - Purpose: Manages customer attribute data with configuration settings
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/MatrixData.java (Java source file)
  - Purpose: Manages matrix-structured data for segments, categories, and product groups
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/FlashInfoBase.java (Java source file)
  - Purpose: Represents a flash message or notification with role-based visibility control
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/KumsCustomerInfo.java (Java source file)
  - Purpose: Stores VIP status and change tracking information for customers
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PayableTicket.java (Java source file)
  - Purpose: Represents a billable ticket or service request with customer and service details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SimplePage.java (Java source file)
  - Purpose: Generic pagination data transfer object for handling paginated results
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CuCoGamificationLoginMessage.java (Java source file)
  - Purpose: Data transfer object for gamification login credentials and session information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UserAdminSegment.java (Java source file)
  - Purpose: Data transfer object for user administration feature segmentation
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ImageSize.java (Java source file)
  - Purpose: Represents dimensions and metadata for an image resource
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductHierarchy.java (Java source file)
  - Purpose: Represents a hierarchical product structure with multiple levels of categorization
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CrmAuthenticationPasswordInfo.java (Java source file)
  - Purpose: Stores authentication password information for CRM system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductOverviewConfigurations.java (Java source file)
  - Purpose: Stores configuration settings for product overview display and filtering
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CustomerInteractionAttributes.java (Java source file)
  - Purpose: Defines enumeration of possible customer interaction attribute types
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/BillingCycle.java (Java source file)
  - Purpose: Represents a billing cycle period with associated billing entries
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UserShopAssignment.java (Java source file)
  - Purpose: Represents an assignment between a user and a shop in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PhoneNumber.java (Java source file)
  - Purpose: Represents phone number details with associated telecommunications information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/GamificationMessage.java (Java source file)
  - Purpose: Represents a gamification-related message or notification in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/OpportunityFilter.java (Java source file)
  - Purpose: Defines filtering criteria for opportunity/quote searches
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UserShopAssignmentLogLine.java (Java source file)
  - Purpose: Represents a log entry for user shop assignment activities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AccessTokenRequest.java (Java source file)
  - Purpose: Manages access token request data between systems
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductFeasibility.java (Java source file)
  - Purpose: Represents the feasibility status of a product in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/freeunits/FreeUnits.java (Java source file)
  - Purpose: Manages free units/quota information with standardized unit definitions
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/freeunits/FreeUnitsData.java (Java source file)
  - Purpose: Aggregates free units information across different grouping levels
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/freeunits/FreeUnitsResult.java (Java source file)
  - Purpose: Data transfer object for representing free units/minutes information in a telecom system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/access/ContextAwareCustomerUnlockRequest.java (Java source file)
  - Purpose: Request object for customer unlock operations with contextual information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/access/UnlockRequestContext.java (Java source file)
  - Purpose: Defines context information for unlock requests in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/access/UnlockStateEnum.java (Java source file)
  - Purpose: Enumeration defining possible unlock states for access control
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/DateValueBean.java (Java source file)
  - Purpose: Data transfer object for representing a date-value pair
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/UsageDetail.java (Java source file)
  - Purpose: Data transfer object for representing detailed usage information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/AonProduct.java (Java source file)
  - Purpose: Represents an AON (All Optical Network) product with associated details and phone number information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/Product.java (Java source file)
  - Purpose: Defines contract for product-related functionality across the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/MobileUsage.java (Java source file)
  - Purpose: Tracks mobile service usage metrics including data, duration, and fees
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/NetworkProvider.java (Java source file)
  - Purpose: Defines network provider enumeration for telecom services
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/ProductType.java (Java source file)
  - Purpose: Defines product types for telecom services
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/InetUsage.java (Java source file)
  - Purpose: Represents internet usage data and associated fees
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/VoiceUsage.java (Java source file)
  - Purpose: Represents voice call usage data with duration, fees and classification details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/ProductNode.java (Java source file)
  - Purpose: Defines a node in a product hierarchy structure with party and phone number information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/ProductChartRequest.java (Java source file)
  - Purpose: Represents a request for product chart data with filtering criteria
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/ProductRootNode.java (Java source file)
  - Purpose: Represents a wrapper class for the root product node in a product hierarchy structure
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/nbo/VBMProductDetails.java (Java source file)
  - Purpose: Defines product details for Value Based Management (VBM) functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/nbo/VBMProductFeedback.java (Java source file)
  - Purpose: Manages feedback data for products in Value Based Management system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/nbo/VBMProduct.java (Java source file)
  - Purpose: Data transfer object for representing VBM (Value Based Management) product information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/nbo/VBMDeclineReason.java (Java source file)
  - Purpose: Data transfer object for representing reasons for declining a VBM product
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffSimulationContainer.java (Java source file)
  - Purpose: Container class for tariff simulation data and results
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/Price.java (Java source file)
  - Purpose: Represents a price entity with gross and net values for tariff-related calculations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffLists.java (Java source file)
  - Purpose: Manages collections of tariffs, separating all available tariffs from recommended ones
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffSimulation.java (Java source file)
  - Purpose: Handles tariff simulation functionality for A1 Telekom Austria AG
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/Tariff.java (Java source file)
  - Purpose: Represents a tariff model for pricing and product configuration
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffCharacteristic.java (Java source file)
  - Purpose: Defines specific characteristics and pricing attributes for tariffs
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/ContributionMargin.java (Java source file)
  - Purpose: Manages contribution margin calculations and indicators for tariffs
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffSimulationRequest.java (Java source file)
  - Purpose: Represents a request object for tariff simulation calculations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/mobilpoints/MobilPointsBundle.java (Java source file)
  - Purpose: Manages mobile points and hardware replacement information for a phone number
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/mobilpoints/BusinessHardwareReplacement.java (Java source file)
  - Purpose: Manages business hardware replacement details and calculations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/mobilpoints/MobilPoints.java (Java source file)
  - Purpose: Data transfer object for managing mobile points across different systems
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/chart/ChartData.java (Java source file)
  - Purpose: Generic container for chart data sets with key-value mappings
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/chart/ChartDataSet.java (Java source file)
  - Purpose: Represents a single data set within a chart with generic key-value pairs
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/chart/Chart.java (Java source file)
  - Purpose: Represents a chart image file with associated image map functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/chart/ChartOptions.java (Java source file)
  - Purpose: Defines configuration options for chart rendering
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/chart/ChartMetaData.java (Java source file)
  - Purpose: Stores metadata associated with a chart image
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/chart/ChartColor.java (Java source file)
  - Purpose: Defines a set of predefined colors for chart visualization with RGB values
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/marketingproduct/ProductMoveAction.java (Java source file)
  - Purpose: Defines possible directional movements for product positioning
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/marketingproduct/MarketingProductGroup.java (Java source file)
  - Purpose: Categorizes marketing products into main and additional product types
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/DefaultProductNode.java (Java source file)
  - Purpose: Represents a default product node in a hierarchical product structure with serialization support
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/NodeHelper.java (Java source file)
  - Purpose: Utility class providing helper methods for node operations and traversal
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/ProductHeaderNode.java (Java source file)
  - Purpose: Defines a header node for product-related information display
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SubscriptionHeaderNode.java (Java source file)
  - Purpose: Defines base interface for node objects in a tree structure for product-related data
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SAPSubscriptionNode.java (Java source file)
  - Purpose: Represents SAP-specific subscription information extending base subscription functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/Node.java (Java source file)
  - Purpose: Manages subscription header information with detailed addressing and identification
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoComponentProductPrice.java (Java source file)
  - Purpose: Represents pricing information for a component product including tax and indexation details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CCTSupervisorSelect.java (Java source file)
  - Purpose: Manages supervisor approval information for CCT processes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/Promotion.java (Java source file)
  - Purpose: Represents promotional offers with discount information and validity periods
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/PhysicalResourceNode.java (Java source file)
  - Purpose: Represents a physical resource node in a product hierarchy with text description
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/PartyNode.java (Java source file)
  - Purpose: Represents a party (entity) node in a product hierarchy with contact details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/DefaultSubscriptionType.java (Java source file)
  - Purpose: Defines standard subscription types available in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/AccountAware.java (Java source file)
  - Purpose: Interface defining contract for objects that have account awareness/association
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CallNumber.java (Java source file)
  - Purpose: Data transfer object representing a telephone number with country code, area code and number components
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/DefaultSubscriptionNode.java (Java source file)
  - Purpose: Default implementation of subscription node representing a customer subscription
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/BillableUser.java (Java source file)
  - Purpose: Represents a billable user entity for product-related functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/BaseNode.java (Java source file)
  - Purpose: Implements hierarchical node structure for contract/product organization
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/Coordinates.java (Java source file)
  - Purpose: Represents geographical coordinates with longitude and latitude
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/LastMileId.java (Java source file)
  - Purpose: Represents an identifier for last mile connectivity components in telecommunications
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/GetPartySummaryResponse.java (Java source file)
  - Purpose: Response object for party summary retrieval operations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SAPProductNode.java (Java source file)
  - Purpose: Represents a node in SAP product hierarchy with equipment attributes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/MetaData.java (Java source file)
  - Purpose: Manages metadata entries in both list and map formats for product-related information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoProductPriceBase.java (Java source file)
  - Purpose: Base class for product pricing information with core identifier and naming attributes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoProdPriceCharge.java (Java source file)
  - Purpose: Represents product price charges with specific charge types like recurring or usage-based
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CCTClearanceStage.java (Java source file)
  - Purpose: Represents a clearance stage for product offerings in a customer care tool
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/EmptyProductNode.java (Java source file)
  - Purpose: Represents a placeholder node for when no products are available
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/AccountNode.java (Java source file)
  - Purpose: Represents an account node in the product hierarchy
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/ProductTree.java (Java source file)
  - Purpose: Represents a hierarchical structure of products with associated locations and party nodes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/GeoCallNumber.java (Java source file)
  - Purpose: Represents a geographical telephone number with country code, area code, and number components
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/Location.java (Java source file)
  - Purpose: Represents a physical or virtual location with associated addressing and type information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SAPPhysicalResourceNode.java (Java source file)
  - Purpose: Represents a physical resource node in SAP with equipment attributes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/BRKAccountInfo.java (Java source file)
  - Purpose: Represents account information for BRK (likely Broker) system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoProdPriceAlterations.java (Java source file)
  - Purpose: Manages product price alterations including discounts and allowances
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CCTOrgStructureElement.java (Java source file)
  - Purpose: Represents an organizational structure element in the CCT system with user hierarchy and approval information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/LocationNode.java (Java source file)
  - Purpose: Represents a node in a location hierarchy tree structure
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/AsyncPlaceholderNode.java (Java source file)
  - Purpose: Provides a placeholder node for asynchronously loaded content in a tree structure
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoPrice.java (Java source file)
  - Purpose: Represents a price value with currency units in the CuCo system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CCTAuthorizedQuoteApproversForLevel.java (Java source file)
  - Purpose: Manages approvers for quotes at specific organizational levels
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/MetaDataEntryType.java (Java source file)
  - Purpose: Defines allowed types for metadata entries in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SubscriptionTree.java (Java source file)
  - Purpose: Represents a hierarchical structure of subscription and product nodes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/AutoVvlInfo.java (Java source file)
  - Purpose: Manages automatic contract extension information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SubscriptionNode.java (Java source file)
  - Purpose: Represents a subscription node in the product hierarchy
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/MetaDataEntry.java (Java source file)
  - Purpose: Represents metadata information for products with temporal validity
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/PartySummaryItem.java (Java source file)
  - Purpose: Represents a summary item for party-related information with count or URL
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/Equipment.java (Java source file)
  - Purpose: Represents hierarchical equipment data with parent-child relationships
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/EquipmentTree.java (Java source file)
  - Purpose: Represents a hierarchical structure of equipment with associated summaries and party information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/EquipmentAttribute.java (Java source file)
  - Purpose: Represents an attribute associated with a specific piece of equipment
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/EquipmentSum.java (Java source file)
  - Purpose: Provides a summary representation of equipment with count information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/EquipmentConsignee.java (Java source file)
  - Purpose: Represents a consignee/recipient entity for equipment with address and identification details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/DummyEquipmentConsignee.java (Java source file)
  - Purpose: Provides a dummy implementation of EquipmentConsignee for testing or placeholder purposes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/HistoryNote.java (Java source file)
  - Purpose: Represents historical notes with different levels and types for sales information tracking
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/VisitReportSuccessorExistsException.java (Java source file)
  - Purpose: Custom exception class to handle cases where a visit report already has a successor
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/FeedbackQuestionsRow.java (Java source file)
  - Purpose: Data transfer object for storing feedback question responses with different value types
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SimpleNote.java (Java source file)
  - Purpose: Represents a basic note type in the sales information system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesInfoNote.java (Java source file)
  - Purpose: Base class for sales information notes that provides common functionality for tracking sales-related information and notes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/AppointmentNote.java (Java source file)
  - Purpose: Represents a sales appointment note with communication and contact details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesConvProductNoteRow.java (Java source file)
  - Purpose: Represents a row of product-related information in a sales conversation note
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesInfoNoteHistoryModificationType.java (Java source file)
  - Purpose: Defines the possible modification types for sales information note history tracking
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SbsNoteReportRow.java (Java source file)
  - Purpose: Represents a row in an SBS note report with communication and contact details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesInfoNoteHistory.java (Java source file)
  - Purpose: Tracks historical changes to sales information notes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/Task.java (Java source file)
  - Purpose: Represents a task entity in the sales information system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesConvNoteReportRow.java (Java source file)
  - Purpose: Represents a row in the sales conversation note report
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/CompetitorNote.java (Java source file)
  - Purpose: Represents competitor-related notes in the sales information system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesInfoOverviewRow.java (Java source file)
  - Purpose: Abstract base class for sales information overview rows that provides common functionality for UI display
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/ToDoGroupNote.java (Java source file)
  - Purpose: Represents a group note for todo items related to sales processing tasks
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SmartHomeNew.java (Java source file)
  - Purpose: Represents smart home product configuration and pricing information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SecurityOld.java (Java source file)
  - Purpose: Represents legacy security product configuration for digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedNew.java (Java source file)
  - Purpose: Manages new internet speed product configurations with protection features
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariff.java (Java source file)
  - Purpose: Defines mobile tariff data structure for digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariffNew.java (Java source file)
  - Purpose: Represents a new mobile tariff configuration for digital selling, extending base mobile tariff functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/ServicesOld.java (Java source file)
  - Purpose: Defines legacy service configurations for digital selling platform
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SecurityBase.java (Java source file)
  - Purpose: Provides base security configuration for digital selling functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariffBase.java (Java source file)
  - Purpose: Base class for mobile tariff data transfer objects in digital selling context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedOld.java (Java source file)
  - Purpose: Represents legacy internet speed configuration with virus protection options
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/Payment.java (Java source file)
  - Purpose: Represents payment information for digital selling transactions
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SecurityNew.java (Java source file)
  - Purpose: Represents new security product offerings with pricing and configuration details
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SmartHomeOld.java (Java source file)
  - Purpose: Manages legacy smart home product offerings and pricing information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobilePhoneBase.java (Java source file)
  - Purpose: Base class for mobile phone product offerings and configurations
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedMainUseType.java (Java source file)
  - Purpose: Defines enumeration of internet usage categories for digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/Household.java (Java source file)
  - Purpose: Represents household information for digital selling context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/TV.java (Java source file)
  - Purpose: Represents television service information for digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MusicSpeakerType.java (Java source file)
  - Purpose: Defines an enumeration of music speaker/headphone types for digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/ServicesNew.java (Java source file)
  - Purpose: Represents new service offerings in digital selling system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariffOld.java (Java source file)
  - Purpose: Represents legacy mobile tariff configurations in digital selling system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SummaryItem.java (Java source file)
  - Purpose: Represents a summary item in a digital selling visit report with serialization support
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobilePhoneMainUseType.java (Java source file)
  - Purpose: Defines enumeration of primary mobile phone usage categories
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedType.java (Java source file)
  - Purpose: Defines enumeration of available internet speed tiers
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeed.java (Java source file)
  - Purpose: Represents internet speed measurements in a digital selling context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/DigitalSellingNote.java (Java source file)
  - Purpose: Represents digital selling notes and related information for visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MusicApp.java (Java source file)
  - Purpose: Defines available music application options for digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/TVOld.java (Java source file)
  - Purpose: Represents a legacy TV service data transfer object in the digital selling visit report system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/Security.java (Java source file)
  - Purpose: Represents security-related information in digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetType.java (Java source file)
  - Purpose: Defines the available types of internet connections for digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedBase.java (Java source file)
  - Purpose: Base class for representing internet speed information in digital selling context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobilePhoneOld.java (Java source file)
  - Purpose: Legacy class for handling mobile phone sales information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/PaymentOld.java (Java source file)
  - Purpose: Legacy class for handling payment information in digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/ServicesBase.java (Java source file)
  - Purpose: Base DTO class for digital selling services information in visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobilePhone.java (Java source file)
  - Purpose: DTO for mobile phone related information in digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SmartHome.java (Java source file)
  - Purpose: DTO for smart home related information in digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/Services.java (Java source file)
  - Purpose: Represents a data transfer object for services information in digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/TVType.java (Java source file)
  - Purpose: Defines the available types of TV service delivery methods
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/TVNew.java (Java source file)
  - Purpose: Represents a new TV service configuration in digital selling
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/TVBase.java (Java source file)
  - Purpose: Data transfer object for TV-related information in digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SmartHomeBase.java (Java source file)
  - Purpose: Data transfer object for smart home product information in digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/HouseholdType.java (Java source file)
  - Purpose: Enumeration defining types of households for digital selling context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariffMainUseType.java (Java source file)
  - Purpose: Defines enumeration of main usage types for mobile tariffs in digital selling context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobilePhoneNew.java (Java source file)
  - Purpose: Represents a new mobile phone offering in digital selling context with payment options
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/PaymentNew.java (Java source file)
  - Purpose: Manages payment information for digital selling transactions
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/Music.java (Java source file)
  - Purpose: Represents music-related information for digital selling visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/Country.java (Java source file)
  - Purpose: Represents country information for SBS (Service Business System) visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SetupType.java (Java source file)
  - Purpose: Defines the types of setup operations in SBS visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/HandlingAssigneeType.java (Java source file)
  - Purpose: Defines the types of entities that can be assigned to handle tasks or requests in the SBS system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSOrgUnit.java (Java source file)
  - Purpose: Represents an organizational unit within the SBS system with address and identification information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/CommunicationType.java (Java source file)
  - Purpose: Defines the possible types of communication methods in the SBS system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/ContactSource.java (Java source file)
  - Purpose: Defines the possible sources/origins of a sales contact in the SBS system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSProductNote.java (Java source file)
  - Purpose: Represents product-specific notes for SBS visit reports
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSProduct.java (Java source file)
  - Purpose: Defines the structure and properties of a product in the SBS system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SetupCategory.java (Java source file)
  - Purpose: Defines categories for different types of setup operations in a sales/service context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSNote.java (Java source file)
  - Purpose: Represents a structured note for SBS (seems to be a sales/business system) with various attributes and relationships
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/QuoteStatus.java (Java source file)
  - Purpose: Defines possible states for a quote in the sales process
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/ContactType.java (Java source file)
  - Purpose: Defines the types of contact interactions in a visit report system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/VisitReportDetail.java (Java source file)
  - Purpose: Represents detailed information about a visit report entry
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/CommunicationChannel.java (Java source file)
  - Purpose: Defines the direction of communication in a visit report
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSProductNoteConfig.java (Java source file)
  - Purpose: Defines configuration for SBS product notes containing product and organizational unit lists
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/generic/GenericNote.java (Java source file)
  - Purpose: Represents a generic note type in the sales information system with file attachment support
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/generic/FileAttachment.java (Java source file)
  - Purpose: Represents an attached file in the sales information system
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/salesconvnote/SalesConvNote.java (Java source file)
  - Purpose: Represents a sales conversation note with associated attributes and attachments
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/salesconvnote/TeamEmailAdminGroup.java (Java source file)
  - Purpose: Manages team email administration group information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/salesconvnote/ProductHistoryItem.java (Java source file)
  - Purpose: Tracks historical information about product-related activities
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/salesconvnote/ContactType.java (Java source file)
  - Purpose: Defines the types of contact methods used in sales conversation notes
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/PhonenumberValidator.java (Java source file)
  - Purpose: Validates phone number formats (implementation incomplete)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/PartyIdValidator.java (Java source file)
  - Purpose: Validates party identification numbers according to specific format rules
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/BANValidator.java (Java source file)
  - Purpose: Validates Bank Account Numbers (BAN) according to specific format rules
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/OfferNumberValidator.java (Java source file)
  - Purpose: Validates offer numbers, though currently implements no specific validation rules
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/LastnameValidator.java (Java source file)
  - Purpose: Validates last names according to minimum length requirements
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/ZipCodeValidator.java (Java source file)
  - Purpose: Validates postal/zip code format according to specific length and digit requirements
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/HousenumberValidator.java (Java source file)
  - Purpose: Validates house number format with permissive rules
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/OneTVUserValidator.java (Java source file)
  - Purpose: Validates OneTV user identifiers against a specified pattern
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/BvkUserValidator.java (Java source file)
  - Purpose: Validates user input against a specified pattern
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/FirstnameValidator.java (Java source file)
  - Purpose: Validates first name input
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/StreetValidator.java (Java source file)
  - Purpose: Validates street address input
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/AONNumberValidator.java (Java source file)
  - Purpose: Validates AON (Assumed Office Number) format according to specific rules
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/CityValidator.java (Java source file)
  - Purpose: Validates city name inputs according to length requirements
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/CommonValidator.java (Java source file)
  - Purpose: Provides common validation utilities used across different validators
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/PartyModel.java (Java source file)
  - Purpose: Represents a customer/party entity with personal and business information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/DualSegment.java (Java source file)
  - Purpose: Defines customer segment classifications for dual service offerings
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/PartyModelFactory.java (Java source file)
  - Purpose: Factory class for creating PartyModel instances from various data sources
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/AddressLinkData.java (Java source file)
  - Purpose: Represents a data structure for storing address information in a serializable format
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/productdetail/ProductDetail.java (Java source file)
  - Purpose: Defines a product detail model containing comprehensive product information
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/seg/MultiPartyMatrixData.java (Java source file)
  - Purpose: Manages a matrix structure for multi-party product group relationships
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/seg/MultiPartyProductGroup.java (Java source file)
  - Purpose: Manages product group data across multiple parties in a business context
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/contactperson/ContactPersonComparator.java (Java source file)
  - Purpose: Provides comparison logic for sorting ContactPerson objects
- cuco-core/src/main/java/at/a1ta/cuco/core/audit/CuCoAuditEvent.java (Java source file)
  - Purpose: Handles audit event logging for the CuCo system
- cuco-core/src/main/java/at/a1ta/cuco/core/audit/CuCoAuditScope.java (Java source file)
  - Purpose: Defines audit scope categories for the CuCo application's auditing system
- cuco-core/src/main/java/at/a1ta/cuco/core/audit/CuCoAuditAttribute.java (Java source file)
  - Purpose: Defines audit attributes for tracking changes and activities in the CuCo system
- cuco-core/src/main/java/at/a1ta/cuco/core/audit/CuCoAuditActivity.java (Java source file)
  - Purpose: Defines auditable activities for tracking user or system actions in the CuCo system
- cuco-core/src/main/java/at/a1ta/cuco/core/audit/ContextAwareAuditHelper.java (Java source file)
  - Purpose: Provides auditing functionality with context awareness for tracking system activities
- cuco-core/src/main/java/at/a1ta/cuco/core/export/CSVFieldFormater.java (Java source file)
  - Purpose: Handles formatting of individual CSV fields according to RFC4180 standards
- cuco-core/src/main/java/at/a1ta/cuco/core/export/CSVRowFormater.java (Java source file)
  - Purpose: Handles formatting of complete CSV rows with configurable separators
- cuco-core/src/main/java/at/a1ta/cuco/core/export/DateFormater.java (Java source file)
  - Purpose: Provides date formatting functionality for export operations
- cuco-core/src/main/java/at/a1ta/cuco/core/export/TableContent.java (Java source file)
  - Purpose: Manages tabular data structure for export operations
- cuco-core/src/main/java/at/a1ta/cuco/core/export/Formater.java (Java source file)
  - Purpose: Defines the contract for formatting objects in the export system
- cuco-core/src/main/java/at/a1ta/cuco/core/export/ExportContent.java (Java source file)
  - Purpose: Defines an interface for formatting and managing exportable content with customizable formatting rules
- cuco-core/src/main/java/at/a1ta/cuco/core/export/BooleanFormater.java (Java source file)
  - Purpose: Implements boolean value formatting with customizable true/false string representations
- cuco-core/src/main/java/at/a1ta/cuco/core/export/NullFormater.java (Java source file)
  - Purpose: Provides formatting logic for handling null values in exports
- cuco-core/src/main/java/at/a1ta/cuco/core/service/VIPHistoryService.java (Java source file)
  - Purpose: Manages VIP customer history and status tracking
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ProductBrowserService.java (Java source file)
  - Purpose: Manages product catalog browsing and subscription information
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CustomerInteractionService.java (Java source file)
  - Purpose: Manages customer interactions and communication history
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CustomerEquipmentService.java (Java source file)
  - Purpose: Service interface for managing customer equipment and related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/UserShopAssignmentService.java (Java source file)
  - Purpose: Service interface for managing user-shop assignments and relationships
- cuco-core/src/main/java/at/a1ta/cuco/core/service/BillingCycleService.java (Java source file)
  - Purpose: Service interface for managing billing cycles and related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PartyProfileService.java (Java source file)
  - Purpose: Interface defining methods to retrieve party profile information from different user systems
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CustomerUnlockService.java (Java source file)
  - Purpose: Interface providing access to Point of Sale (POS) data in the KUMS system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/KUMSCommonService.java (Java source file)
  - Purpose: Service interface related to customer unlocking functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/VBMProductsService.java (Java source file)
  - Purpose: Service interface for managing VBM (Value Based Management) product data
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CucoLogsService.java (Java source file)
  - Purpose: Service interface for handling logging operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/AttributeService.java (Java source file)
  - Purpose: Service interface for managing attribute configurations and history
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CdPersonService.java (Java source file)
  - Purpose: Interface defining services for retrieving person information from CD (Customer Data) system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/DuposMobileSignatureService.java (Java source file)
  - Purpose: Interface for handling mobile signature operations through DUPOS system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CrmAuthenticationService.java (Java source file)
  - Purpose: Interface for CRM authentication and customer information retrieval
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PartySearchValueFormatHelper.java (Java source file)
  - Purpose: Helper component for formatting and standardizing party search values, particularly phone numbers
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ProductAdminService.java (Java source file)
  - Purpose: Service interface for product administration functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/POSService.java (Java source file)
  - Purpose: Service interface for Point of Sale (POS) operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/UnknownAreaCodeService.java (Java source file)
  - Purpose: Service interface for handling unknown area codes in the telecommunications system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/FreeUnitService.java (Java source file)
  - Purpose: Service interface for managing free unit allocations in the telecommunications system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/LinksPortletService.java (Java source file)
  - Purpose: Service interface for managing and retrieving links in a portlet system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/UITextsEditorService.java (Java source file)
  - Purpose: Interface defining operations for managing UI text content in the application
- cuco-core/src/main/java/at/a1ta/cuco/core/service/EsbPartyService.java (Java source file)
  - Purpose: Interface for retrieving party information from ESB (Enterprise Service Bus)
- cuco-core/src/main/java/at/a1ta/cuco/core/service/GamificationLocalService.java (Java source file)
  - Purpose: Interface for managing gamification messages locally
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ImageSizeService.java (Java source file)
  - Purpose: Service for managing and validating image sizes in the application
- cuco-core/src/main/java/at/a1ta/cuco/core/service/KumsCustomerService.java (Java source file)
  - Purpose: Service interface for managing customer data from KUMS (Customer Management System)
- cuco-core/src/main/java/at/a1ta/cuco/core/service/SalesInfoService.java (Java source file)
  - Purpose: Service interface for managing sales information, appointments, and competitor notes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/SettingsEditorService.java (Java source file)
  - Purpose: Interface defining operations for managing application settings
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CustomerBlockService.java (Java source file)
  - Purpose: Service interface related to customer blocking functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/FlashInfoService.java (Java source file)
  - Purpose: Service interface for managing flash information/notifications
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ChargingTypeService.java (Java source file)
  - Purpose: Service interface for managing charging types in the billing/charging system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ReportingService.java (Java source file)
  - Purpose: Service interface for generating and managing reports
- cuco-core/src/main/java/at/a1ta/cuco/core/service/UserInfoStatisticsService.java (Java source file)
  - Purpose: Service interface for managing user information statistics
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CCTOrgStructureElementService.java (Java source file)
  - Purpose: Interface defining operations for managing organizational structure elements in the CCT system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ContactPersonService.java (Java source file)
  - Purpose: Service interface for managing contact person functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CuCoGamificationPlainWebsocketEndPoint.java (Java source file)
  - Purpose: WebSocket endpoint implementation for gamification features
- cuco-core/src/main/java/at/a1ta/cuco/core/service/MarketplaceInventoryService.java (Java source file)
  - Purpose: Interface defining marketplace inventory management operations for retrieving account and subscription information
- cuco-core/src/main/java/at/a1ta/cuco/core/service/LocationService.java (Java source file)
  - Purpose: Service interface for location-related operations within A1 Telekom Austria system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/InvoiceService.java (Java source file)
  - Purpose: Interface defining invoice management and retrieval operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/TurnoverService.java (Java source file)
  - Purpose: Service interface for managing turnover-related operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CreditTypeService.java (Java source file)
  - Purpose: Service interface for managing credit type operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/InsuranceBrokerCpiService.java (Java source file)
  - Purpose: Service interface for retrieving insurance broker CPI (Consumer Price Index) contract information
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PhoneNumberService.java (Java source file)
  - Purpose: Service interface for managing phone number related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/UsageDataService.java (Java source file)
  - Purpose: Service interface for retrieving various types of usage data for telecommunications services
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PartyDeclarationOfConsentService.java (Java source file)
  - Purpose: Service interface for managing GDPR-related consent declarations for parties
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PartyCustomerLoyaltyService.java (Java source file)
  - Purpose: Interface defining service operations for managing customer loyalty information for parties
- cuco-core/src/main/java/at/a1ta/cuco/core/service/AccessTokenService.java (Java source file)
  - Purpose: Interface for managing access token operations and authentication services
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ServiceService.java (Java source file)
  - Purpose: Service interface for A1 Telekom Austria AG business operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/AutoVvlService.java (Java source file)
  - Purpose: Interface defining services for retrieving automatic VVL (likely customer verification) information using different identifiers
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PayableTicketService.java (Java source file)
  - Purpose: Service interface for managing payable tickets in the A1 Telekom Austria system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PromotionService.java (Java source file)
  - Purpose: Interface for retrieving customer subscription promotions based on call numbers
- cuco-core/src/main/java/at/a1ta/cuco/core/service/InsuranceBrokerHsiService.java (Java source file)
  - Purpose: Interface defining services for handling insurance broker HSI (Home Service Interface) related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ImageService.java (Java source file)
  - Purpose: Service interface for image handling operations within A1 Telekom Austria system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/MasterSessionControlService.java (Java source file)
  - Purpose: Interface for managing master session control and DOC home URL generation
- cuco-core/src/main/java/at/a1ta/cuco/core/service/MobilPointsService.java (Java source file)
  - Purpose: Service interface for handling mobile points functionality (full implementation details not visible in preview)
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CMBuddyHttpService.java (Java source file)
  - Purpose: Interface defining HTTP service operations for buddy link functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/CuscoUnlockService.java (Java source file)
  - Purpose: Interface for managing customer unlock operations and signature processes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/PartyService.java (Java source file)
  - Purpose: Service interface for managing party-related operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/GamificationHttpService.java (Java source file)
  - Purpose: Interface defining HTTP service operations for gamification features
- cuco-core/src/main/java/at/a1ta/cuco/core/service/BrkServiceClient.java (Java source file)
  - Purpose: Interface for accessing BRK (likely Billing/Revenue/Knowledge) account information
- cuco-core/src/main/java/at/a1ta/cuco/core/service/TeamService.java (Java source file)
  - Purpose: Interface defining team management operations for the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/ClearingAccountService.java (Java source file)
  - Purpose: Service interface for managing clearing account operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/PayableTicketServiceImpl.java (Java source file)
  - Purpose: Implementation of service handling payable tickets
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ContactPersonServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing contact person operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/KumsCustomerServiceImpl.java (Java source file)
  - Purpose: Implementation of customer service integration with KUMS web service
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/MobilPointsServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling mobile points operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ImageServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling image-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/NoteMailHelper.java (Java source file)
  - Purpose: Helper class for handling email operations related to sales info notes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/MasterSessionControlServiceImpl.java (Java source file)
  - Purpose: Implementation of session control service for master data
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/BusinessHardwareReplacementCallable.java (Java source file)
  - Purpose: Handles asynchronous business hardware replacement operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/UITextsEditorServiceImpl.java (Java source file)
  - Purpose: Implements service layer for managing UI text content
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/PhoneNumberServiceImpl.java (Java source file)
  - Purpose: Implements service layer for phone number management
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/PartyDeclarationOfConsentServiceImpl.java (Java source file)
  - Purpose: Handles party declarations of consent for GDPR compliance
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/SettingsEditorServiceImpl.java (Java source file)
  - Purpose: Manages application settings editing functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CdPersonServiceImpl.java (Java source file)
  - Purpose: Manages customer/person data operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/TeamServiceImpl.java (Java source file)
  - Purpose: Implements team management functionality including CRUD operations and team member management
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ReportingServiceImpl.java (Java source file)
  - Purpose: Generates Excel reports for business data analysis
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CustomerInteractionServiceImpl.java (Java source file)
  - Purpose: Manages customer interactions and workflow processing
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/VIPHistoryServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing VIP customer history records
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/MobilPointsCallable.java (Java source file)
  - Purpose: Callable implementation for asynchronous mobile points retrieval
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ImageSizeServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing image size configurations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/LocationServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing location-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/BillingCycleServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing billing cycle operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CustomerUnlockServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing customer unlock operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ChargingTypeServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing charging types in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/LinksPortletServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing links portlet functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/PartyCustomerLoyaltyServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing party customer loyalty operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/KUMSCommonServiceImpl.java (Java source file)
  - Purpose: Service implementation for KUMS (likely Knowledge/User Management System) common operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/MailService.java (Java source file)
  - Purpose: Service for handling email operations with date/time formatting capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CustomerBlockServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing customer blocking functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CCTOrgStructureElementServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing organizational structure elements in the CCT system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ProductAdminServiceImpl.java (Java source file)
  - Purpose: Service implementation for product administration functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/SalesInfoServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing sales information and user-related sales data
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CreditTypeServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing credit type operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ServiceServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing generic service operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/FlashInfoServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing flash information operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/KumsAccountService.java (Java source file)
  - Purpose: Service for retrieving account information from KUMS (Telekom account management system)
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/UsageDataServiceImpl.java (Java source file)
  - Purpose: Implementation of usage data service for managing internet usage information
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/UserShopAssignmentServiceImpl.java (Java source file)
  - Purpose: Implementation of service managing user-shop assignments
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CustomerAssignmentService.java (Java source file)
  - Purpose: Manages customer contract assignments and ownership relationships
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/PartyProfileServiceImpl.java (Java source file)
  - Purpose: Implements party profile management functionality with file handling capabilities
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/BrkServiceClientImpl.java (Java source file)
  - Purpose: Implements BRK service client functionality with calendar operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/ClearingAccountServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing clearing accounts in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CrmAuthenticationServiceImpl.java (Java source file)
  - Purpose: Implementation of authentication service for CRM integration
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/GamificationHttpServiceImpl.java (Java source file)
  - Purpose: Implementation of HTTP service for gamification features
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/GamificationLocalServiceImpl.java (Java source file)
  - Purpose: Implements local gamification service functionality for customer engagement features
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CMBuddyHttpServiceImpl.java (Java source file)
  - Purpose: Implements HTTP client service for CM Buddy system integration
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/VBMProductsServiceImpl.java (Java source file)
  - Purpose: Implements service layer for VBM (Value-Based Management) products functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/FreeUnitServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing free units/minutes for telecommunications services
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/AccessTokenServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing authentication access tokens
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/InvoiceServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling invoice-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/EsbPartyServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling ESB party-related operations and data mapping
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/DuposMobileSignatureServiceImpl.java (Java source file)
  - Purpose: Implementation of mobile signature service using DUPOS system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/UnknownAreaCodeServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling unknown area code scenarios
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/AutoVvlServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling automatic VVL (likely insurance-related) operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/InsuranceBrokerHsiServiceImpl.java (Java source file)
  - Purpose: Implementation of insurance broker HSI (Host System Interface) service for handling insurance contract operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/UserInfoStatisticsServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing user information statistics
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/POSServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling Point of Sale (POS) related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/AttributeServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing attributes with user context
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/TurnoverServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing turnover operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/PartyServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing party-related operations in the CUCO system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/InsuranceBrokerCpiServiceImpl.java (Java source file)
  - Purpose: Implementation of insurance broker CPI (Customer Program Interface) services
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CuscoUnlockServiceImpl.java (Java source file)
  - Purpose: Service implementation for handling CUSCO system unlocking operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/MarketplaceInventoryServiceImpl.java (Java source file)
  - Purpose: Service implementation for managing marketplace inventory operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/impl/CucoLogsServiceImpl.java (Java source file)
  - Purpose: Implementation of logging service for CUCO application
- cuco-core/src/main/java/at/a1ta/cuco/core/service/visitreport/VisitReportPrintService.java (Java source file)
  - Purpose: Service for generating and formatting visit reports for printing
- cuco-core/src/main/java/at/a1ta/cuco/core/service/visitreport/VisitReportServiceImpl.java (Java source file)
  - Purpose: Implementation of visit report service handling digital selling note generation and processing
- cuco-core/src/main/java/at/a1ta/cuco/core/service/visitreport/DigitalSellingNotePrintModel.java (Java source file)
  - Purpose: Data model for digital selling note printing information
- cuco-core/src/main/java/at/a1ta/cuco/core/service/visitreport/VisitReportService.java (Java source file)
  - Purpose: Interface defining visit report service operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/util/JasperUtil.java (Java source file)
  - Purpose: Utility class for Jasper reporting functionality, though implementation appears minimal
- cuco-core/src/main/java/at/a1ta/cuco/core/service/util/ImageUtil.java (Java source file)
  - Purpose: Utility class for image processing operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/util/ReportUtil.java (Java source file)
  - Purpose: Utility class for report generation functionality
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/CustomerEquipmentHelper.java (Java source file)
  - Purpose: Helper class for processing and transforming customer equipment data
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/CustomerEquipmentServiceImpl.java (Java source file)
  - Purpose: Implementation of customer equipment service handling core business logic
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/CustomerEquipmentExcelHelper.java (Java source file)
  - Purpose: Helper class for generating Excel reports of customer equipment data
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/CustomerEquipmentTranslator.java (Java source file)
  - Purpose: Translates customer equipment data between different formats and handles equipment-related transformations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/PartySummaryServiceImpl.java (Java source file)
  - Purpose: Implements party summary service functionality for customer equipment management
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/PromotionServiceImpl.java (Java source file)
  - Purpose: Implements promotion service functionality for customer equipment
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/ProductBrowserServiceImpl.java (Java source file)
  - Purpose: Implementation of product browsing functionality for customer equipment management
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/MetaDataHelper.java (Java source file)
  - Purpose: Helper class for managing metadata related to customer equipment
- cuco-core/src/main/java/at/a1ta/cuco/core/service/customerequipment/PartySummaryService.java (Java source file)
  - Purpose: Interface defining party summary operations for customer equipment
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyNotesServiceImpl.java (Java source file)
  - Purpose: Interface defining operations for managing sales info notes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyNotesService.java (Java source file)
  - Purpose: Implementation of MyNotesService for managing sales info notes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyCustomersServiceImpl.java (Java source file)
  - Purpose: Implementation for managing customer-related operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyBindingsService.java (Java source file)
  - Purpose: Interface defining service operations for managing customer bindings
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyToDoNotesServiceImpl.java (Java source file)
  - Purpose: Interface defining service operations for managing sales-related todo notes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyToDoNotesService.java (Java source file)
  - Purpose: Implementation of MyToDoNotesService for managing sales-related todo notes
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyFlashInfosService.java (Java source file)
  - Purpose: Interface defining services for managing flash information and related party data for agents
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyQuoteServiceImpl.java (Java source file)
  - Purpose: Implementation of quote management service with opportunity tracking
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyCustomersService.java (Java source file)
  - Purpose: Interface defining customer management services with focus on support user operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyBindingsServiceImpl.java (Java source file)
  - Purpose: Implementation of service to manage customer bindings/relationships
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyFlashInfosServiceImpl.java (Java source file)
  - Purpose: Implementation of service to handle flash information/notifications
- cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyQuoteService.java (Java source file)
  - Purpose: Interface defining quote and opportunity management operations
- cuco-core/src/main/java/at/a1ta/cuco/core/service/report/UserActionStatistics.java (Java source file)
  - Purpose: Tracks and calculates statistics for user actions/activities in the system
- cuco-core/src/main/java/at/a1ta/cuco/core/service/report/DepartmentActionStatistics.java (Java source file)
  - Purpose: Manages and calculates statistics for actions at department level
- cuco-core/src/main/java/at/a1ta/cuco/core/service/report/ActionStatisticBase.java (Java source file)
  - Purpose: Base abstract class providing common functionality for action statistics
- cuco-core/src/main/java/at/a1ta/cuco/core/service/cron/DataTheftRapidAlertJob.java (Java source file)
  - Purpose: Scheduled job to process and alert on potential data theft incidents
- cuco-core/src/main/java/at/a1ta/cuco/core/service/cron/PhoneNumberCacheJob.java (Java source file)
  - Purpose: Scheduled job to manage and update phone number cache
- cuco-core/src/main/java/at/a1ta/cuco/core/service/cron/LDAPSynchronizationJob.java (Java source file)
  - Purpose: Scheduled job to synchronize data with LDAP directory
- cuco-core/src/main/java/at/a1ta/cuco/core/service/cron/SalesInfoReminderMailJob.java (Java source file)
  - Purpose: Scheduled job for sending sales information reminder emails
- cuco-core/src/main/java/at/a1ta/cuco/core/service/cron/KumsSkzShopSynchronizationJob.java (Java source file)
  - Purpose: Scheduled job for synchronizing shop data with KUMS SKZ system

## 3. Functionality
### Main Features
- Event class for handling role selection operations in the admin UI
- Data access implementation for managing single turnaround operations in the database
- Defines a product detail model containing comprehensive product information
- Implementation of logging service for CUCO application
- Represents the response structure for customer communication operations
- Interface defining operations for managing UI text content in the application
- Represents the feasibility status of a product in the system
- Represents a physical resource node in a product hierarchy with text description
- Represents a file entity with MIME type support for various file formats
- Service interface for managing free unit allocations in the telecommunications system
- Manages team service-related functionality in a panel interface
- Represents a task entity in the sales information system
- Unit test class for validating phone number parsing functionality
- Data access object for managing sales information and notes in the CUCO system
- Data access object for managing links portlet data in the CUCO system
- Abstract base class for Solr repository test classes providing common test infrastructure
- Manages the association between inventory product groups and products
- Implementation of service to manage customer bindings/relationships
- Implementation of partner center landing page data access
- Interface defining services for handling insurance broker HSI (Home Service Interface) related operations
- Interface defining repository operations for Party entities in Solr search
- Defines possible states for a quote in the sales process
- Extension of GXT ComboBox that handles expansion errors gracefully
- Implementation of insurance broker CPI (Customer Program Interface) services
- Event class for handling team member addition operations in the admin UI
- Validates party identification numbers according to specific format rules
- Represents information about an insurance broker with status tracking capabilities
- Represents hierarchical equipment data with parent-child relationships
- Service interface for retrieving various types of usage data for telecommunications services
- Custom iBATIS type handler to convert between Java Boolean values and Y/N database representations
- Data access implementation for managing invoice records in the database
- Represents service class information with status indicators and descriptive text
- Provides a summary representation of equipment with count information
- Represents a party entity that extends customer functionality
- Defines the types of contact methods used in sales conversation notes
- Exports organization structure errors to Excel format
- Custom iBATIS type handler for mapping IndexationStatus enum values to database representations
- Manages customer interactions and workflow processing
- Represents a billing cycle period with associated metadata
- Categorizes marketing products into main and additional product types
- Implementation of service handling payable tickets
- Asynchronous service interface for managing services in the administration UI
- Represents a hierarchical structure of products with associated locations and party nodes
- Data transfer object representing a customer block entity
- Dialog interface for editing role group management settings in the administration system
- Represents a billable ticket or service request with customer and service details
- Data access interface for managing marketing interactions
- Scheduled job to synchronize data with LDAP directory
- Data access implementation for managing UI text content in the database
- Data transfer object for gamification-related requests
- Represents a row of product-related information in a sales conversation note
- Data access interface for managing location-related data in the CUCO system
- Service interface for managing contact person functionality
- Interface defining service operations for managing sales-related todo notes
- Custom exception class to handle cases where a visit report already has a successor
- Represents a request object for obtaining access tokens specific to Partner Center authentication
- Interface defining HTTP service operations for buddy link functionality
- Implementation of customer service integration with KUMS web service
- Utility class for Jasper reporting functionality, though implementation appears minimal
- Defines customer segment classifications for dual service offerings
- Service interface for managing user information statistics
- Custom exception class for reporting-related errors
- Data access implementation for managing clearing account operations in the database
- Unit test suite for ProductBrowserService implementation that validates product browsing functionality
- Represents a portlet containing link information with authentication requirements
- Interface for partner center landing page authentication and access operations
- Integration test class for Product Browser functionality
- Servlet handling organizational structure element uploads
- Interface defining filtering capability for memory-based data proxies
- Service implementation for managing organizational structure elements in the CCT system
- Service implementation for handling mobile points operations
- Unit tests for VisitReportService implementation, focusing on digital selling functionality
- Provides UI panel for team management operations
- Servlet implementation for handling charging type related operations through web services
- Defines the direction of communication in a visit report
- Manages VIP customer history and status tracking
- Represents a price entity with gross and net values for tariff-related calculations
- Defines available music application options for digital selling
- Data access implementation for managing ContactPerson entities in the database
- Service interface for handling logging operations in the CUCO system
- Implementation of usage data service for managing internet usage information
- Validates AON (Assumed Office Number) format according to specific rules
- Provides base security configuration for digital selling functionality
- Service implementation for managing links portlet functionality
- Service implementation for managing attributes with user context
- Represents a message entity in the system with copyright information
- Remote service interface for handling service-related operations in the administration UI
- Dialog for managing role group assignments and configurations
- Service interface for managing charging types in the billing/charging system
- GWT-based dialog for selecting services in the web client
- Data access interface for managing system settings
- Service implementation for managing sales information and user-related sales data
- Service implementation for managing turnover operations
- Dialog component for selecting services with pagination support
- Data access implementation for managing user-shop assignments in the database
- Defines a filter structure for querying product details with various search criteria
- Custom type handler for ProductOffering objects in iBatis SQL mapping
- Represents a product entity with hierarchical structure and inventory group assignment capabilities
- Implementation of service to handle flash information/notifications
- Implementation class for ESB-based data access operations
- Abstract base class for sales information overview rows that provides common functionality for UI display
- Represents internet speed measurements in a digital selling context
- Handles local pagination functionality for data grids and lists
- Interface defining data access operations for Brian service
- Test class for validating department-level action statistics reporting functionality
- Helper class for managing metadata related to customer equipment
- Default implementation of subscription node representing a customer subscription
- Models printable summary information for a party
- Defines an interface for objects that can be assigned to inventory product groups
- Unit test class to verify the validation logic for street addresses
- Represents historical notes with different levels and types for sales information tracking
- Represents a supporting organizational unit with status tracking capabilities
- Data access interface for managing invoice-related operations in the CUCO system
- Defines the available types of internet connections for digital selling
- Manages customer attribute data with configuration settings
- Implementation of session control service for master data
- Data access implementation for managing application settings
- Data transfer object for aggregating user-related statistics and metrics
- Service implementation for product administration functionality
- Represents a row in the sales conversation note report
- Service interface for Point of Sale (POS) operations
- Represents a clearance stage for product offerings in a customer care tool
- Data access interface for managing customer blocking functionality
- Represents a hierarchical product structure with multiple levels of categorization
- Tracks historical changes to attributes with various value types
- Service interface for managing flash information/notifications
- Utility class for parsing and validating phone numbers
- DTO for smart home related information in digital selling visit reports
- Provides a workaround implementation for number field issues in GWT 2.1 with GXT 2.1.2
- Represents a hierarchical structure of subscription and product nodes
- Data access interface for managing image size configurations
- Represents a geographical telephone number with country code, area code, and number components
- Manages the display and interaction with team member data in a panel format using GXT UI components
- Validates house number format with permissive rules
- Manages subscription header information with detailed addressing and identification
- Manages party profile information with status tracking capabilities
- Data access interface for managing customer unlock requests
- Aggregates free units information across different grouping levels
- Provides formatting logic for handling null values in exports
- Data access implementation for managing customer unlock requests
- Service for handling email operations with date/time formatting capabilities
- Provides date formatting functionality for export operations
- Data access implementation for Service entities in the CUCO core system
- Service implementation for managing free units/minutes for telecommunications services
- Data transfer object for gamification-related data in the CuCo system
- Represents digital selling notes and related information for visit reports
- Implements the UI component for VIP search functionality
- Unit test class for SalesInfoDaoImpl to verify sales information data access operations
- Test class for Solr query construction for party searches
- Manages product group data across multiple parties in a business context
- Defines the possible modification types for sales information note history tracking
- Defines audit attributes for tracking changes and activities in the CuCo system
- Event class for handling the addition of team members in the administration UI
- Handles audit event logging for the CuCo system
- Implementation of HTTP service for gamification features
- Provides comparison logic for sorting ContactPerson objects
- Unit test class for MyNotesDaoImpl to verify user notes data access operations
- Comparator implementation for sorting Party objects in search results
- Manages supervisor approval information for CCT processes
- Interface defining operations for managing application settings
- Represents an identifier for last mile connectivity components in telecommunications
- Data access interface for managing local gamification data and messages
- Data access interface for managing opportunities and quotes
- Represents a default product node in a hierarchical product structure with serialization support
- Service interface for managing sales information, appointments, and competitor notes
- Data access implementation for retrieving image size configurations
- DTO representing a clearing account for invoice and payment processing
- Stores authentication password information for CRM system
- Data access interface for managing customer inventory and bindings
- Handles file uploads for user-shop assignments through HTTP servlet
- Dialog interface for creating and editing credit types in the system
- Represents a chart image file with associated image map functionality
- Remote service interface for handling unknown area code operations in the CUCO admin UI
- Provides filtering capabilities for sales information notes and todo items
- Service implementation for managing customer unlock operations
- Implementation of billing cycle data access operations extending AbstractDao
- Implements local gamification service functionality for customer engagement features
- Service implementation for managing user information statistics
- Asynchronous interface for managing organizational structure elements
- Data access implementation for managing ICT service information from CmDB
- Data access implementation for managing CCT organizational structure elements in the database
- Defines available product offerings with associated IDs and codes
- Test class for CusCo DAO HTTP POST operations
- Service for managing and validating image sizes in the application
- Custom renderer for grid columns that display interactive buttons with icons
- Service interface related to customer blocking functionality
- Validates OneTV user identifiers against a specified pattern
- Tracks and calculates statistics for user actions/activities in the system
- Defines enumeration of possible customer interaction attribute types
- Manages a matrix structure for multi-party product group relationships
- Service interface for managing customer data from KUMS (Customer Management System)
- Implements a dialog component for displaying details in a GXT-based UI
- Dialog interface for editing unknown areas codes
- Data transfer object for standardized address information
- Data transfer object for flash message information with party/creator details
- Dialog for editing unknown area codes in the system
- Represents an attached file in the sales information system
- Implementation of customer equipment service handling core business logic
- Represents a physical or virtual location with associated addressing and type information
- Implementation of product browsing functionality for customer equipment management
- Handles file upload operations through HTTP servlet
- Data access interface for retrieving customer usage data across different services
- Data access interface for managing inventory product group operations
- Generic pagination data transfer object for handling paginated results
- Central access point for common UI resources and configuration in the admin interface
- Spring-enabled servlet implementation for iBATIS database operations
- Portlet for managing credit types with clickable interface elements
- Service interface for managing clearing account operations
- Service implementation for handling invoice-related operations
- Stores VIP status and change tracking information for customers
- Dialog interface for editing messages in the system
- Extends GWT's PopupImpl to provide custom z-index handling for popup elements
- Asynchronous service interface for handling reporting operations in the web client
- Defines allowed types for metadata entries in the system
- Represents a basic note type in the sales information system
- Implements a paging proxy for in-memory data with filtering capabilities for GXT grid components
- Data access implementation for managing sales-related information including appointments, competitor notes, and other sales data
- Interface defining team management operations for the CUCO system
- Implements boolean value formatting with customizable true/false string representations
- Manages feedback data for products in Value Based Management system
- Application starter class for the PKB (Personal Knowledge Base) client application
- Data access interface for retrieving ICT services associated with a party/customer
- Defines an interface for formatting and managing exportable content with customizable formatting rules
- Data access interface for service-related operations
- Portlet for handling and displaying unknown area codes in the system
- Service implementation for managing flash information operations
- Data access implementation for managing link portlet data in the database
- Manages customer contract assignments and ownership relationships
- Data access implementation for phone number related operations
- Base class for representing internet speed information in digital selling context
- Implements service layer for VBM (Value-Based Management) products functionality
- Remote service interface definition for VIP history operations
- WebSocket endpoint implementation for gamification features
- Test suite for PayableTicketService implementation that handles ticket payment processing
- Service implementation for managing marketplace inventory operations
- Defines filtering criteria for contract bindings
- Defines a node in a product hierarchy structure with party and phone number information
- Represents a sales conversation note with associated attributes and attachments
- Defines enumeration of primary mobile phone usage categories
- Authentication servlet implementation for handling authorization requests
- Container for various party/customer related information components
- Application-specific configuration manager extending base settings functionality
- Service for generating and formatting visit reports for printing
- Service implementation for managing image size configurations
- Represents smart home product configuration and pricing information
- Utility class providing helper methods for node operations and traversal
- Defines an enumeration of music speaker/headphone types for digital selling
- Unit test class to verify the validation logic for AON numbers
- Exception class to handle unknown area code scenarios
- Manages customer/person data operations
- Asynchronous interface for user-shop assignment operations in GWT client code
- Data access implementation for managing turnover records in the database
- Represents an assignment between a user and a shop in the system
- Represents a grouping of inventory products with visibility and ordering properties
- Interface defining methods to retrieve party profile information from different user systems
- Test class for validating user-level action statistics reporting functionality
- Data access implementation for managing party-related data
- HTTP POST implementation of the CusCoDao interface
- Defines filtering criteria for TODO notes
- Implements BRK service client functionality with calendar operations
- Custom type handler for converting SetupType sets between Java and database representations
- Generates Excel reports for business data analysis
- Data access implementation for managing product hierarchy data
- Defines categories for different types of setup operations in a sales/service context
- Response object for party summary retrieval operations
- Service implementation for managing party customer loyalty operations
- Scheduled job to process and alert on potential data theft incidents
- Servlet implementation for handling organizational structure element operations in the administration UI
- Utility class for file operations
- Unit test suite for PartyService implementation to verify party management functionality
- Service interface for managing VBM (Value Based Management) product data
- Data transfer object for storing attribute configuration settings
- Extends IE6 popup implementation to ensure proper z-index handling for popup elements
- Data access implementation for managing VBM (Value Based Management) products and decline reasons
- Enumeration defining types of households for digital selling context
- Data transfer object representing customer information with business and personal details
- Data access interface for managing party/customer related operations
- Represents an account node in the product hierarchy
- Interface for managing gamification messages locally
- Handles party declarations of consent for GDPR compliance
- Data access interface for user statistics information
- Represents new security product offerings with pricing and configuration details
- Stores metadata associated with a chart image
- Data access implementation for managing payable tickets
- Translates customer equipment data between different formats and handles equipment-related transformations
- Defines segments for categorizing or grouping data in the system
- Defines possible status values for overview displays in the system
- Manages contribution margin calculations and indicators for tariffs
- Portlet for managing and displaying unknown area codes using ExtJS/GXT grid components
- Implementation of customer assignment data access operations for ESB integration
- Represents product price charges with specific charge types like recurring or usage-based
- Dialog component for selecting user roles in the application
- Defines filtering criteria for customer data queries
- Represents SAP-specific subscription information extending base subscription functionality
- Implements VIP search functionality as a portlet
- Represents a party entity in the ESB (Enterprise Service Bus) system with address information
- Data transfer object for TV-related information in digital selling visit reports
- GWT-based dialog for editing service properties
- Defines time-based granularity levels for data analysis or reporting
- Base class for mobile tariff data transfer objects in digital selling context
- Handles image rendering and display functionality for the UI
- Utility class for creating and managing portlet-style UI components with tooltips and icons
- Manages business hardware replacement details and calculations
- Legacy class for handling payment information in digital selling
- Helper class for processing and transforming customer equipment data
- Represents VIP status information with state and numeric value
- Defines the types of contact interactions in a visit report system
- Implementation of MyNotesService for managing sales info notes
- Response object for gamification-related operations containing status and data
- Defines base interface for node objects in a tree structure for product-related data
- Data access interface for managing single turnaround operations in the clearing and settlement system
- Data access implementation for handling reporting data operations
- Represents a sales appointment note with communication and contact details
- Service locator pattern implementation for managing GWT service instances in the admin UI
- Generic tuple implementation for storing two values of different types
- Represents a service entity with associated properties and validity period
- Extended repository implementation for Party entities with phone number handling
- Remote service interface for managing charging types in the system
- Data access interface for team management operations
- Application starter class for the MyCuCo client application that initializes configuration and resources
- Defines configuration for SBS product notes containing product and organizational unit lists
- Represents competitor-related notes in the sales information system
- Represents a node in a location hierarchy tree structure
- Interface defining marketplace inventory management operations for retrieving account and subscription information
- Represents a position in a matrix structure with generic type support
- Servlet implementation for handling user role management operations
- Implementation of quote management service with opportunity tracking
- Represents a row in an SBS note report with communication and contact details
- Unit test suite for BillingCycleService implementation that validates billing cycle operations
- Data access interface for retrieving mobile points information
- Portlet for displaying and managing system messages across the platform
- Unit test class for validating phone number formats
- Data transfer object for PWU (presumably Payment Web Unit) token response information
- Represents an event for removing services in the administration UI
- Stores configuration settings for product overview display and filtering
- Defines enumeration of internet usage categories for digital selling
- Data access interface for managing customer categories or classifications
- Data access interface for retrieving product hierarchy information
- Implements party summary service functionality for customer equipment management
- Represents inventory data for customer assets and contracts in the system
- Unit test class for validating Bank Account Numbers (BAN)
- Configuration class for metrics collection and monitoring setup
- Data transfer object for business opportunities or leads
- Unit test class to verify the validation logic for last names
- Represents a node in SAP product hierarchy with equipment attributes
- Manages role groups in a web client portlet interface
- Interface defining party summary operations for customer equipment
- Represents a single financial transaction or turnaround event for a customer
- Defines event types for the CuCo administration UI system as an enumeration
- Test class for customer inventory ESB operations
- Data access interface for managing attribute configurations and history
- Manages customer loyalty information status for a party
- Servlet for handling user shop assignment downloads
- Manages gamification-related messages for customer care operations
- Represents voice call usage data with duration, fees and classification details
- Integration test suite for mail service implementation
- Data access implementation for managing customer blocks related to flash info
- Service implementation for managing party-related operations in the CUCO system
- Data access implementation for managing standard addresses in the system
- Represents a key-value pair for UI text elements, likely used for internationalization or dynamic text content
- Provides comparison functionality for GamificationMessage objects based on timestamps
- Manages CRM authentication state and credentials information
- Implements servlet for managing user-shop assignments
- Data transfer object for handling login credentials
- Data access implementation for managing flash info entities with batch processing capabilities
- Health check implementation for Solr service monitoring
- Remote service interface for managing user roles and permissions
- Integration test suite for AttributeService implementation using Spring context
- Extends Mozilla-specific popup implementation to provide custom z-index handling
- Represents an AON (All Optical Network) product with associated details and phone number information
- Represents country information for SBS (Service Business System) visit reports
- Data access implementation for charging types management
- Test class for Brian ESB DAO implementation
- Interface defining data access operations for customer contract assignments
- Represents a team entity with members and metadata
- Data Access Object interface for handling unknown area codes
- Validates offer numbers, though currently implements no specific validation rules
- Interface defining customer management services with focus on support user operations
- Defines the types of entities that can be assigned to handle tasks or requests in the SBS system
- Event handler class for adding teams in the administration UI
- Manages information about customer consent status
- Manages product catalog browsing and subscription information
- Data access interface for retrieving turnover information for parties
- Service implementation for handling unknown area code scenarios
- GWT-specific implementation of role selection dialog
- Data access interface for retrieving point of sale information
- Interface for querying order information from Brian Cee system
- Represents metadata information for products with temporal validity
- Represents an attribute associated with a specific piece of equipment
- Remote service interface for managing CCT organizational structure elements
- Unit test suite for GamificationHttpService implementation that tests gamification-related HTTP service functionality
- Defines possible directional movements for product positioning
- Defines audit scope categories for the CuCo application's auditing system
- Represents a business offer with customer and product information
- Remote service interface for system tracking functionality in the CUCO admin UI
- Represents a billing cycle period with associated billing entries
- Base settings management class that handles key-value configuration storage and retrieval
- Represents geographical coordinates with longitude and latitude
- Event handler class for adding team members in the GWT-based administration UI
- Handles conversion between Java Boolean objects and Y/N character values in database, supporting null values
- Service implementation for handling automatic VVL (likely insurance-related) operations
- Stub class for handling Brian CEE query order web service interactions
- Service interface for retrieving insurance broker CPI (Consumer Price Index) contract information
- Stores Net Promoter Score (NPS) information for a party profile
- Servlet implementation for handling VIP history data and operations
- Service implementation for managing contact person operations in the CUCO system
- Integration test class for testing Partner Center landing page DAO functionality
- Implements service layer for managing UI text content
- Represents charging type configuration for mobile services
- Service implementation for managing customer blocking functionality
- Defines constants and configuration for VIP data export functionality
- Data access implementation for managing team-related operations in the database
- Service implementation for KUMS (likely Knowledge/User Management System) common operations
- Interface defining HTTP service operations for gamification features
- Manages collections of tariffs, separating all available tariffs from recommended ones
- Data access implementation for handling CUCO system logs
- Defines interface for accessing localized text strings used in admin UI
- Unit test class to verify the validation logic for house numbers
- Provides a dummy implementation of EquipmentConsignee for testing or placeholder purposes
- Defines legacy service configurations for digital selling platform
- Represents detailed information about a visit report entry
- Service interface for managing GDPR-related consent declarations for parties
- Data access implementation for usage data tracking in the CUCO core system
- Scheduled job for synchronizing shop data with KUMS SKZ system
- Dialog for creating and editing team information
- Stores information about insurance broker contracts related to devices
- Service interface for A1 Telekom Austria AG business operations
- Handles formatting of complete CSV rows with configurable separators
- Data model class for RT code information in the admin UI
- Validates street address input
- Handles file upload functionality through HTTP requests
- Service interface for managing attribute configurations and history
- Tracks historical information about product-related activities
- Data access implementation for managing location data in the database
- Base test class providing common functionality for action statistics testing
- Represents a placeholder location object with default invalid ID values
- Service interface for managing customer equipment and related operations
- Represents hierarchical product level structure with inventory group assignment capabilities
- Custom renderer for displaying service images in a grid
- Provides GWT RPC whitelisting functionality for report-related classes that need to be serialized
- Remote service interface for managing credit type operations
- Data access interface for managing phone number related operations and queries
- Test implementation for AutoVvlService that handles automated VVL (likely contract extension) operations
- Represents pricing information for a component product including tax and indexation details
- Represents a rate/tariff code entity with product and sales information
- Defines the structure and properties of a product in the SBS system
- Data access implementation for managing category entities
- Service interface for handling unknown area codes in the telecommunications system
- Interface defining operations for managing organizational structure elements in the CCT system
- Asynchronous interface for VIP history operations in GWT client code
- Defines specific characteristics and pricing attributes for tariffs
- Represents a billable user entity for product-related functionality
- Represents a tariff model for pricing and product configuration
- Data transfer object for managing mobile points across different systems
- Service implementation for managing billing cycle operations
- Synchronous service interface for iBATIS DAO operations in GWT server
- Helper class to build Solr queries for Party entity searches
- Interface for iBatis database operations through a GXT-based UI
- Defines the types of setup operations in SBS visit reports
- Represents an organizational unit within the SBS system with address and identification information
- Data access implementation for credit type management
- Represents a new TV service configuration in digital selling
- Handles conversion between Java List<String> objects and delimited string values for iBatis database operations
- Represents payment information for digital selling transactions
- Unit test class to verify the validation logic for postal/ZIP codes
- Defines context information for unlock requests in the system
- Defines a recipient entity for message or notification delivery
- Defines a set of predefined colors for chart visualization with RGB values
- Data access interface for managing user-shop assignments and their audit logs
- Defines network provider enumeration for telecom services
- Service interface for managing party-related operations in the CUCO system
- Implementation of ESB query order operations for BrianCee system
- Defines the possible types of communication methods in the SBS system
- Integration test class for ESB Location Service functionality
- Service interface for managing and retrieving links in a portlet system
- Helper class for generating Excel reports of customer equipment data
- Implements reporting functionality for the Customer Communication Settings system
- Remote service interface for handling authentication and authorization operations
- Implementation of ESB party data access operations
- Defines possible states for product installation feasibility
- Represents logging data structure for customer-related operations
- Servlet implementation for team management operations in the web client
- Abstract base test class for ESB DAO implementations that require parameters
- Implements hierarchical node structure for contract/product organization
- Service interface for managing credit type operations in the CUCO system
- Represents a summary item in a digital selling visit report with serialization support
- Implementation of mobile signature service using DUPOS system
- Represents a consignee/recipient entity for equipment with address and identification details
- Portlet component for team management functionality
- Unit test suite for the CustomerUnlockService implementation that handles customer account unlocking functionality
- Implementation of service-related operations servlet in the administration UI
- Asynchronous interface for user and role management operations
- Integration test class for ESB Party Service implementation
- Unit test class for testing Solr repository functionality related to party entities with phone numbers
- Implementation of data access operations for visit reports in the CUCO system
- Data access interface for handling reporting functionality
- Manages and calculates statistics for actions at department level
- Defines contract for beans that have a unique identifier
- Represents a structured note for SBS (seems to be a sales/business system) with various attributes and relationships
- Container class for tariff simulation data and results
- Manages metadata entries in both list and map formats for product-related information
- Manages access token information for target systems
- Asynchronous service interface for credit type management operations in GWT client
- Data transfer object for representing a date-value pair
- Service interface related to customer unlocking functionality
- Service implementation for managing authentication access tokens
- Data transfer object representing point of sale information for dealers
- Data access interface for managing standard addresses
- Unit test class to verify the validation logic for party identifiers
- Represents a hierarchical structure of equipment with associated summaries and party information
- Dialog interface for editing team information using UiBinder
- Unit test suite for ContactPersonServiceImpl class that verifies contact person management functionality
- Asynchronous service interface for retrieving charging type data in GWT client
- Handles formatting of individual CSV fields according to RFC4180 standards
- Data access implementation for handling gamification-related data operations locally
- Request object for customer unlock operations with contextual information
- Wrapper class for product offerings with selection state
- Represents a data transfer object for services information in digital selling visit reports
- Represents account information for BRK (likely Broker) system
- Unit test class to verify the functionality of IndexationStatus enum conversion methods
- Validates last names according to minimum length requirements
- Asynchronous service interface for team management operations in GWT client
- Tracks usage information for inventory product groups
- Defines standard subscription types available in the system
- Represents television service information for digital selling
- Represents product-specific notes for SBS visit reports
- Unit test suite for the InvoiceService class to verify invoice processing functionality
- Data access object interface for managing payable tickets in the database
- Interface defining billing cycle data access operations
- Data access implementation for managing image entities
- Unit test class for CustomerUnlockRequestDaoImpl to verify customer unlock request operations
- Service interface for managing payable tickets in the A1 Telekom Austria system
- Data Access Object interface for managing to-do notes in the system
- Defines enumeration of available internet speed tiers
- Represents flash information/notification data structure with time bounds and customer blocks
- Represents a customer/party entity with personal and business information
- Validates phone number formats (implementation incomplete)
- Service implementation for handling ESB party-related operations and data mapping
- Base DTO class for digital selling services information in visit reports
- Renders images in a grid component for the web client UI
- Asynchronous service interface for system tracking and analysis operations
- Servlet implementation for handling credit type related operations in the web client
- Data transfer object representing a category entity with basic metadata
- Data transfer object for searching party/customer information
- Interface defining visit report service operations
- Manages legacy smart home product offerings and pricing information
- Interface for managing access token operations and authentication services
- Validates city name inputs according to length requirements
- Defines the contract for formatting objects in the export system
- Callable implementation for asynchronous mobile points retrieval
- Interface for retrieving party information from ESB (Enterprise Service Bus)
- Interface defining service operations for managing customer loyalty information for parties
- Scheduled job for sending sales information reminder emails
- Servlet for handling past export operations and generating export data in a specific format
- Asynchronous service interface for managing unknown area codes in the administration UI
- Base class for mobile phone product offerings and configurations
- Portlet for managing team configurations in the web client interface
- Portlet for managing user assignments to shops/stores
- Defines product types for telecom services
- Manages automatic contract extension information
- Provides filtering functionality for memory-based data proxies
- Unit test suite for CustomerInteractionService implementation
- Manages customer interactions and communication history
- Interface for handling mobile signature operations through DUPOS system
- Defines configuration options for chart rendering
- Implements a servlet filter to control caching behavior for GWT application resources
- Represents a binding between a customer and their product/service contracts
- Data transfer object for representing person information with Solr integration
- Service for retrieving account information from KUMS (Telekom account management system)
- Service implementation for handling Point of Sale (POS) related operations
- Represents a legacy TV service data transfer object in the digital selling visit report system
- Service interface for product administration functionality
- Represents a group note for todo items related to sales processing tasks
- Helper component for formatting and standardizing party search values, particularly phone numbers
- Data model class for service information in the admin UI
- Unit test class for testing basic Solr repository operations for party entities
- Data access object interface for handling image-related database operations
- Data transfer object for representing mobile customer churn likelihood information
- Data transfer object for user administration feature segmentation
- Data transfer object for representing image metadata in the system
- Unit test suite for ClearingAccountService implementation
- Interface defining contract for objects that have account awareness/association
- Validates Bank Account Numbers (BAN) according to specific format rules
- Represents phone number details with associated telecommunications information
- Data transfer object for storing feedback question responses with different value types
- Manages matrix-structured data for segments, categories, and product groups
- Represents the assignment of billing accounts to a party/contract owner
- A custom checkbox widget that can be associated with a generic marker object
- Service implementation for managing charging types in the system
- Defines enumeration for edit permissions based on category
- Handles tariff simulation functionality for A1 Telekom Austria AG
- Unit test suite for KUMS customer service implementation handling customer data
- Renders clickable links in GXT grid cells
- Data access interface for managing UI text content
- Data access interface for managing organizational structure elements in CCT system
- Tracks historical changes to VIP customer status
- Dialog interface for selecting team members with pagination support
- Event class for handling role-related operations in the administration UI
- Represents a subscription node in the product hierarchy
- Service implementation for managing clearing accounts in the CUCO system
- Data transfer object for representing VBM (Value Based Management) product information
- Represents legacy mobile tariff configurations in digital selling system
- Manages free units/quota information with standardized unit definitions
- Grid component for displaying system messages with paging functionality
- Data access implementation for inventory management in the CUCO core system
- Defines search query fields and functionality for party/customer data in Solr search engine
- Represents a group of products with metadata and tracking information
- Service interface for location-related operations within A1 Telekom Austria system
- Data Access Object interface for customer communication operations
- Data access interface for managing clearing accounts in the settlement system
- Data access interface for managing contact person information
- Tracks historical changes to sales information notes
- Service interface for managing billing cycles and related operations
- Represents a new mobile tariff configuration for digital selling, extending base mobile tariff functionality
- Data transfer object for representing free units/minutes information in a telecom system
- Manages approvers for quotes at specific organizational levels
- Unit test suite for service handling unknown area codes in telecommunications context
- Manages access token request data between systems
- Event handler class for adding unknown area codes in the administration UI
- Handles asynchronous business hardware replacement operations
- Represents a single data set within a chart with generic key-value pairs
- Service implementation for managing location-related operations
- Interface for retrieving customer subscription promotions based on call numbers
- Implements service layer for phone number management
- Represents a flash message or notification with role-based visibility control
- ExtJS-based dialog for editing service properties
- Manages team service-related operations in a GWT panel interface
- Data access implementation for user information statistics
- Provides a placeholder node for asynchronously loaded content in a tree structure
- Manages new internet speed product configurations with protection features
- Implementation of authentication service for CRM integration
- Asynchronous interface for authentication-related service calls in GWT client
- Portlet for managing user accounts and permissions in the administration interface
- Provides comprehensive team member management functionality including selection and click handling
- Unit test class to verify the validation logic for first names
- Represents a request for product chart data with filtering criteria
- Represents new service offerings in digital selling system
- Service locator pattern implementation for various settings-related services
- Represents a generic note type in the sales information system with file attachment support
- Represents a reporting entity that contains query and metadata information for generating reports
- Defines an interface for proxy filters that can be bound to data loaders in a GXT UI framework
- Custom iBATIS type handler to convert between Java Boolean values and 1/0 database representations
- Defines the available types of TV service delivery methods
- Interface for managing master session control and DOC home URL generation
- Implementation of insurance broker HSI (Host System Interface) service for handling insurance contract operations
- Handles conversion between database and application representations of ToDo group statuses
- Data model for digital selling note printing information
- Provides common validation utilities used across different validators
- Integration test class for user action statistics functionality
- Represents promotional offers with discount information and validity periods
- Portlet for managing service-related configurations with paging support
- Represents internet usage data and associated fees
- Data transfer object for representing detailed usage information
- Base abstract class providing common functionality for action statistics
- Provides utility functions and fixes for GXT framework components
- Implementation of data access layer for handling MobilPoints service interactions through ESB
- Dialog for editing credit type configurations
- Implementation of visit report service handling digital selling note generation and processing
- Defines filtering criteria for opportunity/quote searches
- Implements a grid component for displaying system messages with date formatting and selection handling
- Synchronous service interface for team management operations in GWT
- Implements a reporting interface widget with data table functionality
- Data transfer object representing a telephone number with country code, area code and number components
- Interface defining invoice management and retrieval operations
- Event class for handling credit type addition operations in the admin UI
- Represents security-related information in digital selling visit reports
- Unit test suite for AccessTokenService implementation that handles authentication token management
- Implementation of system tracking functionality via servlet
- Test class for validating the DataTheftRapidAlert job functionality
- Represents a contact person entity associated with a customer in the system
- Servlet implementation for handling reporting functionality in the web client
- Validates first name input
- Data transfer object for representing reasons for declining a VBM product
- Manages application settings editing functionality
- Provides auditing functionality with context awareness for tracking system activities
- Portlet component for managing credit type configurations in the administration interface
- Data access interface for managing VIP customer history records
- Manages product price alterations including discounts and allowances
- Represents legacy security product configuration for digital selling visit reports
- Implements promotion service functionality for customer equipment
- Panel component for displaying and managing team-related information
- Legacy class for handling mobile phone sales information
- Represents a gamification-related message or notification in the system
- Interface providing access to Point of Sale (POS) data in the KUMS system
- Data access interface for managing sales information notes with filtering capabilities
- Represents a summary item for party-related information with count or URL
- Base class for sales information notes that provides common functionality for tracking sales-related information and notes
- Service implementation for managing VIP customer history records
- Manages organizational structure elements in the Customer Communication Settings system
- Data access implementation for managing user notes with search functionality
- Data access implementation for managing customer interactions in the MK system
- Entry point for the main application module that initializes core application components
- Test class for validating conversions between PayableTicket and credit request objects
- Data transfer object for structured phone number representation
- Represents dimensions and metadata for an image resource
- Provides UI component for previewing system messages
- Base abstract portlet class for Customer Communication Settings functionality
- Remote service interface for handling reporting functionality
- Helper class for handling email operations related to sales info notes
- Data Access Object interface for managing credit types
- Interface for accessing BRK (likely Billing/Revenue/Knowledge) account information
- Service implementation for handling image-related operations
- Scheduled job to manage and update phone number cache
- Data transfer object for smart home product information in digital selling visit reports
- Enumeration defining possible states for product indexation status
- Data access implementation for managing quote-related operations
- Implements party profile management functionality with file handling capabilities
- Interface for CRM authentication and customer information retrieval
- Service interface for image handling operations within A1 Telekom Austria system
- Data access interface for managing VBM (Value Based Management) products and related information
- A GWT portlet for checking usage statistics or metrics with date-based filtering
- Asynchronous service interface for iBATIS DAO operations in GWT client
- Defines authorization/permission constants for the application
- Represents aggregated usage data for inventory product groups with associated parties
- Service interface for managing phone number related operations
- Remote service interface for managing user-shop assignments in the administration UI
- Implementation of business hardware replacement operations through ESB
- Service interface for generating and managing reports
- Represents a party (entity) node in a product hierarchy with contact details
- Manages payment information for digital selling transactions
- Implementation for managing customer-related operations
- Implements HTTP client service for CM Buddy system integration
- Test class for validating shop synchronization job functionality
- Implementation of MyToDoNotesService for managing sales-related todo notes
- Manages tabular data structure for export operations
- Service interface for managing user-shop assignments and relationships
- Interface defining data access operations for ESB party-related functionality
- Interface defining operations for managing sales info notes
- Manages the lifecycle and status of a sales process
- Manages invoice data and provides invoice comparison functionality
- Service implementation for managing credit type operations
- Represents a request object for tariff simulation calculations
- Defines auditable activities for tracking user or system actions in the CuCo system
- Service interface for managing turnover-related operations in the CUCO system
- Represents music-related information for digital selling visit reports
- Servlet handling usage statistics for A1 Telekom Austria system
- Unit test class to verify the validation logic for city names
- Defines mobile tariff data structure for digital selling
- Defines the possible sources/origins of a sales contact in the SBS system
- Defines enumeration of main usage types for mobile tariffs in digital selling context
- Manages mobile points and hardware replacement information for a phone number
- Interface defining services for retrieving automatic VVL (likely customer verification) information using different identifiers
- Entry point for the admin module that initializes administration interface components
- Renders buttons within grid cells with associated actions
- Implementation of service managing user-shop assignments
- Interface for retrieving business hardware replacement information
- Represents a price value with currency units in the CuCo system
- Interface defining services for retrieving person information from CD (Customer Data) system
- Represents legacy internet speed configuration with virus protection options
- Represents a wrapper class for the root product node in a product hierarchy structure
- Data access implementation for inventory product group management
- Defines contract for product-related functionality across the system
- Implements servlet handling unknown area code operations
- Dialog component for selecting team members using GWT UI framework
- Data access interface for system logging operations
- Defines product details for Value Based Management (VBM) functionality
- Custom type handler for mapping VIP status values between database and Java objects in iBatis
- Represents a type of credit in the system
- Interface defining service operations for managing customer bindings
- Implements team management functionality including CRUD operations and team member management
- Manages a collection of Billing Account Numbers (BANs) associated with a party
- Interface for managing customer unlock operations and signature processes
- Utility class for report generation functionality
- Represents a placeholder node for when no products are available
- Data transfer object for representing turnover/revenue information
- Data access object for managing flash information/notifications in the CUCO system
- Data access interface for segment-related operations
- Interface defining data access operations for visit reports
- Unit test suite for CustomerAssignmentService to verify customer contract assignment functionality
- Extends GridContainer to provide pagination functionality for grid displays
- Data access implementation for managing to-do notes
- Renders boolean values as Yes/No text in grid cells using localized strings
- Tracks mobile service usage metrics including data, duration, and fees
- Service implementation for managing generic service operations
- Dialog interface for editing system messages or notifications
- Represents a physical resource node in SAP with equipment attributes
- Enumeration defining possible unlock states for access control
- Data access implementation for managing VIP history records in the database
- Represents a log entry for user shop assignment activities
- Generic container for chart data sets with key-value mappings
- Represents a data structure for storing address information in a serializable format
- Unit test class for Flash Info Service functionality
- Represents household information for digital selling context
- Data access implementation for managing Segment entities in the database
- Validates user input against a specified pattern
- Represents a settings cell container for segment and category data
- Event class for handling product group operations in the administration UI
- Validates postal/zip code format according to specific length and digit requirements
- Unit test suite for LocationService implementation
- Data access interface for managing charging types in the billing system
- Data access implementation for managing unknown area codes in the database
- Represents a billing account with associated brands and phone numbers
- Provides base functionality for filtering in-memory data in GXT components
- Utility class for image processing operations
- Data access implementation for managing customer attributes
- Dialog for editing user information and settings
- DTO for mobile phone related information in digital selling visit reports
- Interface defining quote and opportunity management operations
- Unit tests for CustomerEquipmentHelper utility class
- Handles conversion between Java List objects and Oracle Array types for iBatis database operations
- Data transfer object for email communication data in sales conversations
- GWT-based portlet implementation for handling service-related functionality in the CUCOSETT web client
- Implementation of Brian service data access operations
- Represents a new mobile phone offering in digital selling context with payment options
- Service interface for handling mobile points functionality (full implementation details not visible in preview)
- Represents solvency/credit information for a party profile in the system
- Factory class for creating PartyModel instances from various data sources
- Manages role groups with paging support using GXT framework
- Base class for product pricing information with core identifier and naming attributes
- Manages team email administration group information
- A container component that extends ContentPanel to provide grid functionality with selection and filtering capabilities
- Defines a header node for product-related information display
- Represents an event for adding services in the administration UI
- Data transfer object for gamification login credentials and session information
- Interface defining services for managing flash information and related party data for agents
- Represents an organizational structure element in the CCT system with user hierarchy and approval information
- Holds configuration data for quote clearance including product offerings and roles
- Service implementation for handling CUSCO system unlocking operations

### Data Structures
#### Configuration Pools
Fields:
- LocalSettingPool
- SettingPool
- TextPool
- SystemMessagePool
Relationships:
- Inherited from BiteEntryPoint
#### Admin Configuration
Fields:
- LocalSettingPool
- SettingPool
- TextPool
Relationships:
- Inherited from BiteEntryPoint
#### StartupConfiguration
Fields:
- LocalSettingPool
- SettingPool
- TextPool
- SystemMessagePool
Relationships:
- Aggregates configuration pools
#### Configuration
Fields:
- LocalSettingPool
- SettingPool
- TextPool
- SystemMessagePool
Relationships:
- Aggregates configuration settings
#### Authority
Fields:
- authorization details
Relationships:
- Used by AuthorityService
#### Export Data
Fields:
- date
- numeric values
Relationships:
- Formats data using DateFormat and NumberFormat
#### FileItem
Fields:
- file data
- form fields
Relationships:
- Processed by Apache Commons FileUpload
#### SqlMapClientDaoSupport
Fields:
- SQL mappings
Relationships:
- Extends Spring's DAO support for iBATIS
#### CreditType
Fields:
- credit type details
Relationships:
- Managed by CreditTypeService
#### File
Fields:
- file metadata
Relationships:
- Used in report generation
#### Rep
Fields:
- report configuration
Relationships:
- Associated with File
#### BiteUser
Fields:
- user information
Relationships:
- Member of Team
#### Auth
Fields:
- authentication details
Relationships:
- Associated with BiteUser
#### ChargingType
Fields:
- Not visible in preview
Relationships:
- Managed by ChargingTypeService
#### FileItem
Fields:
- Not visible in preview
Relationships:
- Used for file upload processing
#### Not visible in preview
Fields:
- Not visible in preview
Relationships:
- Not visible in preview
#### SystemMessage
Fields:
- date
- message
Relationships:
- Displayed in grid rows
#### ModelData
Fields:
- button properties
Relationships:
- Used in grid column rendering
#### HashMap
Fields:
- report data
Relationships:
- Used for storing report configuration
#### MarkableCheckbox<B>
Fields:
- marker: B
Relationships:
- extends CheckBox
#### BaseModelData
Fields:
- not visible in preview
Relationships:
- used for grid data model
#### ModelData
Fields:
- not visible in preview
Relationships:
- used for grid data
#### SettingsCell
Fields:
- Long segment
- Long category
Relationships:
- Extends FlowPanel
#### Service Selection Data
Fields:
- service list
- selected service
Relationships:
- Uses GWT UiBinder for UI template binding
#### Service Edit Data
Fields:
- service properties
- number format
Relationships:
- Uses GWT UiBinder for UI template binding
#### Service Model
Fields:
- service data
- list store
Relationships:
- Uses BaseModelData for data storage
- ListStore for data management
#### TeamMember
Fields:
- ArrayList<TeamMember>
Relationships:
- Used in selection list
#### Team
Fields:
- name
- description
- date
Relationships:
- Contains TextField and TextArea components
#### User
Fields:
- ArrayList<UserData>
- user settings
Relationships:
- Handles user information updates
#### RoleGroup
Fields:
- roles
- permissions
Relationships:
- Many-to-many with Roles
- Many-to-many with Permissions
#### CreditType
Fields:
- name
- description
Relationships:
- One-to-many with Credits
#### Message
Fields:
- content
- date
- recipients
Relationships:
- Many-to-many with Users
#### BaseModelData
Fields:
- message content
- date
- properties
Relationships:
- extends GXT ModelData
#### BasePagingLoader
Fields:
- member data
- paging information
Relationships:
- uses BaseModelData
- implements PagingLoadResult
#### UiFields
Fields:
- team properties
- UI components
Relationships:
- bound to UiBinder template
#### BaseModelData
Fields:
- role information
Relationships:
- Used in ListStore for role data management
#### FormFields
Fields:
- TextArea
- TextField
Relationships:
- Input validation and data entry
#### RoleSelection
Fields:
- role data
Relationships:
- Event handlers for selection changes
#### BaseModelData
Fields:
- service properties
Relationships:
- extends ModelData
#### CreditType
Fields:
- credit type properties
Relationships:
- managed through UiFields
#### BaseModelData
Fields:
- role group properties
Relationships:
- used in ListStore
#### Date handling
Fields:
- Date
- DateTimeFormat
Relationships:
- Used for filtering usage data
#### BaseModelData
Fields:
- role group attributes
Relationships:
- Used with BasePagingLoader
#### ListStore
Fields:
- BaseModelData items
Relationships:
- Stores database query results
#### User
Fields:
- username
- permissions
- status
Relationships:
- Many-to-many with Permissions
#### SystemMessage
Fields:
- message
- timestamp
- type
#### BaseModelData
Fields:
- userId
- shopId
- assignmentStatus
Relationships:
- Many-to-many between Users and Shops
#### PortletDefinition
Fields:
- definition parameters
Relationships:
- Inherited from AbstractPortlet
#### ArrayList
Fields:
- report data
Relationships:
- Contains report entries
#### HashMap
Fields:
- key-value pairs
Relationships:
- Stores report configuration
#### InputElement
Fields:
- form inputs
Relationships:
- DOM interaction
#### ArrayList
Fields:
- dynamic
Relationships:
- Used for storing role group data
#### VipSearchPortlet
Fields:
- instance
- component
Relationships:
- Extends AbstractPortlet
- Contains VipSearchComponent
#### SearchData
Fields:
- Date
- List
Relationships:
- Used for managing search parameters
#### PortletDefinition
Fields:
- portlet configuration parameters
Relationships:
- Extends base portlet structure
#### BaseModelData
Fields:
- service configuration data
Relationships:
- Used in BasePagingLoader
#### ArrayList
Fields:
- credit type entries
Relationships:
- Used in HTML display logic
#### BaseModelData
Fields:
- credit type properties
Relationships:
- extends GXT BaseModelData
#### PortletDefinition
Fields:
- team configuration data
Relationships:
- uses BITE core DTO
#### ArrayList
Fields:
- area code data
Relationships:
- Java util collection
#### BaseModelData
Fields:
- area code data fields
Relationships:
- extends ExtJS model for grid data
#### BaseModelData
Fields:
- team data fields
Relationships:
- used with BasePagingLoader for team data
#### BaseModelData
Fields:
- team member properties
Relationships:
- Extends GXT ModelData for grid data binding
#### PagingLoadResult
Fields:
- service data
Relationships:
- Used with BasePagingLoader for data management
#### List<TeamMember>
Fields:
- member data
Relationships:
- Managed through SelectionHandler
#### ArrayList
Fields:
- team service entries
Relationships:
- Contains team service data objects
#### ArrayList
Fields:
- team entries
Relationships:
- Contains team data objects
#### Service Clients
Fields:
- creditTypeServlet
- chargingTypeServlet
- teamServlet
- authServlet
- ibatisServlet
Relationships:
- Static singleton instances
#### ChargingType
Fields:
- Not visible in interface
Relationships:
- List<ChargingType> returned by getAllCharging method
#### Reporting
Fields:
- Not visible in interface
Relationships:
- ArrayList<Reporting> returned by service methods
#### ReportingException
Fields:
- message (inherited from RuntimeException)
Relationships:
- Extends RuntimeException
- Implements Serializable
#### ChargingType
Fields:
- Not visible in interface
Relationships:
- Returned as List in getAllChargingTypes
#### RpcStatus
Fields:
- Not visible in interface
Relationships:
- Returned in flush operations
#### RpcStatus
Fields:
- Not visible in interface
Relationships:
- Returned in flush operations
#### CreditType
Fields:
- Not directly visible in interface
Relationships:
- Used as DTO in service operations
#### Team
Fields:
- Not directly visible in interface
Relationships:
- Associated with BiteUser and Service
#### Team
Fields:
- Not directly visible in interface
Relationships:
- Associated with BiteUser and Service
#### Reporting
Fields:
- id
- report data
Relationships:
- Used as return type in callbacks
#### CreditType
Fields:
- credit type attributes
Relationships:
- Used as data transfer object
#### Authority
Fields:
- authority attributes
Relationships:
- Returned as ArrayList in getAllAuthorities
#### Authority
Fields:
- Not visible in interface
Relationships:
- Used as collection return type
#### User Roles
Fields:
- roleId
- userId
- groupId
Relationships:
- User to Role
- Role to RoleGroup
#### ExcelWorkbook
Fields:
- cells
- styles
- fonts
Relationships:
- HSSFWorkbook composition
#### BaseModelData
Fields:
- timestamp
- trackingData
- metrics
Relationships:
- ExtJS data model integration
#### UploadedAssignments
Fields:
- user data
- shop assignments
Relationships:
- Maps users to shops
#### AreaCode
Fields:
- code
- description
Relationships:
- Connected to UnknownAreaCodeService
#### UserShopAssignment
Fields:
- user
- shop
- assignment details
Relationships:
- Links to UserShopAssignmentService
#### CCTOrgStructureElement
Fields:
- organizational structure data
Relationships:
- Inherits from AuthenticationServlet
#### ServiceDTO
Fields:
- service related data
Relationships:
- Inherits from SpringRemoteServiceServlet
#### VIPHistory
Fields:
- date
- history records
Relationships:
- Uses HttpServlet functionality
#### ServiceModel
Fields:
- id
- name
- costs
Relationships:
- extends BaseModelData
- maps to Service DTO
#### RTCodeModel
Fields:
- prodNum
Relationships:
- extends BaseModelData
- maps to RTCode DTO
#### BaseModelData
Fields:
- dynamic fields
Relationships:
- extends GXT BaseModelData
#### SystemMessage
Fields:
- message content
- system details
Relationships:
- Used as data model for preview
#### TextPool
Fields:
- loading
- noData
- error
- yes
- no
- info
- save
- cancel
Relationships:
- Extends at.a1ta.bite.ui.client.generator.textpool.TextPool
#### settings
Fields:
- Map<String, String>
Relationships:
- static shared storage
#### UnknownAreaCode
Fields:
- Not visible in interface
Relationships:
- Used as DTO from core.shared package
#### BaseModelData
Fields:
- Not visible in interface
Relationships:
- Extended from GXT UI framework
#### CCTOrgStructureElement
Fields:
- Not visible in interface
Relationships:
- Used as DTO from core.shared.dto.product package
#### Static Service References
Fields:
- systemTrackingServlet
- roleServlet
- serviceServlet
- unknownAreaCode
- vipHistoryServlet
Relationships:
- Each field holds an async service implementation
#### Service Methods
Fields:
- getVIPHistory(Date from, Date to, String searchTerm, String vipStatus)
Relationships:
- Returns List<VIPHistoryEntry>
#### Async Methods
Fields:
- getVIPHistory(Date from, Date to, String searchTerm, String vipStatus, AsyncCallback<List<VIPHistoryEntry>> callback)
Relationships:
- Callback returns List<VIPHistoryEntry>
#### UserShopAssignment
Fields:
- Not visible in interface
Relationships:
- Maps users to shops
#### UserShopAssignmentLogLine
Fields:
- Not visible in interface
Relationships:
- Tracks history of assignment changes
#### AsyncCallback
Fields:
- <List<UserShopAssignment>>
Relationships:
- Handles async responses for user-shop assignments
#### BiteUser
Fields:
- Not visible in interface
Relationships:
- Contains user information
#### UserInfo
Fields:
- Not visible in interface
Relationships:
- Contains user details
#### UnknownAreaCode
Fields:
- Not directly visible in interface
Relationships:
- Used in ArrayList return type
#### BaseModelData
Fields:
- Not visible in interface
Relationships:
- Used in ArrayList return type
#### Service
Fields:
- Not visible in interface
Relationships:
- Used in ArrayList return type
#### Service
Fields:
- Not visible in interface
Relationships:
- Used as DTO for service operations
#### BiteUser
Fields:
- Not visible in interface
Relationships:
- Related to UserInfo, Role, RoleGroup
#### CCTOrgStructureElement
Fields:
- Not visible in interface
Relationships:
- Used in organizational structure operations
#### AddCreditTypeEvent
Fields:
- CreditType credit
Relationships:
- extends PortletEvent
- uses CreditType
#### SelectRolesEvent
Fields:
- List<Role> roles
Relationships:
- extends PortletEvent
- uses Role
#### AddTeamMemberEvent
Fields:
- List<ModelData<BiteUser>> teamMember
Relationships:
- extends PortletEvent
- uses ModelData
- uses BiteUser
#### AddUnknownAreaCodeEvent
Fields:
- UnknownAreaCode code
Relationships:
- extends PortletEvent
#### GwtAddTeamMembersEvent
Fields:
- List<ModelData<BiteUser>> teamMembers
Relationships:
- extends PortletEvent
#### AddTeamEvent
Fields:
- Team team
Relationships:
- extends PortletEvent
#### CuCoEventType
Fields:
- PRODUCT_GROUPUPDATE
- LOAD_MESSAGES
- ROLE_UPDATE
- SELECT_ROLES
- UPDATE_USERS
- UPDATE_USER
- UPDATECREDIT_TYPES
- UPDATE_SERVICES
- UPDATE_TEAMS
- ACTIVATE_TEAM
- ADDTEAM_MEMBERS
- ADD_SERVICES
- REMOVE_SERVICES
- UPDATEUNKNOWN_AREACODES
Relationships:
- implements PortletEventType
#### AddServicesEvent
Fields:
- services: List<ServiceModel>
Relationships:
- extends PortletEvent
#### RemoveServicesEvent
Fields:
- service: Service
Relationships:
- extends PortletEvent
#### AddTeamMembersEvent
Fields:
- List<BaseModelData> teamMembers
Relationships:
- extends PortletEvent
#### RoleEvent
Fields:
- Role role
- UpdateType enum {insert, update}
Relationships:
- extends PortletEvent
#### ProductgroupEvent
Fields:
- ProductGroup group
- UpdateType enum {insert, update, none}
- UpdateType type
Relationships:
- extends PortletEvent
#### ModelData
Fields:
- generic
Relationships:
- Used as data type for grid rows
#### ModelData
Fields:
- generic <M>
Relationships:
- Used as data type for filtered items
#### ModelData
Fields:
- generic
Relationships:
- Associated with grid row data
#### ProxyFilter<M>
Relationships:
- Binds to BaseListLoader
#### NumberFieldFixed
Relationships:
- Extends NumberField
#### DetailsDialog
Relationships:
- Extends Dialog
#### BasePagingLoadResult
Fields:
- data
- offset
- totalLength
Relationships:
- extends BaseListLoadResult
#### BaseListLoadResult
Fields:
- data
Relationships:
- implements ListLoadResult
#### ColumnData
Fields:
- css
- style
Relationships:
- used by GridCellRenderer
#### ModelData
Fields:
- generic type parameter
Relationships:
- Used as data type for grid content
#### ProxyFilter
Fields:
- generic type parameter
Relationships:
- Used as filter type for proxy
#### ModelData
Fields:
- generic type parameter D
Relationships:
- Extends ComboBox<D>
#### PayableTicket
Fields:
- phoneNumber
Relationships:
- BiteUser
#### EsbAccessParameter
Fields:
- Not visible in snippet
Relationships:
- Used by ESB DAOs
#### CustomerInventory
Fields:
- Not visible in snippet
Relationships:
- Accessed via ESB
#### BiteUser
Fields:
- Not visible in snippet
Relationships:
- Used in Brian ESB operations
#### AccessToken
Fields:
- not visible in snippet
Relationships:
- Used as response object
#### PartnerCenterAccessTokenRequest
Fields:
- not visible in snippet
Relationships:
- Used as request object
#### EsbPartyServiceImpl
Fields:
- not visible in snippet
Relationships:
- Service being tested
#### Text
Fields:
- not visible in snippet
Relationships:
- Used by TextService
#### COUNTRY_CODES
Fields:
- List<String>
Relationships:
- Static test data for country code validation
#### PartySearch
Fields:
- Query parameters for party search
Relationships:
- Used by SolrPartyQueryHelper
#### Party
Fields:
- phoneNumbers
Relationships:
- Extends AbstractSolrRepositoryTest
#### Party
Fields:
- id
- name
Relationships:
- Extends AbstractSolrRepositoryTest
#### SolrTemplate
Fields:
- solrTemplateMock
Relationships:
- Used by child test classes
#### SalesInfo
Fields:
- date
- salesInfo
Relationships:
- Mapped to sales_info database table
#### MyNotes
Fields:
- noteContent
- userId
Relationships:
- Mapped to my_notes database table
#### CustomerUnlockRequest
Fields:
- customerId
- requestDate
- status
Relationships:
- Mapped to customer_unlock_request database table
#### IndexationStatus
Fields:
- INDEXED
Relationships:
- Enum being tested
#### HousenumberValidator
Fields:
- validator
Relationships:
- Class being tested
#### CityValidator
Fields:
- validator
Relationships:
- Mocked test dependency
#### FirstnameValidator
Fields:
- validator
Relationships:
- Tested class
#### ZipCodeValidator
Fields:
- validator
Relationships:
- Tested class
#### AONNumberValidator
Fields:
- validator
Relationships:
- Tested class
#### StreetValidator
Fields:
- validator
Relationships:
- Tested by StreetValidatorTest
#### PartyIdValidator
Fields:
- validator
Relationships:
- Tested by PartyIdValidatorTest
#### LastnameValidator
Fields:
- validator
Relationships:
- Tested by LastnameValidatorTest
#### PhonenumberValidator
Fields:
- validator instance
Relationships:
- tested class
#### BANValidator
Fields:
- validator instance
Relationships:
- tested class
#### Collection
Fields:
- ArrayList
Relationships:
- data container
#### Invoice
Fields:
- Not visible in preview
Relationships:
- Used as test data in service operations
#### ContractOwnerAssignment
Fields:
- Not visible in preview
Relationships:
- Used by CustomerAssignmentService
#### Mail
Fields:
- Not visible in preview
Relationships:
- Used in mail service operations
#### AccessToken
Fields:
- UUID
- token value
Relationships:
- Associated with SettingService
#### AreaCode
Fields:
- code
- status
Relationships:
- Associated with telecommunications service
#### Customer
Fields:
- customer data
Relationships:
- Cached in EhCache
#### CustomerUnlockService
Fields:
- unlockStatus
- customerId
Relationships:
- depends on CustomerUnlockServiceImpl
#### PayableTicket
Fields:
- ticketId
- paymentStatus
- amount
Relationships:
- depends on PayableTicketServiceImpl
#### AutoVvlService
Fields:
- vvlStatus
- contractId
Relationships:
- implements AutoVvlService interface
#### Product Data
Fields:
- id
- properties
Relationships:
- HashMap<String,Object> for product properties
#### Billing Data
Fields:
- cycle information
- billing parameters
Relationships:
- ArrayList for billing records
#### CustomerInteraction
Fields:
- date
- type
- customer
Relationships:
- Customer
- InteractionType
#### Location
Fields:
- address
- coordinates
Relationships:
- Customer
- Address
#### ClearingAccount
Fields:
- accountId
- balance
- transactions
Relationships:
- Transaction
- Account
#### ContactPerson
Fields:
- id
- name
- details
Relationships:
- Associated with Party
#### Party
Fields:
- id
- attributes
- relationships
Relationships:
- Has many ContactPersons
#### Attribute
Fields:
- id
- name
- value
Relationships:
- Belongs to Party
#### DigitalSellingNote
Fields:
- Not fully visible in preview
Relationships:
- Part of visit report data model
#### CustomerEquipmentHelper
Fields:
- Static utility methods
Relationships:
- Used by equipment-related services
#### UserActionStatistics
Fields:
- Not visible in preview
Relationships:
- Related to user activity tracking
#### DepartmentActionStatistics
Fields:
- department
- actionCounts
- periodStart
- periodEnd
Relationships:
- extends UserActionStatisticsTestBase
#### UserActionStatistics
Fields:
- user
- actionCounts
- periodStart
- periodEnd
Relationships:
- extends UserActionStatisticsTestBase
#### TestData
Fields:
- dateFormat
- locale
- testFiles
Relationships:
- used by DepartmentActionStatisticsTest and UserActionStatisticsTest
#### MetricsConfig
Fields:
- metrics settings
- monitoring parameters
Relationships:
- Application monitoring system
#### Reporting
Fields:
- id: Long - unique identifier
- name: String - report name
- query: String - SQL or report query
- longRunning: boolean - flag for long-running reports
- tableName: String - target table name
Relationships:
- implements KeyableBean
- implements Serializable
#### KeyableBean
Fields:
- getId(): Long
Relationships:
- implemented by beans requiring unique identifiers
#### File
Fields:
- serialVersionUID: long
Relationships:
- implements Serializable
#### MIMEType
Fields:
- PNG: image/png
- CSV: text/csv
- PDF: application/pdf
- XLS: application/x-excel
- XLSX: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
#### PWUTokenResponse
Fields:
- a1Login: String
- orderId: String
- retailerId: String
- token: String
- firstName: String
- lastName: String
- invokationDuration: long
- partyId: String
Relationships:
- implements Serializable
#### BillingCycle
Fields:
- not visible in snippet
Relationships:
- List<BillingCycle> returned from getBillingCycle method
#### BillingCycle
Fields:
- not visible in snippet
Relationships:
- List<BillingCycle> returned from getBillingCycle method
#### MobilPoints
Fields:
- phoneNumber
- points
Relationships:
- PhoneNumberStructure
#### DateTimeFormatter
Fields:
- format pattern
Relationships:
- Joda Time
#### Party
Fields:
- partyId
Relationships:
- External ESB Party entity
#### EsbParty
Fields:
- partyId
Relationships:
- Internal DTO representation of Party
#### BillingAccountNumber
Fields:
- unknown
Relationships:
- Used for billing account identification
#### ContractOwnerAssignment
Fields:
- unknown
Relationships:
- Maps contracts to owners
#### BusinessHardwareReplacement
Fields:
- unknown
Relationships:
- Related to hardware replacement processes
#### MobilPoints
Fields:
- not visible in interface
Relationships:
- Retrieved based on PhoneNumberStructure
#### PointOfSaleInfo
Fields:
- not visible in interface
Relationships:
- Returned as ArrayList collection
#### EsbParty
Fields:
- not visible in preview
Relationships:
- Managed through BaseEsbClient
#### ContractOwnerAssignment
Fields:
- ban
- partyId
Relationships:
- Used as return type for queries
#### AccessToken
Fields:
- token details
Relationships:
- Return type for authentication
#### PartnerCenterAccessTokenRequest
Fields:
- request parameters
Relationships:
- Input for token generation
#### BusinessHardwareReplacement
Fields:
- billingAccountNumber
Relationships:
- at.a1ta.cuco.core.shared.dto.mobilpoints.BusinessHardwareReplacement
#### PWUTokenResponse
Fields:
- not visible in preview
Relationships:
- at.a1ta.cuco.core.bean.PWUTokenResponse
#### List
Fields:
- generic elements
Relationships:
- Converted to/from Oracle ARRAY type
#### List<String>
Fields:
- String elements
Relationships:
- Converted to/from delimited string
#### Boolean
Fields:
- true/false/null
Relationships:
- Maps to Y/N/null in database
#### Boolean
Fields:
- true
- false
Relationships:
- maps to Y/N strings in database
#### IndexationStatus
Fields:
- enum values
Relationships:
- maps to database values
#### Boolean
Fields:
- true
- false
Relationships:
- maps to 1/0 strings in database
#### VipStatus
Fields:
- State enum
Relationships:
- Used by TypeHandlerCallback interface
#### PhoneNumber
Fields:
- likely contains number, country code, area code
Relationships:
- Used by parsing methods
#### CusCoResponse
Fields:
- status
- responseCode
- message
Relationships:
- Used by CusCoDao
#### CusCoDao
Relationships:
- Implemented by HttpPostCusCoDao
#### HttpPostCusCoDao
Fields:
- httpClient
- endpoint
- timeout
Relationships:
- Implements CusCoDao
- Uses CusCoResponse
#### Party
Fields:
- Not directly visible in interface
Relationships:
- Managed by Solr document store
#### PartySearchCriteria
Fields:
- Not directly visible in preview
Relationships:
- Used to build Solr Query objects
#### Party
Fields:
- phone numbers
- other fields not visible in preview
Relationships:
- Stored in Solr with phone number associations
#### SearchField
Fields:
- TITLE
- FIRSTNAME
- LASTNAME
- STREET
- POSTCODE
- HOUSENU
Relationships:
- Implements Field interface
#### ContextAwareCustomerUnlockRequest
Fields:
- Not visible in interface
Relationships:
- Used as parameter/return type for CRUD operations
#### SearchResult
Fields:
- Not visible in interface
Relationships:
- Contains inventory query results
#### BindingsFilter
Fields:
- Not visible in interface
Relationships:
- Used to filter inventory queries
#### SingleTurnaround
Fields:
- Not visible in preview
Relationships:
- Likely related to clearing accounts and transactions
#### ChargingType
Fields:
- Not visible in preview
Relationships:
- Likely related to billing and payment configurations
#### ClearingAccount
Fields:
- partyIds
- accountNumber
- phoneNumber
Relationships:
- Associated with parties and account holders
#### SearchResult<SalesInfoNote>
Fields:
- SalesInfoNote collection
- pagination info
Relationships:
- Contains SalesInfoNote objects
#### Party
Fields:
- Not directly visible in interface
Relationships:
- Referenced as main entity type
#### CustomerFilter
Fields:
- Not directly visible in interface
Relationships:
- Used as search criteria
#### UIText
Fields:
- Not directly visible in interface
Relationships:
- Main entity for UI text management
#### Reporting
Fields:
- Not directly visible in interface
Relationships:
- Main entity for reporting operations
#### HashMap<String, Object>
Fields:
- Dynamic key-value pairs
Relationships:
- Used for report execution results
#### SearchResult<MyOpportunity>
Fields:
- MyOpportunity objects
Relationships:
- OpportunityFilter
- SalesInfoOverviewRow
#### StandardAddress
Fields:
- addressId
- lkmsId
- partyId
Relationships:
- Country
#### UserShopAssignment
Relationships:
- User
- Shop
#### UserShopAssignmentLogLine
Relationships:
- UserShopAssignment
#### ProductHierarchy
Fields:
- Not visible in interface
Relationships:
- Referenced as return type in getProductHierarchy()
#### Location
Fields:
- Not visible in preview
Relationships:
- Likely related to customer or service addresses
#### Invoice
Fields:
- Not visible in preview
Relationships:
- Likely related to customer billing and payments
#### PhoneNumber
Fields:
- number
- structure
- billing account
Relationships:
- Related to BillingAccountNumber
- Related to PhoneNumberStructure
#### MobileChurnLikeliness
Fields:
- churn indicators
- risk factors
Relationships:
- Associated with PhoneNumber
#### Link
Fields:
- id
- url
- title
- description
Relationships:
- Belongs to Links Portlet
#### SalesInfoNote
Fields:
- id
- type
- content
- timestamp
Relationships:
- Has AppointmentNote
- Has CompetitorNote
#### SalesConvNoteReportRow
Fields:
- noteData
- reportMetrics
Relationships:
- Derived from SalesInfoNote
#### FlashInfo
Fields:
- id
- message
- timestamp
- priority
Relationships:
- System Notifications
#### AttributeConfig
Fields:
- configuration properties
Relationships:
- One-to-many with Attribute
#### AttributeHistory
Fields:
- historical attribute data
Relationships:
- Many-to-one with Attribute
#### CustomerBlock
Fields:
- blocking information
Relationships:
- Many-to-one with Customer
#### ContactPerson
Fields:
- contact information
Relationships:
- Many-to-one with Customer
#### Image
Fields:
- Not visible in interface
Relationships:
- Likely related to other entities requiring image storage
#### PayableTicket
Fields:
- Not visible in interface
Relationships:
- Likely related to payment and ticket management entities
#### GamificationMessage
Fields:
- message content
- agentId
Relationships:
- Associated with agents
#### VBMProduct
Fields:
- customerId
- productName
- monthYearPeriod
- scoringTotal
Relationships:
- VBMProductDetails
- VBMDeclineReason
#### Turnover
Fields:
- partyId
#### SalesInfoNote
Fields:
- type
- filter criteria
Relationships:
- NotesFilter
- SearchResult
#### CCTOrgStructureElement
Fields:
- not visible in interface
Relationships:
- Used as parameter for updates and batch operations
#### Team
Fields:
- not visible in interface
Relationships:
- BiteUser
- Auth
- Service
#### InetUsage
Fields:
- internet usage metrics
Relationships:
- NetworkProvider
#### MobileUsage
Fields:
- mobile usage metrics
Relationships:
- NetworkProvider
#### VoiceUsage
Fields:
- voice call metrics
Relationships:
- NetworkProvider
#### PartySummaryItem
Fields:
- Not visible in interface
Relationships:
- Associated with partyId
#### Setting
Fields:
- Not visible in interface
Relationships:
- Independent entity
#### Not visible in preview
Fields:
- Not visible in preview
Relationships:
- Not visible in preview
#### ClearingAccount
Fields:
- Not visible in preview
Relationships:
- Managed by AbstractDao
#### Team
Fields:
- Not visible in preview
Relationships:
- Associated with BiteUser
- Associated with Auth
- Associated with Service
#### PartySummaryItem
Fields:
- Not visible in preview
Relationships:
- Related to partyId
#### StandardAddress
Fields:
- address fields
Relationships:
- Relates to Country entity
#### ProductHierarchy
Fields:
- hierarchy related fields
Relationships:
- Parent-child relationship between products
#### Party
Fields:
- BigDecimal fields
- List collections
Relationships:
- Associated with SettingService
#### Category
Fields:
- not visible in provided code
Relationships:
- Retrieved via SegCategory.list query
#### SearchResult
Fields:
- not visible in provided code
Relationships:
- Contains MyOpportunity data
#### Image
Fields:
- id
- uuser
Relationships:
- Retrieved based on id and user parameters
#### CustomerInteraction
Fields:
- customerId
Relationships:
- belongs to AbstractDao
#### PayableTicket
Fields:
- not visible in preview
Relationships:
- belongs to AbstractDao
- associated with Party
#### SearchResult
Fields:
- not visible in preview
Relationships:
- belongs to AbstractDao
#### Service
Fields:
- not visible in preview
Relationships:
- extends AbstractDao
- implements ServiceDao
#### SearchResult
Fields:
- not visible in preview
Relationships:
- extends AbstractDao
#### InetUsage
Fields:
- not visible in preview
Relationships:
- used in UsageDataDao operations
#### MobileUsage
Fields:
- not visible in preview
Relationships:
- used in UsageDataDao operations
#### NetworkProvider
Fields:
- not visible in preview
Relationships:
- used in UsageDataDao operations
#### PhoneNumber
Fields:
- billingAccountNumber
- mobileChurnLikeliness
Relationships:
- BillingAccountNumber
- MobileChurnLikeliness
#### InventoryProductGroup
Fields:
- Collection<InventoryProduct>
Relationships:
- InventoryProduct
#### CreditType
Fields:
- id
- type details
#### Turnover
Fields:
- partyId
Relationships:
- belongs to Party
#### Location
Fields:
- id
Relationships:
- mapped in HashMap by Long key
#### Invoice
Fields:
- partyId
Relationships:
- belongs to Party
#### Segment
Fields:
- not visible in provided code
Relationships:
- Retrieved via SegSegment.list query
#### ContactPerson
Fields:
- not visible in provided code
Relationships:
- Retrieved via list operation
#### CCTOrgStructureElement
Fields:
- not visible in provided code
Relationships:
- Managed through SqlMapClient
#### Reporting
Fields:
- id
Relationships:
- extends AbstractDao
- implements ReportingDao
#### UserInfoStatistics
Fields:
- not visible in preview
Relationships:
- extends AbstractDao
- implements UserInfoStatisticsDao
#### ChargingType
Fields:
- not visible in preview
Relationships:
- extends AbstractDao
- implements ChargingTypeDao
#### CustomerBlock
Fields:
- flashInfoId
Relationships:
- Associated with FlashInfo through flashInfoId
#### FlashInfo
Fields:
- Not fully visible in preview
Relationships:
- May have associated CustomerBlocks
#### Setting
Fields:
- Not visible in preview
Relationships:
- Standalone entity for application configuration
#### AppointmentNote
Fields:
- not visible in preview
Relationships:
- Mapped to database table
#### CompetitorNote
Fields:
- not visible in preview
Relationships:
- Mapped to database table
#### ImageSize
Fields:
- not visible in preview
Relationships:
- Retrieved via ImageSize.GetImageSizes query
#### GamificationMessage
Fields:
- not visible in preview
Relationships:
- Managed through SQL operations
#### UIText
Fields:
- Not visible in snippet
Relationships:
- Referenced as return type in getUITexts()
#### LinksPortlet
Fields:
- Not visible in snippet
Relationships:
- Referenced as return type in getAllLinks()
#### UnknownAreaCode
Fields:
- id (Long)
Relationships:
- Referenced as DTO class
#### SingleTurnaround
Fields:
- not visible in preview
Relationships:
- Managed by SingleTurnaroundDao
#### VBMProduct
Fields:
- not visible in preview
Relationships:
- Associated with VBMDeclineReason
#### VBMDeclineReason
Fields:
- not visible in preview
Relationships:
- Related to VBMProduct
#### SearchResult
Fields:
- not visible in preview
Relationships:
- Contains note search results
#### HashMap
Fields:
- key
- value
Relationships:
- Used for parameter mapping
#### Attribute
Fields:
- not visible in preview
Relationships:
- Related to AttributeConfig
- Related to AttributeHistory
#### ContextAwareCustomerUnlockRequest
Fields:
- not visible in preview
Relationships:
- Related to BiteUser
#### UserShopAssignment
Fields:
- not visible in preview
Relationships:
- Extends AbstractDao
- Implements UserShopAssignmentDao
#### VIPHistoryEntry
Fields:
- not visible in preview
Relationships:
- Extends AbstractDao
- Implements VIPHistoryDao
#### SetupType
Fields:
- not visible in preview
Relationships:
- Used in Set<SetupType> collections
#### Attribute
Fields:
- not fully visible in preview
Relationships:
- Associated with AttributeConfig
#### ToDoStatus
Fields:
- enum values not visible in preview
Relationships:
- Used in ToDoGroupNote
#### SalesInfoNote
Fields:
- type: SalesInfoNoteType
Relationships:
- Related to HistoryNote, ToDoGroupNote
#### LinksPortlet
Fields:
- key: String
- text: String
- url: String
- requiredAuthority: Auth
Relationships:
- implements Serializable
#### ProductOfferingTypeHandler
Relationships:
- extends BaseTypeHandler
#### AttributeHistory
Fields:
- attributeId: Long
- attributeConfig: AttributeConfig
- kundeId: Long
- booleanValue: Boolean
- numberValue: Integer
- textValue: String
- dateValue: Date
Relationships:
- implements Serializable
- references AttributeConfig
- references BiteUser
#### ContactPerson
Fields:
- customerId: Long
- customerRole: String
- dayPhoneNumber: String
- faxNumber: String
- id: Long
- isMainContact: boolean
- mail: String
- mobilephone: String
Relationships:
- extends Person
#### Message
Fields:
- Not visible in preview
#### Granularity
Fields:
- ALL
- DAILY
- WEEKLY
- MONTHLY
- QUATERLY
- YEARLY
#### GamificationRequest
Fields:
- agentId: String
- limit: int
- contentType: String
- apiKey: String
- queryString: String
Relationships:
- implements Serializable
#### AggregatedInventoryProductGroupUsage
Fields:
- parties: List<Party>
Relationships:
- extends InventoryProductGroupUsage
- contains List<Party>
#### BillingCycleEntry
Fields:
- id: Long
- vBlock: String
- column: int
- step: String
- from: Date
- to: Date
- hr: Date
Relationships:
- implements Serializable
#### InventoryProductGroupAssignable
Fields:
- description
- inventoryProductGroup
- parent
Relationships:
- Has-A InventoryProductGroup
- Has-A ProductLevel as parent
#### NotesFilter
Fields:
- USER_ID
- LAST_MOD_DATE
- NOTE_TYPE
Relationships:
- Uses SalesInfoNoteType enum
- Uses ToDoStatus enum
#### CreditType
Fields:
- id
- name
- description
- active
Relationships:
- Implements Serializable
#### SingleTurnaround
Fields:
- customerId: long
- rtCode: RTCode
- date: Date
- amount: double
Relationships:
- Implements Serializable
#### Status
Fields:
- CREATED
- SAVED
- APPROVED
- DISAPPROVED
- FINALIZED
- SENT
- ACCEPTED
Relationships:
- Enum type within Salesstage
#### Party
Fields:
- serialVersionUID
Relationships:
- Extends Customer
- Uses PartyDeclarationOfConsentInfo.StatusOfCompleteness
- References KumsSkzShop
#### LocationPlaceholder
Relationships:
- extends Location
- implements Serializable
#### Tupel<N,M>
Fields:
- value1: N
- value2: M
Relationships:
- implements Serializable
#### Team
Fields:
- id: Long
- name: String
- description: String
- creator: BiteUser
- createDate: Date
- members: List<BiteUser>
Relationships:
- implements Serializable
#### Image
Fields:
- id
- uuser
- filename
- name
- creationDate
- imageSizeId
Relationships:
- implements Serializable
#### MyOpportunity
Fields:
- partyid
- leadId
- partyType
- quoteNumber
- firstname
Relationships:
- implements Serializable
- references BiteUser
#### StandardAddress
Fields:
- additional
Relationships:
- implements Serializable
- references BiteUser
#### SalesConvEmailData
Fields:
- partyId
- sender
- recipient
- subject
- message
- attachmentUrls
Relationships:
- implements Serializable
#### PointOfSaleInfo
Fields:
- status
- dealerId
- dealerName
- delearEmailId
- dealerPhonenumber
- address
Relationships:
- implements Serializable
- uses StandardAddress
#### PhoneNumberStructure
Fields:
- countryCode
- onkz
- number
- extension
Relationships:
- implements Serializable
#### Product
Fields:
- productId: String
- productDescription: String
- inventoryProductGroup: InventoryProductGroup
- parent: ProductLevel
Relationships:
- Has-A InventoryProductGroup
- Has-A ProductLevel (parent)
#### EsbParty
Fields:
- partyId: long
- shortName: String
- address: StandardAddress
Relationships:
- Has-A StandardAddress
#### BANCollection
Fields:
- partyId: long
- bans: ArrayList<BillingAccountNumber>
Relationships:
- Contains-Many BillingAccountNumber
#### MobileChurnLikeliness
Fields:
- countryIdentification
- cityIdentification
- callNumber
- churnLikeliness
#### Customer
Fields:
- businessRuleDescription
- businessSegment
- businessVolume
Relationships:
- extends Person
- includes VBMProduct
#### IndexationStatus
Fields:
- INDEXED(2, "INDEXED_PRODUCTS")
- NOT_INDEXED(3, "EXCLUDED")
- INDEXED_NOT_STARTED(1, "INDEXED_PRODUCTS_NOT_USED")
- NOT_AVAILABLE(0, "")
- relatedValueInCustomerInventory
- relatedDwhValue
#### Inventory
Fields:
- aonCustomerNumber: Long
- assetId: Long
- contractBindingDate: Date
- contractId: Long
- customerId: Long
- id: long
- unlistedNumberIdentification: String
- networkOperator: String
Relationships:
- Implements Serializable
#### Segment
Fields:
- id: long
- name: String
- description: String
- sequence: int
- timestamp: Date
Relationships:
- Implements Serializable
#### Invoice
Fields:
- BOB_INVOICE_ID_PREFIX: String (constant)
- BOB_INVOICE_ID_MIN_LENGTH: int (constant)
Relationships:
- Implements Serializable
#### Auth
Fields:
- CONTENT_MYTODOs
- SEARCH_CUSTOMERS
- FEATURE_SEG_DISPLAY_1
- FEATURE_SEG_DISPLAY_2
- FEATURE_SEG_DISPLAY_3
- FEATURE_SEG_DISPLAY_4
Relationships:
- implements AuthInfo
#### BillingAccountNumber
Fields:
- ban: long
- brands: HashSet<String>
- brand: String
- numbers: List<PhoneNumber>
Relationships:
- contains PhoneNumber objects
#### ToDoNotesFilter
Fields:
- USER_ID: String
- LAST_MOD_DATE: String
- CREATE_DATE: String
- GROUP_NAME: String
Relationships:
- uses ToDoStatus from ToDoGroupNote
#### ContractOwnerAssignment
Fields:
- partyId: String
- accounts: List<BillingAccountNumber>
Relationships:
- Contains list of BillingAccountNumber objects
#### PartyCustomerLoyaltyInfo
Fields:
- serialVersionUID: long
- status: int
- isCustomer: boolean
#### PartyProfileNPSInfo
Fields:
- serialVersionUID: long
- scoringType: String
- scoringValue: String
- scoringDate: String
#### Category
Fields:
- id: long
- name: String
- description: String
- sequence: int
- timestamp: Date
Relationships:
- implements Serializable
#### ClearingAccount
Fields:
- accountNumber: Long
- ban: Long
- ben: Long
- partyId: Long
- invoiceType: String
- invoiceReceiverSalution: String
Relationships:
- implements Serializable
- implements Comparable<ClearingAccount>
#### SelectedProductOffering
Fields:
- productOffering: ProductOffering
- selected: boolean
Relationships:
- contains ProductOffering
#### InsuranceBrokerInfo
Fields:
- serialVersionUID
- ERROR
- LOADING
- NOT_RECEIVED
- LOADED
Relationships:
- implements Serializable
#### CustomerFilter
Fields:
- VIP_ID
- TURNOVERREGIONS_ID
Relationships:
- uses KeyValuePair
- uses VBMProductDetails
- uses DualSegment
#### ProductGroup
Fields:
- id
- code
- name
- description
- anbLookup
- updateTs
- nrNotes
- nrNotesImported
- nrSingleTurn
Relationships:
- implements Serializable
#### AttributeConfig
Fields:
- Serializable fields (not fully visible in preview)
Relationships:
- Implements Serializable
- References BiteUser
#### CustomerBlock
Fields:
- id: long
- name: String
- count: long
- imported: boolean
- data: String
- flashInfo: FlashInfo
Relationships:
- Implements Serializable
- Contains FlashInfo
#### SearchResultComparator
Relationships:
- Implements Comparator<Party>
- Implements Serializable
#### PartySearch
Fields:
- id
- leadId
- lastName
- firstName
- birthDate
- postcode
- city
- village
- street
- country
Relationships:
- implements Serializable
#### PartyAdditionalInfo
Fields:
- serviceClassInfo
- pointOfSaleInfo
- partyDeclarationOfConsentInfo
- partyProfileInfo
Relationships:
- implements Serializable
- contains ServiceClassInfo
- contains PointOfSaleInfo
- contains PartyDeclarationOfConsentInfo
- contains PartyProfileInfo
#### StatusOfCompleteness
Fields:
- COMPLETE("Grün")
- NONE("Rot")
- PARTIAL("Gelb")
- UNKNOWN("Unbekannt")
Relationships:
- inner enum of PartyDeclarationOfConsentInfo
#### OverviewStatus
Fields:
- OPEN
- PUT
- ACCEPTED
- DECLINED
- POST_CREATION
- CLOSED
- NONE
- WORKING
- DONE
- IN_PROCESS
#### VipExport
Fields:
- SEARCH_VIP_STATUS
- SEARCH_REPORTER
- SEARCH_TO
- SEARCH_FROM
- SERIALIZATION_DATE_PATTERN
#### BindingsFilter
Fields:
- CONTRACT_ID
- CONTRACT_START_ID
- PARTY_ID
- PRODUCT_DESCRIPTION_ID
#### ProductDetailFilter
Fields:
- location
- serviceNumber
- customerType
- productName
- baseServiceNumber
- secretLevel
- ban
- description
Relationships:
- implements Serializable
#### CucoLogs
Fields:
- kundeId
- name
- userId
- passwordType
- ban
- LogType
Relationships:
- implements Serializable
#### ProductFeasibilityStatus
Fields:
- INSTALLABLE
- NOT_INSTALLABLE
- INSTALLED
Relationships:
- implements Serializable
#### UIText
Fields:
- key: String
- value: String
Relationships:
- implements Serializable
#### InsuranceBrokerContractInfo
Fields:
- marketingContractTypeName: String
- deviceMarketingName: String
- imei: String
Relationships:
- implements Serializable
#### InventoryProductGroupAssignation
Fields:
- inventoryProductGroupId: long
- levelId: long
- productId: String
Relationships:
- implements Serializable
#### CrmAuthenticationInfo
Fields:
- status (int)
- password (String)
- serialVersionUID (long)
Relationships:
- implements Serializable
#### ProductOffering
Fields:
- A1BN(1, 'a1bn')
- MOBILE_INTERNET_ET_GT(2, 'etgt')
- FIB(3, 'fib')
- BIZKO(4, 'bizko')
- Additional product offerings...
Relationships:
- implements Serializable
#### AccessToken
Fields:
- targetSystem (String)
- token (String)
- NONE (static final AccessToken)
#### ServiceClassInfo
Fields:
- serviceClass: int
- serviceClassText: String
- SERVICE_CLASS_ERROR: int (constant)
- SERVICE_CLASS_LOADING: int (constant)
Relationships:
- implements Serializable
#### BusinessOffer
Fields:
- customerId: Long
- productDescription: String
Relationships:
- implements Serializable
#### InventoryProductGroupUsage
Fields:
- name: String
- number: int
- anb: boolean
- order: int
Relationships:
- implements Serializable
#### Turnover
Fields:
- partyId: long
- month: Date
- turnoverTa: float
- marginTa: float
- turnoverMk: float
- marginMk: float
#### Person
Fields:
- firstname: String
- gender: String
- lastname: String
- birthdate: Date
- title: String
- salutation: String
#### QuoteClearanceConfigurationHolder
Fields:
- ArrayList<ProductOffering> offerings
- ArrayList<String> roles
Relationships:
- Contains ProductOffering objects
- Contains role identifiers as strings
#### PartyProfileInfo
Fields:
- serialVersionUID
- ERROR (99)
- LOADING (-1)
- NOT_RECEIVED (98)
- LOADED
#### ReadOnlyStatusBasedOnCategory
Fields:
- EDITABLE
- READ_ONLY
#### GamificationMessageComparator
Fields:
- serialVersionUID
Relationships:
- implements Comparator<GamificationMessage>
- implements Serializable
#### MatrixPosition<T>
Fields:
- segment
- category
- sequence
- object
Relationships:
- implements Serializable
#### Service
Fields:
- id
- validity
- name
- productCode
- costs
- comment
- product
Relationships:
- implements Serializable
- uses PeriodOfValidity
#### GamificationData
Fields:
- cucoMessages: GamificationCuCoMessages
Relationships:
- Contains GamificationCuCoMessages
#### GamificationResponse
Fields:
- data: GamificationData
- status: String
- unreadMsgCount: int
Relationships:
- Contains GamificationData
#### ChargingType
Fields:
- MOBILE_CHARGING_TYPE: Long (constant = 3L)
- id: Long
- name: String
- description: String
#### PartyProfileSolvency
Fields:
- creditLimit (String)
#### InventoryProductGroup
Fields:
- id (Long)
- name (String)
- order (int)
- visible (boolean)
- anb (boolean)
#### PartySummaryPrintModel
Fields:
- party (Party)
Relationships:
- Has-a Party
- Uses PartySummaryItem from product package
#### UserInfoStatistics
Fields:
- nrOfCustomers: int
- nrOfExpiringBindings: int
- nrOfQuotes: int
- nrOfTasks: int
- nrOfOpenToDos: int
Relationships:
- implements Serializable
#### SupportingUnit
Fields:
- status: int
- skzText: String
- supportName: String
- ERROR: int (constant)
- LOADING: int (constant)
- NOT_RECEIVED: int (constant)
- LOADED: int (constant)
Relationships:
- implements Serializable
#### CMBuddyLogin
Fields:
- username: String
- password: String
- serialVersionUID: long (constant)
Relationships:
- implements Serializable
#### MyFlashInfo
Fields:
- partyId: Long
- creatorName: String
Relationships:
- extends FlashInfo
- implements Serializable
#### VipStatus
Fields:
- intValue: Integer
- state: State
Relationships:
- implements Serializable
#### ProductLevel
Fields:
- productLevelId: Long
- productLevelDescription: String
- subProductLevels: List<ProductLevel>
- products: List<Product>
- inventoryProductGroup: InventoryProductGroup
Relationships:
- implements Serializable
- implements InventoryProductGroupAssignable
- has-many ProductLevel
- has-many Product
#### FlashInfo
Fields:
- Date from
- Date to
- List<CustomerBlock> customerBlocks
- BiteUser creator
Relationships:
- Extends FlashInfoBase
- Contains CustomerBlock list
- References BiteUser
#### Recipient
Fields:
- Long recipientId
- String recipientName
Relationships:
- Implements Serializable
#### VIPHistoryEntry
Fields:
- Long vipHistoryId
- Long customerId
- Date created
- Long userId
- String name
- String reported
- Integer oldStatus
- Integer newStatus
Relationships:
- Implements Serializable
#### PartnerCenterAccessTokenRequest
Fields:
- targetSystem
- sourceSystem
- countryCode
Relationships:
- extends AccessTokenRequest
#### RTCode
Fields:
- prodNum
- description
- sales
- months
Relationships:
- implements Serializable
#### GamificationCuCoMessages
Fields:
- agentId
- messages
Relationships:
- implements Serializable
- contains List<GamificationMessage>
#### CustomerBinding
Fields:
- partyId
- contractStart
- contractEnd
- productDescription
- customer
- service
- product
Relationships:
- Contains Customer object
- References AddressLinkData
#### Attribute
Fields:
- attributeId
- attributeConfig
- kundeId
Relationships:
- References AttributeConfig
- Associated with BiteUser
#### MatrixData
Fields:
- segments
- categories
- matrixData
Relationships:
- Contains ArrayList<Segment>
- Contains ArrayList<Category>
- Contains nested HashMap of ProductGroup lists
#### FlashInfoBase
Fields:
- id
- title
- text
- active
- popup
- roles
- viewed
Relationships:
- Has many Role objects through roles list
#### KumsCustomerInfo
Fields:
- vipStatus
- lastChangeDate
#### PayableTicket
Fields:
- id
- customerId
- ban
- lknz
- onkz
- number
- service
- comment
Relationships:
- References Service object
- References BiteUser object (partial visible in preview)
#### SimplePage<T>
Fields:
- count: long
- content: ArrayList<T>
- isInputValid: boolean
Relationships:
- implements Serializable
#### CuCoGamificationLoginMessage
Fields:
- messageType: String
- id: String
- pswd: String
- sessionKey: String
Relationships:
- implements Serializable
#### UserAdminSegment
Fields:
- featureSeg1: String
- featureSeg2: String
- featureSeg3: String
- featureSeg4: String
- featureSeg5: String
Relationships:
- implements Serializable
#### ImageSize
Fields:
- id: Long
- name: String
- width: Long
- height: Long
Relationships:
- implements Serializable
#### ProductHierarchy
Fields:
- productId: String
- productDescription: String
- productLevel1Id: Long
- productLevel1Description: String
- productLevel2Id: Long
- productLevel2Description: String
- productLevel3Id: Long
- productLevel3Description: String
Relationships:
- implements Serializable
#### CrmAuthenticationPasswordInfo
Fields:
- value: String
- type: String
- serialVersionUID: long
Relationships:
- implements Serializable
#### ProductOverviewConfigurations
Fields:
- amountOfSubscriptionToPreload
- depthOfProductTree
- mode
- whitelist
- blacklist
Relationships:
- implements Serializable
#### CustomerInteractionAttributes
Fields:
- PRODUCT
- REASON1
- REASON2
- REASON3
- RESULT
- NOTE
#### BillingCycle
Fields:
- billingDate
- entries
Relationships:
- implements Serializable
- contains List<BillingCycleEntry>
#### UserShopAssignment
Fields:
- userName: String
- shopID: String
Relationships:
- Implements Serializable
#### PhoneNumber
Fields:
- broadbandPossible: Boolean
- cityIdentificationNumber: String
- connectorSpecification: String
- contractNumber: Long
- countryIdentificationNumber: String
- customerId: Long
- unlistedNumberIdentification: String
Relationships:
- Implements Serializable
#### GamificationMessage
Fields:
- serialVersionUID: long
- url: String
- messageUid: String
- timestamp: String
- timestampDateFormat: Date
- type: String
- title: String
- message: String
Relationships:
- Implements Serializable
#### OpportunityFilter
Fields:
- QUOTE_NUMBER
- FILTER_TYPE
- PARTY_ID
- FIRST_NAME
#### UserShopAssignmentLogLine
Fields:
- userName: String
- logText: String
Relationships:
- implements Serializable
#### AccessTokenRequest
Fields:
- targetSystem: String
- sourceSystem: String
- parameters: HashMap<String, String>
Relationships:
- implements Iterable<Entry<String, String>>
- implements Serializable
#### ProductFeasibility
Fields:
- productId: String
- displayName: String
- status: ProductFeasibilityStatus
Relationships:
- Uses ProductFeasibilityStatus enum
#### FreeUnits
Fields:
- ACCUMULATOR_UNIT_MIN: String
- ACCUMULATOR_UNIT_SEC: String
- ACCUMULATOR_UNIT_MSEC: String
#### FreeUnitsData
Fields:
- freeUnits: ArrayList<FreeUnitsResult>
- sumsPerProduct: ArrayList<FreeUnitsResult>
- sumsPerSidGroup: ArrayList<FreeUnitsResult>
- dateOf: Date
- usageEnd: Date
Relationships:
- Contains FreeUnitsResult collections
#### FreeUnitsResult
Fields:
- name: String
- description: String
- isPulseUnit: boolean
- minutesMaximum: BigInteger
- minutesUsed: BigInteger
- minutesUnused: BigInteger
Relationships:
- implements Serializable
#### ContextAwareCustomerUnlockRequest
Fields:
- Not fully visible in preview
Relationships:
- Likely extends or implements base request classes
#### UnlockRequestContext
Fields:
- Not fully visible in preview
Relationships:
- Likely used by ContextAwareCustomerUnlockRequest
#### DateValueBean
Fields:
- date: Date
- value: Double
Relationships:
- implements Serializable
#### UsageDetail
Fields:
- date: Date
- tarif: String
- value: Double
- fee: Double
Relationships:
- implements Serializable
#### AonProduct
Fields:
- aonNumber
- productNames (ArrayList<String>)
- phoneNumber
- phoneNumberStructure
Relationships:
- Aggregates PhoneNumberStructure
#### Product
Relationships:
- Uses Party
- Uses ProductType
- Uses NetworkProvider
- Uses PhoneNumberStructure
#### MobileUsage
Fields:
- date
- duration
- connectionFees
- upload
- download
- gbIbData
- gbObEuData
#### NetworkProvider
Fields:
- value: String
- label: String
#### ProductType
Fields:
- VOICE_FIXED_LINE
- INET_FIXED_LINE
- INET_FIXED_LINE_PRODUCT
- MOBILE
- MOBILE_BAN
#### InetUsage
Fields:
- date: Date
- duration: long
- uploadVolume: long
- downloadVolume: long
- subscriptionFee: double
- variableFee: double
- highUsageFee: double
- transferVolumeOverrun: long
Relationships:
- implements Serializable
#### VoiceUsage
Fields:
- date: Date
- duration: Double
- connectionFee: Double
- zone: String
- timeType: String
- provider: String
Relationships:
- implements Serializable
#### ProductNode
Fields:
- label: String
- value: String
- party: Party
- phoneNumberStructure: PhoneNumberStructure
Relationships:
- implements Product
- implements Serializable
#### ProductChartRequest
Fields:
- party: Party
- type: ProductType
- provider: NetworkProvider
- value: String
Relationships:
- implements Product
- implements Serializable
#### ProductRootNode
Fields:
- rootProduct: ProductNode
Relationships:
- Contains one ProductNode as root
#### VBMProductDetails
Fields:
- productId: String
- productName: String
- maxScoring: Long
- clarifyProductId: String
- partWebProductId: String
- description: String
#### VBMProductFeedback
Fields:
- customerId: Long
- productId: String
- monthYearPeriod: String
- selectedDeclineReason: VBMDeclineReason
- feedbackTime: Date
Relationships:
- Contains VBMDeclineReason
#### VBMProduct
Fields:
- customerId: Long
- productId: String
- monthYearPeriod: String
- party: Party
- scoringTotal: Long
- productDetail: VBMProductDetails
Relationships:
- Has-A Party
- Has-A VBMProductDetails
#### VBMDeclineReason
Fields:
- declineReasonId: String
- declineReasonText: String
- productId: String
#### TariffSimulationContainer
Fields:
- currentTariff: Tariff
- tariffLists: TariffLists
- esbResponseMessage: Message
Relationships:
- Has-A Tariff
- Has-A TariffLists
- Has-A Message
#### Price
Fields:
- Float gross
- Float net
#### TariffLists
Fields:
- List<Tariff> allTariffsList
- List<Tariff> recommendedTariffsList
Relationships:
- Contains Tariff objects
#### TariffSimulation
Fields:
- Not visible in preview
Relationships:
- Not visible in preview
#### Tariff
Fields:
- id
- name
- characteristics
- contributionMargins
Relationships:
- Contains TariffCharacteristic
- Contains ContributionMargin
#### TariffCharacteristic
Fields:
- id
- name
- code
- price
- usedInSimulationCalculation
Relationships:
- Contains Price
#### ContributionMargin
Fields:
- price
- indicator
Relationships:
- Contains Price
- Uses Indicator enum
#### TariffSimulationRequest
Fields:
- phoneNumber
- billingAccountNumber
Relationships:
- Uses PhoneNumberStructure
- Uses BillingAccountNumber
- Uses SimulationType
#### MobilPointsBundle
Fields:
- phoneNumber
- mobilPoints
- businessHardwareReplacement
Relationships:
- Contains MobilPoints
- Contains BusinessHardwareReplacement
#### BusinessHardwareReplacement
Fields:
- billingAccountNumber
- simCount
- bindingMonthsPerSim
- openBasicFeePerBan
- possibleHardwareReplacement
#### MobilPoints
Fields:
- amdocsPoints: long
- partnerWebPoints: long
- clarifyPoints: long
- number: PhoneNumberStructure
Relationships:
- Aggregates PhoneNumberStructure
#### ChartData<K,V>
Fields:
- data: LinkedHashMap<String, ChartDataSet<K,V>>
Relationships:
- Contains ChartDataSet instances
#### ChartDataSet<K,V>
Fields:
- id: String
- data: LinkedHashMap<K,V>
Relationships:
- Used by ChartData class
#### Chart
Fields:
- imageMap
- imageMapId
- mimeType
Relationships:
- extends File
#### ChartOptions
Fields:
- width
- height
- imgMapId
- colors
Relationships:
- implements Serializable
#### ChartMetaData
Fields:
- imageMap
- imageMapId
- hash
Relationships:
- implements Serializable
#### ChartColor
Fields:
- r: int
- g: int
- b: int
#### ProductMoveAction
Fields:
- UP
- DOWN
#### MarketingProductGroup
Fields:
- PRODUCT
- ADDITIONAL_PRODUCT
#### DefaultProductNode
Fields:
- BigDecimal
- ProductType
- IndexationStatus
Relationships:
- Inherits from BaseNode
- Implements Serializable
#### NodeHelper
Relationships:
- Uses Node
- Uses PartyNode
- Uses ProductType
#### ProductHeaderNode
Fields:
- nameHeader
- detailsHeader
- idxInfoHeader
- callNumberHeader
- brandHeader
- validFromHeader
- validToHeader
Relationships:
- Inherits from BaseNode
#### Node
Fields:
- text
- id
- parent
- children
Relationships:
- extends Serializable
- contains ArrayList<BaseNode>
#### SAPSubscriptionNode
Fields:
- consigneeId
- consigneeName
Relationships:
- extends SubscriptionNode
- implements Serializable
#### SubscriptionHeaderNode
Fields:
- subscriptionIdHeader
- custAccountNoHeader
- callNumberHeader
- addressLine1Header
- addressLine2Header
- addressLine3Header
Relationships:
- extends SubscriptionNode
#### CuCoComponentProductPrice
Fields:
- price (CuCoPrice)
- taxRate (BigDecimal)
- idxStatus (IndexationStatus)
- idxStartDate (Date)
- basePrice (CuCoPrice)
Relationships:
- Extends CuCoProductPriceBase
- Uses IndexationStatus enum
- Contains CuCoPrice objects
#### CCTSupervisorSelect
Fields:
- superVisor (String)
- approvalLevel (int)
- release (String)
- date (String)
- comment (String)
Relationships:
- Implements Serializable
#### Promotion
Fields:
- soc (String)
- reasonCode (String)
- reasonDescription (String)
- effectiveDate (Date)
- expirationDate (Date)
- discountPercent (double)
Relationships:
- Implements Serializable
#### PhysicalResourceNode
Fields:
- text: String
Relationships:
- extends BaseNode
- implements Serializable
#### PartyNode
Fields:
- name: String
- address: String
Relationships:
- extends BaseNode
- implements Serializable
#### DefaultSubscriptionType
Fields:
- Wireline
- Mobile
- Mixed
- Marketplace
- BillableUser
- Unknown
Relationships:
- implements Serializable
#### CallNumber
Fields:
- countryCode: String
- onkz: String
- tnum: String
Relationships:
- implements Serializable
#### DefaultSubscriptionNode
Fields:
- accountNumber: String
- subscriptionId: String
- type: DefaultSubscriptionType
- callNumber: CallNumber
Relationships:
- extends SubscriptionNode
#### BillableUser
Fields:
- userName: String
Relationships:
- implements Serializable
#### BaseNode
Fields:
- id: String
- contractSegment: String
- parent: BaseNode
- depth: int
- effectiveDepthForView: int
- children: ArrayList<BaseNode>
- childrenLoaded: boolean
Relationships:
- implements Node
- self-referential parent-child relationship
- uses IndexationStatus
#### Coordinates
Fields:
- longitude: double
- latitude: double
Relationships:
- implements Serializable
#### LastMileId
Fields:
- countryCode: String
- onkz: String
- tnum: String
Relationships:
- implements Serializable
#### GetPartySummaryResponse
Fields:
- serialVersionUID: long
- errorResponse: boolean
- errorText: String
- productSummaryItems: ArrayList<PartySummaryItem>
- parties: ArrayList<Party>
Relationships:
- implements Serializable
#### SAPProductNode
Fields:
- text: String
- equipmentAttributes: MetaData
Relationships:
- extends BaseNode
- implements Serializable
#### MetaData
Fields:
- ArrayList<MetaDataEntry> list
- HashMap<String, MetaDataEntry> map
Relationships:
- Contains MetaDataEntry objects
#### CuCoProductPriceBase
Fields:
- String productPriceId
- String productOfferingPriceId
- String Name
Relationships:
- Base class for product price hierarchy
#### CuCoProdPriceCharge
Fields:
- ProdPriceChargeType chargeType
Relationships:
- Extends CuCoComponentProductPrice
- Contains ProdPriceChargeType enum
#### CCTClearanceStage
Fields:
- productOfferingId
- quoteNumber
- login
- name
- Date fields (implied from preview)
Relationships:
- References BiteUser
#### EmptyProductNode
Relationships:
- Extends BaseNode
#### AccountNode
Fields:
- Not visible in preview
Relationships:
- Implied inheritance relationship
#### locationMap
Fields:
- HashMap<Long, ArrayList<Location>>
Relationships:
- Maps party IDs to lists of locations
#### partyNodes
Fields:
- ArrayList<BaseNode>
Relationships:
- Contains hierarchical party node information
#### GeoCallNumber
Fields:
- countryCode: String
- onkz: String
- tnum: String
#### Location
Fields:
- partyId: long
- locationId: String
- address: String
- city: String
- street: String
- poBox: String
- coordinates: Coordinates
- locationType: LocationType
Relationships:
- Contains Coordinates object
- Uses LocationType enum
#### SAPPhysicalResourceNode
Fields:
- text
- equipmentAttributes
Relationships:
- extends BaseNode
- implements Serializable
#### BRKAccountInfo
Fields:
- accountNumber
- accountStatus
- accountName
- handlingFee
Relationships:
- implements Serializable
#### CuCoProdPriceAlterations
Fields:
- frequency
- UnitOfMeasure
- alterationType
Relationships:
- extends CuCoComponentProductPrice
#### CCTOrgStructureElement
Fields:
- userID
- approvalLevel
- supervisorUserID
- user
- supervisor
- BiteUser
Relationships:
- Implements Serializable
- References BiteUser
#### LocationNode
Fields:
- location
Relationships:
- Extends BaseNode
- Contains Location object
#### AsyncPlaceholderNode
Relationships:
- Extends BaseNode
- Implements Serializable
#### CuCoPrice
Fields:
- units: String
- amount: BigDecimal
Relationships:
- implements Serializable
#### CCTAuthorizedQuoteApproversForLevel
Fields:
- level: int
- approvers: ArrayList<CCTOrgStructureElement>
Relationships:
- implements Serializable
- contains CCTOrgStructureElement
#### MetaDataEntryType
Fields:
- STRING(1)
- LONG(2)
- BOOLEAN(3)
- DATE_TIME(4)
- DECIMAL(5)
- LKMS_ID(6)
- MBIT(7)
- KBIT(8)
- MB(9)
- value: int
#### SubscriptionTree
Fields:
- ArrayList<BaseNode> productNodes
- DefaultSubscriptionNode subscriptionNode
Relationships:
- Contains BaseNode
- Contains DefaultSubscriptionNode
#### AutoVvlInfo
Fields:
- AutoVvlStatus autoVvlStatus
- Date latestCommitmentEndDate
- String commitmentDuration
- Date commitmentDurationStartTime
Relationships:
- Contains AutoVvlStatus enum
#### SubscriptionNode
Fields:
- String accountNumber
- String vertragNoForDisplay
- String subscriptionId
- String topLevelProducts
- ArrayList<BaseNode> childrenWithMatchinCa
Relationships:
- Extends BaseNode
- Implements AccountAware
- Contains ArrayList<BaseNode>
#### MetaDataEntry
Fields:
- name
- description
- value
- id
- type
- validForStart
- validForEnd
Relationships:
- implements Serializable
#### PartySummaryItem
Fields:
- name
- url
- count
Relationships:
- implements Serializable
#### Equipment
Fields:
- id
- name
- parent
- parentId
Relationships:
- implements Serializable, Comparable<Equipment>
- self-referential through parent field
#### EquipmentTree
Fields:
- equipmentSums
- equipmentConsignee
- party
- materialSum
Relationships:
- extends Equipment
- contains ArrayList<EquipmentSum>
- contains EquipmentConsignee
- references Party
#### EquipmentAttribute
Fields:
- equipmentId
Relationships:
- extends KeyValuePair
#### EquipmentSum
Fields:
- id
- title
- count
- EMPTY
Relationships:
- implements Serializable
- implements Comparable<EquipmentSum>
#### EquipmentConsignee
Fields:
- id
- summaryShort
- summary
- partyId
- title
- name1
- name2
- plz
- city
- street
Relationships:
- implements Serializable
#### DummyEquipmentConsignee
Relationships:
- extends EquipmentConsignee
#### HistoryNote
Relationships:
- extends SalesInfoNote
#### HistoryLevel
Fields:
- NOTE
- PRODUCT_NOTE
- TODO_GROUP_NOTE
#### HistoryTitle
Fields:
- NOTE_CREATED
- NOTE_UPDATED
- NOTE_FINALIZED
- NOTE_DELETED
- ATTACHMENT_ADDED
- ATTACHMENT_DELETED
- TERMIN_CREATED
- TERMIN_MIGRATED
- TERMIN_DELETED
- PRODUCT_CREATED
#### FeedbackQuestionsRow
Fields:
- attributeName: String
- attributeType: String
- numberValue: Integer
- booleanValue: Boolean
- textValue: String
#### SimpleNote
Fields:
- Inherits from SalesInfoNote
Relationships:
- extends SalesInfoNote
#### SalesInfoNote
Fields:
- Date
- List<Party>
- BiteUser
Relationships:
- extends SalesInfoOverview
- aggregates Party
- aggregates BiteUser
#### AppointmentNote
Fields:
- CommunicationType
- CommunicationChannel
- ContactType
Relationships:
- extends SalesInfoNote
#### SalesConvProductNoteRow
Fields:
- productNoteId
- predecessorSiNoteId
- productCategory
- productDisplayName
- setupCategory
- quoteStatus
- turnoverQuantity
- assigneeType
- contactCount
#### SalesInfoNoteHistoryModificationType
Fields:
- CREATED
- CREATED_BY_PREDECESSOR
- FOLLOWER_CREATED
- MODIFIED
- DELETED
- ASSIGNED
- ORDER_ACCEPTED
- IN_PROCESSING
- COMPLETED_SUCCESSFULLY
- PRODUCT_SAVED
- APPOINTMENT_COMMUNICATION
#### SbsNoteReportRow
Fields:
- Date
- CommunicationChannel
- CommunicationType
- ContactSource
- ContactType
Relationships:
- Uses enums from visitreport.sbs package
#### SalesInfoNoteHistory
Fields:
- salesInfoNoteId
- modificationTimestamp
- modificationUser
- modificationType
- predecessorId
Relationships:
- References UserInfo
- References SalesInfoNoteHistoryModificationType
#### Task
Fields:
- serialVersionUID
Relationships:
- implements Serializable
- uses StandardAddress
- uses BiteUser
#### SalesConvNoteReportRow
Fields:
- siNoteId
- predecessorSiNoteId
- campaignId
- campaignName
- lastUpdate
- lastModUser
- customerId
Relationships:
- uses BiteUser
#### CompetitorNote
Fields:
- name
- productGroupName
- productName
- bindingDate
- reminderMailSentDate
Relationships:
- extends SalesInfoNote
#### SalesInfoOverviewRow
Fields:
- Serializable interface implementation
Relationships:
- Implements Serializable
- Extended by concrete row implementations
#### ToDoGroupNote
Fields:
- ArrayList contents
Relationships:
- Uses BiteUser
- Uses PointOfSaleInfo
- Uses SBSProductNote
#### SmartHomeNew
Fields:
- smartHomeTariff (boolean)
- smartHomeTariffPrice (BigDecimal)
- smartHomeTariffString
Relationships:
- Extends SmartHomeBase
#### SecurityOld
Fields:
- cyberDefence: boolean
- cyberDefencePrice: BigDecimal
- cyberDefenceText: String
Relationships:
- extends SecurityBase
#### InternetSpeedNew
Fields:
- productName: String
- a1InternetProtection: boolean
Relationships:
- extends InternetSpeedBase
#### MobileTariff
Fields:
- serialVersionUID: long
Relationships:
- implements Serializable
#### MobileTariffNew
Fields:
- tariffValue: String
- basicCharge: BigDecimal
Relationships:
- extends MobileTariffBase
#### ServicesOld
Fields:
- protectDataText: String
- initialSetupText: String
- basicEquipment: String
- protectMobileText: String
Relationships:
- extends ServicesBase
#### SecurityBase
Fields:
- serialVersionUID: long
- internal: boolean
Relationships:
- implements Serializable
#### MobileTariffBase
Fields:
- minutes
- serialVersionUID
Relationships:
- implements Serializable
#### InternetSpeedOld
Fields:
- virusProtection
- virusProtectionPrice
Relationships:
- extends InternetSpeedBase
#### Payment
Fields:
- serialVersionUID
Relationships:
- implements Serializable
#### SecurityNew
Fields:
- a1CyberProtectionSingle: boolean
- a1CyberProtectionSinglePrice: BigDecimal
Relationships:
- extends SecurityBase
#### SmartHomeOld
Fields:
- smartSolution: boolean
- smartSolutionPrice: BigDecimal
- smartSolutionText: String
Relationships:
- extends SmartHomeBase
#### MobilePhoneBase
Fields:
- serialVersionUID: long
- mobilePhone: String
Relationships:
- implements Serializable
#### InternetSpeedMainUseType
Fields:
- STREAMING
- SURF
- SOCIAL_MEDIA
- MAIL
- GAMING
#### Household
Fields:
- type
- serialVersionUID
Relationships:
- implements Serializable
- uses HouseholdType
#### TV
Fields:
- serialVersionUID
Relationships:
- implements Serializable
#### MusicSpeakerType
Fields:
- ON_EAR
- IN_EAR
- SPEAKER
#### ServicesNew
Fields:
- a1InitialSetup: boolean
- a1InitialSetupPrice: BigDecimal
Relationships:
- extends ServicesBase
#### MobileTariffOld
Fields:
- serialVersionUID: long
- tariffValue: String
- BigDecimal fields (partial)
Relationships:
- extends MobileTariffBase
#### SummaryItem
Fields:
- name
- serialVersionUID
Relationships:
- implements Serializable
#### MobilePhoneMainUseType
Fields:
- COMMUNICATION
- SOCIAL_MEDIA
- PHOTO_VIDEO
- STREAMING
- GAMING
- NAVIGATION
- SHOPPIMG
#### InternetSpeedType
Fields:
- MBIT_20
- MBIT_40
- MBIT_80
- MBIT_150
- MBIT_300
#### InternetSpeed
Fields:
- serialVersionUID
Relationships:
- implements Serializable
#### DigitalSellingNote
Fields:
- BigDecimal values
- List collections
Relationships:
- XmlRootElement annotated
#### MusicApp
Fields:
- RADIO
- SPOTIFY
- APPLE_MUSIC
- DEEZER
- AMAZON_PRIME_MUSIC
- AUDIBLE
- PODCASTS
#### TVOld
Fields:
- Inherits fields from TVBase
Relationships:
- Extends TVBase
#### Security
Fields:
- serialVersionUID
Relationships:
- Implements Serializable
#### InternetType
Fields:
- WIRE (Leitung)
- MOBILE (Mobil)
#### InternetSpeedBase
Fields:
- serialVersionUID
- InternetType
Relationships:
- implements Serializable
#### MobilePhoneOld
Fields:
- partPayment
- partPaymentPrice
- boolean fields inherited from MobilePhoneBase
Relationships:
- extends MobilePhoneBase
#### PaymentOld
Fields:
- serialVersionUID
- appsPayment
Relationships:
- implements Serializable
#### ServicesBase
Fields:
- eScoot (boolean)
- BigDecimal fields for pricing/financial data
Relationships:
- Implements Serializable
#### MobilePhone
Fields:
- XML annotated fields for mobile phone attributes
Relationships:
- Implements Serializable
#### SmartHome
Fields:
- XML annotated fields for smart home attributes
Relationships:
- Implements Serializable
#### Services
Fields:
- serialVersionUID
Relationships:
- implements Serializable
#### TVType
Fields:
- WIRE
- MOBILE
- SAT
#### TVNew
Relationships:
- extends TVBase
#### TVBase
Fields:
- tvType: TVType
- price: BigDecimal
Relationships:
- implements Serializable
#### SmartHomeBase
Fields:
- comfort: boolean
- price: BigDecimal
Relationships:
- implements Serializable
#### HouseholdType
Fields:
- APARTMENT
- HOUSE
#### MobileTariffMainUseType
Fields:
- COMMUNICATION
- SOCIAL_MEDIA
- PHOTO_VIDEO
- STREAMING
- GAMING
- NAVIGATION
- SHOPPIMG
#### MobilePhoneNew
Fields:
- partPayment
- partPaymentPrice
Relationships:
- extends MobilePhoneBase
#### PaymentNew
Fields:
- serialVersionUID
- a1Master
Relationships:
- implements Serializable
#### Music
Fields:
- usedMusicApps
- serialVersionUID
Relationships:
- implements Serializable
#### Country
Fields:
- iso3166Alpha2
- iso3166Alpha3
- nameGerman
Relationships:
- implements Serializable
#### SetupType
Fields:
- NEW
- NEW_SERVICE
- NEW_LINE
#### HandlingAssigneeType
Fields:
- PARTNER_WEB
- SHOP
#### SBSOrgUnit
Fields:
- id
- name
- street
- postalCode
- city
Relationships:
- implements Serializable
#### CommunicationType
Fields:
- WRITTEN
- PERSONAL
- TELEPHONIC
#### ContactSource
Fields:
- LEAD_SYSTEM
- POLARIS
- SELF_INITIATIVE
- CUSTOMER_REQUEST
#### SBSProductNote
Fields:
- BigDecimal
- List
- ContactPerson
- ProductOffering
- SalesInfoNote
Relationships:
- extends SalesInfoNote
#### SBSProduct
Fields:
- productId
- productAlternativeId
- productDisplayName
- productCategory
- defaultConfig
- siNoteClass
- active
Relationships:
- implements Serializable
#### SetupCategory
Fields:
- CONTRACT_EXTENSION
- NEW_ESTABLISHMENT
- UPGRADE
- DOWNGRADE
- SERVICE
- INFORMATION
- SALE
- ADD_OPTIONS
- TARIFCHANGE_UPGRADE
- TARIFCHANGE_DOWNGRADE
#### SBSNote
Fields:
- Attribute
- ContactPerson
- AppointmentNote
- SalesInfoNote
- ToDoGroupNote
Relationships:
- Extends or implements multiple note-related classes
- Contains lists of attributes and contact information
#### QuoteStatus
Fields:
- OPEN
- PUT
- ACCEPTED
- DECLINED
- OBSOLETE
- POST_CREATION
#### ContactType
Fields:
- SERVICE_BUSINESS_CASE
- SALES_PITCH
- ESCALATION
- CUSTOMER_CARE
#### VisitReportDetail
Fields:
- note: SalesInfoNote
- editable: boolean
Relationships:
- Contains SalesInfoNote
#### CommunicationChannel
Fields:
- INBOUND
- OUTBOUND
#### SBSProductNoteConfig
Fields:
- List<SBSProduct> products
- List<SBSOrgUnit> orgUnits
Relationships:
- Contains list of SBSProduct objects
- Contains list of SBSOrgUnit objects
#### GenericNote
Fields:
- List<FileAttachment> fileAttachments
Relationships:
- Extends SalesInfoNote
- Contains list of FileAttachment objects
#### FileAttachment
Fields:
- Date date
- BiteUser user
Relationships:
- References BiteUser for user information
#### SalesConvNote
Fields:
- attributes
- fileAttachments
- productNotes
Relationships:
- extends SalesInfoNote
- contains List<Attribute>
- contains List<FileAttachment>
- contains List<SBSProductNote>
#### TeamEmailAdminGroup
Fields:
- id
- teamName
- teamEmail
- userList
- isDefault
Relationships:
- implements Serializable
#### ProductHistoryItem
Fields:
- id
- productNoteId
- note
- creationUser
- creationDate
Relationships:
- implements Serializable
- references BiteUser
#### ContactType
Fields:
- PHONE_OUTBOUND
- PHONE_INBOUND
- LEAD
- MAIL
#### PartyModel
Fields:
- id: Long
- bans: String
- commercialRegisterNumber: String
- businessSegment: String
- serviceClass: String
- gender: String
- firstname: String
Relationships:
- implements Serializable
#### DualSegment
Fields:
- ALL(8, 'Alle')
- WIRED(1, 'Festnetz')
- MOBILE(2, 'Mobilfunk')
- DUAL(3, 'Dual')
- CONVERGENT(4, 'Konvergent')
- CONVERGENTWIRED(5, 'Festnetz & konvergent')
- CONVERGENTMOBILE(6, 'Mobilfunk & konvergent')
- DUALCONVERGENT(7, 'Dual & konvergent')
- NONCUSTOMER(9)
#### PartyModelFactory
Relationships:
- uses Party
- uses PartyCustomerLoyaltyInfo
- uses PartyProfileInfo
- uses PartyProfileNPSInfo
- uses BillingAccountNumber
- uses MobileChurnLikeliness
#### AddressLinkData
Fields:
- street
- houseNumber
- zipCode
- city
- village
- country
Relationships:
- implements Serializable
#### ProductDetail
Fields:
- category
- locationId
Relationships:
- implements Serializable
- uses AddressLinkData
- uses Party
- uses PhoneNumber
#### MultiPartyMatrixData
Fields:
- matrixData
Relationships:
- uses HashMap<Long, HashMap<Long, ArrayList<MultiPartyProductGroup>>>
- uses MatrixPosition
#### MultiPartyProductGroup
Fields:
- List<Party>
- List<ProductGroup>
- Map<String, RTCode>
Relationships:
- Contains Party objects
- Contains ProductGroup objects
- Maps RTCodes to identifiers
#### ContactPersonComparator
Relationships:
- Implements Comparator<ContactPerson>
- Implements Serializable
#### CuCoAuditEvent
Fields:
- Audit event related fields
Relationships:
- Part of audit subsystem
#### CuCoAuditScope
Fields:
- APPLICATION
- SEARCH
- CUSTOMER
Relationships:
- implements AuditScope
#### CuCoAuditAttribute
Fields:
- Not visible in preview
Relationships:
- Likely implements an audit interface
#### CuCoAuditActivity
Fields:
- Not visible in preview
Relationships:
- Likely implements an audit interface
#### Constants
Fields:
- SEPERATOR_DEFAULT_RFC4180
- SEPERATOR
- EMPTY
#### Constants
Fields:
- LINE_BREAK
- seperator
#### DateFormater
Fields:
- DEFAULT_PATTERN: String
- DEFAULT_VALUE: String
- log: Logger
Relationships:
- implements Formater
#### TableContent
Fields:
- DEFAULT_ROW_LEN: int
- table: List<List<Object>>
Relationships:
- implements ExportContent
#### Formater
Relationships:
- implemented by DateFormater
#### ExportContent
Fields:
- N/A - Interface
Relationships:
- Formater
#### BooleanFormater
Fields:
- DEFAULT_TRUE
- DEFAULT_FALSE
- DEFAULT_VALUE
- trueValue
- falseValue
- defaultValue
Relationships:
- implements Formater
#### NullFormater
Fields:
- DEFAULT_VALUE
- defaultValue
Relationships:
- implements Formater
#### VIPHistory
Fields:
- customerId
- statusChanges
- timestamps
Relationships:
- Customer
#### ProductTree
Fields:
- nodes
- products
- hierarchy
Relationships:
- BaseNode
- Product
#### SubscriptionTree
Fields:
- subscriptions
- nodes
Relationships:
- SubscriptionNode
#### CustomerInteraction
Fields:
- customerId
- interactionType
- timestamp
- details
Relationships:
- Customer
#### CustomerEquipment
Fields:
- equipment details
- customer association
Relationships:
- Customer
- Equipment inventory
#### UserShopAssignment
Fields:
- user
- shop
- assignment details
Relationships:
- User
- Shop
#### UserShopAssignmentLogLine
Fields:
- assignment history
- timestamp
Relationships:
- UserShopAssignment
#### BillingCycle
Fields:
- cycle period
- billing details
Relationships:
- Customer
- Invoice
#### PartyProfileInfo
Fields:
- unknown - defined in external DTO
Relationships:
- Used as return type for getParty method
#### PointOfSaleInfo
Fields:
- unknown - defined in external DTO
Relationships:
- Returned as ArrayList in loadAvailablePOSList
#### AttributeConfig
Fields:
- configuration properties
Relationships:
- Attribute
- AttributeHistory
#### Attribute
Fields:
- attribute properties
Relationships:
- AttributeConfig
#### AttributeHistory
Fields:
- historical data
Relationships:
- AttributeConfig
#### CdPerson
Fields:
- Not visible in interface
Relationships:
- Returned as single entity or list
#### byte[]
Fields:
- raw contract data
Relationships:
- Input parameter for signing
#### CrmAuthenticationInfo
Fields:
- Not visible in interface
Relationships:
- Returned in HashMap with String key
#### UserInfo
Fields:
- Not visible in interface
Relationships:
- Referenced from bite.core
#### PhoneNumberStructure
Fields:
- phone number components
Relationships:
- Used by PartySearchValueFormatHelper
#### Product
Fields:
- not visible in preview
Relationships:
- Managed by ProductAdminService
#### Party
Fields:
- party information
Relationships:
- Associated with PointOfSaleInfo
#### PointOfSaleInfo
Fields:
- POS details
Relationships:
- Associated with Party
#### LinksPortlet
Fields:
- Not visible in interface
Relationships:
- Referenced in List<LinksPortlet> return type
#### UIText
Fields:
- not visible in interface
Relationships:
- Used as return type and parameter
#### EsbParty
Fields:
- not visible in interface
Relationships:
- Return type for getESBParty
#### Party
Fields:
- not visible in interface
Relationships:
- Return type for getParty
#### GamificationMessage
Fields:
- not visible in interface
Relationships:
- Used in ArrayList collections
#### AppointmentNote
Fields:
- Not visible in preview
Relationships:
- Part of sales information tracking
#### CompetitorNote
Fields:
- Not visible in preview
Relationships:
- Part of sales information tracking
#### SalesConvNoteReportRow
Fields:
- Not visible in preview
Relationships:
- Used for reporting sales conversation notes
#### SalesInfoNote
Fields:
- Not visible in preview
Relationships:
- Base type for sales-related notes
#### Setting
Fields:
- not visible in interface
Relationships:
- Used as return type and parameter
#### Not visible in preview
Fields:
- Not visible in preview
Relationships:
- Not visible in preview
#### Not visible in preview
Fields:
- Not visible in preview
Relationships:
- Not visible in preview
#### Reporting
Fields:
- id
- other reporting fields
Relationships:
- File (for export)
#### CCTOrgStructureElement
Fields:
- not visible in interface
Relationships:
- Used in updateCCTOrg method
#### ConcurrentHashMap
Fields:
- not visible in preview
Relationships:
- Used for concurrent operations
#### LocationNode
Fields:
- Not visible in interface
Relationships:
- Used as return type for marketplace account hierarchy
#### ClearingAccount
Fields:
- Not visible in interface
Relationships:
- Associated with Invoice
#### Invoice
Fields:
- Not visible in interface
Relationships:
- Associated with ClearingAccount
#### InsuranceBrokerInfo
Fields:
- Not visible in interface
Relationships:
- Used as return type for getCpiContractQuickInfo
#### SubscriptionNode
Fields:
- Not visible in interface
Relationships:
- Used as parameter for getCpiContractQuickInfo
#### InetUsage
Fields:
- not visible in preview
Relationships:
- Used as return type
#### MobileUsage
Fields:
- not visible in preview
Relationships:
- Used as return type
#### VoiceUsage
Fields:
- not visible in preview
Relationships:
- Used as return type
#### PartyDeclarationOfConsentInfo
Fields:
- not visible in preview
Relationships:
- Return type for consent information
#### PartyCustomerLoyaltyInfo
Fields:
- partyId
Relationships:
- Used as return type for getParty method
#### PWUTokenResponse
Fields:
- Not visible in preview
Relationships:
- Used for token responses
#### AccessToken
Fields:
- Not visible in preview
Relationships:
- DTO for access token data
#### PartnerCenterAccessTokenRequest
Fields:
- Not visible in preview
Relationships:
- Used for token requests
#### Not visible in preview
Fields:
- Not visible in preview
Relationships:
- Not visible in preview
#### AutoVvlInfo
Fields:
- not visible in interface
Relationships:
- Retrieved by CallNumber or BAN
#### PayableTicket
Fields:
- not visible in interface
Relationships:
- not visible in preview
#### Promotion
Fields:
- not visible in interface
Relationships:
- Associated with CallNumber
#### InsuranceBrokerInfo
Fields:
- not visible in interface
Relationships:
- Return type for both service methods
#### SubscriptionNode
Fields:
- not visible in interface
Relationships:
- Input parameter for both service methods
#### CusCoResponse
Fields:
- unknown
Relationships:
- Response type for unlock operations
#### GamificationRequest
Fields:
- not visible in interface
Relationships:
- Used as input parameter
#### GamificationResponse
Fields:
- not visible in interface
Relationships:
- Used as return type
#### BRKAccountInfo
Fields:
- not visible in interface
Relationships:
- Used as return type for account info methods
#### Team
Fields:
- not visible in interface
Relationships:
- BiteUser
- Auth
- Service
#### ClearingAccount
Fields:
- not visible in interface
#### PayableTicket
Fields:
- not fully visible in preview
Relationships:
- Date
#### ContactPerson
Fields:
- Not visible in preview
Relationships:
- Party
- ContactPersonDao
#### Cache
Fields:
- Element
Relationships:
- EhCache implementation
#### ExecutorService
Fields:
- Future
Relationships:
- Concurrent task execution
#### Image
Fields:
- Not fully visible in preview
Relationships:
- Managed by ImageDao
#### SalesInfoNote
Fields:
- SalesInfoNoteType
Relationships:
- Associated with BiteUser
#### HashMap
Fields:
- key-value pairs for session data
Relationships:
- Used for session management
#### BusinessHardwareReplacement
Fields:
- Not visible in preview
Relationships:
- Used as DTO for hardware replacement data
#### UIText
Fields:
- Not visible in preview
Relationships:
- Managed by UITextsEditorDAO
#### BillingAccountNumber
Fields:
- Not visible in preview
Relationships:
- Associated with phone numbers
#### GetCurrentDeclarationOfConsentForPartyRequest
Fields:
- brand
- partyId
Relationships:
- Brand enum
#### Setting
Fields:
- not visible in preview
Relationships:
- SettingsEditorDAO
#### CdPerson
Fields:
- not visible in preview
Relationships:
- CdPersonDao
#### Team
Fields:
- id
- members
- auth
Relationships:
- Many-to-Many with BiteUser
- One-to-One with Auth
#### HSSFWorkbook
Fields:
- sheets
- rows
- cells
Relationships:
- Hierarchical structure for Excel documents
#### CustomerInteraction
Fields:
- interaction details
- workflow status
Relationships:
- One-to-Many with Workflow
#### VIP History
Fields:
- Date
- List<HistoryRecord>
Relationships:
- Depends on transaction management
#### PhoneNumberStructure
Fields:
- phone number details
Relationships:
- Connected to MobilPointsDao
#### ImageSize
Fields:
- image size parameters
Relationships:
- Managed by ImageSizeDao
#### Location
Fields:
- id
- name
- address
Relationships:
- Many-to-One with Customer
#### BillingCycle
Fields:
- id
- date
- status
Relationships:
- One-to-Many with Billing Records
#### CustomerUnlock
Fields:
- customerId
- unlockDate
- reason
Relationships:
- One-to-One with Customer
#### ChargingType
Fields:
- Not visible in preview
Relationships:
- Managed by ChargingTypeDao
#### LinksPortlet
Fields:
- Not visible in preview
Relationships:
- Managed by LinksPortletDao
#### Not visible in preview
Fields:
- File operations related fields
Relationships:
- Integrates with ESB client
#### ImageSize
Fields:
- Not fully visible in preview
Relationships:
- Managed through ImageSizeDao
#### SimpleDateFormat
Fields:
- date
- timezone
Relationships:
- Used for date formatting in emails
#### CustomerBlock
Fields:
- Not fully visible in preview
Relationships:
- Managed through CustomerBlockDao
#### CCTOrgStructureElement
Fields:
- Not visible in preview
Relationships:
- Managed by CCTOrgStructureElementDao
#### Product
Fields:
- Not visible in preview
Relationships:
- Managed through HashSet and HashMap collections
#### UserInfo
Fields:
- Not visible in preview
Relationships:
- Associated with SalesInfo through UserDao
#### SalesInfo
Fields:
- Date
- Additional fields not visible in preview
Relationships:
- Managed by SalesInfoDao
#### CreditType
Fields:
- Not visible in preview
Relationships:
- Managed by CreditTypeDao
#### Service
Fields:
- Not visible in preview
Relationships:
- Managed by ServiceDao
#### FlashInfo
Fields:
- Not visible in preview
Relationships:
- Managed by FlashInfoDao
- Associated with Role
#### GetAccountDocument
Fields:
- account request parameters
Relationships:
- Maps to KUMS web service request
#### GetAccountResponseDocument
Fields:
- account details
Relationships:
- Contains WSKUMSRetrieveAccountResponseACC1ACCOUNTType
#### InetUsage
Fields:
- usage metrics
- internet usage data
Relationships:
- Managed by UsageDataDao
#### UserShopAssignment
Fields:
- user ID
- shop ID
- assignment details
Relationships:
- Connected to TeamDao
- Managed by UserShopAssignmentDao
#### ContractOwnerAssignment
Fields:
- Not fully visible in preview
Relationships:
- Managed by CustomerAssignmentDao
#### File
Fields:
- file system operations
Relationships:
- Managed through FileUtils
#### HashMap
Fields:
- key-value pairs
Relationships:
- Used for service parameters
#### ClearingAccount
Fields:
- Not visible in preview
Relationships:
- Managed by ClearingAccountDao
#### HashMap
Fields:
- Not visible in preview
Relationships:
- Used for authentication data
#### HttpPost
Fields:
- Not visible in preview
Relationships:
- Used for HTTP communications
#### GamificationLocalDTO
Fields:
- Not fully visible in preview
Relationships:
- Managed by GamificationLocalDAO
#### HttpResponse
Fields:
- Headers
- Entity
- StatusCode
Relationships:
- Used for API responses
#### VBMDeclineReason
Fields:
- Not fully visible in preview
Relationships:
- Related to VbmProductsDao
#### FreeMinutesRequest
Fields:
- requestData
- timestamp
Relationships:
- FreeMinutesResponse
#### AccessToken
Fields:
- token
- validationData
#### Invoice
Fields:
- invoiceData
- collections
Relationships:
- LinkedHashMap
#### EsbParty
Fields:
- party details
Relationships:
- Maps to at.a1telekom.eai.party.Party
#### DuposMobileSignatureStub
Fields:
- signature data
Relationships:
- Integrates with ESB mobile signature service
#### Unknown
Fields:
- area code information
Relationships:
- Internal service relationships
#### Product DTO
Fields:
- Not fully visible in preview
Relationships:
- Used as data transfer object
#### GetContractQuickInfoSoapMethodRequestDocument
Fields:
- Not fully visible in preview
Relationships:
- Used for SOAP communications
#### UserInfoStatistics
Fields:
- Not fully visible in preview
Relationships:
- Associated with UserInfoStatisticsDao
#### Mail
Fields:
- sender
- recipient
- content
Relationships:
- Used for POS notifications
#### Attribute
Fields:
- id
- date
- user
Relationships:
- Associated with BiteUser
#### Turnover
Fields:
- id
- amount
- date
Relationships:
- Managed by TurnoverDao
#### Party
Fields:
- calendar
- timeZone
- partyData
Relationships:
- Maps to customer/party domain entities
#### ContractQuickInfo
Fields:
- contractData
- testDataCd
Relationships:
- Integrates with external CPI system
#### UnlockRequest
Fields:
- url
- xmlData
Relationships:
- Interfaces with external unlock system
#### HashMap
Fields:
- Date
- SimpleDateFormat
Relationships:
- Used for inventory data mapping
#### UserInfo
Fields:
- user details
Relationships:
- Associated with BillingAccount
#### HashMap
Fields:
- BigDecimal
- DecimalFormat
Relationships:
- Used for report data formatting
#### XML Processing
Fields:
- JAXBContext
- Marshaller
- Unmarshaller
Relationships:
- Handles XML conversion for visit reports
#### DigitalSellingNotePrintModel
Fields:
- title
- priceOld
- noteOld
- priceNew
- noteNew
Relationships:
- Serializable
#### Service Operations
Fields:
- BiteUser
- UserInfo
- ErrorMessage
Relationships:
- Uses customer contact and user information models
#### Equipment Data Maps
Fields:
- equipmentId
- customerId
- equipmentDetails
Relationships:
- Maps customer equipment data to internal representations
#### Cache
Fields:
- customerEquipmentCache
Relationships:
- Caches customer equipment data using ehcache
#### Excel Workbook
Fields:
- cells
- styles
- sheets
Relationships:
- Formats customer data into Excel structure
#### Equipment
Fields:
- equipment details
- customer information
Relationships:
- Maps to customer equipment domain objects
#### PartySummary
Fields:
- party information
- summary data
Relationships:
- Connected to ESB client
- Uses SettingService
#### Promotion
Fields:
- promotion details
- inventory data
Relationships:
- Connected to ODSRawDataInventory
- Implements PromotionService
#### Product
Fields:
- id
- price
- metadata
Relationships:
- Customer Equipment
- File Attachments
#### Metadata
Fields:
- properties
- attributes
Relationships:
- Customer Equipment
#### GetPartySummaryResponse
Fields:
- partyId
- summaryItems
Relationships:
- PartySummaryItem
#### PartySummaryItem
Fields:
- serviceDetails
Relationships:
- ICT Services
#### SalesInfoNote
Fields:
- type
- content
Relationships:
- NotesFilter
#### MyNotesDao
Fields:
- database operations
Relationships:
- PartyDao
#### Customer
Fields:
- BigDecimal
- HashMap
- LinkedHashMap
- TreeMap
Relationships:
- Party
#### CustomerBinding
Fields:
- not visible in interface
Relationships:
- Referenced in SearchResult
#### SalesInfoNote
Fields:
- not visible in interface
Relationships:
- Contains SalesInfoNoteType enum
#### Not fully visible in preview
Fields:
- Not visible in preview
Relationships:
- Depends on MyToDoNotesDao
- Depends on PartyDao
#### FlashInfo
Fields:
- unspecified
Relationships:
- Party
- FilterCollection
#### MyOpportunity
Fields:
- unspecified
Relationships:
- SearchResult
- OpportunityFilter
#### CustomerFilter
Fields:
- unspecified
Relationships:
- SearchResult
- Party
#### Date/DateMidnight
Fields:
- timestamp
Relationships:
- Used for binding time tracking
#### Filter
Fields:
- search criteria
Relationships:
- Used for filtering flash information
#### MyOpportunity
Fields:
- opportunity details
Relationships:
- Related to SalesInfoOverviewRow
#### OpportunityFilter
Fields:
- filter criteria
Relationships:
- Used with MyOpportunity
#### UserActionStatistics
Fields:
- userId
- actionCounts
- timestamps
Relationships:
- extends ActionStatisticBase
#### DepartmentActionStatistics
Fields:
- departmentId
- aggregatedStats
- periodMetrics
Relationships:
- extends ActionStatisticBase
#### ActionStatisticBase
Fields:
- actionType
- count
- timestamp
- metrics
Relationships:
- parent of UserActionStatistics
- parent of DepartmentActionStatistics
#### Phone Number Cache
Fields:
- phone numbers
Relationships:
- SqlMapClientDaoSupport

### Key Methods/Functions
#### GWTCacheControlFilter
Description: Filter that manages HTTP cache headers for GWT resources
#### AppStarter
Description: Main application initializer extending BiteEntryPoint
#### AdminStarter
Description: Admin interface initializer extending BiteEntryPoint
#### MyCuCoStarter
Description: Entry point class that extends BiteEntryPoint to bootstrap the application
#### PkbStarter
Description: Entry point class that extends BiteEntryPoint to initialize PKB application
#### AuthServletImpl
Description: Web servlet that extends SpringRemoteServiceServlet to handle authentication
#### PastExportServlet
Description: Handles HTTP requests for exporting historical data
#### UploadFileServlet
Description: Processes multipart file uploads using Apache Commons FileUpload
#### IbatisServletImpl
Description: Provides database access through iBATIS with Spring integration
#### CreditTypeServletImpl
Description: Handles credit type management operations through web service endpoints
#### ReportingServletImpl
Description: Manages report generation and processing operations
#### TeamServletImpl
Description: Handles team-related operations and user management within teams
#### ChargingTypeServletImpl
Description: Spring-enabled remote service servlet for charging type operations
#### FileContentServlet
Description: Processes file upload requests and handles file content
#### FileUtil
Description: Provides file handling utility functions
#### SystemMessagesGrid
Description: Grid UI component for displaying and managing system messages
#### IconButtonRenderer
Description: Renders clickable buttons with icons in grid cells
#### ReportingWidget
Description: Widget for displaying and managing report data in tabular format
#### MarkableCheckbox
Description: Extended checkbox that stores a generic marker value
#### SystemMessageGrid
Description: Grid widget for displaying paginated system messages
#### ServiceImageRenderer
Description: Grid column renderer for service images
#### ImageRenderer
Description: Renders image content within grid cells
#### SettingsCell
Description: Container widget for segment and category settings
#### EditUnknownAreasCodeDialog
Description: Provides UI for editing unknown area codes with click handling
#### GwtSelectServiceDialog
Description: UI dialog component for service selection using GWT framework
#### GwtEditServiceDialog
Description: UI dialog component for editing service details using GWT framework
#### EditServiceDialog
Description: UI dialog component for editing service details using ExtJS framework
#### GwtSelectTeamMemberDialog
Description: UI dialog for team member selection with list view and selection capabilities
#### EditTeamDialog
Description: Form dialog for editing team details including name and description
#### EditUserDialog
Description: Form dialog for editing user details with validation
#### EditRoleGroupManagementDialog
Description: Manages the UI and logic for editing role group assignments and permissions
#### EditCreditTypeDialog
Description: Provides form interface for managing credit type definitions
#### GwtEditMessageDialog
Description: Manages the creation and editing of system messages with scheduling capabilities
#### EditMessageDialog
Description: GXT dialog component for editing message content and properties
#### SelectTeamMemberDialog
Description: GXT dialog with grid for selecting team members with paging capabilities
#### EditTeamsDialog
Description: GWT-based dialog using UiBinder for team editing functionality
#### SelectRolesDialog
Description: GXT-based dialog for displaying and selecting user roles
#### EditUnknownAreaCodeDialog
Description: Form dialog for editing area code information
#### GwtSelectRolesDialog
Description: UiBinder-based dialog for role selection using GWT widgets
#### SelectServiceDialog
Description: GXT dialog component with grid for service selection
#### ServiceGrid
Description: Paginated grid displaying service data
#### EditCreditTypesDialog
Description: GWT-based dialog using UiBinder for credit type editing
#### EditRoleGroupDialog
Description: GXT-based dialog for role group management with grid selection
#### CheckUsagePortlet
Description: UI component that provides date selection and usage checking functionality
#### RoleGroupManagementPortlet
Description: UI component for role group CRUD operations with pagination
#### IbatisPortlet
Description: UI component for database operations using iBatis
#### UserManagementPortlet
Description: Main portlet class for user management functionality
#### AllMessagesPortlet
Description: Displays system messages in a tabbed interface
#### SystemMessagesGrid
Description: Grid component for displaying message data
#### UserShopAssignmentPortlet
Description: Manages the assignment of users to shops using a grid interface
#### CuCoSettBasePortlet
Description: Base portlet implementation extending AbstractPortlet with common functionality for CuCoSett portlets
#### ReportingPortlet
Description: GWT-based portlet handling report generation and display
#### CCTOrgStructureElementPortlet
Description: Handles organization structure element display and manipulation
#### RoleGroupsManagementPortlet
Description: Main portlet component for managing role groups with UI elements
#### VipSearchPortlet
Description: Main portlet for VIP search functionality with singleton pattern implementation
#### VipSearchComponent
Description: Handles VIP search interface and interactions
#### TeamManagementPortlet
Description: UI component for team management functionality using FlexTable and TabPanel
#### ServicePortlet
Description: Service management interface with data grid and paging functionality
#### CreditTypesPortlet
Description: UI component for credit type management with anchor links and HTML panels
#### CreditTypePortlet
Description: UI component for displaying and managing credit type data using ExtJS/GXT grid
#### TeamPortlet
Description: UI component using GWT FlexTable and TabPanel for team information display
#### UnknownAreasCodePortlet
Description: UI component with clickable elements for managing unknown area codes
#### GwtServicePortlet
Description: Handles service-related UI interactions and event handling using GWT framework
#### UnknownAreaCodePortlet
Description: Manages grid-based display and interaction with unknown area code data
#### TeamPanel
Description: Provides team management interface using GXT components with pagination support
#### TeamMemberPanel
Description: Grid panel displaying team member information with paging capabilities
#### TeamServicePanel
Description: Panel for managing team services with horizontal alignment and paging support
#### TeamMemberManagementPanel
Description: Panel with click handlers and selection management for team members
#### TeamServiceManagementPanel
Description: UI panel for managing team services with click handlers and selection events
#### TeamManagementPanel
Description: UI panel containing team management controls and event handlers
#### SettingsServiceLocator
Description: Manages singleton instances of various service clients
#### ChargingTypeServlet
Description: Defines remote service contract for charging type operations
#### ReportingServlet
Description: Defines remote service contract for reporting operations
#### ReportingException
Description: Serializable runtime exception for reporting errors
#### ChargingTypeServletAsync
Description: Async interface for charging type operations
#### IbatisServletAsync
Description: Async interface for iBATIS data access operations
#### IbatisServlet
Description: Remote service interface for iBATIS data access operations
#### CreditTypeServletAsync
Description: Defines async operations for managing credit types
#### TeamServletAsync
Description: Defines async operations for managing teams
#### TeamServlet
Description: Defines RPC service operations for team management
#### ReportingServletAsync
Description: Defines asynchronous methods for retrieving and executing reports
#### CreditTypeServlet
Description: Remote service endpoint for credit type management
#### AuthServlet
Description: Remote service endpoint for authority management
#### AuthServletAsync
Description: Defines async methods for retrieving authority information
#### UsageStatisticsServlet
Description: Processes usage statistics data
#### CCTOrgStructureElementUploadServlet
Description: Manages file uploads for organizational structure elements
#### UserRoleServletImpl
Description: Handles user role management operations through web interface
#### CCTOrgStructureErrorExport
Description: Generates Excel reports for organization structure validation errors
#### SystemTrackingServletImpl
Description: Handles system tracking and monitoring operations
#### UserShopAssignmentUploadServlet
Description: Processes file uploads containing user-shop assignment data
#### UnknownAreaCodeServletImpl
Description: Handles requests related to unknown area codes
#### UserShopAssignmentServletImpl
Description: Handles user-shop assignment operations with authentication
#### CCTOrgStructureElementServletImpl
Description: Implements CCTOrgStructureElementServlet interface to manage org structure elements
#### ServiceServletImpl
Description: Handles service-related requests and operations
#### VIPHistoryServletImpl
Description: Manages VIP history records and operations with date formatting
#### UserShopAssignmentDownloadServlet
Description: Handles HTTP requests for downloading user shop assignments
#### ServiceModel
Description: Represents service data for UI display and manipulation
#### RTCodeModel
Description: Represents RT code data for UI display and manipulation
#### PortletHelper
Description: Provides helper methods for creating portlet UI elements with tooltips
#### LocalPagingDetails
Description: Manages pagination state and logic for client-side data handling
#### ImageRenderer
Description: Manages image rendering and display in the application
#### BooleanRenderer
Description: Renders boolean values in grid cells with localized Yes/No text
#### SystemMessagePreviewComponent
Description: Grid-based preview display for system messages
#### AdminCommonTextPool
Description: Text resource interface with admin_ prefix for localization
#### ADMINCOMMONTEXTPOOL
Description: GWT-created text resource pool for admin UI internationalization
#### CONFIG
Description: Global configuration instance for the admin UI
#### SettingsManager
Description: Manages application settings through a key-value map
#### CuCoConfiguration
Description: Provides typed access to specific application configuration values
#### UnknownAreaCodeServlet
Description: GWT RemoteService interface for unknown area code management
#### SystemTrackingServlet
Description: GWT RemoteService interface for system tracking operations
#### CCTOrgStructureElementServlet
Description: GWT RemoteService interface for CCT organizational structure operations
#### CommonServiceLocator
Description: Singleton-style service locator that provides access to various GWT service implementations
#### VIPHistoryServlet
Description: GWT RemoteService interface for retrieving VIP history data
#### VIPHistoryServletAsync
Description: Async version of VIPHistoryServlet for GWT RPC calls
#### UserShopAssignmentServlet
Description: Defines RPC methods for CRUD operations on user-shop assignments
#### UserShopAssignmentServletAsync
Description: Provides async versions of UserShopAssignmentServlet methods
#### UserRoleServlet
Description: Defines RPC methods for user role management
#### UnknownAreaCodeServletAsync
Description: Defines async operations for retrieving and saving unknown area codes
#### SystemTrackingServletAsync
Description: Provides async methods for loading system analysis data
#### ServiceServletAsync
Description: Defines async operations for service management
#### ServiceServlet
Description: GWT RemoteService interface for service management operations
#### UserRoleServletAsync
Description: GWT async interface for user and role management operations
#### CCTOrgStructureElementServletAsync
Description: GWT async interface for organizational structure operations
#### AddCreditTypeEvent
Description: Extends PortletEvent to handle credit type addition events
#### SelectRolesEvent
Description: Extends PortletEvent to handle role selection events
#### AddTeamMemberEvent
Description: Extends PortletEvent to handle team member addition events
#### AddUnknownAreaCodeEvent
Description: Extends PortletEvent to handle unknown area code addition events
#### GwtAddTeamMembersEvent
Description: Extends PortletEvent to handle team member addition events
#### AddTeamEvent
Description: Extends PortletEvent to handle team addition events
#### CuCoEventType
Description: Enumeration of all possible event types that can occur in the administration UI
#### AddServicesEvent
Description: Event class that handles the addition of services
#### RemoveServicesEvent
Description: Event class that handles the removal of a single service
#### AddTeamMembersEvent
Description: Extends PortletEvent to handle team member addition operations
#### RoleEvent
Description: Handles role update and insert operations
#### ProductgroupEvent
Description: Handles product group insert, update, and other operations
#### PopupImplExtended
Description: Custom implementation of popup behavior that ensures popups appear on top of other elements
#### Util
Description: Contains static utility methods and inner classes for GXT framework
#### PagingToolBarFix
Description: Fixed implementation of PagingToolBar to address button width issues
#### PopupImplMozillaExtended
Description: Mozilla-specific implementation of popup behavior with custom z-index management
#### PagingGridContainer
Description: Container component that combines a grid with paging toolbar
#### ProxyFilterField
Description: Filter field component for FilterablePagingMemoryProxy
#### ButtonRenderer
Description: Grid cell renderer that creates clickable buttons
#### ProxyFilter
Description: Generic interface for implementing proxy filtering functionality
#### NumberFieldFixed
Description: Extended NumberField implementation with fixed key press handling
#### DetailsDialog
Description: Dialog component for detail views
#### FilterablePagingMemoryProxy
Description: Extends PagingMemoryProxy to provide filtered data pagination
#### BaseFilterableMemoryProxy
Description: Base class implementing filtering logic for memory proxies
#### LinkCellRenderer
Description: Implements GridCellRenderer to display clickable links in grid cells
#### GridContainer
Description: Container component that wraps a grid with selection mode and filtering support
#### FilterableMemoryProxy
Description: Defines contract for adding filters to memory proxies
#### ComboBoxFix
Description: Enhanced ComboBox with error handling for expand operation
#### PopupImplIE6Extended
Description: Extension of GWT's PopupImplIE6 that modifies z-index behavior
#### EsbBrianDaoBeanConverterTest
Description: Unit tests for PayableTicket2AddCreditRequestConverter
#### ITestESBLocationService
Description: Tests ESB Location Service with mock interactions
#### AbstractParametrizedESBDaoTest
Description: Provides common test setup and mocking for ESB DAO tests
#### CustomerInventoryTest
Description: Tests customer inventory data access operations
#### EsbBrianDaoTest
Description: Tests Brian-specific ESB data access operations
#### ITestDefaultPartnerCenterLandingPageDao
Description: Integration tests for Partner Center landing page data access operations
#### ITestESBPartyService
Description: Integration tests for ESB party service operations
#### ITestProductBrowser
Description: Integration tests for product browsing operations
#### PhoneNumberParserTest
Description: Contains test methods to verify phone number parsing logic
#### HttpPostCusCoDaoTest
Description: Tests HTTP POST operations for customer data access
#### SolrPartyQueryHelperTest
Description: Validates Solr query construction for party search functionality
#### SolrPartyRepositoryWithPhoneNumbersTest
Description: Contains test methods for verifying party search functionality with phone number criteria
#### SolrPartyRepositoryTest
Description: Tests basic CRUD and search operations for party entities in Solr
#### AbstractSolrRepositoryTest
Description: Provides common setup and mock objects for Solr repository tests
#### SalesInfoDaoImplTest
Description: Test suite for validating sales information database operations
#### MyNotesDaoImplTest
Description: Test suite for validating user notes database operations
#### CustomerUnlockRequestDaoImplTest
Description: Test suite for validating customer unlock request database operations
#### IndexationStatusTest
Description: Contains test methods to validate IndexationStatus enum conversions
#### HousenumberValidatorTest
Description: Tests validation rules for house number format and content
#### CityValidatorTest
Description: Tests validation rules for city name format and content
#### FirstnameValidatorTest
Description: Contains test cases for validating first name formats and rules
#### ZipCodeValidatorTest
Description: Contains test cases for validating ZIP code formats and rules
#### AONNumberValidatorTest
Description: Contains test cases for validating AON number formats and rules
#### StreetValidatorTest
Description: Contains test methods to validate street address formatting rules
#### PartyIdValidatorTest
Description: Contains test methods to validate party ID formatting rules
#### LastnameValidatorTest
Description: Contains test methods to validate lastname formatting rules
#### PhonenumberValidatorTest
Description: Contains test cases for phone number validation logic
#### BANValidatorTest
Description: Contains test cases for bank account number validation logic
#### FlashInfoServiceTest
Description: Tests flash information service operations
#### InvoiceServiceTest
Description: Contains test methods to verify invoice service operations
#### CustomerAssignmentServiceTest
Description: Tests for customer assignment operations
#### IMailServiceTest
Description: Tests email service functionality with Spring context
#### AccessTokenServiceImplTest
Description: Tests token validation, generation and management functionality
#### UnknownAreaCodeServiceImplTest
Description: Tests handling of unknown area codes
#### KumsCustomerServiceImplTest
Description: Tests customer service operations with caching
#### CustomerUnlockServiceImplTest
Description: Contains test cases for validating customer unlock service operations
#### PayableTicketServiceImplTest
Description: Validates functionality of payable ticket operations
#### IAutoVvlServiceImplTest
Description: Tests automated VVL service functionality
#### GamificationHttpServiceImplTest
Description: Contains test cases for gamification HTTP service operations
#### ProductBrowserServiceImplTest
Description: Tests product browsing operations and data retrieval
#### BillingCycleServiceImplTest
Description: Tests billing cycle management and processing
#### CustomerInteractionServiceImplTest
Description: Tests customer interaction service operations including creation and retrieval
#### LocationServiceImplTests
Description: Tests location-related operations and validations
#### ClearingAccountServiceImplTest
Description: Tests clearing account operations and validations
#### ContactPersonServiceImplTest
Description: Contains test methods to verify contact person service operations
#### PartyServiceTest
Description: Test cases for party-related operations and business logic
#### IAttributeServiceImplTest
Description: Tests attribute service functionality with Spring dependency injection
#### VisitReportServiceImplTest
Description: Test suite for validating visit report service functionality
#### CustomerEquipmentHelperTest
Description: Tests for equipment number cleaning functionality
#### ITestUserActionStatistics
Description: Tests for user action tracking and statistics
#### DepartmentActionStatisticsTest
Description: Contains test cases for department action statistics calculations
#### UserActionStatisticsTest
Description: Contains test cases for individual user action statistics calculations
#### UserActionStatisticsTestBase
Description: Provides shared test utilities and setup for action statistics tests
#### DataTheftRapidAlertJobTest
Description: Contains test cases for the rapid alert system related to data theft detection
#### IKumsSkzShopSynchronizationJobTest
Description: Tests synchronization between KUMS SKZ shop systems
#### MetricsConfiguration
Description: Defines metrics collection settings and configurations for the application
#### Reporting
Description: Bean class implementing Serializable and KeyableBean interfaces for report definitions
#### KeyableBean
Description: Interface defining getId() method for beans with unique identifiers
#### File
Description: Bean class for file metadata with MIME type enumeration
#### MIMEType
Description: Enumeration of supported file MIME types
#### ReportingWhitelist
Description: Whitelist container for GWT RPC serialization compatibility
#### PWUTokenResponse
Description: Serializable response container for token-related data
#### SolrHealthCheck
Description: Component for checking Solr service health status
#### DefaultBillingCycleDao
Description: Concrete implementation of BillingCycleDao interface for handling billing cycle data access
#### BillingCycleDao
Description: Defines contract for billing cycle data access operations
#### BrianCeeQueryOrderDaoImpl
Description: Repository component for handling BrianCee order queries through ESB
#### MobilPointsDaoImpl
Description: Handles integration with MobilPoints service through ESB client
#### BrianDao
Description: Defines contract for Brian service data access operations
#### BrianDaoImpl
Description: Implements BrianDao interface with ESB integration
#### EsbPartyDao
Description: Defines methods for retrieving party information from ESB
#### CustomerAssignmentDaoImpl
Description: Spring component implementing customer assignment operations
#### BusinessHardwareReplacementDaoImpl
Description: Spring repository for handling business hardware replacement operations
#### MobilPointsDao
Description: Defines contract for accessing mobile points data
#### KUMSCommonDao
Description: Defines contract for accessing point of sale data
#### EsbPartyDaoImpl
Description: Repository implementation for ESB party operations
#### CustomerAssignmentDao
Description: DAO interface for retrieving contract owner assignments by different identifiers
#### KUMSCommonDaoImpl
Description: Repository implementation for ESB client operations
#### PartnerCenterLandingPageDao
Description: DAO interface for managing partner center access tokens
#### BrianCeeQueryOrderDao
Description: Data access interface for Brian Cee order queries
#### BusinessHardwareReplacementDao
Description: Data access interface for hardware replacement queries
#### PartnerCenterLandingPageDaoImpl
Description: Repository implementation for partner center landing page operations
#### OracleArrayTypeHandler
Description: TypeHandler implementation for converting between Java Lists and Oracle Array types
#### ListStringTypeHandler
Description: TypeHandler implementation for converting between List<String> and delimited strings
#### YNNullableBooleanTypeHandler
Description: TypeHandler implementation for converting between Boolean and Y/N characters with null support
#### YNBooleanTypeHandler
Description: Implements TypeHandlerCallback to handle Boolean to Y/N string conversions
#### IdxStatusDBMappingHandler
Description: Implements TypeHandlerCallback to handle IndexationStatus enum conversions
#### BooleanTypeHandler
Description: Implements TypeHandlerCallback to handle Boolean to 1/0 string conversions
#### VIPStatusHandler
Description: Implements TypeHandlerCallback to handle conversion between database values and VipStatus enum
#### BrianCeeQueryOrderStub
Description: Extends BrianA1Stub to provide specific implementation for CEE order queries
#### PhoneNumberParser
Description: Provides phone number parsing and validation functionality
#### CusCoResponse
Description: Data transfer object for customer communication responses
#### CusCoDao
Description: Defines contract for customer communication data access
#### HttpPostCusCoDao
Description: Implements customer communication operations via HTTP POST
#### SolrPartyRepository
Description: Repository interface for Party search operations using Solr
#### SolrPartyQueryHelper
Description: Utility class for constructing Solr query criteria
#### SolrPartyRepositoryWithPhoneNumbers
Description: Repository implementation with specialized phone number search capabilities
#### SolrPartyQuery
Description: Extends BasicQuery to provide party-specific search field definitions
#### CustomerUnlockRequestDao
Description: Provides CRUD operations for customer unlock requests
#### InventoryDao
Description: Handles inventory queries and customer binding operations
#### SingleTurnaroundDao
Description: Defines data access methods for single turnaround operations
#### ChargingTypeDao
Description: Defines data access methods for charging type operations
#### ClearingAccountDao
Description: Defines data access methods for clearing account operations
#### MyToDoNotesDao
Description: Defines contract for accessing and managing to-do notes data
#### UnknownAreaCodeDao
Description: Manages data access for unknown area codes
#### CreditTypeDao
Description: Handles data access operations for credit type entities
#### PartyDao
Description: Provides methods for customer/party data access and search operations
#### UITextsEditorDAO
Description: Manages CRUD operations for UI text content
#### ReportingDao
Description: Manages reporting data access and execution
#### MKInteractionDao
Description: Defines data access operations for marketing interactions
#### MyQuoteDao
Description: Defines operations for loading and managing opportunities and sales information
#### StandardAddressDao
Description: Defines CRUD operations for standard addresses
#### InventoryProductGroupDao
Description: Defines database operations for inventory product groups
#### UserShopAssignmentDao
Description: Defines operations for managing user-shop assignments and logs
#### ServiceDao
Description: Defines database operations for services
#### ImageSizeDao
Description: Defines data access methods for image size operations
#### ProductHierarchyDao
Description: Defines methods to access product hierarchy data
#### CucoLogsDao
Description: Defines data access methods for logging operations
#### LocationDao
Description: Provides data access methods for location information
#### InvoiceDao
Description: Handles invoice data persistence and retrieval operations
#### PhoneNumberDao
Description: Handles phone number data access and related operations
#### LinksPortletDao
Description: Defines data access methods for links portlet functionality
#### SalesInfoDao
Description: Handles CRUD operations for sales information, appointments, and competitor notes
#### FlashInfoDao
Description: Manages flash information data persistence and retrieval
#### AttributeDao
Description: Defines contract for attribute data access operations
#### CustomerBlockDao
Description: Handles customer blocking data operations
#### ContactPersonDao
Description: Handles contact person data operations
#### ImageDao
Description: Defines database operations for image data management
#### PayableTicketDao
Description: Handles database operations for payable ticket entities
#### GamificationLocalDAO
Description: Manages gamification messages and related data in local database
#### VbmProductsDao
Description: Defines methods for retrieving VBM product information with filtering capabilities
#### TurnoverDao
Description: Provides methods to access turnover data for specific parties
#### MyNotesDao
Description: Handles retrieval of sales information notes with filtering support
#### CCTOrgStructureElementDao
Description: Defines operations for managing CCT organizational structure data
#### UserInfoStatisticsDao
Description: Interface for accessing user statistics data
#### TeamDao
Description: Defines operations for managing teams and team membership
#### VIPHistoryDao
Description: Provides data access methods for VIP customer history tracking
#### UsageDataDao
Description: Provides methods to access customer usage data for fixed line, mobile, internet and voice services
#### CategoryDao
Description: Provides data access methods for customer category management
#### CmDBICTServiceDao
Description: Defines contract for accessing ICT service data from database
#### SettingsEditorDAO
Description: Provides CRUD operations for system settings
#### SegmentDao
Description: Interface for segment data access operations
#### ClearingAccountDaoImpl
Description: Implementation of ClearingAccountDao interface extending AbstractDao for database operations
#### TeamDaoImpl
Description: Implementation of TeamDao interface extending AbstractDao for team management operations
#### CmDBICTServiceDaoImpl
Description: Implementation of CmDBICTServiceDao interface for retrieving ICT service information
#### StandardAddressDaoImpl
Description: Implementation of StandardAddressDao interface for database operations related to addresses
#### ProductHierarchyDaoImpl
Description: Implementation of ProductHierarchyDao interface for retrieving product hierarchy information
#### PartyDaoImpl
Description: Implementation of party-related database operations with Spring integration
#### CategoryDaoImpl
Description: Implementation of CategoryDao interface for database operations on categories
#### MyQuoteDaoImpl
Description: Implementation of MyQuoteDao interface for database operations on quotes
#### ImageDaoImpl
Description: Implementation of ImageDao interface for database operations on images
#### MKInteractionDaoImpl
Description: Implementation of MKInteractionDao interface for database operations related to customer interactions
#### PayableTicketDaoImpl
Description: Implementation of PayableTicketDao interface for database operations related to payable tickets
#### MyToDoNotesDaoImpl
Description: Implementation of MyToDoNotesDao interface for database operations related to to-do notes
#### ServiceDaoImpl
Description: Implementation of ServiceDao interface handling database operations for Service entities
#### InventoryDaoImpl
Description: Implementation handling inventory-related database operations
#### UsageDataDaoImpl
Description: Implementation handling database operations for internet and mobile usage data
#### PhoneNumberDaoImpl
Description: Handles database operations for phone numbers and related billing information
#### InventoryProductGroupDaoImpl
Description: Manages database operations for inventory product groups
#### CreditTypeDaoImpl
Description: Handles CRUD operations for credit types
#### TurnoverDaoImpl
Description: Implementation of TurnoverDao interface handling database operations for turnover data
#### LocationDaoImpl
Description: Implementation of LocationDao interface handling database operations for location data
#### InvoiceDaoImpl
Description: Implementation of InvoiceDao interface handling database operations for invoice data
#### SegmentDaoImpl
Description: Implementation of SegmentDao interface providing segment data access operations
#### ContactPersonDaoImpl
Description: Implementation of ContactPersonDao interface providing contact person data access operations
#### CCTOrgStructureElementDaoImpl
Description: Implementation of CCTOrgStructureElementDao interface providing organizational structure data access operations
#### ReportingDaoImpl
Description: Implementation of ReportingDao interface for database operations related to reporting
#### UserInfoStatisticsDaoImpl
Description: Implementation of UserInfoStatisticsDao for managing user statistics data
#### ChargingTypeDaoImpl
Description: Implementation of ChargingTypeDao for managing charging type data
#### CustomerBlockDaoImpl
Description: Implements database operations for customer blocks, extending AbstractDao
#### FlashInfoDaoImpl
Description: Implements database operations for flash info entities with SQL mapping support
#### SettingsEditorDAOImpl
Description: Implements database operations for application settings
#### SalesInfoDaoImpl
Description: Implementation of SalesInfoDao interface extending AbstractDao for database operations
#### ImageSizeDaoImpl
Description: Implementation of ImageSizeDao interface for managing image size data
#### GamificationLocalDAOImpl
Description: Implementation of GamificationLocalDAO interface for managing gamification data
#### UITextsEditorDAOImpl
Description: Implements database operations for UI texts management
#### LinksPortletDaoImpl
Description: Implements database operations for links portlet functionality
#### UnknownAreaCodeDaoImpl
Description: Implements database operations for unknown area code management
#### SingleTurnaroundDaoImpl
Description: Implementation of SingleTurnaroundDao interface extending AbstractDao for database operations
#### VbmProductsDaoImpl
Description: Implementation of VbmProductsDao interface for database operations related to VBM products
#### MyNotesDaoImpl
Description: Implementation of MyNotesDao interface for database operations related to user notes
#### CucoLogsDaoImpl
Description: Implements database operations for system logging functionality
#### AttributeDaoImpl
Description: Handles CRUD operations for customer attributes and their configurations
#### CustomerUnlockRequestDaoImpl
Description: Handles database operations for customer unlock request processing
#### UserShopAssignmentDaoImpl
Description: Implementation of UserShopAssignmentDao interface for database operations
#### VIPHistoryDaoImpl
Description: Implementation of VIPHistoryDao interface for database operations
#### SetupTypeSetTypeHandler
Description: iBatis type handler for SetupType set conversion
#### VisitReportDaoImpl
Description: Implements VisitReportDao interface, handles database operations for visit reports
#### ToDoGroupStatusHandler
Description: iBatis type handler for ToDo status conversions
#### VisitReportDao
Description: Defines contract for visit report data access operations
#### LinksPortlet
Description: Data transfer object for link information in portlets
#### ProductOfferingTypeHandler
Description: Handles conversion between database and Java ProductOffering objects
#### AttributeHistory
Description: Records historical attribute values and metadata
#### ContactPerson
Description: Data transfer object extending Person class to represent customer contact information
#### Message
Description: Data transfer object for message handling
#### Granularity
Description: Enumeration of different time period granularity options
#### GamificationRequest
Description: Handles request parameters for gamification operations
#### AggregatedInventoryProductGroupUsage
Description: Extends InventoryProductGroupUsage to include party information
#### BillingCycleEntry
Description: Stores billing cycle information including dates and identifiers
#### InventoryProductGroupAssignable
Description: Interface defining methods for objects that can be associated with inventory product groups
#### NotesFilter
Description: Filter class containing constants and criteria for filtering notes
#### CreditType
Description: Entity class representing different types of credits
#### SingleTurnaround
Description: Data transfer object for customer transaction information
#### Salesstage
Description: Represents different stages in a sales process with status tracking
#### Party
Description: Extended customer class with additional party-specific attributes
#### LocationPlaceholder
Description: Extension of Location class that initializes with placeholder values
#### Tupel
Description: Generic class holding two values of types N and M
#### Team
Description: Data transfer object for team information
#### Image
Description: Serializable class containing image metadata information
#### MyOpportunity
Description: Serializable class representing business opportunity data
#### StandardAddress
Description: Serializable class containing standardized address data with custom hashCode implementation
#### SalesConvEmailData
Description: Holds email message details including sender, recipient, and attachments
#### PointOfSaleInfo
Description: Contains dealer contact information and status
#### PhoneNumberStructure
Description: Represents phone numbers with country code, area code, number and extension
#### Product
Description: DTO for product information implementing Serializable and InventoryProductGroupAssignable
#### EsbParty
Description: DTO for party information with standard addressing capabilities
#### BANCollection
Description: Serializable collection of billing account numbers linked to a party
#### MobileChurnLikeliness
Description: DTO implementing Serializable for storing churn prediction data
#### Customer
Description: Extended Person class with additional business-related attributes
#### IndexationStatus
Description: Defines indexation states with associated inventory values and DWH mappings
#### Inventory
Description: Data transfer object for inventory information
#### Segment
Description: Data transfer object for segment information
#### Invoice
Description: Data transfer object for invoice information
#### InvoiceDateComparator
Description: Comparator for sorting invoices by date
#### Auth
Description: Enumeration of authorization permissions implementing AuthInfo interface
#### BillingAccountNumber
Description: Data transfer object for billing account information
#### ToDoNotesFilter
Description: Filter configuration for TODO notes queries
#### ContractOwnerAssignment
Description: Data transfer object for mapping party IDs to their billing accounts
#### PartyCustomerLoyaltyInfo
Description: Data transfer object for customer loyalty status information
#### PartyProfileNPSInfo
Description: Data transfer object for NPS scoring information
#### Category
Description: Serializable class containing category information
#### ClearingAccount
Description: Serializable and comparable class containing clearing account details
#### SelectedProductOffering
Description: Class combining a product offering with its selection status
#### InsuranceBrokerInfo
Description: Data transfer object for insurance broker information with status constants
#### CustomerFilter
Description: Contains filter parameters for customer queries including VIP and turnover region filters
#### ProductGroup
Description: Data transfer object for product group information including notes and turnover tracking
#### AttributeConfig
Description: Serializable class for managing attribute configurations with copy constructor functionality
#### CustomerBlock
Description: Serializable class managing customer block information including ID, name, count, and import status
#### SearchResultComparator
Description: Implements comparison logic for Party objects based on a computed comparison string
#### PartySearch
Description: Serializable class containing search criteria for party/customer lookup
#### PartyAdditionalInfo
Description: Aggregates different aspects of party information including service class, point of sale, consent, and profile data
#### PartyDeclarationOfConsentInfo
Description: Tracks consent status with enumerated completion states
#### StatusOfCompleteness
Description: Defines possible consent completion states with display text
#### OverviewStatus
Description: Enumeration of possible status values for tracking item states
#### VipExport
Description: Contains constants for VIP export search parameters and formatting
#### BindingsFilter
Description: Contains constants and enums for filtering contract bindings
#### Contract
Description: Enumeration of contract filter types
#### ProductDetailFilter
Description: Filter container for product search parameters
#### CucoLogs
Description: Container for customer operation logging information
#### ProductFeasibilityStatus
Description: Enumeration of possible product installation status values
#### UIText
Description: Data transfer object for storing text key-value pairs
#### InsuranceBrokerContractInfo
Description: Data transfer object for insurance broker contract details
#### InventoryProductGroupAssignation
Description: Data transfer object for product group assignments
#### CrmAuthenticationInfo
Description: Data transfer object for CRM authentication status and credentials
#### ProductOffering
Description: Enumeration of product offerings with numeric IDs and string codes
#### AccessToken
Description: Represents an access token with target system information
#### ServiceClassInfo
Description: Data transfer object for service class status and description
#### BusinessOffer
Description: Data transfer object for business offers
#### InventoryProductGroupUsage
Description: Data transfer object for inventory product group usage tracking
#### UnknownAreaCode
Description: Custom exception for area code validation
#### Turnover
Description: Holds turnover and margin data for TA and MK types
#### Person
Description: Stores personal information with Solr field mapping
#### QuoteClearanceConfigurationHolder
Description: Container for quote clearance configuration data that can be serialized
#### PartyProfileInfo
Description: Represents profile information for a party with status tracking
#### ReadOnlyStatusBasedOnCategory
Description: Enumeration defining whether content is editable or read-only based on category
#### GamificationMessageComparator
Description: Comparator implementation for sorting GamificationMessage objects in reverse chronological order
#### MatrixPosition
Description: Generic container for storing position information in a matrix with segment (column), category (row), and sequence
#### Service
Description: Data transfer object for service information including costs, validity period, and product details
#### GamificationData
Description: Container for gamification messages and related data
#### GamificationResponse
Description: Response wrapper for gamification operations
#### ChargingType
Description: Defines charging type attributes and mobile charging constant
#### PartyProfileSolvency
Description: Data transfer object for party solvency information
#### InventoryProductGroup
Description: Data transfer object for product group information
#### PartySummaryPrintModel
Description: Data transfer object for party summary printing
#### UserInfoStatistics
Description: Holds counters for various user-related entities like customers, tasks, and quotes
#### SupportingUnit
Description: Maintains information about a support unit including its status, SKZ text and name
#### CMBuddyLogin
Description: Stores username and password for authentication purposes
#### MyFlashInfo
Description: Extends FlashInfo to add party and creator information to flash messages
#### VipStatus
Description: Manages VIP status state and integer value representation
#### State
Description: Defines possible VIP states: VIP, NO_VIP, UNKNOWN
#### ProductLevel
Description: Manages product level hierarchy and associated products
#### FlashInfo
Description: Data transfer object extending FlashInfoBase to handle flash notifications with temporal and customer data
#### Recipient
Description: Serializable data transfer object representing a message recipient
#### VIPHistoryEntry
Description: Serializable data transfer object for logging VIP status changes
#### PartnerCenterAccessTokenRequest
Description: Extends AccessTokenRequest to handle Partner Center specific token requests
#### RTCode
Description: Data transfer object for rate/tariff code information
#### GamificationCuCoMessages
Description: Container for gamification messages associated with an agent
#### CustomerBinding
Description: Data transfer object for customer contract binding information
#### Attribute
Description: Data transfer object for customer attributes with configuration
#### MatrixData
Description: Data transfer object for matrix-organized product and category data
#### FlashInfoBase
Description: Data transfer object for flash messages/notifications
#### KumsCustomerInfo
Description: Data transfer object for customer VIP information
#### PayableTicket
Description: Data transfer object for billable service tickets
#### SimplePage
Description: Generic container for paginated data with count and content
#### CuCoGamificationLoginMessage
Description: Container for login message data including credentials and session key
#### UserAdminSegment
Description: Container for user feature segment assignments
#### ImageSize
Description: Data transfer object for image dimension information
#### ProductHierarchy
Description: Data transfer object for product hierarchy information
#### CrmAuthenticationPasswordInfo
Description: Data transfer object for CRM password authentication data
#### ProductOverviewConfigurations
Description: Data transfer object for product overview display settings
#### CustomerInteractionAttributes
Description: Enumeration of customer interaction categories
#### BillingCycle
Description: Data transfer object for billing cycle information
#### UserShopAssignment
Description: Data transfer object for user-shop relationships
#### PhoneNumber
Description: Data transfer object for phone number and related attributes
#### GamificationMessage
Description: Data transfer object for gamification messages and notifications
#### FilterType
Description: Enumeration of filter categories (ALL, MYQUOTES, MYAPPROVINGS, MYCUSTOMERS)
#### UserShopAssignmentLogLine
Description: Data transfer object for shop assignment log entries
#### AccessTokenRequest
Description: DTO for handling system access token requests with parameters
#### ProductFeasibility
Description: Data transfer object for product feasibility information
#### FreeUnits
Description: Handles free units data with predefined accumulator units
#### FreeUnitsData
Description: Contains collections of free units results with temporal information
#### FreeUnitsResult
Description: Holds information about available and used telecom units/minutes
#### ContextAwareCustomerUnlockRequest
Description: Handles customer unlock requests with additional context data
#### UnlockRequestContext
Description: Contains contextual information for unlock requests
#### UnlockStateEnum
Description: Defines constants for different unlock states
#### DateValueBean
Description: Bean class holding a date and associated numeric value
#### UsageDetail
Description: Class containing usage details including date, tariff, value and fee information
#### AonProduct
Description: Serializable class containing AON product information
#### Product
Description: Interface defining common product behaviors and attributes
#### MobileUsage
Description: Serializable class containing mobile usage statistics
#### NetworkProvider
Description: Enumeration of telecom network providers with associated values and labels
#### ProductType
Description: Enumeration of available telecom product types
#### InetUsage
Description: Data container for internet usage metrics and costs
#### VoiceUsage
Description: Data transfer object for voice call usage information
#### ProductNode
Description: Represents a product node with label, value and associated party data
#### ProductChartRequest
Description: Data transfer object for product chart request parameters
#### ProductRootNode
Description: Container class that holds reference to the root product node
#### VBMProductDetails
Description: Data transfer object containing product information for VBM
#### VBMProductFeedback
Description: Data transfer object for storing product feedback information
#### VBMProduct
Description: Serializable DTO containing customer and product details for VBM
#### VBMDeclineReason
Description: Serializable DTO containing decline reason information
#### TariffSimulationContainer
Description: Serializable container holding current tariff, tariff lists and ESB response message
#### Price
Description: Data transfer object for price information containing gross and net values
#### TariffLists
Description: Container for managing multiple tariff lists with different classifications
#### TariffSimulation
Description: Proprietary implementation for tariff simulation operations
#### Tariff
Description: Core tariff entity containing tariff details and characteristics
#### TariffCharacteristic
Description: Represents individual characteristics and their associated prices for a tariff
#### ContributionMargin
Description: Handles contribution margin data and calculations with associated indicators
#### TariffSimulationRequest
Description: Data transfer object for carrying tariff simulation parameters
#### MobilPointsBundle
Description: Bundles mobile points and business hardware replacement data for a specific phone number
#### BusinessHardwareReplacement
Description: Stores and manages business hardware replacement information including billing account details and hardware calculations
#### MobilPoints
Description: Represents point balances from different systems for a phone number
#### ChartData
Description: Manages multiple named chart data sets with generic type parameters
#### ChartDataSet
Description: Stores identified chart data as key-value pairs
#### Chart
Description: Extends File class to handle chart images with image map capabilities
#### ChartOptions
Description: Contains customizable parameters for chart display
#### ChartMetaData
Description: Holds image map information and hash for chart identification
#### ChartColor
Description: Enumeration of chart colors with RGB components
#### ProductMoveAction
Description: Simple enumeration for vertical movement actions
#### MarketingProductGroup
Description: Enumeration defining product group categories
#### DefaultProductNode
Description: Extends BaseNode and implements Serializable to represent product information
#### NodeHelper
Description: Contains static methods for node manipulation and retrieval
#### ProductHeaderNode
Description: Extends BaseNode to represent product header information
#### Node
Description: Base interface defining core node functionality for tree structures
#### SAPSubscriptionNode
Description: SAP subscription node implementation with consignee information
#### SubscriptionHeaderNode
Description: Header node containing subscription metadata and addressing information
#### CuCoComponentProductPrice
Description: Extends CuCoProductPriceBase to handle component product pricing with indexation
#### CCTSupervisorSelect
Description: Stores supervisor selection and approval details
#### Promotion
Description: Stores promotion details including dates and discount percentages
#### PhysicalResourceNode
Description: Data transfer object for physical resource information extending BaseNode
#### PartyNode
Description: Data transfer object for party information extending BaseNode
#### DefaultSubscriptionType
Description: Enumeration of possible subscription types
#### AccountAware
Description: Defines contract for objects that can provide account information
#### CallNumber
Description: Serializable DTO for phone number information
#### DefaultSubscriptionNode
Description: Concrete implementation of SubscriptionNode for default subscription types
#### BillableUser
Description: Data transfer object for billable user information
#### BaseNode
Description: Base implementation of Node interface for hierarchical data structure
#### Coordinates
Description: Data transfer object for geographical coordinate information
#### LastMileId
Description: Data transfer object for last mile identification using country code, area code (onkz) and terminal number (tnum)
#### GetPartySummaryResponse
Description: Contains response data including error information and collections of party/product summaries
#### SAPProductNode
Description: Extended node class specific to SAP products with text and equipment metadata
#### MetaData
Description: Container class for managing metadata entries with dual storage mechanisms
#### CuCoProductPriceBase
Description: Base class containing fundamental product price properties
#### CuCoProdPriceCharge
Description: Handles different types of product price charges
#### ProdPriceChargeType
Description: Defines available charge types
#### CCTClearanceStage
Description: Data transfer object for product clearance stage information
#### EmptyProductNode
Description: Node implementation for empty product state
#### AccountNode
Description: Node implementation for account information
#### ProductTree
Description: Container class managing location mappings and party nodes
#### GeoCallNumber
Description: Data container for telephone number information
#### Location
Description: Data container for location details
#### LocationType
Description: Enumeration of possible location types (MOBILE, FIXED, HYBRID)
#### SAPPhysicalResourceNode
Description: Data transfer object for SAP physical resource information extending BaseNode
#### BRKAccountInfo
Description: Data transfer object containing account details and handling fee information
#### CuCoProdPriceAlterations
Description: Handles different types of price alterations for products
#### ProdPriceAlterationType
Description: Defines types of price alterations: recurring discount, one-time discount, allowance
#### CCTOrgStructureElement
Description: Data transfer object for organizational structure information including user and supervisor relationships
#### LocationNode
Description: Extension of BaseNode that wraps Location information for tree structure representation
#### AsyncPlaceholderNode
Description: Temporary placeholder node showing loading status for async operations
#### CuCoPrice
Description: Data transfer object for price information containing amount and currency units
#### CCTAuthorizedQuoteApproversForLevel
Description: Contains information about quote approvers for a specific organizational level
#### MetaDataEntryType
Description: Enumeration of supported metadata types with associated numeric values
#### SubscriptionTree
Description: Container class managing product nodes and subscription node hierarchies
#### AutoVvlInfo
Description: Stores and manages automatic contract extension status and dates
#### AutoVvlStatus
Description: Enumeration of possible automatic extension statuses
#### SubscriptionNode
Description: Extended BaseNode class with subscription-specific information
#### MetaDataEntry
Description: Data transfer object for product metadata with validity period
#### PartySummaryItem
Description: Data transfer object for party summary information
#### Equipment
Description: Data transfer object for equipment with hierarchical structure
#### EquipmentTree
Description: Extends Equipment class to provide a tree structure with equipment summaries and consignee details
#### EquipmentAttribute
Description: Extends KeyValuePair to associate attributes with equipment through an ID
#### EquipmentSum
Description: Implements Serializable and Comparable interfaces to represent equipment summaries
#### EquipmentConsignee
Description: Data transfer object for equipment consignee information implementing Serializable
#### DummyEquipmentConsignee
Description: Empty extension of EquipmentConsignee class
#### HistoryNote
Description: Extension of SalesInfoNote with specific history-related enumerations
#### HistoryLevel
Description: Defines levels of history notes (NOTE, PRODUCT_NOTE, TODO_GROUP_NOTE)
#### HistoryTitle
Description: Defines various types of history events for notes and activities
#### VisitReportSuccessorExistsException
Description: Simple exception class extending Throwable with default constructor
#### FeedbackQuestionsRow
Description: Represents a row of feedback question data with flexible value types
#### SimpleNote
Description: Basic note implementation extending SalesInfoNote
#### SalesInfoNote
Description: Abstract base class for sales information notes with XML binding support
#### AppointmentNote
Description: Specialized sales note for tracking appointments and communication details
#### SalesConvProductNoteRow
Description: Data structure for product details in sales conversation notes
#### SalesInfoNoteHistoryModificationType
Description: Enumeration of all possible modification states for sales note history
#### SbsNoteReportRow
Description: Data structure for SBS note report entries
#### SalesInfoNoteHistory
Description: Entity class representing historical records of sales note modifications
#### Task
Description: Data transfer object for task information with serialization support
#### SalesConvNoteReportRow
Description: Data structure for sales conversation reporting
#### CompetitorNote
Description: Extension of SalesInfoNote for competitor-specific information
#### SalesInfoOverviewRow
Description: Base class implementing Serializable for sales info display rows
#### ToDoGroupNote
Description: Entity class for managing todo group notes
#### SmartHomeNew
Description: Entity class for smart home product details extending SmartHomeBase
#### SecurityOld
Description: Extends SecurityBase to handle old security product offerings including CyberDefence features
#### InternetSpeedNew
Description: Extends InternetSpeedBase to handle new internet speed offerings with additional protection features
#### MobileTariff
Description: Serializable class representing mobile tariff information
#### MobileTariffNew
Description: DTO for new mobile tariff information extending MobileTariffBase
#### ServicesOld
Description: DTO containing old/legacy service text descriptions and configurations
#### SecurityBase
Description: Base class for security-related configurations implementing Serializable
#### MobileTariffBase
Description: Serializable base class for mobile tariff information
#### InternetSpeedOld
Description: Extended internet speed class with virus protection features
#### Payment
Description: Serializable payment information container
#### SecurityNew
Description: Extends SecurityBase to handle new security product configurations
#### SmartHomeOld
Description: Extends SmartHomeBase to handle legacy smart home solutions
#### MobilePhoneBase
Description: Provides base functionality for mobile phone product management
#### InternetSpeedMainUseType
Description: Enumeration of main internet usage types for customer profiling
#### Household
Description: Data transfer object for household information
#### TV
Description: Data transfer object for TV service details
#### MusicSpeakerType
Description: Enumeration of different speaker and headphone types
#### ServicesNew
Description: Data transfer object for new service configurations
#### MobileTariffOld
Description: Data transfer object for legacy mobile tariff information
#### SummaryItem
Description: Data transfer object for summary information with XML binding capabilities
#### MobilePhoneMainUseType
Description: Enumeration of possible main uses for mobile phones
#### InternetSpeedType
Description: Enumeration of internet speed options in Mbit/s
#### InternetSpeed
Description: Serializable data transfer object for internet speed information
#### DigitalSellingNote
Description: Data transfer object containing digital selling information from visits
#### MusicApp
Description: Enumeration of supported music streaming and audio applications
#### TVOld
Description: Extension of TVBase class for legacy TV service information
#### Security
Description: Data transfer object for security information with XML binding support
#### InternetType
Description: Enumeration of internet connection types with wire and mobile options
#### InternetSpeedBase
Description: Serializable base class for internet speed data transfer
#### MobilePhoneOld
Description: Extends MobilePhoneBase to handle mobile phone payment and contract details
#### PaymentOld
Description: Manages payment-related data for digital selling transactions
#### ServicesBase
Description: Serializable class containing base service offerings information
#### MobilePhone
Description: Serializable class for mobile phone product/service details
#### SmartHome
Description: Serializable class for smart home product/service details
#### Services
Description: Serializable DTO for services data with XML binding capabilities
#### TVType
Description: Enumeration of TV service types including wire, mobile, and satellite
#### TVNew
Description: Extension of TVBase class for new TV service configurations with XML binding support
#### TVBase
Description: Base class for storing TV product information and pricing
#### SmartHomeBase
Description: Base class for storing smart home product details and pricing
#### HouseholdType
Description: Enumeration of possible household types (APARTMENT, HOUSE)
#### MobileTariffMainUseType
Description: Enumeration of different primary use cases for mobile tariffs
#### MobilePhoneNew
Description: Extension of MobilePhoneBase with additional payment-related attributes
#### PaymentNew
Description: Serializable payment information container
#### Music
Description: Data transfer object for music streaming service information
#### Country
Description: Data transfer object containing ISO country codes and German name
#### SetupType
Description: Enumeration of possible setup types for services or lines
#### HandlingAssigneeType
Description: Enumeration of possible assignee types: PARTNER_WEB and SHOP
#### SBSOrgUnit
Description: Data transfer object for organizational unit information
#### CommunicationType
Description: Enumeration of communication types: WRITTEN, PERSONAL, TELEPHONIC
#### ContactSource
Description: Enumeration of valid contact source types
#### SBSProductNote
Description: Data transfer object for SBS product notes
#### SBSProduct
Description: Data transfer object representing an SBS product
#### SetupCategory
Description: Enumeration of possible setup categories with bilingual labels (German/English)
#### SBSNote
Description: Data transfer object for SBS notes containing contact and appointment information
#### QuoteStatus
Description: Enumeration of possible states for a quote
#### ContactType
Description: Enumeration of possible contact types in a sales/service context
#### VisitReportDetail
Description: Data container for visit report details including notes and edit permissions
#### CommunicationChannel
Description: Enumeration of communication direction types
#### SBSProductNoteConfig
Description: Configuration container for SBS product notes with product and org unit collections
#### GenericNote
Description: Extension of SalesInfoNote that includes file attachment functionality
#### FileAttachment
Description: Serializable entity for managing file attachments with user and date information
#### SalesConvNote
Description: Data transfer object for sales conversation notes extending SalesInfoNote
#### TeamEmailAdminGroup
Description: DTO for team email administration groups with basic properties
#### ProductHistoryItem
Description: DTO for storing product history entries with user and timestamp information
#### ContactType
Description: Enumeration of possible contact types for sales interactions
#### PhonenumberValidator
Description: Validator class for phone number validation
#### PartyIdValidator
Description: Validator for party ID validation with specific format rules
#### BANValidator
Description: Provides validation logic for bank account numbers
#### isValid
Description: Validates if a given string meets BAN format requirements
#### OfferNumberValidator
Description: Provides validation logic for offer numbers
#### isValid
Description: Validates if a given string is a valid offer number
#### LastnameValidator
Description: Provides validation logic for last names
#### isValid
Description: Validates if a given string meets last name requirements
#### ZipCodeValidator
Description: Provides validation logic for zip code strings
#### isValid
Description: Validates if a given string meets zip code format requirements
#### HousenumberValidator
Description: Provides validation logic for house numbers
#### isValid
Description: Always returns true, allowing any format including special characters
#### OneTVUserValidator
Description: Provides validation logic for OneTV user identifiers
#### isValid
Description: Validates a string value against a provided pattern
#### BvkUserValidator
Description: Validator class that checks if a string value matches a given pattern
#### isValid
Description: Validates input string against a regex pattern
#### FirstnameValidator
Description: Validator class for first name validation
#### isValid
Description: Validates first name input (currently always returns true)
#### StreetValidator
Description: Validator class for street address validation
#### isValid
Description: Validates street address string
#### AONNumberValidator
Description: Validator for AON numbers with specific length and digit requirements
#### CityValidator
Description: Validator for city names with minimum length requirement
#### CommonValidator
Description: Contains static utility methods for common validation operations
#### PartyModel
Description: Data model class for storing party/customer information
#### DualSegment
Description: Enumeration of possible customer segment types
#### PartyModelFactory
Description: Creates and transforms Party-related objects
#### AddressLinkData
Description: Container for address-related fields with getter/setter methods
#### ProductDetail
Description: Product information container including category and location details
#### MultiPartyMatrixData
Description: Maintains a nested hash map structure for storing multi-party product group data
#### MultiPartyProductGroup
Description: Handles product group relationships and data across multiple business parties
#### ContactPersonComparator
Description: Implements comparison logic for ContactPerson objects
#### CuCoAuditEvent
Description: Manages audit event data and logging functionality
#### CuCoAuditScope
Description: Enumeration implementing AuditScope interface to define different auditing scopes
#### CuCoAuditAttribute
Description: Defines trackable attributes for audit logging
#### CuCoAuditActivity
Description: Defines trackable activities for audit logging
#### ContextAwareAuditHelper
Description: Helper class for context-aware audit logging
#### CSVFieldFormater
Description: Formats individual fields for CSV output
#### CSVRowFormater
Description: Formats complete rows for CSV output
#### DateFormater
Description: Implements Formater interface to handle date formatting with a default pattern
#### TableContent
Description: Implements ExportContent interface to handle table-structured data
#### Formater
Description: Defines format method for converting objects to strings
#### ExportContent
Description: Interface defining methods for content formatting and row management in exports
#### BooleanFormater
Description: Formatter that converts boolean values to configurable string representations
#### NullFormater
Description: Formatter that handles null values by returning a configurable default value
#### VIPHistoryService
Description: Service for handling VIP customer historical data and status changes
#### ProductBrowserService
Description: Service for browsing product catalog and managing subscription trees
#### CustomerInteractionService
Description: Service for tracking and managing customer interactions
#### CustomerEquipmentService
Description: Defines operations for customer equipment management
#### UserShopAssignmentService
Description: Manages user to shop mappings and assignments
#### BillingCycleService
Description: Handles billing cycle operations and management
#### getParty
Description: Retrieves party profile information by party ID
#### getBvkUser
Description: Retrieves BVK user information by user ID
#### getOneTVUser
Description: Retrieves OneTV user information by user ID
#### loadAvailablePOSList
Description: Retrieves list of all available points of sale
#### VBMProductsService
Description: Defines operations for VBM product management
#### CucoLogsService
Description: Defines logging operations for the CUCO application
#### AttributeService
Description: Defines operations for attribute management and configuration
#### getPersons
Description: Retrieves multiple person records based on provided usernames
#### getPerson
Description: Retrieves a single person record based on username
#### sendContractToSign
Description: Sends contract data for mobile signature processing
#### getCustomerPasswo
Description: Retrieves customer authentication information (method name appears truncated)
#### PartySearchValueFormatHelper
Description: Formats search values and phone numbers for party searches
#### ProductAdminService
Description: Defines product administration operations
#### POSService
Description: Manages Point of Sale related operations and notifications
#### UnknownAreaCodeService
Description: Defines operations for managing unknown area code data
#### FreeUnitService
Description: Defines operations for managing free unit data and allocations
#### LinksPortletService
Description: Defines operations for retrieving link collections for portlet display
#### getUITexts
Description: Retrieves all UI text entries
#### updateUIText
Description: Updates a single UI text entry
#### searchText
Description: Searches for UI texts matching given criteria
#### getESBParty
Description: Retrieves ESB party by ID
#### getParty
Description: Retrieves generic party by ID
#### markAllMessagesRead
Description: Marks multiple gamification messages as read for an agent
#### addAllMessagesToCuCoDB
Description: Persists multiple gamification messages to database
#### ImageSizeService
Description: Defines operations for image size management
#### KumsCustomerService
Description: Handles customer data operations and interactions with KUMS system
#### SalesInfoService
Description: Manages sales-related information and notes
#### SettingsEditorService
Description: Service interface for CRUD operations on settings
#### CustomerBlockService
Description: Service for managing customer blocks/restrictions
#### FlashInfoService
Description: Service for handling flash messages or notifications
#### ChargingTypeService
Description: Defines contract for charging type management operations
#### ReportingService
Description: Defines contract for reporting operations including retrieval, execution and export
#### UserInfoStatisticsService
Description: Defines contract for user statistics operations
#### CCTOrgStructureElementService
Description: Service interface for organizational structure management operations
#### ContactPersonService
Description: Service for contact person operations (full implementation details not visible in preview)
#### CuCoGamificationPlainWebsocketEndPoint
Description: WebSocket endpoint handling gamification-related communications
#### getMarketplaceAccountsWithSubscriptionsForParty
Description: Retrieves marketplace accounts and associated subscriptions for a given party ID
#### LocationService
Description: Defines location management operations (methods not visible in preview)
#### getInvoiceData
Description: Retrieves clearing account data for multiple party IDs
#### getMobileInvoiceDownloadLink
Description: Generates download link for mobile invoices
#### TurnoverService
Description: Defines contract for turnover management operations
#### CreditTypeService
Description: Defines contract for credit type management operations
#### InsuranceBrokerCpiService
Description: Provides methods to fetch CPI contract quick information for insurance brokers
#### PhoneNumberService
Description: Defines contract for phone number management operations
#### UsageDataService
Description: Defines methods for accessing fixed line, mobile, voice, and internet usage data
#### PartyDeclarationOfConsentService
Description: Handles retrieval of consent declarations based on party, user, and brand information
#### PartyCustomerLoyaltyService
Description: Service interface for retrieving party customer loyalty information
#### AccessTokenService
Description: Service interface for token management and authentication
#### ServiceService
Description: Core service interface with copyright by A1 Telekom Austria AG
#### AutoVvlService
Description: Service interface for retrieving AutoVvl information
#### PayableTicketService
Description: Service for ticket payment operations
#### PromotionService
Description: Service for accessing promotion information
#### getCostFreeClaimInfo
Description: Retrieves cost-free claim information for a given subscription
#### getHsiContractQuickInfo
Description: Retrieves quick contract information for HSI based on subscription
#### getURLForDOCHome
Description: Generates URL for DOC home page based on user and party information
#### getBuddyLink
Description: Retrieves buddy link for a given party ID
#### prepareForSign
Description: Prepares customer data for signature process
#### checkStatusForSigned
Description: Checks signature status for a given job
#### PartyService
Description: Defines contract for party management operations
#### GamificationHttpService
Description: Handles HTTP communication for gamification message retrieval
#### BrkServiceClient
Description: Client interface for retrieving BRK account information
#### TeamService
Description: Defines core team management operations including CRUD operations
#### ClearingAccountService
Description: Defines operations for clearing account management
#### PayableTicketServiceImpl
Description: Spring service implementation for managing payable tickets
#### ContactPersonServiceImpl
Description: Implements contact person management functionality including CRUD operations
#### KumsCustomerServiceImpl
Description: Handles customer data retrieval and caching from KUMS system
#### MobilPointsServiceImpl
Description: Manages mobile points operations using concurrent execution
#### ImageServiceImpl
Description: Implements ImageService interface to provide image management functionality
#### NoteMailHelper
Description: Manages email functionality for sales information notes
#### MasterSessionControlServiceImpl
Description: Manages master session control with ESB integration
#### BusinessHardwareReplacementCallable
Description: Callable implementation for processing hardware replacement requests
#### UITextsEditorServiceImpl
Description: Implementation of UITextsEditorService interface for managing UI texts
#### PhoneNumberServiceImpl
Description: Implementation of PhoneNumberService interface for phone number operations
#### PartyDeclarationOfConsentServiceImpl
Description: Implements consent management operations for parties/customers
#### SettingsEditorServiceImpl
Description: Implements operations for managing system settings
#### CdPersonServiceImpl
Description: Implements operations for managing person/customer data
#### TeamServiceImpl
Description: Implements TeamService interface to handle team-related operations
#### ReportingServiceImpl
Description: Implements report generation using Apache POI for Excel creation
#### CustomerInteractionServiceImpl
Description: Handles customer interaction data and workflow management
#### VIPHistoryServiceImpl
Description: Implements business logic for tracking VIP customer history
#### MobilPointsCallable
Description: Handles asynchronous fetching of mobile points data
#### ImageSizeServiceImpl
Description: Implements image size management functionality
#### LocationServiceImpl
Description: Implements location management functionality with CRUD operations
#### BillingCycleServiceImpl
Description: Handles billing cycle management and processing
#### CustomerUnlockServiceImpl
Description: Handles customer account unlocking functionality
#### ChargingTypeServiceImpl
Description: Implements ChargingTypeService interface to handle charging type operations
#### LinksPortletServiceImpl
Description: Implements LinksPortletService interface to handle portlet operations
#### PartyCustomerLoyaltyServiceImpl
Description: Implements customer loyalty service operations with ESB integration
#### KUMSCommonServiceImpl
Description: Implements common KUMS operations with ESB integration
#### MailService
Description: Handles email operations with timezone and date formatting support
#### CustomerBlockServiceImpl
Description: Implements CustomerBlockService interface for customer blocking operations
#### CCTOrgStructureElementServiceImpl
Description: Implements CCTOrgStructureElementService interface to handle org structure operations
#### ProductAdminServiceImpl
Description: Handles product administration operations including sorting and management
#### SalesInfoServiceImpl
Description: Handles sales information operations and user data integration
#### CreditTypeServiceImpl
Description: Implements CreditTypeService interface to handle credit type business logic
#### ServiceServiceImpl
Description: Implements ServiceService interface to handle service-related business logic
#### FlashInfoServiceImpl
Description: Implements flash info management with transactional support
#### KumsAccountService
Description: Handles account retrieval operations through ESB client
#### UsageDataServiceImpl
Description: Manages internet usage data operations
#### UserShopAssignmentServiceImpl
Description: Manages relationships between users and shops
#### CustomerAssignmentService
Description: Handles operations related to customer contract assignments
#### PartyProfileServiceImpl
Description: Handles party profile operations with ESB integration
#### BrkServiceClientImpl
Description: Handles BRK service operations with ESB integration
#### ClearingAccountServiceImpl
Description: Implements ClearingAccountService interface to handle clearing account operations
#### CrmAuthenticationServiceImpl
Description: Handles CRM authentication using ESB client
#### GamificationHttpServiceImpl
Description: Handles HTTP communications for gamification functionality
#### GamificationLocalServiceImpl
Description: Handles local gamification logic and data management
#### CMBuddyHttpServiceImpl
Description: Handles HTTP communications with CM Buddy system
#### VBMProductsServiceImpl
Description: Manages VBM products data and business logic
#### FreeUnitServiceImpl
Description: Implements FreeUnitService interface to handle free minutes/units operations
#### AccessTokenServiceImpl
Description: Handles access token operations and validation
#### InvoiceServiceImpl
Description: Manages invoice processing and related operations
#### EsbPartyServiceImpl
Description: Implements EsbPartyService interface to provide ESB party management functionality
#### DuposMobileSignatureServiceImpl
Description: Handles mobile signature operations through ESB integration
#### UnknownAreaCodeServiceImpl
Description: Manages logic for processing unknown telephone area codes
#### AutoVvlServiceImpl
Description: Spring service implementation for processing automatic VVL operations
#### InsuranceBrokerHsiServiceImpl
Description: Handles insurance broker operations through HSI interface
#### UserInfoStatisticsServiceImpl
Description: Handles user statistics data operations
#### POSServiceImpl
Description: Implements POS business logic including mail notifications and person management
#### AttributeServiceImpl
Description: Handles CRUD operations for attributes with user context
#### TurnoverServiceImpl
Description: Implements business logic for turnover management
#### PartyServiceImpl
Description: Implements party management business logic including customer data handling and validation
#### InsuranceBrokerCpiServiceImpl
Description: Handles insurance broker integration and contract information retrieval
#### CuscoUnlockServiceImpl
Description: Manages system unlocking functionality with XML processing
#### MarketplaceInventoryServiceImpl
Description: Implements marketplace inventory management functionality with ESB integration
#### CucoLogsServiceImpl
Description: Handles logging operations and user activity tracking
#### VisitReportPrintService
Description: Handles formatting and generation of printable visit reports
#### VisitReportServiceImpl
Description: Implements VisitReportService interface to handle visit report operations and digital selling note processing
#### DigitalSellingNotePrintModel
Description: Represents the structure of a digital selling note with price and note comparisons
#### VisitReportService
Description: Defines contract for visit report operations and customer contact handling
#### JasperUtil
Description: Contains utility methods for Jasper report processing, currently only has empty doSomething() method
#### ImageUtil
Description: Contains methods for image processing and manipulation
#### ReportUtil
Description: Contains utility methods for report processing
#### CustomerEquipmentHelper
Description: Provides utility methods for processing customer equipment information
#### CustomerEquipmentServiceImpl
Description: Implements business logic for customer equipment management
#### CustomerEquipmentExcelHelper
Description: Creates Excel spreadsheets from customer equipment data
#### CustomerEquipmentTranslator
Description: Handles translation and transformation of customer equipment data
#### PartySummaryServiceImpl
Description: Handles party summary operations and ESB interactions
#### PromotionServiceImpl
Description: Manages promotion-related operations and ODS Raw Data Inventory interactions
#### ProductBrowserServiceImpl
Description: Handles product browsing and management operations for customer equipment
#### MetaDataHelper
Description: Provides utility methods for metadata handling
#### PartySummaryService
Description: Defines methods for retrieving party summaries and ICT services
#### loadMyNotes
Description: Retrieves filtered sales info notes with pagination
#### MyNotesServiceImpl
Description: Service implementation for note management operations
#### MyCustomersServiceImpl
Description: Service implementation for customer management
#### getBindingsInfo
Description: Retrieves binding information counts for a given user
#### filterBindings
Description: Searches and filters customer bindings based on criteria
#### loadMyToDoNotes
Description: Retrieves filtered todo notes for sales information
#### MyToDoNotesServiceImpl
Description: Spring service implementation for todo notes management
#### loadFlashInfosForAgent
Description: Retrieves flash information filtered by agent user ID
#### loadPartiesOfFlashInfoAndAgent
Description: Retrieves parties associated with flash info and agent
#### MyQuoteServiceImpl
Description: Service implementation for quote operations
#### loadNumberOfCustomersForSupportUser
Description: Retrieves customer count for support user
#### loadNumberOfCustomersWithChurnForSupportUser
Description: Retrieves count of customers with churn risk
#### MyBindingsServiceImpl
Description: Handles business logic for customer binding operations
#### MyFlashInfosServiceImpl
Description: Manages flash information processing and delivery
#### MyQuoteService
Description: Defines contract for quote and opportunity operations
#### UserActionStatistics
Description: Handles user-specific action statistics tracking and calculations
#### DepartmentActionStatistics
Description: Handles department-level action statistics aggregation
#### ActionStatisticBase
Description: Common base implementation for action statistics tracking
#### DataTheftRapidAlertJob
Description: Executes periodic checks for data theft alerts
#### PhoneNumberCacheJob
Description: Maintains cache of phone numbers through periodic updates
#### LDAPSynchronizationJob
Description: Handles periodic synchronization with corporate directory
#### SalesInfoReminderMailJob
Description: Spring component that extends AbstractCronJob to handle scheduled email reminders
#### KumsSkzShopSynchronizationJob
Description: Spring component that extends AbstractCronJob to handle shop data synchronization

## 4. Dependencies
- at.a1ta.bite.core.shared.dto.*
- java.util.Iterator
- MetaDataEntry
- at.a1ta.bite.data.solr.repository.support.SimpleSolrRepository
- UIText
- com.telekomaustriagroup.esb.cuscocustomercontact.ErrorMessage
- javax.xml.bind.annotation.XmlAccessType
- at.a1ta.bite.core.shared.dto.Filter
- A1 Telekom Austria AG proprietary classes
- java.util.Map
- at.a1ta.cuco.core.shared.dto.EsbParty
- at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote
- at.a1ta.cuco.core.shared.dto.product.*
- com.extjs.gxt.ui.client.widget.form.ComboBox
- Spring framework components
- at.a1ta.cuco.core.shared.dto.Image
- at.mobilkom.eai.mobilpointsservice
- at.a1ta.bite.core.server.service.SettingService
- at.a1ta.cuco.core.service.UnknownAreaCodeService
- com.extjs.gxt.ui.client.widget.grid.ColumnModel
- at.a1ta.cuco.admin.ui.common.client.bundle.configuration.CuCoConfiguration
- at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNoteHistoryModificationType
- org.apache.commons.lang3.ObjectUtils
- com.extjs.gxt.ui.client.widget.form.TriggerField
- ProductNode
- java.io.*
- at.a1ta.bite.core.shared.dto.KeyValuePair
- Arrays
- UserInfo
- at.a1ta.cuco.core.service.AutoVvlService
- at.a1ta.cuco.core.dao.db.VbmProductsDao
- at.a1ta.bite.core.shared.util.CommonUtils
- java.lang.Enum
- at.a1ta.cuco.core.dao.db.CustomerUnlockRequestDao
- BillingCycleService
- RoleGroupService
- at.a1ta.bite.data.clarify.shared.dto.CustomerInteraction
- org.springframework.data.domain.Page
- MetaData
- com.google.gwt.i18n.client
- at.a1ta.cuco.core.dao.db.CucoLogsDao
- InventoryProductGroupAssignable
- FreeMinutesRequestDocument
- at.a1ta.cuco.core.shared.dto.ImageSize
- java.util.Date
- java.io.FileInputStream
- at.a1ta.cuco.core.dao.db.CustomerBlockDao
- java.util.concurrent.Executors
- Not visible in preview but likely includes phone number formatting/validation libraries
- at.a1ta.cuco.core.service.CustomerUnlockService
- com.google.gwt.user.client.rpc
- UserActionStatisticsTestBase
- PhoneNumberParser
- DefaultSubscriptionNode
- at.a1ta.cuco.core.shared.dto.ProductOffering
- org.junit.Before
- Party class (not shown)
- at.a1ta.cuco.core.dao.db.PhoneNumberDao
- java.util.Collections
- com.extjs.gxt.ui.client.event.SelectionListener
- AONNumberValidator
- at.a1ta.cuco.core.dao.db package
- at.a1ta.bite.core.shared.dto.security.Role
- at.a1ta.cuco.core.shared.dto.ChargingType
- java.util.TimeZone
- mergedcpi01soapv1controller
- org.springframework.context.annotation.Profile
- A1 Telekom Austria AG proprietary systems
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.Country
- CuCoPrice
- java.util.List
- org.springframework.beans
- com.extjs.gxt.ui.client.event
- Spring Framework ResourceUtils
- at.a1ta.cuco.core.shared.dto.product.Location
- at.a1ta.cuco.core.service.CreditTypeService
- at.a1ta.cuco.core.dao.db.CmDBICTServiceDao
- Party
- at.a1ta.bite.core.shared.dto.SearchResult
- at.a1ta.cuco.core.shared.dto.*
- at.a1ta.bite.ui.client.generator.textpool.Prefix
- javax.xml.transform
- java.util.*
- Java Util
- at.a1ta.cuco.core.service.PayableTicketService
- at.a1ta.cuco.core.shared.dto.CustomerBinding
- com.extjs.gxt.ui.client.event.*
- at.a1ta.bite.core.shared.util.SharedStringUtils
- at.a1ta.cuco.core.dao.db.MyQuoteDao
- java.util.Collection
- at.a1ta.cuco.ui.common.shared.ApplicationId
- GamificationMessage
- com.google.gwt.i18n.shared
- com.extjs.gxt.ui.client.data
- SLF4J Logger
- BillingAccountNumber
- org.apache.commons.io.FileUtils
- com.extjs.gxt.ui.client.widget.toolbar.PagingToolBar
- net.sf.ehcache.Cache
- ChartColor
- at.a1ta.bite.core.server.esb.BaseEsbClient
- at.a1ta.cuco.core.service.ImageService
- at.a1ta.cuco.core.dao.esb.EsbPartyDao
- ArrayList
- at.a1ta.cuco.core.shared.dto.mobilpoints.BusinessHardwareReplacement
- at.a1ta.bite.core.shared.dto.UserInfo
- org.springframework.transaction.annotation
- org.springframework
- Standard Java IO libraries (implied)
- org.apache.commons.fileupload
- FileAttachment
- at.a1ta.cuco.core.dao.esb.MobilPointsDao
- at.a1ta.framework.ui.client.dto.RpcStatus
- RoleService
- com.google.gwt.i18n.client.DateTimeFormat
- at.a1ta.cuco.core.shared.dto.VIPHistoryEntry
- com.extjs.gxt.ui.client.GXT
- com.extjs.gxt.ui.client.event.FieldEvent
- at.a1ta.cuco.core.dao.db.FlashInfoDao
- at.a1ta.cuco.core.bean.PWUTokenResponse
- javax.xml.bind.annotation.XmlElement
- GamificationLocalService
- at.a1ta.cuco.admin.ui.common.client.dto.ServiceModel
- org.apache.commons.lang3.StringUtils
- org.apache.axis2.context.ConfigurationContext
- org.springframework.core.convert
- at.a1ta.cuco.core.dao.db.LocationDao
- java.util.Properties
- org.springframework.data.domain
- at.a1ta.bite.core.shared.dto.BiteUser
- com.extjs.gxt.ui.client.widget.grid.Grid
- org.mockito.Mock
- at.a1ta.bite.core.mail.MailSender
- UserService
- java.security.KeyStore
- A1 Telekom Austria AG proprietary code
- at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet
- at.a1ta.bite.core.server.dao.EsbAccessParameterDao
- at.a1ta.cuco.admin.ui.common.client.bundle.configuration.SettingsManager
- CustomerAssignmentDao
- org.apache.xmlbeans.XmlException
- com.extjs.gxt.ui.client.data.*
- at.a1ta.cuco.core.dao.db.StandardAddressDao
- com.extjs.gxt.ui.client.widget.tips.ToolTipConfig
- at.a1ta.cuco.core.shared.dto.usagedata.MobileUsage
- at.a1ta.cuco.core.shared.dto.product.DefaultProductNode.ProductType
- at.a1ta.cuco.core.shared.dto.Category
- at.a1ta.cuco.core.shared.dto.PhoneNumberStructure
- java.util.HashMap
- at.a1ta.cuco.core.dao.esb.KUMSCommonDao
- com.extjs.gxt.ui.client.widget.WidgetComponent
- org.springframework.beans.factory.annotation.Qualifier
- ToDoGroupNote
- org.springframework.orm.ibatis.*
- com.extjs.gxt.ui.client.event.ComponentEvent
- at.a1ta.cuco.core.dao.cusco.CusCoDao
- at.a1ta.cuco.core.shared.dto.Party
- at.a1ta.bite.ui.client.BiteEntryPoint
- javax.servlet.annotation.WebServlet
- a1.gdpr.webservice.*
- Not fully visible in preview but likely includes testing frameworks and user action related classes
- java.sql.SQLException
- at.a1ta.cuco.core.shared.dto.mobilpoints.MobilPoints
- GamificationData
- at.a1ta.cuco.core.service.ImageSizeService
- at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest
- at.a1ta.cuco.core.dao.db.SegmentDao
- java.text.NumberFormat
- BaseEsbClient
- CorporateDirectorySynchronizationService
- junit.Assert
- at.a1ta.cuco.core.shared.dto.product.AutoVvlInfo
- at.a1ta.bite.core.server.cron.AbstractCronJob
- at.a1ta.cuco.core.dao.db.ClearingAccountDao
- at.a1ta.cuco.core.bean.*
- com.google.gwt.core.client
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.InternetSpeedType
- at.a1ta.cuco.core.shared.dto.AttributeHistory
- at.a1ta.cuco.core.shared.dto.Message
- org.apache.commons.lang.math.RandomUtils
- at.a1ta.cuco.core.shared.dto.UserShopAssignment
- org.junit.Assert
- at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoOverviewRow
- at.a1ta.cuco.core.shared.dto.usagedata.*
- at.a1ta.cuco.core.shared.dto.tariff.TariffLists
- at.a1ta.cuco.core.service.AttributeService
- HashMap
- Spring Framework
- com.google.gwt.event.logical.shared
- org.apache.commons.lang.NullArgumentException
- com.extjs.gxt.ui.client.Style.SelectionMode
- at.a1ta.cuco.core.dao.db.CategoryDao
- UITextsEditorService
- at.a1ta.cuco.core.shared.dto.Customer
- junit.framework.Assert
- Specific dependencies not visible in preview but likely includes GWT image handling libraries
- InventoryProductGroup
- at.a1ta.cuco.core.shared.dto.OverviewStatus
- com.google.gwt.user.client.ui.HTMLPanel
- AttributeConfig (implied)
- at.a1ta.cuco.core.shared.dto.chart.ChartDataSet
- javax.xml.ws.WebServiceException
- javax.swing.ImageIcon
- at.a1ta.cuco.core.shared.dto.OpportunityFilter
- at.a1ta.cuco.core.bean.File
- com.google.gwt.user.client.rpc.AsyncCallback
- CCTOrgStructureElementService
- at.a1ta.cuco.core.dao.db.SettingsEditorDAO
- at.a1ta.cuco.core.shared.dto.PartyCustomerLoyaltyInfo
- org.springframework.beans.factory.annotation
- com.google.gwt.user.client.ui
- com.extjs.gxt.ui.client.widget.Dialog
- java.math.BigDecimal
- at.a1ta.cuco.core.shared.model.AddressLinkData
- at.a1ta.cuco.core.dao.db.PayableTicketDao
- ServicesBase
- at.a1ta.cuco.core.shared.dto.GamificationRequest
- ClearingAccount DTO
- at.a1ta.cuco.core.shared.dto.ToDoNotesFilter
- java.math.BigInteger
- com.extjs.gxt.ui.client.data.PagingLoader
- com.extjs.gxt.ui.client.widget.Component
- ToDoStatus
- javax.xml.bind.annotation.XmlAccessorType
- at.a1ta.cuco.core.shared.dto.IndexationStatus
- Coordinates (assumed internal class)
- com.extjs.gxt.ui.client.store.ListStore
- ProductLevel
- at.a1ta.cuco.core.shared.dto.usagedata.NetworkProvider
- com.extjs.gxt.ui.client.data.BaseModelData
- at.a1ta.cuco.core.dao.db.SalesInfoDao
- java.util.concurrent.Callable
- at.a1ta.cuco.core.shared.dto.Service
- com.google.gwt.event.logical.shared.*
- at.a1ta.cuco.core.dao.cusco.CusCoResponse
- at.a1ta.bite.data.clarify.shared.dto.Location
- AccountAware
- org.apache.poi.ss.usermodel
- com.extjs.gxt.ui.client.widget.form.NumberField
- at.a1ta.cuco.core.service.UsageDataService
- org.springframework.test.context
- Auth (implied)
- at.a1ta.cuco.core
- ProdPriceChargeType
- java.io.ByteArrayOutputStream
- at.a1ta.bite.core.shared.AuthInfo
- InventoryProductGroupUsage
- at.a1ta.bite.core
- at.a1ta.bite.core.shared.dto.systemmessage.PeriodOfValidity
- at.a1ta.cuco.core.shared.dto.Segment
- at.a1ta.cuco.core.service.visitreport.VisitReportService
- at.a1ta.cuco.core.shared.dto.product.BRKAccountInfo
- com.google.gwt.resources.client.ImageResource
- com.google.gwt.user.client.ui.CheckBox
- at.a1ta.cuco.core.shared.dto.Auth
- com.extjs.gxt.ui.client.widget.ContentPanel
- com.extjs.gxt.ui.client.*
- java.util.Set
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling.DigitalSellingNote
- com.google.gwt.user.client.Window
- com.ibatis.sqlmap.client.extensions.*
- at.a1ta.cuco.core.shared.dto.BillingAccountNumber
- at.a1ta.cuco.core.shared.dto.StandardAddress
- com.ibatis.sqlmap.engine.type.BaseTypeHandler
- CronjobConfigurationDao
- at.a1ta.cuco.core.shared.dto.product.BaseNode
- at.a1ta.cuco.core.dao.db.UnknownAreaCodeDao
- Formater
- BiteUser
- at.a1ta.cuco.core.dao.db.ServiceDao
- com.google.gwt.user.client.ui.TabPanel
- SubscriptionNode
- at.a1ta.bite.ui.server.servlet
- at.a1ta.cuco.core.shared.dto.Invoice
- at.a1ta.cuco.core.shared.dto.NotesFilter
- at.a1ta.bite.core.shared.dto.Text
- com.google.gwt.core.client.*
- StandardAddress
- AbstractSolrRepositoryTest
- org.apache.http.client.HttpClient
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.ContactSource
- at.a1ta.cuco.core.shared.validator.CommonValidator
- java.rmi.RemoteException
- java.util.concurrent.ConcurrentHashMap
- javax.xml.parsers
- org.springframework.web.context.*
- at.a1ta.bite.core.shared.dto.security.Authority
- at.a1ta.cuco.core.shared.dto.ReadOnlyStatusBasedOnCategory
- SBSProduct
- org.mockito.runners.MockitoJUnitRunner
- at.a1ta.cuco.core.shared.dto.ContractOwnerAssignment
- CCTOrgStructureElement
- at.a1ta.cuco.core.shared.dto.PartySearch
- com.extjs.gxt.ui.client.widget.grid.*
- Various *ServletAsync interfaces
- java.util.regex.Pattern
- com.google.gwt.event.dom.client.*
- com.extjs.gxt.ui.client.data.BaseListLoader
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.CommunicationType
- Price
- com.google.gwt.user.client.ui.impl.PopupImplIE6
- at.a1ta.cuco.core.dao.db.MKInteractionDao
- SalesInfoNoteType
- Node interface
- org.junit.Test
- GXT UI components
- Paging functionality
- java.util.logging.Logger
- at.a1ta.cuco.core.shared.dto.PhoneNumber
- at.a1ta.cuco.core.shared.validator.StreetValidator
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic.FileAttachment
- org.apache.commons.lang.StringUtils
- at.a1ta.cuco.core.shared.dto.MobileChurnLikeliness
- java.util.Map.Entry
- ListLoadResult
- at.a1ta.cuco.core.dao.db.CCTOrgStructureElement
- javax.servlet.http.HttpServletResponse
- at.a1ta.bite.core.server.dao.cd.CdPersonDao
- java.util collections (ArrayList, HashMap, HashSet)
- at.a1ta.cuco.ui.common.client.ui.table
- javax.servlet
- com.google.gwt.*
- javax.persistence
- GamificationCuCoMessages
- org.apache.http.HttpResponse
- java.io.File
- at.a1ta.cuco.core.dao.db.ImageDao
- java.io.PrintWriter
- at.a1ta.framework.ui.client.event.PortletEvent
- at.a1ta.bite.core.server.esb.EsbStubFactory
- at.a1ta.cuco.core.shared.dto.UnknownAreaCode
- org.slf4j.Logger
- CCTOrgStructureElementDao
- BaseListLoader
- MIMEType
- com.ibatis.sqlmap.client.SqlMapClient
- GamificationHttpService
- com.extjs.gxt.ui.client.event.Listener
- Spring Test Framework
- at.a1ta.framework.ui.client.event.PortletEventType
- java.text.SimpleDateFormat
- Specific dependencies not visible in preview
- at.a1ta.cuco.core.shared.dto.usagedata.InetUsage
- A1 Telekom Austria AG proprietary components
- java.util collections
- javax.xml.bind.annotation.*
- java.util.Comparator
- org.apache.http.client.methods.HttpGet
- org.apache.commons.lang.time.FastDateFormat
- at.a1ta.cuco.core.dao.esb.CustomerAssignmentDao
- org.junit
- Spring Context
- at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType
- java.io.BufferedReader
- com.google.gwt.user.client.ui.Image
- JUnit
- javax.servlet.http.HttpServletRequest
- org.apache.http.client.methods.HttpPost
- at.a1ta.cuco.core.service.PhoneNumberService
- CommonValidator
- org.junit.runner
- at.a1ta.cuco.core.shared.dto.PartyProfileInfo
- at.a1ta.cuco.core.shared.dto.ProductDetailFilter
- at.a1ta.cuco.core.dao.db.ReportingDao
- at.a1ta.cuco.core.shared.dto.FlashInfo
- at.a1ta.cuco.core.bean.KeyableBean
- at.a1ta.bite.core.server.esb.EsbException
- Apache Commons IO
- com.google.gwt.event.dom.client
- at.a1telekom.eai.customerinventory
- at.a1ta.cuco.core.service
- at.a1ta.cuco.core.service.SalesInfoService
- java.text.*
- ProductOffering
- mockito.Mock
- javax.servlet.*
- org.springframework.stereotype.Service
- javax.servlet.HttpServlet
- at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote
- at.a1ta.bite.core.shared.UnknownUsernameException
- at.a1ta.cuco.core.dao.db.UsageDataDao
- GXT Grid components
- GamificationLocalDAO
- org.apache.commons.lang3
- PartyProfileInfo
- com.google.gwt.user.client
- SBSOrgUnit
- at.a1ta.bite.audit.AuditScope
- javax.xml.bind.DatatypeConverter
- at.a1ta.cuco.core.dao.db.SingleTurnaroundDao
- com.google.gwt.dom.client.Element
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.ContactType
- at.a1ta.cuco.core.dao.db.AttributeDao
- at.a1ta.bite.core.shared.dto.FilterCollection
- at.a1ta.bite.ui.client.generator.textpool.TextPool
- at.a1telekom.eai.party.Party
- java.awt.image.BufferedImage
- a1.gdpr.webservice.Brand
- PhoneNumberStructure
- at.a1ta.cuco.core.shared.dto.CustomerFilter
- at.a1ta.cuco.core.service.ChargingTypeService
- at.a1ta.cuco.core.shared.dto.nbo.VBMProduct
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SetupType
- TariffCharacteristic
- at.a1ta.cuco.core.shared.dto.salesinfo.AppointmentNote
- ProductFeasibilityStatus
- com.google.gwt.user.client.*
- at.a1ta.cuco.core.shared.dto.ProductHierarchy
- ContributionMargin
- Mockito
- at.a1ta.cuco.core.shared.dto.nbo.VBMProductDetails
- FlashInfoService
- org.mockito.*
- javax.imageio.ImageIO
- org.springframework.stereotype
- AccessTokenRequest
- java.util.LinkedHashMap
- FlashInfo
- a1.gdpr.webservice.UserType
- java.io.OutputStream
- at.a1ta.cuco.core.shared.dto.AttributeConfig
- MobilePhoneBase
- org.junit.*
- Report class
- java.util.Arrays
- at.a1ta.cuco.core.service.UserShopAssignmentService
- at.a1ta.cuco.core.shared.dto.product.SubscriptionNode
- org.springframework.stereotype.Component
- com.google.gwt.user.client.ui.impl.PopupImplMozilla
- at.a1ta.cuco.core.service.impl.CustomerAssignmentService
- at.a1ta.cuco.core.shared.validator.LastnameValidator
- at.a1ta.cuco.core.shared.dto.UserInfoStatistics
- at.a1ta.cuco.core.service.ServiceService
- org.mockito
- at.a1ta.cuco.core.dao.db.GamificationLocalDAO
- at.a1ta.cuco.core.shared.dto.PartyDeclarationOfConsentInfo
- at.a1ta.bite.data.clarify.dao.ClarifyInteractionAndWorkflowDao
- at.a1ta.cuco.core.shared.dto.LinksPortlet
- at.a1ta.cuco.core.dao.db.TurnoverDao
- at.a1ta.cuco.core.dao.db.ContactPersonDao
- at.a1ta.cuco.core.shared.dto.VipStatus
- com.google.gwt.core.client.GWT
- at.a1ta.bite.core.server.service.KumsCo
- org.springframework.test.context.junit4.SpringJUnit4ClassRunner
- at.a1ta.framework.ui.client.util.Validator
- at.a1ta.bite.data.solr.core.query
- at.a1ta.cuco.core.shared.dto.MatrixPosition
- at.a1ta.cuco.core.dao.db.CreditTypeDao
- at.a1ta.cuco.core.service.impl
- BaseNode
- at.a1ta.bite.core.server.dao.UserDao
- SettingService
- at.a1ta.cuco.core.shared.dto.product.Location.LocationType
- at.a1ta.cuco.core.dao.db.ImageSizeDao
- CuCoProductPriceBase
- ZipCodeValidator
- at.a1ta.cuco.core.shared.validator.PartyIdValidator
- com.extjs.gxt.ui.client.widget.button.Button
- ClearingAccountDao
- org.apache.solr.client.solrj.beans.Field
- at.a1ta.cuco.ui.common.shared.Location
- org.slf4j
- A1 Telekom Austria AG proprietary framework
- at.a1ta.bite.core.server.dao.SettingDao
- at.a1ta.bite.data.solr.core.query.Field
- net.sf.ehcache
- com.telekomaustriagroup.esb.briana1.BrianA1Stub
- at.a1ta.cuco.core.service.CustomerBlockService
- Not visible in preview
- org.springframework.orm.ibatis.SqlMapClientCallback
- at.a1ta.cuco.core.service.customerequipment.CustomerEquipmentHelper
- BusinessHardwareReplacementDao
- at.a1ta.cuco.core.shared.dto.CreditType
- com.extjs.gxt.ui.client.widget.grid.ColumnData
- org.apache.commons
- at.a1ta.cuco.core.shared.dto.CustomerBlock
- junit.Test
- java.util
- SecurityBase
- at.a1ta.cuco.core.shared.dto.tariff.Tariff
- InternetSpeedBase
- java.awt.Image
- org.joda.time.DateMidnight
- at.a1ta.cuco.core.shared.dto.PayableTicket
- SmartHomeBase
- at.a1ta.cuco.core.dao.db.InvoiceDao
- java.net.InetSocketAddress
- at.a1ta.bite.ui.server.servlet.AuthenticationServlet
- at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement
- org.apache.axis2.AxisFault
- org.apache.http.HttpEntity
- TVBase
- java.net.URISyntaxException
- org.springframework.dao.DuplicateKeyException
- at.a1ta.cuco.core.shared.dto.product.PartySummaryItem
- java.rmi
- com.extjs.gxt.ui.client.store
- java.util.Calendar
- com.extjs.gxt.ui.client.widget.grid
- com.google.gwt.user.client.ui.HTML
- com.extjs.gxt.ui.client.widget.layout
- com.google.gwt.user.client.ui.FlowPanel
- at.a1ta.cuco.core.shared.dto.product
- at.a1ta.cuco.core.shared.dto.nbo.VBMDeclineReason
- java.sql.*
- com.google.gwt.event.dom.client.ClickHandler
- mergedhsi01soapv1controller.controller.core.remoteclient.*
- at.a1ta.framework.ui.client.util.HtmlUtils
- Java util logging
- at.telekom.www.eai.wstokumsretrieveaccount.*
- FirstnameValidator
- at.a1ta.cuco.core.shared.dto.Turnover
- PhoneNumberService
- at.a1ta.bite.core.server.service.AuthorityService
- org.slf4j.LoggerFactory
- java.lang.String
- com.google.gwt.event.dom.client.ChangeHandler
- at.a1ta.cuco.core.shared.dto.salesinfo
- AdminCommonTextPool
- Not fully visible in preview
- java.util.Queue
- org.springframework components
- CuCoComponentProductPrice
- BillingCycleEntry
- at.a1ta.cuco.core.shared.dto.PartyProfileNPSInfo
- com.extjs.gxt.ui.client.widget.form
- org.springframework.beans.factory.annotation.Autowired
- com.extjs.gxt.ui.client.data.ModelData
- org.apache.commons.lang.NotImplementedException
- at.a1ta.cuco.core.shared.dto.Team
- UITextsEditorDAO
- com.telekomaustriagroup.esb.odsrawdatainventory.ODSRawDataInventoryStub
- com.google.gwt.user.client.rpc.RemoteServiceRelativePath
- com.google.gwt.uibinder.client
- com.google.gwt.user.client.ui.Grid
- BaseListLoadResult
- com.extjs.gxt.ui.client.event.ButtonEvent
- com.ibatis.sqlmap.client.extensions.TypeHandlerCallback
- at.a1ta.cuco.core.shared.dto.BindingsFilter
- DateUtils
- ClearingAccountService
- at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine
- External CPI system interfaces
- PointOfSaleInfo
- at.a1ta.cuco.core.shared.dto.AccessToken
- org.joda.time
- java.lang.Throwable
- at.a1ta.cuco.ui.common.client.ui.ModelData
- Java IO
- org.springframework.util.Assert
- Various service async interfaces
- at.a1ta.cuco.core.dao.db.UserShopAssignmentDao
- java.util.EnumSet
- ProductBrowserService
- org.springframework.test.context.ContextConfiguration
- javax.servlet.http.HttpServlet
- at.a1ta.cuco.core.shared.dto.PointOfSaleInfo
- at.a1ta.cuco.core.service.LinksPortletService
- at.a1ta.cuco.core.dao.db.VIPHistoryDao
- at.a1ta.cuco.core.shared.dto.GamificationMessage
- at.a1ta.cuco.core.shared.dto.product.Promotion
- at.a1ta.cuco.core.service.TeamService
- AbstractCronJob
- Likely includes context-related dependencies
- PartySummaryItem
- org.springframework.stereotype.Repository
- Audit system dependencies
- java.text.DateFormat
- at.mobilkom.bit.tariffguide.SimulationType
- at.a1ta.cuco.core.shared.dto.product.LocationNode
- at.a1ta.bite.core.shared.dto.KumsSkzShop
- net.sf.ehcache.CacheManager
- com.extjs.gxt.ui.client.widget.button
- at.a1ta.cuco.core.dao.db.ProductHierarchyDao
- org.springframework.transaction
- at.a1ta.bite.core.server.dao.PersonDao
- at.a1ta.bite.core.shared.dto.Setting
- java.util.concurrent.ExecutorService
- java.time
- at.a1ta.bite.core.server.service.TextService
- com.extjs.gxt.ui.client
- org.springframework.context.annotation.Scope
- com.extjs.gxt.ui.client.widget.LayoutContainer
- java.io.UnsupportedEncodingException
- com.telekomaustriagroup.esb.landingpagedealer.OrderServiceFault
- Window utilities
- at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI
- at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote.ToDoStatus
- at.a1ta.cuco.core.dao.db.UserInfoStatisticsDao
- at.a1ta.cuco.core.dao.db.LinksPortletDao
- VBMDeclineReason
- at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote
- at.a1ta.cuco.core.shared.dto.ContactPerson
- ActionStatisticBase
- at.a1ta.bite.core.server.dao.AbstractDao
- GWT RPC framework
- com.google.gwt.user.client.rpc.RemoteService
- at.a1ta.cuco.core.shared.dto.product.CallNumber
- at.a1ta.cuco.core.bean.Reporting
- EnvironmentProfiles
- at.a1ta.cuco.core.shared.dto.salesinfo.HistoryNote
- SpringJUnit4ClassRunner
- com.extjs.gxt.ui.client.Style
- PhoneNumberDao
- at.a1ta.cuco.core.shared.dto.GamificationResponse
- com.extjs.gxt.ui.client.event.Events
- BillingCycleDao
- at.a1ta.cuco.core.dao.db.MyNotesDao
- A1 Telekom Austria AG proprietary libraries
- com.telekomaustriagroup.esb.duposmobilesignature.DuposMobileSignatureStub
- at.a1ta.framework.ui.client.ui.AbstractPortlet
- at.a1ta.cuco.core.shared.dto.ClearingAccount
- at.a1ta.cuco.core.dao.db.PartyDao
- PhonenumberValidator
- javax.servlet.Filter
- at.a1ta.cuco.core.shared.dto.product.DefaultSubscriptionType
- javax.xml.bind.*
- at.a1ta.cuco.core.dao.util.PhoneNumberParser
- Likely includes authentication/authorization related dependencies
- org.junit.runner.RunWith
- at.a1telekom.eai.customerassignment.xsd.*
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.CommunicationChannel
- Spring Framework Test
- ServiceClassInfo
- com.google.gwt.user.client.ui.impl.PopupImpl
- com.ibatis.sqlmap.client.extensions.ParameterSetter
- NullArgumentException
- com.google.gwt.user.client.ui.*
- at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest
- FreeUnitService
- at.a1ta.framework.ui.client.*
- at.a1ta.cuco.core.dao.db.InventoryProductGroupDao
- java.net
- mockito.runners.MockitoJUnitRunner
- ContractOwnerAssignment DTO
- at.a1ta.cuco.core.dao.db.TeamDao
- FreeUnitsResult
- mockito.ArgumentCaptor
- at.a1ta.cuco.core.shared.dto.salesinfo.*
- com.extjs.gxt.ui.client.widget
- java.io.Serializable
- org.apache.commons.lang
- org.springframework.test
- at.a1ta.bite.data.solr.core.query.result.FacetResult
- org.apache.commons.fileupload.*
- LocationDao
- PartyDeclarationOfConsentInfo
- org.apache.commons.lang.time
- java.util.GregorianCalendar
- java.io
- at.a1ta.cuco.core.shared.dto.ProductGroup
- at.a1ta.cuco.core.shared.dto.SingleTurnaround
- at.a1ta.cuco.core.shared.dto.product.PartyNode
- com.google.gwt.user
- at.a1ta.bite.data.solr.core.query.BasicQuery
- com.google.gwt.dom.client.InputElement
- java.util.logging
- javax.xml.bind.annotation
- at.a1ta.cuco.core.shared.model.DualSegment
- java.lang.RuntimeException
- at.a1ta.cuco.core.shared.dto.CrmAuthenticationInfo
- SqlMapClientDaoSupport
- com.extjs.gxt.ui.client.widget.*
- at.a1ta.cuco.core.shared.dto
- at.a1ta.cuco.core.dao
- at.a1ta.bite.core.shared.dto.security.RoleGroup
- org.apache.poi.hssf
- org.springframework.transaction.annotation.Transactional
- MobileTariffBase
- VBMProductsService
- java.io.IOException
- at.a1ta.cuco.core.shared.dto.BillingCycle
- at.a1ta.bite.core.shared.dto.cd.CdPerson
- com.extjs.gxt.ui
- at.a1ta.cuco.core.shared.dto.RTCode
- javax.annotation.PostConstruct
- at.a1ta.cuco.core.shared.dto.Person
- at.a1ta.cuco.core.shared.dto.UIText
- com.google.gwt.uibinder.client.*
- GWT UiBinder
- at.a1ta.cuco.core.dao.db.MyToDoNotesDao
- at.a1ta.cuco.core.dao.db.ChargingTypeDao
- at.a1ta.bite.core.shared.dto.PortletDefinition
- at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage
- org.springframework.beans.factory
- ProductOffering class
- at.a1ta.cuco.core.dao.db.CCTOrgStructureElementDao
- at.a1ta.cuco.core.shared.dto.MyOpportunity
- org.springframework.data
- at.a1ta.bite.data.solr.core.SolrTemplate
- at.a1ta.cuco.core.shared.dto.Attribute
- Product
- com.extjs.gxt.ui.client.core.XDOM
- BANValidator
- java.util.ArrayList
- at.a1ta.bite.ui.client.bundle
- java.util.HashSet
- com.ibatis.sqlmap.client.extensions.ResultGetter
- at.a1ta.cuco.core.dao.db.UITextsEditorDAO
- at.a1ta.cuco.core.shared.dto.InsuranceBrokerInfo

## 5. Business Rules
- Apply cache control headers to HTTP responses
- Initialize application settings and configuration
- Initialize admin interface settings and configuration
- Must initialize required resource pools before application start
- Must load application resources and configuration before startup
- Must validate user authentication and manage authorization
- Process export requests and format data according to specific date and number formatting rules
- Handle multipart file upload requests and process uploaded files
- Integrate Spring context with iBATIS database operations
- Credit type operations must be handled through Spring Remote Service
- Exception handling must include detailed stack traces
- Team operations require proper authentication
- Handles charging type operations through Spring remote service
- Handles HTTP file upload operations
- File handling operations following A1 Telekom Austria AG proprietary rules
- Date formatting using DateTimeFormat
- Selection handling for grid rows
- Button rendering and event handling in grid cells
- Report data display and interaction handling
- Checkbox label is automatically set to marker's string representation
- Implements paging functionality for system messages
- Handles rendering of service images in grid columns
- Image rendering must validate input data before display
- User interactions must be handled through ClickHandler
- Handle service selection events
- Validate and save service modifications
- Service data validation and persistence
- Allow selection of team members from available list
- Validate team information before saving
- Validate user input on blur events
- Handle value changes in form fields
- Validate role group modifications before saving
- Validate credit type fields before saving
- Schedule message delivery using Scheduler
- Message validation and update logic
- Team member selection and pagination logic
- Team data validation and update handling
- Allows multiple role selection
- Validates area code input
- Handles role selection events
- Paginated loading of service data
- Credit type validation and modification logic
- Role group selection and modification rules
- Grid event handling for role groups
- Date-based usage checking
- Paginated role group management
- Database operation handling
- Handle user input validation and key press events
- Handle tab selection events for message filtering
- Handle shop assignment changes and updates
- Portlet must be initialized with a definition and optional details flag
- Handle report generation and user interactions
- Handle organization structure changes
- Process user interactions with structure elements
- Handle role group management operations through click events
- Maintain single instance of VIP search portlet
- Process VIP search operations and handle date formatting
- Team management layout and display rules
- Service data loading and paging logic
- Credit type click handling and display logic
- Load and display credit type configurations in a grid format
- Display team information in tabular format with alignment controls
- Handle click events for area code management
- Handle keyboard and click events for service-related actions
- Load and display unknown area codes in paginated grid
- Handle paginated loading of team data
- Handles pagination of team member data
- Implements horizontal alignment for service display
- Handles member selection events
- Manages click events for member actions
- Handle team service selection and click events
- Handle team management click events
- Lazy initialization of service clients
- Must provide access to all charging types
- Must handle reporting data retrieval and processing
- Must be serializable for GWT RPC compatibility
- Must provide asynchronous access to charging type data
- Provide asynchronous access to DAO management operations
- Must be accessible at path 'cuco/ibatis.rpc'
- Provide synchronous DAO management operations
- Allows retrieval of all credit types
- Supports saving credit type information
- Allows retrieval of team by ID
- Must be configured with RemoteServiceRelativePath annotation
- Asynchronous retrieval of all reporting configurations
- Asynchronous execution of specific report by ID
- Service must be accessible at path 'cuco/creditType.rpc'
- Service must be accessible at path 'cuco/auth.rpc'
- Provides filtered and unfiltered authority retrieval
- Copyright and proprietary information protection
- File upload handling and processing
- User role management and authorization logic
- Excel formatting and data export rules
- System tracking data processing and date handling
- Validates and processes uploaded file content for user-shop assignments
- Processes and manages unknown area codes through Spring service
- Manages user-shop assignments with authentication checks
- Authentication required for accessing org structure operations
- Spring-managed remote service operations
- Date formatting and history record handling
- HTTP request/response handling
- Must validate HTTP session before processing download request
- Must maintain serialization compatibility
- Must support GWT parsing through default constructor
- Must properly map RTCode DTO to model fields
- Tooltips must be configured with specific styling and behavior settings
- Pagination must handle grouping and sorting of local data
- Images must be handled according to A1 Telekom Austria AG's property rights
- Boolean true renders as localized 'Yes'
- Boolean false renders as localized 'No'
- Handles asynchronous loading of system message data
- All text keys must be prefixed with 'admin_'
- Settings must be initialized before reading values
- String values are returned as-is, Integer values require parsing
- Paging size must be configured via 'application_pagingSize' setting
- SEG import customer interactions default to false if not configured
- Service endpoint must be accessible at 'cuco/unknownAreaCode.rpc'
- Service endpoint must be accessible at 'cuco/systemTracking.rpc'
- Service endpoint must be accessible at 'cuco/cctorgstructureelement.rpc'
- Services are lazily initialized using GWT.create()
- Service endpoint mapped to 'cuco/vipHistory.rpc'
- All operations must be asynchronous using AsyncCallback pattern
- Remote service path must be 'cuco/usershopassignment.rpc'
- All operations must be asynchronous with callback handlers
- Must handle UnknownUsernameException for invalid users
- Provides asynchronous access to unknown area code operations
- Handles analysis data for logon events
- Handles analysis data for customer requests
- Allows deletion of services by ID
- Retrieves all available services
- Service endpoint must be accessible at 'cuco/service.rpc'
- Must handle UnknownUsernameException in async operations
- Provides user management and entry cleanup operations
- Must contain a valid CreditType object for event handling
- Must initialize with a list of roles and SELECT_ROLES event type
- Must handle a list of ModelData containing BiteUser objects
- Manages the addition of unknown area codes through event handling
- Handles the addition of multiple team members as a batch operation
- Manages team addition operations through CuCoEventType.UPDATE event type
- Event must be initialized with a list of ServiceModel objects
- Event must be initialized with a single Service object
- Event must be initialized with a list of team members and ADDTEAM_MEMBERS event type
- Event must be initialized with a Role object and ROLE_UPDATE event type
- Event must be initialized with both a ProductGroup object and an UpdateType
- Popup elements should be displayed with the highest z-index value
- ExtJS image resources should be accessed from 'extImg/' directory
- Popup elements in Mozilla browsers should be displayed with the highest z-index value
- Must handle paging of grid data using PagingLoader
- Must implement filtering logic for memory proxy data
- Must handle button click events and associated actions
- Filter can only be bound to one loader at a time
- Special handling of key press events for Gecko-based browsers
- Dialog handling and event management for detail views
- Filters data based on search criteria before pagination
- Maintains sort order while paginating filtered results
- Applies filtering criteria to data collection
- Handles data sorting with custom comparators
- Converts cell data to HTML link format
- Handles click events on rendered links
- Handles grid selection mode configuration
- Allows adding filters to memory proxy implementation
- Attempts to expand combo box twice if first attempt fails
- Popup elements should always appear at the topmost z-index
- ESB access parameters must be properly configured for DAO operations
- Customer inventory data must be properly retrieved and validated
- Brian ESB operations must handle RemoteException and EsbException properly
- Integration tests are ignored by default
- Integration tests are ignored by default
- Integration tests are ignored by default
- Validate phone number parsing against country codes
- Verify HTTP POST operations for customer data
- Verify correct Solr query construction for party searches
- Verify phone number search functionality in Solr queries
- Verify basic party entity operations in Solr
- Establish common test infrastructure for Solr repository tests
- Validate sales information CRUD operations
- Validate user notes CRUD operations
- Validate customer unlock request processing
- DWH value 'INDEXED_PRODUCTS' should map to IndexationStatus.INDEXED
- House number validation rules must be tested
- City name validation rules must be tested
- Validate first name format and constraints
- Validate ZIP code format and constraints
- Validate AON number format and constraints
- Validate street address format and constraints
- Validate party identifier format and constraints
- Validate lastname format and constraints
- Validate phone number format compliance
- Validate bank account number format and checksum
- Verify flash info processing and management
- Verify invoice processing behavior
- Verify customer assignment operations
- Verify email sending functionality
- Validate token generation and validation logic
- Validate area code processing logic
- Validate customer data retrieval and caching
- Verify customer unlock operations and status changes
- Validate ticket payment processing and status updates
- Verify automated contract extension processing
- Verify gamification HTTP service behaviors and responses
- Validate product browsing and search functionality
- Verify billing cycle calculations and processing
- Customer interactions must have valid dates and types
- Location data must be validated before processing
- Null arguments should throw NullArgumentException
- Account operations must maintain data consistency
- Verify contact person creation and retrieval operations
- Validate party creation, modification and relationship management
- Verify attribute management operations within Spring context
- Digital selling notes must be properly handled within visit reports
- Equipment numbers must handle null values correctly
- Empty equipment numbers must be handled appropriately
- Copyright and intellectual property protection for A1 Telekom Austria AG
- Verify department-level statistics aggregation
- Verify user-level statistics aggregation
- Common test data loading and parsing
- Date formatting and handling
- Verify rapid alert processing for data theft scenarios
- Verify shop data synchronization process
- Configure metrics collection parameters
- Must have unique identifier accessible via getId()
- Implementing classes must provide unique Long identifier
- File types must have corresponding MIME type defined in enum
- Classes used in reporting that return Object type must be whitelisted here for GWT RPC
- invokationDuration defaults to -1
- Copyright and proprietary information must be maintained
- Retrieves billing cycles based on vBlock parameter
- Must provide method to retrieve billing cycles by vBlock
- Retrieves MobilPoints information through ESB service calls
- Date formatting and conversion logic
- BigDecimal calculations
- Must provide party information in both internal and external formats
- Handles contract owner assignment requests through ESB
- Manages hardware replacement operations with error handling
- Must provide phone number structure to retrieve mobile points
- Must return all available points of sale as a list
- Must handle ESB exceptions during party operations
- Lookup contract owner assignment using billing account number
- Lookup contract owner assignment using party identifier
- Generate access token for partner center authentication
- Retrieve hardware replacement info by billing account number
- Handle ESB exceptions and remote invocations
- Convert Java List to Oracle Array when setting parameters
- Convert Oracle Array to Java List when getting results
- Convert List<String> to delimited string for database storage
- Parse delimited string into List<String> when retrieving from database
- true maps to 'Y', false maps to 'N', null remains null
- 'Y' maps to true, anything else (including null) maps to false
- true maps to 'Y' in database
- false maps to 'N' in database
- 'Y' from database maps to true
- Convert IndexationStatus enum to database representation
- Convert database value back to IndexationStatus enum
- true maps to '1' in database
- false maps to '0' in database
- '1' from database maps to true
- Maps database values to VipStatus enum states
- Initializes web service client with configuration context
- Validates and parses phone numbers according to A1 Telekom Austria standards
- Response must contain valid status code
- Must handle customer communication operations
- Must handle HTTP communication timeouts
- Must properly format HTTP POST requests
- Pagination support required for party queries
- String validation and pattern matching for search criteria
- Custom pagination handling for phone number related queries
- Search fields must use case-insensitive matching as indicated by _ci suffix
- Unlock requests must maintain context awareness
- Inventory can be filtered by customer IDs, contract IDs, and product details
- Handles individual turnaround operations for the clearing system
- Manages different types of charging configurations
- Retrieve clearing accounts by party IDs
- Lookup clearing account by phone number
- Retrieve clearing account by account number
- Filters to-do notes based on specified criteria
- Supports customer search with filtering and faceting capabilities
- Allows retrieval of all UI texts
- Supports text content updates
- Enables searching through UI texts
- Retrieve single report by ID
- Retrieve all available reports
- Execute custom reporting statements
- Filter opportunities based on customer status
- Unique address identification by LKMS ID and party ID
- Must maintain audit log entries for user-shop assignments
- Must return a list of all product hierarchy entries
- Location data access must comply with A1 Telekom Austria AG proprietary rules
- Invoice handling must comply with A1 Telekom Austria AG business rules
- Must support filtering of phone numbers based on product details
- Must handle mobile churn likelihood calculations
- Manages persistence of link data for portlet display
- Manages sales conversation notes and reporting data
- Handles appointment and competitor information tracking
- Handles flash/urgent notification data management
- Manage attribute configurations including ordering
- Manage customer blocking states and history
- Manage contact person data and relationships
- All messages must be associated with an agent ID
- Messages can be marked as read in bulk
- Product listing must support filtering by customer ID, product name, period, and scoring total
- Must retrieve all turnover records associated with a specific party ID
- Notes must be retrievable using filter criteria and support pagination through SearchResult
- Old entries must be erasable from the system
- Batch updates must be performed in a single transaction
- Copyright and proprietary information must be maintained
- Teams must support member addition and removal
- Access to VIP history data must be controlled and audited
- Usage data must be retrievable by partyId
- Category data must be properly maintained for customer classification
- Retrieve ICT services for a specific party ID
- Retrieve all settings
- Update individual setting
- Search settings by value
- Copyright and proprietary notice indicates A1 Telekom Austria AG ownership
- Implements clearing account data access operations
- Handles team data persistence and retrieval operations
- Retrieves ICT services associated with a specific party ID
- Handles standard address CRUD operations
- Retrieves product hierarchy list
- Handles party data operations with Spring-managed settings
- Retrieve list of all categories
- Quote management with settings integration
- Retrieve images based on ID and user
- Retrieve list of customer interactions for a specific customer ID
- Handle payable ticket operations with party information
- Manage to-do notes with integration to settings service
- Service insertion must use 'Service.insert' named query
- Uses Spring dependency injection for SettingService
- Handles both internet and mobile usage data tracking
- Phone number parsing and validation
- Product group management and organization
- Credit type deletion operation
- Retrieve all turnover records for a specific party
- Map location data using Long keys
- Retrieve invoices by party ID
- Retrieve all segments from database using SegSegment.list named query
- List contact persons from database
- Handle SQL operations for organizational structure elements
- Retrieve reporting information by ID
- Manage user statistics information with Spring integration
- Retrieve all available charging types
- Retrieve customer blocks associated with a specific flash info ID
- Supports batch operations using SqlMapClientCallback
- Retrieve application settings using cucoSettings.getSettings query
- Sales information persistence and retrieval operations
- Retrieve list of image sizes from database
- Handle SQL operations for gamification data
- Retrieves UI texts using named query 'TextsEditor.getUITexts'
- Retrieves all links using named query 'LinksPortlet.getAll'
- Deletes unknown area code records by ID using named query 'UnknownAreaCode'
- Handles retrieval of single turnaround records
- Handles duplicate key violations in product operations
- Integrates with SettingService for configuration
- Extends AbstractDao for base database operations
- Extends AbstractDao for base database operations
- Requires assertion validation for parameters
- Extends AbstractDao for base database operations
- Handles database operations for user-shop assignments
- Manages historical VIP data operations
- Handles conversion between database and Java representations of SetupType sets
- Handles attribute groupings and configurations for visit reports
- Converts between database values and ToDoStatus enum
- Defines operations for managing sales information and visit report data
- Must implement Serializable for data transfer
- Must implement parameter setting for PreparedStatement
- Supports multiple value types (boolean, number, text, date)
- Contact person can be marked as main contact for a customer
- Copyright and intellectual property rules for A1 Telekom Austria AG
- Defines allowed time period grouping options for system operations
- Lazy initialization of parties list when adding new party
- Objects implementing this interface must be able to be associated with an inventory product group
- Filtering can be done based on user ID, last modification date, and note type
- Credit types must have a name, description, and active status
- Credit types must be serializable for data transfer
- Must maintain serializable state for data transfer
- Sales process must follow defined status progression
- Must maintain proper serialization version control
- Location ID must be initialized to -1
- Both values are optional and can be null
- Team must have a creator and creation date
- Members list is initialized as empty ArrayList
- Must maintain image metadata with unique ID and creation date
- Must track party identification and lead information
- Must implement custom hash code calculation for address comparison
- Email data must include party identification for tracking
- Point of sale starts with LOADING status
- Austria country code is defined as '43'
- Product must be assignable to inventory product groups
- Each party must have a unique partyId
- A party can have multiple billing account numbers
- Collection must be serializable for data transfer
- Customer data must be compatible with Solr indexing
- Each status maps to a specific inventory value and DWH value
- Segments must have a unique ID and sequence number
- BOB invoice IDs must start with '5000'
- BOB invoice IDs must be at least 12 characters long
- Each permission must have a unique string identifier
- Brands collection is initialized with capacity of 6
- Defines standard filter field names as constants
- Status constants defined for different states: ERROR(99), LOADING(-1), NOT_RECEIVED(98), LOADED(0)
- Requires default constructor for GWT parsing support
- Categories must have a unique ID
- Categories are ordered by sequence number
- Clearing accounts must be comparable for sorting/ordering
- Product offerings can be marked as selected or unselected
- Status tracking using integer constants: -1 for loading, 0 for loaded, 98 for not received, 99 for error
- VIP filtering identified by 'vip' constant
- Turnover regions filtering identified by 'turnoverRegions' constant
- Tracks number of notes and imported notes separately
- Maintains timestamp of last update
- Must be serializable for data transfer
- Default ID value must be -1
- Comparison must be based on strings built from Party objects
- Must be serializable for transfer between system layers
- Must be serializable for transfer between system layers
- Consent status must be one of: Complete, None, Partial, or Unknown
- Each status has an associated display text in German
- Items must have one of these defined status values
- Date serialization must follow pattern dd.MM.yyyy.HH.mm.ss.SSS
- Contract filtering must use predefined filter IDs
- Must be serializable for transport across system boundaries
- Must be serializable for transport across system boundaries
- Customer ID (kundeId) and user ID must be stored as Long values
- Product status must be one of three defined states: INSTALLABLE, NOT_INSTALLABLE, or INSTALLED
- Must be serializable for transport across system boundaries
- Both key and value must be initialized as empty strings in default constructor
- Must support GWT parsing through default constructor
- Maintains relationship between product groups and individual products
- Status constants define authentication states: ERROR(99), LOADING(-1), NOT_RECEIVED(98), LOADED(0)
- Each product offering must have a unique numeric ID and string code
- NONE constant represents an invalid token
- Token validity can be checked through isValid() method
- Service class error is represented by value 99
- Loading state is represented by value -1
- Business offer must be associated with a customer ID
- Product groups must have a name and number for identification
- Order field determines the sequence of product groups
- Supports two types of turnover: TA and MK
- Fields are mapped to Solr using @Field annotation
- Status constants define specific states: ERROR=99, LOADING=-1, NOT_RECEIVED=98
- Content can only be in one of two states: EDITABLE or READ_ONLY
- Messages should be compared based on their timestamps in descending order
- Position in matrix is defined by segment (column) and category (row)
- Sequence provides ordering within a cell
- Each service must have a validity period
- Services are identified by unique IDs
- Provides agent ID from nested data object if available
- Mobile charging type is defined as constant with value 3
- Must be serializable for GWT parsing
- Must be serializable for data transfer
- Must be serializable for data transfer
- Status must be one of predefined constants: ERROR(99), LOADING(-1), NOT_RECEIVED(98), LOADED(0)
- Default status is LOADING
- Must maintain serialization compatibility with version ID
- Default state is UNKNOWN
- Flash information must have valid time bounds (from/to dates)
- Recipient must have a unique identifier
- Each status change must record both old and new status values
- Status changes must be timestamped
- Must specify target and source systems during initialization
- Must be serializable for data transfer
- Messages must be associated with an agent ID
- Messages list is initialized as empty ArrayList
- Tracks contract duration through start and end dates
- Implements copy constructor pattern for attribute duplication
- Organizes product groups in a matrix structure by segment and category
- Flash messages can be targeted to specific roles
- Messages can be displayed as popups or regular notifications
- VIP status is tracked as an Integer value
- Changes must be tracked with a timestamp
- Each ticket must be associated with a customer ID
- Tickets require business account number (ban) and service identifiers (lknz, onkz)
- Maintains validity state of input data
- Must maintain serialization compatibility
- Must maintain serialization compatibility
- Products are organized in a 3-level hierarchy structure
- Maintains version control through serialVersionUID
- Class must maintain serialization compatibility
- Provides case-sensitive string matching for enum values
- Must maintain billing date and associated entries
- Default constructor initializes empty strings for both fields
- Maintains version control through serialVersionUID
- Provides standard filter field constants for opportunity filtering
- Default constructor initializes empty strings
- Must support iteration over parameter entries
- Must implement Serializable for data transfer
- Defines standard unit types for time-based measurements
- Must implement Serializable for data transfer
- Must implement Serializable for data transfer
- Maintains separate collections for different aggregation levels
- Tracks maximum, used and unused minutes for telecom units
- Distinguishes between pulse and non-pulse units
- Handles customer unlock operations with context awareness
- Maintains context information for unlock operations
- Mobile attributes must have exactly 14 fields
- Products must provide party information
- Products must specify their type
- Products must specify their network provider
- Must track both upload and download data separately
- Must distinguish between IB (Inbound) and ObEu (Outbound EU) data
- A1 provider is represented by value 'T'
- ANB provider is represented by value 'A'
- Combined provider is represented by value 'C'
- Products are categorized into fixed line, internet, and mobile services
- Tracks both volume-based (upload/download) and time-based (duration) usage
- Distinguishes between different fee types: subscription, variable, and high usage
- Voice usage must track call date, duration, fees and classification metadata
- Product nodes must maintain hierarchical relationships and party associations
- Chart requests must specify party, product type and provider information
- Contains a predefined constant ALL_PROD representing all products
- Default decline reason is initialized with new VBMDeclineReason instance
- Container must be initialized with empty constructor
- Price must maintain both gross and net values
- Maintains separate lists for all tariffs and recommended tariffs
- Implementation must comply with A1 Telekom Austria AG's proprietary concepts
- Default unknown tariff instance must be available
- Price retrieval must handle null values safely
- Unknown contribution margin must be immutable
- Handles precise decimal calculations using BigDecimal for binding months
- Uses BigInteger for exact counting of SIMs and fee calculations
- Points must be tracked separately for each system (Amdocs, PartnerWeb, Clarify)
- Data sets are stored with string keys for identification
- Order of data sets is preserved using LinkedHashMap
- Each dataset must have a unique identifier
- Data order is preserved using LinkedHashMap
- Chart mime type must be set to PNG by default
- Default small chart dimensions are 500x300
- Default big chart dimensions are 600x400
- Default dimensions are 400x400 if not specified
- Must support both empty initialization and full data construction
- RGB values must be between 0-255
- Products can only move up or down
- Marketing products must be categorized as either main products or additional products
- Product node must maintain indexation status
- Traverse parent nodes to find PartyNode
- Maintain header information for product display
- All nodes must be serializable
- Nodes must support parent-child relationships
- Must maintain consignee information for SAP subscriptions
- Must maintain header information for subscription identification
- Supports multiple address lines for detailed location information
- Product prices must track indexation status and start date
- Supervisor approvals must include approval level and release status
- Promotions must have effective and expiration dates
- Discount percentage must be specified for each promotion
- Must maintain text description for physical resource
- Must maintain party name and address information
- System must use only predefined subscription types
- Must support GWT parsing through default constructor
- Must be serializable for data transfer
- Maintains parent-child relationships in tree structure
- Tracks depth in hierarchy
- Must be serializable for data transfer
- Stores geographical position using double precision
- Response must include error status and message for error handling
- Must override getText() method from BaseNode
- Maintains synchronized list and map representations of metadata entries
- Must maintain unique identifiers for product prices and offerings
- Charge type must be specified during instantiation or default constructor
- Maintains serialization compatibility
- Returns fixed text 'Keine Produkte' for empty state
- Copyright and intellectual property protection
- Must implement Serializable for data transfer
- Location must be categorized as either MOBILE, FIXED, or HYBRID
- Price alterations must be categorized as either RECURRING_DISCOUNT, ONETIME_DISCOUNT, or ALLOWANCE
- Maintains approval level hierarchy between users and supervisors
- Node text display must be derived from location address
- Must display loading message as placeholder text
- Loading message needs to be externalized (TODO)
- Price must include both a currency unit and numerical amount
- Each approval level must have a numeric identifier and list of authorized approvers
- Each metadata type must have a unique integer value
- Supported metadata types are limited to predefined set of 9 types
- Contract extension status can be JA, NEIN, or KEINE_VEREINBARUNG
- Metadata entries must have temporal validity defined by start and end dates
- Can be initialized either with name and count or name and URL
- Top-level equipment has empty parent ID
- Equipment objects can be compared for ordering
- Equipment attributes must have an equipment ID, key, and value
- Equipment summaries must be comparable
- Equipment summaries must be serializable
- Must maintain serialization compatibility for data transfer
- History notes must be categorized by specific levels
- All history events must be tracked with specific titles
- Indicates that a visit report cannot be modified because it has a successor
- Supports multiple value types (number, boolean, text) for flexible question responses
- Supports copying of note instances through copy constructor
- Sales notes must support XML serialization
- Appointment notes must track communication type, channel and contact type
- Product notes must track product details, quote status, and contact information
- Sales note modifications must be categorized into one of the defined types
- Each modification must be timestamped and associated with a user
- Must implement Serializable for data persistence
- Must maintain serialization compatibility
- Tracks conversation note history through predecessor relationship
- Tracks binding dates and reminder mail status for competitor information
- Must be serializable for data transfer
- Handles processing orders (Abwicklungsauftrag)
- XML field-based access for serialization
- Maintains legacy CyberDefence product information including pricing and description
- Tracks internet protection feature enablement for new speed products
- Must maintain serialization compatibility with version ID
- Must maintain XML serialization compatibility
- Must maintain XML serialization compatibility
- Must maintain serialization compatibility
- Must support XML binding
- Class must be XML serializable for data transfer
- Virus protection is optional with associated pricing
- Payment data must be XML serializable
- Tracks cyber protection product selection and associated pricing
- Manages smart solution selection, pricing, and descriptive text
- Implements Serializable for object persistence
- Customer internet usage must be categorized into one of the defined types
- Household must be serializable for data transfer
- Household must have a defined type
- TV information must be serializable for data transfer
- TV fields must be XML accessible
- Product categorization must be one of three defined types
- Initial setup service availability flag with associated price
- Maintains serialization compatibility with version ID
- Must be XML serializable
- Mobile phone usage must be categorized into one of the defined types
- Internet speeds must be one of the predefined tiers ranging from 20 to 300 Mbit/s
- XML serialization configuration for digital selling data
- Defines the fixed set of music applications that can be referenced in the system
- Class must maintain serialization compatibility
- Internet connection must be classified as either wired or mobile
- Supports part payment functionality for mobile phones
- XML field-level access for serialization
- XML field-level access and element mapping
- XML field-level access and element mapping
- Class must be XML serializable
- TV service must be one of three types: wire-based, mobile, or satellite
- Must follow XML access rules defined by parent class
- Class must be XML serializable for data transfer
- Class must be XML serializable for data transfer
- Only two types of households are supported: APARTMENT and HOUSE
- Mobile tariff usage must be categorized into one of the predefined types
- Part payment option must have associated price when enabled
- Payment information must be serializable for persistence
- Class must be XML serializable
- Must store both 2-letter and 3-letter ISO country codes
- Country name must be stored in German
- Setup operations must be one of three defined types
- Tasks can only be assigned to either partner web interface users or shop users
- Organization unit must be serializable for data transfer
- Communication must be classified as either written, personal, or telephonic
- Contact sources must be one of the predefined enum values
- Product must have a unique identifier
- Product can be marked as active or inactive
- Setup categories are predefined and cannot be modified at runtime
- Quote status must be one of the predefined states
- Contact interactions must be categorized as one of the defined types
- Visit report details can be marked as editable or non-editable
- Communication must be classified as either inbound or outbound
- Must support deep copying through copy constructor
- Must support deep copying through copy constructor
- Team email groups can be marked as default
- Each history item must track creation user and date
- Contact types are limited to phone calls (inbound/outbound), leads, and mail communications
- Currently returns true without validation (placeholder implementation)
- Empty or blank values are considered valid
- Valid party IDs must either pass lead search validation or be exactly 9 digits long
- Non-blank party IDs must contain only digits when 9 characters long
- BAN must be exactly 9 digits long
- BAN must contain only numeric characters
- Empty or null values are considered valid
- Empty or null values are considered valid
- All non-empty values are currently considered valid
- Last name must be longer than 3 characters if not empty
- Empty or null values are considered valid
- Zip code must be between 4 and 5 characters in length
- Zip code must contain only digits
- Empty or null values are considered valid
- All house number formats are considered valid, including special characters
- User identifier must match the provided pattern
- Empty or null values are considered valid
- Empty or null values are considered valid
- Non-empty values must match the provided pattern
- All first names are currently considered valid
- Street address must be either empty or longer than 3 characters
- AON number must be at least 6 characters long
- AON number must contain only digits
- Empty or null values are considered valid
- City name must be at least 2 characters long if not blank
- Empty or null values are considered valid
- String must contain only numeric digits for digit validation
- String length must fall within specified minimum and maximum bounds
- Must be serializable for data transfer
- Each segment has an associated numeric code and description
- Handles transformation of various party-related DTOs to PartyModel
- Matrix data is organized in a nested structure with Long keys
- Maintains relationships between parties and product groups
- Compares ContactPerson objects based on a constructed comparison string
- Maintains audit trail of system events
- Audit scope must return its name as a string representation
- Attributes must follow A1 Telekom Austria AG's proprietary concepts
- Activities must follow A1 Telekom Austria AG's proprietary concepts
- Audit logging must preserve context information
- Fields must be properly escaped according to CSV standards
- Default separator is semicolon, with comma as RFC4180 alternative
- Rows must end with CRLF line break
- Separator is configurable through constructor
- Default date format pattern is 'dd.MM.yyy hh:mm'
- Default row length is 128 characters for StringBuilder performance
- All formatters must implement format(Object) method
- Allows setting formatters at type, column, row and content levels
- Supports dynamic row addition and clearing of content
- Default boolean representations: 'ja' for true, 'nein' for false
- Handles null values with configurable default value
- Returns empty string as default value for null objects if not configured otherwise
- Allows custom default value configuration through constructor
- Track VIP status changes for customers
- Build product hierarchies and subscription relationships
- Record and track customer interaction history
- Equipment management must follow A1 Telekom Austria AG policies
- Users must be associated with shops for management purposes
- Billing operations must comply with A1 Telekom Austria AG standards
- Must return empty list if no POS data is found
- Copyright and proprietary information must be maintained
- Configuration updates require user ID
- Configuration insertions require user ID
- Must support bulk retrieval of person data
- Contract must be provided as byte array with job ID for tracking
- Authentication info must be mapped to customer identifiers in HashMap
- Phone numbers must be formatted according to specific standards
- Product administration operations must follow A1 Telekom Austria AG policies
- POS changes must trigger email notifications
- Service must provide all available links through getAllLinks() method
- UI texts must be retrievable, searchable and updatable
- Party information must be retrievable using party ID
- Messages must be associated with an agent ID
- Messages can be batch processed for reading and storage
- Handles sales information and note management
- Allows retrieval of all settings
- Enables updating individual settings
- Provides text search functionality across settings
- Contains copyright and licensing restrictions for A1 Telekom Austria AG
- Contains copyright and licensing restrictions for A1 Telekom Austria AG
- Charging type operations must follow A1 Telekom Austria AG proprietary rules
- Reports can be retrieved by ID
- Reports can be exported to Excel format
- User statistics operations must follow A1 Telekom Austria AG proprietary rules
- System must maintain a list of all users
- Old entries must be removable from the system
- Organizational structure must be updatable with multiple elements simultaneously
- Copyright and intellectual property belongs to A1 Telekom Austria AG
- Party ID must be valid to retrieve marketplace accounts
- Copyright and intellectual property protection for A1 Telekom Austria AG
- Multiple clearing accounts can be associated with a party ID
- Must provide CPI contract quick information based on subscription details
- Access to usage data is organized by partyId
- Consent declarations are specific to party ID, user ID, brand, and user type
- Must retrieve loyalty information for a given party ID
- Must handle landing page dealer settings with specific prefix
- Software distributed as-is without warranties
- Intellectual property rights belong to A1 Telekom Austria AG
- AutoVvl information can be retrieved using either a call number or BAN number
- Proprietary A1 Telekom Austria ticket payment handling
- Multiple promotions can be retrieved for a single call number
- Must provide insurance broker information based on subscription data
- Copyright and proprietary information must be maintained
- Must generate valid DOC home URL using party ID, username, name, and IP address
- Copyright and proprietary notice indicates this is A1 Telekom Austria AG owned code
- Buddy links are associated with party IDs
- Signature process requires customer info, user info, contact person and template ID
- Signature status can be checked using a job ID
- Copyright and proprietary information rules for A1 Telekom Austria AG
- Gamification messages must be retrieved from specified endpoint
- BRK account information can be retrieved using either account number or BAN number
- BAN number can be used to lookup BRK account number
- Teams can be created, updated and retrieved
- Copyright and proprietary information rules apply
- Service initialization occurs after construction
- Logging is implemented for service operations
- Contact person management operations must be authenticated
- Customer data must be cached for performance
- Handle WebService exceptions gracefully
- Mobile points operations must be executed asynchronously
- ImageDao must be non-null when instantiating service
- Handles sales info note types and their email processing
- Session control logic with ESB client integration
- Executes hardware replacement business logic asynchronously
- Provides CRUD operations for UI text management
- Manages phone number operations and billing account associations
- Manages GDPR consent declarations for parties
- Handles CRUD operations for application settings
- Handles customer data management operations
- Transactional integrity for team operations
- Excel report formatting and data organization
- Customer interaction processing and workflow routing
- Validates null arguments
- Executes mobile points retrieval logic
- Handles image size data operations
- Location data must be validated before persistence
- Billing cycles must have valid date ranges
- Customer unlock must be authorized and logged
- Service layer implementation for charging type management
- Service layer implementation for links portlet management
- Customer loyalty management with file handling capabilities
- ESB client integration for KUMS operations
- Date formatting with timezone consideration
- Customer blocking operations implementation
- Product comparison and sorting logic
- Service must implement CreditTypeService interface
- Service must implement ServiceService interface
- Operations must be transactional
- Account retrieval through KUMS web service
- Internet usage data management and retrieval
- User-shop assignment management and validation
- Contract ownership assignment validation and processing
- Date formatting and file handling for party profiles
- String validation and calendar operations for BRK service
- Service layer implementation for clearing account management
- CRM authentication logic using ESB integration
- HTTP-based gamification feature implementation
- Random utility operations for gamification logic
- HTTP client protocol handling and error management
- Product management and decline reason handling
- Process free minutes requests through ESB client
- Validate and process access tokens
- Token validation assertions
- Process and manage invoice collections
- Handle WebService exceptions
- Party data transformation between ESB and internal representations
- Mobile signature validation and processing
- Error handling for RemoteException and Fault conditions
- Copyright and intellectual property protection
- Calendar/Date based processing logic
- Contract quick info retrieval logic
- User statistics data management logic
- Mail notification handling for POS operations
- Attribute management with user context validation
- Turnover data management and calculations
- Party data validation and processing logic
- Insurance contract data retrieval and processing
- XML-based unlock request processing and validation
- ESB client integration for inventory operations
- Log management and persistence through CucoLogsDao
- Number formatting and text processing for report generation
- XML processing and transformation of visit reports
- Maintains old and new versions of prices and notes
- Defines required operations for visit report processing
- Copyright and intellectual property belongs to A1 Telekom Austria AG
- Transform and validate customer equipment data
- Handle customer equipment data retrieval and caching
- Remote service integration
- Excel formatting and data presentation rules
- Date formatting standards
- Transform equipment data according to business specifications
- Process party summaries according to business requirements
- Handle promotion processing and inventory data management
- Product browsing and file handling operations
- Metadata processing and validation rules
- Party summary retrieval operations
- ICT services retrieval for specific party
- Notes must be filtered according to NotesFilter criteria
- Service must use MyNotesDao for data persistence
- Customer data must be organized using various map implementations
- User authentication required for accessing binding information
- Notes must be categorized by SalesInfoNoteType
- Service must be managed by Spring framework
- Flash info access must be filtered by agent user permissions
- Quote operations must be managed through DAO layer
- Support users must have restricted access to customer data
- Churn risk tracking must be maintained for customers
- Service manages customer binding settings and relationships
- Processes and filters flash information based on specified criteria
- Handles loading of opportunities with custom filtering options
- Track user-specific action metrics and statistics
- Aggregate and calculate department-wide action statistics
- Define core statistics calculation and tracking methods
- Implement common statistical operations
- Periodic execution of data theft detection and alerting
- Periodic cache refresh of phone numbers
- Environment-specific LDAP synchronization (Profile-based)
- Execute reminder email sending based on configured schedule
- Synchronize shop data with external KUMS system on schedule


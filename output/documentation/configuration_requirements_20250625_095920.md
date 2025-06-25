# Requirements Document: Configuration Layer

## 1. Overview
Analysis of configuration layer components and functionality

## 2. Components
- cuco/src/main/filters/logback.xml (XML configuration)
  - Purpose: Logging configuration file that defines logging behavior and output formats using Logback framework
- cuco/src/main/filters/web-ntlm.xml (XML configuration)
  - Purpose: Web application configuration file for NTLM authentication setup
- cuco/src/main/filters/web-external.xml (XML configuration)
  - Purpose: Web application configuration file for external authentication setup
- cuco/src/main/filters/ehcache.xml (XML configuration)
  - Purpose: EhCache distributed caching configuration for application caching management
- cuco/src/main/filters/web-internal.xml (XML configuration)
  - Purpose: Web application deployment descriptor for internal configuration
- cuco/src/main/filters/gwt/PkbStarter.gwt.xml (XML configuration)
  - Purpose: Google Web Toolkit module configuration for PKB application
- cuco/src/main/filters/gwt/AppStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file for the main application starter module
- cuco/src/main/filters/gwt/MyCuCoStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file for the MyCuCo application starter
- cuco/src/main/filters/gwt/AdminStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file for the admin application starter module
- cuco/src/main/resources/logback.xml (XML configuration)
  - Purpose: Logging configuration for the CUCO application
- cuco/src/main/resources/ehcache.xml (XML configuration)
  - Purpose: Cache configuration for distributed caching using JMS
- cuco/src/main/resources/at/a1ta/cuco/app/starter/AppStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration for the CUCO application starter
- cuco/src/main/resources/at/a1ta/cuco/admin/starter/AdminStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file for the admin interface starter module
- cuco/src/main/resources/at/a1ta/cuco/mycuco/starter/MyCuCoStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file for the MyCuCo application starter module
- cuco/src/main/resources/at/a1ta/pkb/starter/PkbStarter.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file that defines the entry point and inheritance structure for the PKB application
- cuco/src/main/webapp/WEB-INF/web.xml (XML configuration)
  - Purpose: Java web application configuration file
- administration.ui/src/main/resources/META-INF/web-fragment.xml (XML configuration)
  - Purpose: Web fragment configuration file defining servlet mappings and configurations for the administration UI module
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/CucoSett.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file defining module inheritance and dependencies
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/EditUserDialog.ui.xml (XML configuration)
  - Purpose: UI definition file for user editing dialog using GWT UiBinder
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/EditCreditTypesDialog.ui.xml (XML configuration)
  - Purpose: UI definition for a dialog to edit credit types in the administration interface
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/EditUnknownAreasCodeDialog.ui.xml (XML configuration)
  - Purpose: UI definition for a dialog to edit unknown area codes in the administration interface
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/GwtSelectRolesDialog.ui.xml (XML configuration)
  - Purpose: UI definition for a dialog to select user roles in the administration interface
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/EditRoleGroupManagementDialog.ui.xml (XML configuration)
  - Purpose: UI definition for role group management dialog in the administration interface
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/GwtSelectServiceDialog.ui.xml (XML configuration)
  - Purpose: UI definition for service selection dialog component
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/EditTeamsDialog.ui.xml (XML configuration)
  - Purpose: UI definition for team editing dialog interface
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/GwtSelectTeamMemberDialog.ui.xml (XML configuration)
  - Purpose: UI definition for a dialog to select team members in a GWT web application
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/GwtEditServiceDialog.ui.xml (XML configuration)
  - Purpose: UI definition for a dialog to edit service settings in a GWT web application
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/dialog/GwtEditMessageDialog.ui.xml (XML configuration)
  - Purpose: UI definition for a dialog to edit messages in a GWT web application
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/portlet/AuthorityAdministrationComponent.ui.xml (XML configuration)
  - Purpose: Defines the UI layout for an authority administration interface component
- administration.ui/src/main/resources/at/a1ta/webclient/cucosett/client/portlet/vip/VipSearchComponent.ui.xml (XML configuration)
  - Purpose: Defines the UI layout for a VIP search component
- administration.ui/src/main/resources/at/a1ta/cuco/admin/ui/common/CuCoAdminCommon.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file defining inheritance and resource dependencies
- administration.ui/src/main/resources/at/a1ta/framework/gxt/GxtUtilities.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file for GXT UI utilities and theme integration
- cuco-core/src/main/resources/at/a1ta/cuco/core/CucoCore.gwt.xml (XML configuration)
  - Purpose: GWT module configuration file defining source paths for core functionality
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/billingcycle/sqlmap-billingCycle.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for billing cycle operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/billingcycle/applicationContext-cuco-dao-bc.xml (XML configuration)
  - Purpose: Spring configuration file for billing cycle DAO layer
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/billingcycle/sqlmap-config-bc.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for billing cycle functionality
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-inventoryProductGroup.xml (XML configuration)
  - Purpose: SQL mapping definitions for inventory product group operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customerUnlockRequest.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for customer unlock request functionality
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-standardAddress.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for standard address management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-gamification.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for gamification messaging system
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-invoice.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for invoice-related database operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-user.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for user-related database operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-billingCycle.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for billing cycle operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-vipHistory.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for VIP customer history tracking
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-team.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for team management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customerBlock.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for customer blocking functionality
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-vbmProducts.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for VBM products with caching configuration
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customer.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for customer-related operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-cucoLogs.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for CUCO logging operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-usageData.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for usage data queries with caching support
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-businessOffers.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for business offers with caching support
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-myquote.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for quote and opportunity management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-location.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for location-related database operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-kumsskzshop.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for KUMS SKZ shop operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-turnover.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for turnover-related database operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-config.xml (XML configuration)
  - Purpose: Main iBatis SQL mapping configuration file that sets up global settings and includes other mapping files
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-linksPortlet.xml (XML configuration)
  - Purpose: SQL mapping configuration for Links Portlet functionality
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-credittype.xml (XML configuration)
  - Purpose: SQL mapping configuration for credit type management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-textseditor.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for managing UI text/translation data
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-reporting.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for reporting functionality
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-flashInfo.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for flash information management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-userInfoStatistics.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for user information statistics with caching
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-mkinteraction.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for marketing interactions with caching
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-userShopAssignments.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for user-shop assignment management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-cucoSettings.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for managing application settings/configurations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-imageSize.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for handling image size data with caching
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-phoneNumber.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for phone number data management with caching
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-chargingtype.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for charging type data access
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-unknownareacode.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for handling unknown area codes
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-inventory.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for inventory management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-contactPerson.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for contact person data access operations with caching support
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-mynotes.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for sales notes and tasks
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-cCTOrgStructureElement.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for CCT organizational structure elements
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-image.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for image-related database operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-clearingAccount.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for clearing account operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/applicationContext-cuco-dao-db.xml (XML configuration)
  - Purpose: Spring application context configuration for database DAO layer
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-productHierarchy.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for product hierarchy data access with caching
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-payableticket.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for payable ticket operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-attribute.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for attribute management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-service.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for Service-related database operations
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-salesInfo.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for Sales Information management
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/visitreport/sqlmap-visitreport.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for Visit Report functionality with SBS (Step-by-Step) features
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/cmdb/applicationContext-cuco-dao-cmdb.xml (XML configuration)
  - Purpose: Spring configuration file for CMDB DAO layer
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/cmdb/sqlmap-config-cmdb.xml (XML configuration)
  - Purpose: iBatis SQL mapping configuration for CMDB
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/cmdb/sqlmap-cmDBICTService.xml (XML configuration)
  - Purpose: SQL mapping definitions for CMDB ICT Service entities
- cuco-core/src/main/resources/at/a1ta/cuco/core/service/applicationContext-cuco-service.xml (XML configuration)
  - Purpose: Spring application context configuration file for CUCO core services
- cuco/pom.xml (XML configuration)
  - Purpose: Maven project configuration for main CUCO module
- administration.ui/pom.xml (XML configuration)
  - Purpose: Maven project configuration for CUCO administration UI module
- cuco-core/pom.xml (XML configuration)
  - Purpose: Maven project configuration file for cuco-core module
- cuco-core/SoapUiProjects/Party-soapui-project.xml (XML configuration)
  - Purpose: SoapUI test project configuration for Party service v1.27
- cuco-core/SoapUiProjects/CustomerAssignment-soapui-project.xml (XML configuration)
  - Purpose: SoapUI test project configuration for CustomerAssignment service
- cuco-core/SoapUiProjects/CustomerAccount-soapui-project.xml (XML configuration)
  - Purpose: SoapUI test project configuration for Customer Account web services
- cuco-core/SoapUiProjects/CustomerInventory-soapui-project.xml (XML configuration)
  - Purpose: SoapUI test project configuration for Customer Inventory web services
- cuco-core/src/test/resources/logback.xml (XML configuration)
  - Purpose: Logging configuration for test environment with audit logging capabilities
- cuco-core/src/test/resources/ehcache.xml (XML configuration)
  - Purpose: EhCache configuration file defining cache settings for the application
- cuco-core/src/test/resources/testApplicationContext-cuco-core.xml (XML configuration)
  - Purpose: Spring application context configuration for testing the CUCO core module
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetTariffOfferSimulationResponse.MSISDN_and_BAN.xml (XML configuration)
  - Purpose: Sample response XML for tariff offer simulation API testing
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetProductsForSubscriptionResponse_ProductCatalogDetails.xml (XML configuration)
  - Purpose: Defines response structure for retrieving product catalog details associated with a subscription
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetProductsForSubscriptionResponse.xml (XML configuration)
  - Purpose: Defines standard response structure for product subscription queries
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetSubscriptionsForPartyResponse.xml (XML configuration)
  - Purpose: Defines response structure for retrieving multiple subscriptions associated with a party
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetTariffOfferSimulationNoSimulationData.xml (XML configuration)
  - Purpose: Defines XML response structure for tariff offer simulation when no simulation data is available
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetTariffOfferSimulationResponse.MSISDN_no_BAN.xml (XML configuration)
  - Purpose: Defines XML response structure for tariff offer simulation when MSISDN exists but no BAN is present
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetSimulationRelevantChartDataListResponseDocument.MSISDN_and_BAN.xml (XML configuration)
  - Purpose: Defines XML response structure for simulation chart data when both MSISDN and BAN are present
- cuco-core/src/test/resources/at/a1ta/cuco/core/service/impl/Kums_KundeBearbeiten_response_ok.xml (XML configuration)
  - Purpose: Test XML response template for successful customer data modification in KUMS system
- cuco-core/src/test/resources/at/a1ta/cuco/core/service/impl/Kums_KundeBearbeiten_response_nok.xml (XML configuration)
  - Purpose: Test XML response template for failed customer data modification in KUMS system

## 3. Functionality
### Main Features
- EhCache distributed caching configuration for application caching management
- iBatis SQL mapping configuration for customer-related operations
- Web application deployment descriptor for internal configuration
- iBatis SQL mapping configuration for invoice-related database operations
- SoapUI test project configuration for Customer Account web services
- Defines the UI layout for a VIP search component
- iBatis SQL mapping configuration for clearing account operations
- iBatis SQL mapping configuration for image-related database operations
- Defines response structure for retrieving multiple subscriptions associated with a party
- GWT module configuration file for the MyCuCo application starter
- SoapUI test project configuration for Party service v1.27
- iBatis SQL mapping configuration for gamification messaging system
- iBatis SQL mapping configuration for turnover-related database operations
- iBatis SQL mapping configuration for reporting functionality
- iBatis SQL mapping configuration for marketing interactions with caching
- GWT module configuration file for GXT UI utilities and theme integration
- GWT module configuration file for the main application starter module
- iBatis SQL mapping configuration for customer unlock request functionality
- iBatis SQL mapping configuration for attribute management
- Maven project configuration for CUCO administration UI module
- Java web application configuration file
- iBatis SQL mapping configuration for managing application settings/configurations
- Logging configuration file that defines logging behavior and output formats using Logback framework
- iBatis SQL mapping configuration for handling unknown area codes
- iBatis SQL mapping configuration for billing cycle functionality
- Maven project configuration for main CUCO module
- Defines standard response structure for product subscription queries
- SQL mapping configuration for credit type management
- iBatis SQL mapping configuration for inventory management
- Test XML response template for successful customer data modification in KUMS system
- Spring application context configuration for testing the CUCO core module
- iBatis SQL mapping configuration for handling image size data with caching
- GWT module configuration file defining inheritance and resource dependencies
- iBatis SQL mapping configuration for phone number data management with caching
- UI definition for a dialog to edit credit types in the administration interface
- iBatis SQL mapping configuration for Visit Report functionality with SBS (Step-by-Step) features
- SQL mapping definitions for CMDB ICT Service entities
- iBatis SQL mapping configuration for CUCO logging operations
- EhCache configuration file defining cache settings for the application
- Defines the UI layout for an authority administration interface component
- Cache configuration for distributed caching using JMS
- UI definition file for user editing dialog using GWT UiBinder
- GWT module configuration file that defines the entry point and inheritance structure for the PKB application
- GWT module configuration for the CUCO application starter
- GWT module configuration file for the MyCuCo application starter module
- iBatis SQL mapping configuration for customer blocking functionality
- Google Web Toolkit module configuration for PKB application
- iBatis SQL mapping configuration for flash information management
- UI definition for a dialog to select team members in a GWT web application
- iBatis SQL mapping configuration for product hierarchy data access with caching
- Spring application context configuration file for CUCO core services
- iBatis SQL mapping configuration for location-related database operations
- iBatis SQL mapping configuration for contact person data access operations with caching support
- Defines response structure for retrieving product catalog details associated with a subscription
- SoapUI test project configuration for Customer Inventory web services
- Web application configuration file for NTLM authentication setup
- Sample response XML for tariff offer simulation API testing
- Defines XML response structure for tariff offer simulation when MSISDN exists but no BAN is present
- UI definition for a dialog to edit unknown area codes in the administration interface
- iBatis SQL mapping configuration for business offers with caching support
- Web fragment configuration file defining servlet mappings and configurations for the administration UI module
- iBatis SQL mapping configuration for quote and opportunity management
- Test XML response template for failed customer data modification in KUMS system
- iBatis SQL mapping configuration for KUMS SKZ shop operations
- Web application configuration file for external authentication setup
- UI definition for role group management dialog in the administration interface
- Main iBatis SQL mapping configuration file that sets up global settings and includes other mapping files
- Spring configuration file for CMDB DAO layer
- SQL mapping definitions for inventory product group operations
- iBatis SQL mapping configuration for charging type data access
- iBatis SQL mapping configuration for VBM products with caching configuration
- iBatis SQL mapping configuration for managing UI text/translation data
- Logging configuration for test environment with audit logging capabilities
- GWT module configuration file defining module inheritance and dependencies
- Spring application context configuration for database DAO layer
- iBatis SQL mapping configuration for user-related database operations
- GWT module configuration file defining source paths for core functionality
- UI definition for a dialog to select user roles in the administration interface
- iBatis SQL mapping configuration for billing cycle operations
- iBatis SQL mapping configuration for usage data queries with caching support
- iBatis SQL mapping configuration for user-shop assignment management
- iBatis SQL mapping configuration for Service-related database operations
- iBatis SQL mapping configuration for sales notes and tasks
- iBatis SQL mapping configuration for payable ticket operations
- SoapUI test project configuration for CustomerAssignment service
- iBatis SQL mapping configuration for user information statistics with caching
- iBatis SQL mapping configuration for Sales Information management
- Maven project configuration file for cuco-core module
- iBatis SQL mapping configuration for VIP customer history tracking
- iBatis SQL mapping configuration for CMDB
- Defines XML response structure for tariff offer simulation when no simulation data is available
- UI definition for team editing dialog interface
- iBatis SQL mapping configuration for team management
- Logging configuration for the CUCO application
- iBatis SQL mapping configuration for CCT organizational structure elements
- UI definition for service selection dialog component
- Defines XML response structure for simulation chart data when both MSISDN and BAN are present
- GWT module configuration file for the admin application starter module
- SQL mapping configuration for Links Portlet functionality
- UI definition for a dialog to edit service settings in a GWT web application
- iBatis SQL mapping configuration for standard address management
- UI definition for a dialog to edit messages in a GWT web application
- Spring configuration file for billing cycle DAO layer
- GWT module configuration file for the admin interface starter module

### Data Structures
#### configuration
Fields:
- debug
- scan
Relationships:
- contains appenders
- contains filters
#### web-app
Fields:
- version
- xmlns
Relationships:
- contains context-params
- contains servlet configurations
#### web-app
Fields:
- version
- xmlns
Relationships:
- contains context-params
- contains servlet configurations
#### ehcache
Fields:
- initialContextFactoryName
- providerURL
Relationships:
- Uses JMS for cache replication
#### web-app
Fields:
- version
- context-param
Relationships:
- References Spring application contexts
#### module
Fields:
- rename-to
- inherits
Relationships:
- Inherits from BiteUi, VisitReports, and PKB modules
#### LogEntry
Fields:
- timestamp
- log level
- message
Relationships:
- writes to filesystem
#### CacheConfiguration
Fields:
- initialContextFactoryName
- providerURL
Relationships:
- connects to ActiveMQ broker
#### ModuleStructure
Fields:
- source paths
- inherited modules
- entry point
Relationships:
- inherits from CuCoCommon
- inherits from App
#### context-param
Fields:
- param-name
- param-value
Relationships:
- References applicationContext-app.xml
#### EditUserDialog
Fields:
- lHeader
Relationships:
- extends HTMLPanel
#### AdminTextPool
Fields:
- text resources
Relationships:
- Provides localized text for the dialog
#### AdminTextPool
Fields:
- text resources
Relationships:
- Provides localized text for the dialog
#### Roles
Fields:
- role data
Relationships:
- Displayed in DataTable
#### RoleGroupDialog
Fields:
- ui:with fields
Relationships:
- Inherits from GWT Dialog
#### ServiceDialog
Fields:
- style
- table components
Relationships:
- Inherits from GWT Dialog
#### TeamsDialog
Fields:
- style
- admintextpool
Relationships:
- Inherits from GWT Dialog
#### StyleResources
Fields:
- style configurations
Relationships:
- at.a1ta.bite.ui.client.bundle
#### AdminCommonTextPool
Fields:
- message resources
Relationships:
- at.a1ta.cuco.admin.ui.common.client.bundle
#### StyleResources
Fields:
- style configurations
Relationships:
- at.a1ta.bite.ui.client.bundle
#### BillingCycle
Fields:
- cycle
- entry
Relationships:
- at.a1ta.cuco.core.shared.dto.BillingCycle
- at.a1ta.cuco.core.shared.dto.BillingCycleEntry
#### InventoryProductGroup
Fields:
- not specified in preview
Relationships:
- Product
#### Product
Fields:
- not specified in preview
Relationships:
- InventoryProductGroup
#### customerUnlockRequest
Fields:
- contextAwareCustomerUnlockRequest
Relationships:
- at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest
#### StandardAddress
Fields:
- address fields
Relationships:
- at.a1ta.cuco.core.shared.dto.StandardAddress
#### Country
Fields:
- country fields
Relationships:
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.Country
#### GamificationMessage
Fields:
- messageUid
- title
Relationships:
- at.a1ta.cuco.core.shared.dto.GamificationMessage
#### Invoice
Fields:
- Not visible in preview
Relationships:
- Likely relationships with billing cycles and users
#### BiteUser
Fields:
- Not visible in preview
Relationships:
- Maps to biteUser-result-slim resultMap
#### BillingCycle
Fields:
- Not visible in preview
Relationships:
- Contains BillingCycleEntry entities
#### BillingCycleEntry
Fields:
- Not visible in preview
Relationships:
- Belongs to BillingCycle
#### VIPHistoryEntry
Fields:
- vipHistoryId
- customerId
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.VIPHistoryEntry
#### Team
Fields:
- id
- name
- description
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.Team
#### CustomerBlock
Fields:
- id
- kundenblock_id
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.CustomerBlock
#### vbmProducts
Fields:
- Not visible in preview
Relationships:
- Cached using ehcacheProvider
#### Opportunity
Fields:
- Not visible in preview
Relationships:
- Maps to at.a1ta.cuco.cct.shared.dto.Opportunity
#### cucoLogEntry
Fields:
- kunde_id
- name
- user_id
- passw
Relationships:
- Maps to java.util.Map
#### UsageData
Fields:
- Not visible in preview
Relationships:
- Appears to be related to voice usage tracking
#### BusinessOffer
Fields:
- Not visible in preview
Relationships:
- Likely related to business offer management
#### MyOpportunity
Fields:
- Not visible in preview
Relationships:
- Related to Quote and Opportunity entities
#### Quote
Fields:
- Not visible in preview
Relationships:
- Related to MyOpportunity
#### Opportunity
Fields:
- Not visible in preview
Relationships:
- Related to Quote and MyOpportunity
#### Location
Fields:
- Not fully visible in preview
Relationships:
- Cached entity mapping
#### KumsSkzShop
Fields:
- Not fully visible in preview
Relationships:
- Maps to at.a1ta.bite.core.shared.dto.KumsSkzShop
#### Turnover
Fields:
- Not fully visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.Turnover
#### linksPortlet
Fields:
- key
- LINK_KEY
#### creditType
#### UIText
Fields:
- key
- value
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.UIText
#### Reporting
Fields:
- id
Relationships:
- Maps to at.a1ta.cuco.core.bean.Reporting
#### FlashInfo
Fields:
- not visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.FlashInfo
- Maps to at.a1ta.cuco.core.shared.dto.MyFlashInfo
#### UserInfoStatistics
Fields:
- Not visible in snippet
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.UserInfoStatistics
#### mkInteraction
Fields:
- Not visible in snippet
Relationships:
- Defined in resultMap with id='mk'
#### UserShopAssignmentLogLine
Fields:
- Not visible in snippet
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine
#### UserShopAssignment
Fields:
- Not visible in snippet
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.UserShopAssignment
#### Setting
Fields:
- key
- value
#### ImageSize
Fields:
- not visible in preview
#### PhoneNumber
Fields:
- not visible in preview
#### ChargingType
Fields:
- Inferred from at.a1ta.cuco.core.shared.dto.ChargingType
Relationships:
- Maps to database charging type table
#### UnknownAreaCode
Fields:
- Inferred from at.a1ta.cuco.core.shared.dto.UnknownAreaCode
Relationships:
- Maps to database unknown area code table
#### inventory
Fields:
- Inferred from result mapping
Relationships:
- Maps to database inventory table
#### ContactPerson
Fields:
- Not fully visible in preview
Relationships:
- Appears to have a cache relationship with EhCache provider
#### SalesInfoNote
Fields:
- Not fully visible in preview
Relationships:
- Mapped from at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote
#### Task
Fields:
- Not fully visible in preview
Relationships:
- Mapped from at.a1ta.cuco.core.shared.dto.salesinfo.Task
#### cctOrgStructureElement
Fields:
- Not fully visible in preview
Relationships:
- Mapped from at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement
#### Image
Fields:
- Not fully visible in preview
Relationships:
- Namespace scoped under 'Image'
#### ClearingAccount
Fields:
- Not fully visible in preview
Relationships:
- Namespace scoped under 'ClearingAccount'
#### Spring beans
Fields:
- Not fully visible in preview
Relationships:
- Uses Spring AOP, context, and transaction management
#### ProductHierarchy
Fields:
- Not fully visible in preview
Relationships:
- Appears to define product hierarchy relationships
#### payableticket
Fields:
- Not fully visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.PayableTicket
#### AttributeConfig
Fields:
- Not fully visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.AttributeConfig
#### Attribute
Fields:
- Not fully visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.Attribute
#### AttributeHistory
Fields:
- Not fully visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.AttributeHistory
#### Service
Fields:
- Not visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.Service
#### SalesInfoNote
Fields:
- Not visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote
#### SimpleNote
Fields:
- Not visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.salesinfo.SimpleNote
#### SBSProductNote
Fields:
- Not visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote
#### SBSNote
Fields:
- Not visible in preview
Relationships:
- Maps to at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSNote
#### CmDBICTService
Fields:
- Not fully visible in preview
Relationships:
- Cached entity with ehcache provider
#### Project Coordinates
Fields:
- groupId: at.a1ta.cuco
- artifactId: cuco
- version: 2025.03.01
Relationships:
- parent: cuco.pom
#### Project Coordinates
Fields:
- groupId: at.a1ta.cuco
- artifactId: administration.ui
- version: 2025.03.01
Relationships:
- parent: cuco.pom
#### project
Fields:
- modelVersion
- artifactId
- parent
Relationships:
- inherits from at.a1ta.cuco:cuco.pom:2025.03.01
#### soapui-project
Fields:
- name
- resourceRoot
- soapui-version
- settings
Relationships:
- contains test cases and configurations
#### soapui-project
Fields:
- name
- resourceRoot
- soapui-version
- interface
Relationships:
- binds to CustomerAssignmentPortTypeHttpBinding WSDL interface
#### CustomerAccount
Fields:
- WSDL operations and messages
Relationships:
- Binds to CustomerAccountPortType
#### CustomerInventory
Fields:
- WSDL operations and messages
Relationships:
- Binds to CustomerInventoryPortType
#### LoggingConfiguration
Fields:
- appender
- encoder
- layout
Relationships:
- Uses at.a1ta.bite.audit.core components
#### cacheConfiguration
Fields:
- maxElementsInMemory
- eternal
- timeToIdleSeconds
- timeToLiveSeconds
- overflowToDisk
- diskSpoolBufferSizeMB
- maxElementsOnDisk
#### springBeans
Fields:
- bean definitions
- aop configurations
- transaction settings
Relationships:
- bean dependencies
#### CurrentTariff
Fields:
- Code
- Name
Relationships:
- has many Services
#### Service
Fields:
- Code
- Name
Relationships:
- belongs to CurrentTariff
#### Subscription
Fields:
- Id
- CustomerAccount.AccountNumber
Relationships:
- BNAccount type relationship with CustomerAccount
#### Subscription
Fields:
- Id
- CustomerAccount.AccountNumber
Relationships:
- BNAccount type relationship with CustomerAccount
#### Subscriptions
Fields:
- Subscription.Id
- Subscription.CustomerAccount.AccountNumber
Relationships:
- Contains multiple Subscription elements
- BNAccount type relationship with CustomerAccount
#### CurrentTariff
Fields:
- Code
- Name
Relationships:
- Part of GetTariffOfferSimulationResult
#### AdditionalInformation
Fields:
- Code
- Text
Relationships:
- Part of GetTariffOfferSimulationResult
#### CurrentBaseFee
Fields:
- Gross
- Net
Relationships:
- Part of GetTariffOfferSimulationResult
#### CurrentAvgInvoiceAmount
Fields:
- Gross
- Net
Relationships:
- Part of GetTariffOfferSimulationResult
#### DataPairItem
Fields:
- SegmentDescription
- SegmentValue
Relationships:
- Multiple items in GetSimulationRelevantChartDataListResult
#### WS_KUMS_KUNDE_BEARBEITEN_Output
Fields:
- Kundennummer
- Meldung
Relationships:
- Part of SOAP response body
#### WS_KUMS_KUNDE_BEARBEITEN_ReturnCode
Fields:
- RC
- FEHLERNR
- FEHLERTEXT
Relationships:
- Part of SOAP error response body

### Key Methods/Functions
#### DuplicateMessageFilter
Description: Filters duplicate log messages, allowing only 5 repetitions
#### RollingFileAppender
Description: Handles log file rotation and management
#### contextConfigLocation
Description: Specifies Spring application context configuration files
#### contextConfigLocation
Description: Specifies Spring application context configuration files
#### cacheManagerPeerProviderFactory
Description: JMS-based cache replication configuration using ActiveMQ
#### contextConfigLocation
Description: Spring application context configuration locations
#### pkb
Description: Main PKB application module with UI components
#### module
Description: Root module configuration renamed to 'app'
#### module
Description: MyCuCo starter module configuration renamed to 'mycuco'
#### module
Description: Admin starter module configuration renamed to 'admin'
#### FILE appender
Description: Configures log file output to d:/logs/cuco/cuco.log
#### Layout encoder
Description: Defines log message format using PatternLayout
#### CacheManagerPeerProvider
Description: Configures distributed cache using ActiveMQ for transport
#### Module configuration
Description: Defines GWT module inheritance and entry point
#### AdminStarter
Description: Entry point configuration for the admin interface
#### MyCuCoStarter
Description: Entry point configuration for the MyCuCo interface
#### module
Description: Root configuration element that defines PKB module settings
#### Web App Configuration
Description: Defines servlet 3.0 configuration and context parameters
#### Context Configuration
Description: Specifies Spring application context configuration locations
#### userShopAssignmentUploadServlet
Description: Servlet handling user shop assignment uploads
#### HTMLPanel
Description: Main container for the dialog
#### Label
Description: Header label component from BITE UI library
#### UiBinder
Description: Defines the structure of the credit types editing dialog
#### StyleResources
Description: Provides styling information for the dialog components
#### UiBinder
Description: Defines the structure of the unknown areas code editing dialog
#### StyleResources
Description: Provides styling information for the dialog components
#### DataTable
Description: Displays and allows selection of roles
#### Button
Description: Save button for confirming role selection
#### UiBinder
Description: Defines layout and structure of role group management dialog
#### AdminCommonTextPool
Description: Text resources for admin interface localization
#### UiBinder
Description: Defines layout for service selection interface
#### StyleResources
Description: Style definitions for the dialog
#### UiBinder
Description: Defines layout for team editing interface
#### StyleResources
Description: Style definitions for the dialog
#### UiBinder
Description: Defines the structure and layout of the team member selection dialog
#### UiBinder
Description: Defines the structure and layout of the service editing dialog
#### UiBinder
Description: Defines the structure and layout of the message editing dialog
#### txtFilter
Description: Text input field for filtering authorities
#### table
Description: Table component for displaying authority data
#### pager
Description: Pagination component for the authority table
#### msg
Description: Message bundle for internationalization
#### GxtUtilities
Description: Configures GXT UI framework integration and theme support
#### CucoCore
Description: Defines client-side accessible source paths for shared and bean packages
#### BillingCycle
Description: Defines database mappings for billing cycle operations
#### Spring Beans Configuration
Description: Defines Spring beans and their dependencies for billing cycle data access
#### SQLMap Configuration
Description: Configures iBatis SQL mapping settings and cache behavior
#### EhCache Controller
Description: Custom cache implementation for SQL query results
#### InventoryProductGroup SQLMap
Description: Defines SQL operations for inventory product groups
#### CustomerUnlockRequest
Description: Handles database operations for customer unlock requests
#### StandardAddress
Description: Manages standard address and country data mappings
#### Gamification
Description: Handles gamification message data operations
#### invoice-cache
Description: EhCache configuration for invoice data with 3-hour flush interval and 1000 entry capacity
#### app-user-cache
Description: EhCache configuration for user data
#### biteUser-result-slim
Description: Mapping configuration for user data transformation
#### billingCycle-result
Description: Mapping configuration for billing cycle data transformation
#### VIPHistory
Description: Manages database operations for VIP customer history records
#### Team
Description: Handles database operations for team entities
#### CustomerBlock
Description: Manages database operations for customer blocking records
#### vbmProducts-cache
Description: EhCache-based caching configuration for VBM products with 1-minute flush interval
#### Customer
Description: SQL mappings for customer operations
#### cucoLogEntry-insert
Description: Parameter mapping for log entry insertion
#### voiceUsage-cache
Description: Ehcache configuration for voice usage data with 3-hour flush interval
#### businessoffer-cache
Description: Ehcache configuration for business offers with 3-hour flush interval
#### MyQuote
Description: SQL mapping namespace for quote operations
#### location-cache
Description: 3-hour cache configuration for location data with 1000 entry limit
#### location-res
Description: Maps location query results to object properties
#### kumsSkzShop-cache
Description: 1-hour cache configuration for shop data
#### kumsSkzShop
Description: Type alias for KumsSkzShop DTO
#### turnover-cache
Description: Serializable cache configuration for turnover data
#### turnover
Description: Type alias for Turnover DTO
#### settings
Description: Global iBatis settings including namespace and cache configuration
#### ehcacheProvider
Description: Cache controller implementation for EhCache integration
#### LinksPortlet
Description: Contains SQL mappings for links portlet operations
#### CreditType
Description: Contains SQL mappings for credit type operations
#### credittype-cache
Description: EhCache-based caching configuration for credit types
#### TextsEditor
Description: Handles database operations for UI text management
#### Reporting
Description: Manages database operations for reporting features
#### FlashInfo
Description: Handles database operations for flash information and notifications
#### UserInfoStats
Description: Contains SQL mappings for user statistics operations
#### stats-cache
Description: EhCache configuration for caching user statistics with 1-minute refresh interval
#### MKInteraction
Description: Contains SQL mappings for marketing interaction operations
#### mkInteraction-cache
Description: EhCache configuration for caching marketing interactions with 3-hour refresh interval
#### ImportUserShopAssignment
Description: Contains SQL mappings for user-shop assignment operations
#### cucoSettings
Description: Contains SQL mappings for settings operations
#### Setting
Description: Maps to at.a1ta.bite.core.shared.dto.Setting class
#### ImageSize
Description: Contains SQL mappings for image size operations
#### imagesize-cache
Description: Ehcache configuration for image size data caching
#### PhoneNumber
Description: Contains SQL mappings for phone number operations
#### phonenumber-cache
Description: Ehcache configuration for phone number data caching
#### ChargingType
Description: Defines SQL mappings for charging type operations
#### chargingtype-cache
Description: EhCache configuration for charging type data caching
#### UnknownAreaCode
Description: Defines SQL mappings for unknown area code operations
#### unknownareacode-cache
Description: EhCache configuration for unknown area code caching
#### Inventory
Description: Defines SQL mappings for inventory operations
#### inventory-cache
Description: EhCache configuration for inventory data with 3-hour flush interval
#### contact-cache
Description: EhCache-based caching configuration for contact person data with 3-hour flush interval
#### MyNotes
Description: SQL mapping definitions for sales info notes and tasks
#### CCTOrgStructureElement
Description: SQL mapping definitions for CCT organizational structure operations
#### image-cache
Description: EhCache configuration for image data caching with 3-hour flush interval
#### clearingAccount-cache
Description: EhCache configuration for clearing account data with 3-hour flush interval
#### Spring beans configuration
Description: Database access layer configuration using Spring framework
#### productHierarchy-cache
Description: EhCache configuration for product hierarchy with 2 hour flush interval
#### PayableTicket
Description: SQL mappings for payable ticket operations
#### Attribute
Description: SQL mappings for attribute operations
#### Service namespace
Description: Contains SQL mappings for service entity operations
#### service-cache
Description: EhCache-based caching configuration for service data
#### SalesInfo namespace
Description: Contains SQL mappings for sales information and notes
#### VisitReport namespace
Description: Contains SQL mappings for visit report and SBS product notes
#### Spring Beans Configuration
Description: Defines Spring beans and their dependencies for CMDB data access
#### SQLMap Configuration
Description: Global settings for iBatis SQL mapping including caching and lazy loading
#### EhCache Provider
Description: Custom cache controller implementation for iBatis
#### CmDBICTService Cache
Description: EhCache configuration for ICT service data with 1-hour flush interval
#### Spring Beans Configuration
Description: Defines Spring beans and their dependencies for the CUCO core service layer
#### Maven Project
Description: Defines project metadata and build configuration for CUCO module
#### Maven Project
Description: Defines project metadata and build configuration for administration UI component
#### cuco-core
Description: Core module of the CUCO project with parent cuco.pom
#### Party
Description: Test configurations for Party web service version 1.27
#### CustomerAssignment
Description: Test configurations for CustomerAssignment web service with WSDL binding
#### CustomerAccountPortTypeHttpBinding
Description: SOAP web service interface for customer account operations
#### CustomerInventoryPortTypeHttpBinding
Description: SOAP web service interface for customer inventory operations
#### AUDITLOG
Description: Custom appender for audit logging with file rolling capability
#### AuditEventLayout
Description: Custom layout for formatting audit log entries
#### diskStore
Description: Defines temporary storage location for cache overflow
#### defaultCache
Description: Default cache configuration with memory and disk storage parameters
#### Spring Context
Description: Defines Spring beans and their configurations for testing
#### TariffOffer
Description: Contains current tariff and service information
#### getProductsForSubscriptionResponse
Description: Root element containing subscription and product catalog information
#### getProductsForSubscriptionResponse
Description: Standard response format for subscription product queries
#### getSubscriptionsForPartyResponse
Description: Contains list of subscriptions for a given party
#### GetTariffOfferSimulationResponse
Description: Contains response data for tariff simulation request
#### CurrentTariff
Description: Holds current tariff information including code and name
#### GetTariffOfferSimulationResponse
Description: Contains empty response structure when BAN is missing
#### GetSimulationRelevantChartDataListResponse
Description: Contains chart data pairs for tariff simulation visualization
#### DataPairItem
Description: Represents individual chart data points with description and value
#### WS_KUMS_KUNDE_BEARBEITEN
Description: Container for successful customer modification response
#### WS_KUMS_KUNDE_BEARBEITEN_Output
Description: Success response container with customer number and message
#### WS_KUMS_KUNDE_BEARBEITEN
Description: Container for failed customer modification response
#### WS_KUMS_KUNDE_BEARBEITEN_ReturnCode
Description: Error response container with error details

## 4. Dependencies
- at.a1ta.bite.ui.client.bundle.StyleResources
- at.a1ta.cuco.core.shared.dto.Turnover
- java.util.Map
- at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote
- ehcache.xsd
- Java EE 3.0
- at.a1ta.cuco.core.shared.dto.Team
- http://eai.a1telekom.at/CustomerInventory/wsdl
- Google Web Toolkit 2.5.1
- at.a1ta.bite.ui.client.widget
- com.google.gwt.logging.Logging
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSNote
- at.a1ta.cuco.core.shared.dto.salesinfo.SimpleNote
- at.a1ta.bite.sqlmap.engine.chache.ehcache.EhCacheController
- at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine
- com.allen_sauer.gwt.dnd.gwt-dnd
- com.google.gwt.user.client.ui
- Spring Context
- at.a1ta.cuco.core.shared.dto.salesinfo.Task
- at.a1ta.cuco.mycuco.MyCuCo
- at.a1ta.cuco.ui.visitreports.VisitReports
- at.a1ta.cuco:cuco.pom:2025.03.01
- ch.qos.logback.core
- at.a1ta.cuco.core.shared.dto.FlashInfo
- ibatis.apache.org SQL Map 2.0
- spring-beans
- at.a1ta.cuco.core.shared.dto.MyFlashInfo
- spring-context.xsd
- at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote
- at.a1ta.bite.ui.BiteUi
- Spring Framework core
- ch.qos.logback
- at.a1ta.cuco.core.shared.dto.access package
- cuco.pom (parent)
- at.a1ta.framework.gxt.GxtUtilities
- at.a1ta.bite.core.shared.dto.KumsSkzShop
- ibatis.apache.org SQL Map DTD 2.0
- spring-context
- at.a1ta.cuco.core.shared.dto.Service
- at.a1ta.cuco.ui.common.CuCoCommon
- at.a1ta.bite.core.shared.dto.Setting
- at.a1ta.bite.audit.core
- at.a1ta.cuco.core.shared.dto.InventoryProductGroup
- at.a1ta.framework.ui.Framework
- at.a1ta.cuco.core.shared.dto.ChargingType
- XML Schema Instance (xsi) namespace
- http://bit.mobilkom.at/TariffGuide/ namespace
- at.a1ta.bite[incomplete]
- at.a1ta.cuco.core.shared.dto.BillingCycleEntry
- Spring AOP
- spring-beans.xsd
- logback-core
- at.a1ta.cuco.cct.shared.dto.Opportunity
- com.extjs.gxt.ui.GXT
- at.a1ta.cuco.core.bean.Reporting
- at.a1ta.bite.core.BiteCore
- iBatis
- at.a1ta.cuco.ui.pkb.PKB
- http://eai.a1telekom.at/CustomerAccount/wsdl
- ehcache
- http://eai.a1telekom.at/CustomerInventory namespace
- web-fragment_3_0.xsd
- SOAP-ENV namespace
- ehcacheProvider
- at.a1ta.cuco.core.shared.dto.AttributeConfig
- ch.qos.logback.classic
- ActiveMQ
- ActiveMQ message broker
- at.a1ta.pkb.ui.Pkb
- net.sf.ehcache.distribution.jms
- ch.qos.logback.classic.PatternLayout
- at.a1ta.cuco.admin.ui.common.CuCoAdminCommon
- at.a1ta.cuco.core.shared.dto.UserInfoStatistics
- at.a1ta.cuco.core.shared.dto.VIPHistoryEntry
- SoapUI 3.6
- at.a1ta.cuco.core.shared.dto.LinksPortlet
- at.a1ta.bite.core.shared.dto.BiteUser
- spring-aop.xsd
- WSKUMS_S_WSToKUMSKundeBearbeiten_WSKUMS_S_WSToKUMSKundeBearbeiten namespace
- ibatis-sqlmap
- iBatis SQL Map 2.0
- ibatis.apache.org SQL Map 2.0 DTD
- SoapUI 3.6.1
- TariffGuide namespace
- spring-tx.xsd
- com.google.gwt.user.cellview.client
- ch.qos.logback.core.FileAppender
- at.a1ta.cuco.ui.admin.Admin
- ch.qos.logback.core.encoder.LayoutWrappingEncoder
- CustomerAssignmentPortTypeHttpBinding WSDL
- at.a1ta.cuco.core.shared.dto package
- com.google.gwt.uibinder
- at.a1ta.cuco.core.shared.dto.BillingCycle
- Java EE 3.0 specification
- at.a1ta.bite.core.server.util.EhCacheReplicationActiveMQInitialContextFactory
- applicationContext-app.xml
- at.a1ta.cuco.ui.pkb.PKBSt
- at.a1ta.cuco.core.shared.dto.UIText
- at.a1ta.cuco.cct.shared.dto.Quote
- net.sf.ehcache
- at.a1ta.cuco.ui.app.App
- at.a1ta.cuco.core.shared.dto.CreditType
- at.a1ta.cuco.core.shared.dto.CustomerBlock
- at.a1ta.cuco.core.shared.dto.PayableTicket
- at.a1ta.cuco.core.shared.dto.MyOpportunity
- spring-aop
- at.a1ta.cuco.ui.common.client.ui.table
- at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement
- at.a1ta.cuco.core.shared.dto.Attribute
- at.a1ta.cuco.core.shared.dto.AttributeHistory
- com.extjs.gxt.themes.Themes
- at.a1ta.cuco.core.shared.dto.UserShopAssignment
- Spring Transaction Management
- at.a1ta.cuco.core.shared.dto.UnknownAreaCode
- spring-tx
- ibatis.apache.org SQL Map Config 2.0 DTD
- at.a1ta.cuco.core.shared.dto.Product
- Spring Framework

## 5. Business Rules
- Duplicate messages are limited to 5 repetitions
- Application must load Spring contexts from specified classpath locations
- Application must load Spring contexts from specified classpath locations
- Cache replication must use ActiveMQ as message broker
- Application must load Spring contexts from specified classpath locations
- Module must include logging and required UI component inheritances
- Module must be renamed to 'app' for deployment
- Module must be renamed to 'mycuco' for deployment
- Module must be renamed to 'admin' for deployment
- Debug mode and automatic configuration scanning enabled
- Uses custom ActiveMQ initial context factory for cache replication
- Module must inherit logging and CUCO UI components
- Module must be renamed to 'admin' in compiled output
- Module must be renamed to 'mycuco' in compiled output
- Module must inherit logging functionality
- Application must use Java EE 3.0 web specifications
- Servlet configuration must follow Java EE web fragment specification 3.0
- Module must inherit required GWT and custom modules
- Dialog must provide username input functionality
- User must be able to select roles from the table
- Changes must be saved explicitly via Save button
- Role group management interface components
- Service selection interface components
- Team management interface components
- Only shared and bean packages are exposed to GWT compilation
- Billing cycle data must conform to defined DTO structures
- Statement namespaces must be enabled
- Lazy loading is disabled
- Maps customer unlock request data between database and DTO objects
- Implements caching for address data
- Defines minimal result mapping for gamification messages
- Invoice data is cached for 3 hours
- Cache is read-only and non-serializable
- Uses slim result mapping for optimized user data retrieval
- Billing cycles contain multiple entries
- Tracks historical VIP status changes for customers
- Manages team information and metadata
- Handles customer blocking/restriction functionality
- Cache invalidation occurs every minute
- Cache limited to 1000 entries
- Uses EhCache for caching customer data
- Log entries require customer ID, name, user ID, and password fields
- Cache invalidation every 3 hours
- Cache limited to 1000 entries
- Cache invalidation every 3 hours
- Type aliases defined for domain objects
- Location data is cached for 3 hours
- Cache is read-only and non-serializable
- Shop data is cached for 1 hour
- Cache is read-only
- Turnover cache is serializable and not read-only
- Statement namespaces must be enabled
- Cache models are enabled globally
- Lazy loading is disabled globally
- Links must have a unique key identifier
- Credit type data is cached and read-only
- Text entries are mapped using key-value pairs
- Reporting data is mapped to specific bean structure
- Supports multiple flash info types including role-based information
- Statistics cache refreshes every minute
- Cache refreshes every 3 hours
- Cache limited to 1000 entries
- Manages relationships between users and shops
- Settings are stored as key-value pairs
- Cache expires every 3 hours
- Cache limited to 1000 entries
- Cache expires every 3 hours
- Cache limited to 1000 entries
- Read-only caching enabled for charging type data
- Read-only caching enabled for unknown area code data
- Cache refreshes every 3 hours
- Cache limited to 1000 entries
- Contact person data is cached for 3 hours before refresh
- Cache is read-only and limited to 1000 entries
- Uses ehcache provider for caching
- Supports insertion of CCT organizational structure elements
- Image cache is read-only and non-serializable
- Cache expires every 3 hours
- Clearing account cache is writable and serializable
- Cache expires every 3 hours
- Database access layer configuration and transaction management
- Cache invalidation every 2 hours
- Read-only cache access
- Payable ticket result mapping configuration
- Attribute data mapping configurations
- Read-only caching implemented for service data
- Handles sales information note management
- Manages visit report data with SBS product notes
- Statement namespaces must be enabled
- Cache models are enabled
- Lazy loading is disabled
- Cache refreshes every hour
- Cache is read-only
- Spring AOP and transaction management configuration
- Project versioning follows date-based scheme
- UI module must maintain version consistency with parent POM
- Must follow Maven project structure standards
- Must conform to SoapUI 3.6.1 project structure
- Must implement WSDL interface according to namespace http://xmlns.example.com/1299666729563
- Defines SOAP service endpoints and operations for customer account management
- Defines SOAP service endpoints and operations for customer inventory management
- Implements audit logging with custom formatting and file rolling
- Cache entries expire after 120 seconds of idle time
- Maximum 10000 elements stored in memory
- Test context configuration for dependency injection
- Tariff information must include both code and name
- Services are listed as separate entities under CurrentServices
- Response must include subscription ID and associated business account details
- Response must contain subscription identifier and business account information
- Response must include all subscriptions associated with the queried party
- Response must include current tariff details even when no simulation is possible
- All monetary values default to 0 when BAN is missing
- Chart data must include segment descriptions and corresponding numeric values
- Successful customer modification must return customer number and confirmation message
- Failed customer modification must return error code, error number and error text
- Error code 8 indicates customer number not found condition


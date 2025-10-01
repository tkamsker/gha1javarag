# cuco-core - Database Layer Requirements

## 1. Overview

Brief purpose within the application for the database layer.

## 2. Components

### Component Type: dao

- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetTariffOfferSimulationResponse.MSISDN_and_BAN.xml (xml)
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetProductsForSubscriptionResponse_ProductCatalogDetails.xml (xml) domain:product
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetProductsForSubscriptionResponse.xml (xml) domain:product
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetSubscriptionsForPartyResponse.xml (xml)
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetTariffOfferSimulationNoSimulationData.xml (xml)
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetTariffOfferSimulationResponse.MSISDN_no_BAN.xml (xml)
- cuco-core/src/test/resources/at/a1ta/cuco/core/dao/esb/GetSimulationRelevantChartDataListResponseDocument.MSISDN_and_BAN.xml (xml)
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/billingcycle/sqlmap-billingCycle.xml (xml) [db] domain:billing
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/billingcycle/applicationContext-cuco-dao-bc.xml (xml) [db] domain:billing
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/billingcycle/sqlmap-config-bc.xml (xml) [db] domain:billing
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-inventoryProductGroup.xml (xml) [db] domain:product
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customerUnlockRequest.xml (xml) [db] domain:customer
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-standardAddress.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-gamification.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-invoice.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-user.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-billingCycle.xml (xml) [db] domain:billing
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-vipHistory.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-team.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customerBlock.xml (xml) [db] domain:customer
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-vbmProducts.xml (xml) [db] domain:product
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customer.xml (xml) [db] domain:customer
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-cucoLogs.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-usageData.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-businessOffers.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-myquote.xml (xml) [db] domain:quote
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-location.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-kumsskzshop.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-turnover.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-config.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-linksPortlet.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-credittype.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-textseditor.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-reporting.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-flashInfo.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-userInfoStatistics.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-mkinteraction.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-userShopAssignments.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-cucoSettings.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-imageSize.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-phoneNumber.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-chargingtype.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-unknownareacode.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-inventory.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-contactPerson.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-mynotes.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-cCTOrgStructureElement.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-image.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-clearingAccount.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/applicationContext-cuco-dao-db.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-productHierarchy.xml (xml) [db] domain:product
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-payableticket.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-attribute.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-salesInfo.xml (xml) [db] domain:sales
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/visitreport/sqlmap-visitreport.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/cmdb/applicationContext-cuco-dao-cmdb.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/cmdb/sqlmap-config-cmdb.xml (xml) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/billingcycle/DefaultBillingCycleDao.java (java) domain:billing
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/billingcycle/BillingCycleDao.java (java) domain:billing
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/EsbPartyDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/CustomerAssignmentDaoImpl.java (java) domain:customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/MobilPointsDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/KUMSCommonDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/CustomerAssignmentDao.java (java) domain:customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/PartnerCenterLandingPageDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianCeeQueryOrderDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BusinessHardwareReplacementDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/OracleArrayTypeHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/ListStringTypeHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/YNNullableBooleanTypeHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/YNBooleanTypeHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/IdxStatusDBMappingHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/BooleanTypeHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/VIPStatusHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/BrianCeeQueryOrderStub.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/PhoneNumberParser.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/cusco/CusCoResponse.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/cusco/CusCoDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyQueryHelper.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyQuery.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CustomerUnlockRequestDao.java (java) domain:customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/InventoryDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SingleTurnaroundDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ChargingTypeDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ClearingAccountDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyToDoNotesDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UnknownAreaCodeDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CreditTypeDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/PartyDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UITextsEditorDAO.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ReportingDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MKInteractionDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyQuoteDao.java (java) domain:quote
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/StandardAddressDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/InventoryProductGroupDao.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UserShopAssignmentDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ImageSizeDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ProductHierarchyDao.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CucoLogsDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/LocationDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/InvoiceDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/PhoneNumberDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/LinksPortletDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SalesInfoDao.java (java) domain:sales
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/FlashInfoDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/AttributeDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CustomerBlockDao.java (java) domain:customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ContactPersonDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ImageDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/PayableTicketDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/GamificationLocalDAO.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/VbmProductsDao.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/TurnoverDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyNotesDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CCTOrgStructureElementDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UserInfoStatisticsDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/TeamDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/VIPHistoryDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/UsageDataDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CategoryDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SettingsEditorDAO.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/SegmentDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ClearingAccountDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/TeamDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/StandardAddressDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ProductHierarchyDaoImpl.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/PartyDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CategoryDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MyQuoteDaoImpl.java (java) domain:quote
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ImageDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MKInteractionDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/PayableTicketDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MyToDoNotesDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/InventoryDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UsageDataDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/PhoneNumberDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/InventoryProductGroupDaoImpl.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CreditTypeDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/TurnoverDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/LocationDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/InvoiceDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SegmentDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ContactPersonDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CCTOrgStructureElementDaoImpl.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ReportingDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UserInfoStatisticsDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ChargingTypeDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CustomerBlockDaoImpl.java (java) domain:customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/FlashInfoDaoImpl.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SettingsEditorDAOImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SalesInfoDaoImpl.java (java) domain:sales
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ImageSizeDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/GamificationLocalDAOImpl.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UITextsEditorDAOImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/LinksPortletDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UnknownAreaCodeDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/SingleTurnaroundDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/VbmProductsDaoImpl.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/MyNotesDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CucoLogsDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/AttributeDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CustomerUnlockRequestDaoImpl.java (java) domain:customer
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/UserShopAssignmentDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/VIPHistoryDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/SetupTypeSetTypeHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/VisitReportDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/ToDoGroupStatusHandler.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/visitreport/VisitReportDao.java (java)

### Component Type: dto

- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AttributeConfig.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/QuoteClearanceConfigurationHolder.java (java) domain:quote
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductOverviewConfigurations.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSProductNoteConfig.java (java) domain:product

### Component Type: repository

- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianCeeQueryOrderDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/MobilPointsDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BrianDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/BusinessHardwareReplacementDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/EsbPartyDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/KUMSCommonDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/esb/PartnerCenterLandingPageDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/cusco/impl/HttpPostCusCoDao.java (java) [db]
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyRepository.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyRepositoryWithPhoneNumbers.java (java)

### Component Type: service_layer

- cuco-core/src/test/resources/at/a1ta/cuco/core/service/impl/Kums_KundeBearbeiten_response_ok.xml (xml)
- cuco-core/src/test/resources/at/a1ta/cuco/core/service/impl/Kums_KundeBearbeiten_response_nok.xml (xml)
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-service.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/dao/cmdb/sqlmap-cmDBICTService.xml (xml) [db]
- cuco-core/src/main/resources/at/a1ta/cuco/core/service/applicationContext-cuco-service.xml (xml)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/ServiceDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/CmDBICTServiceDao.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/CmDBICTServiceDaoImpl.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/impl/ServiceDaoImpl.java (java)

### Component Type: unknown

- cuco-core/pom.xml (xml) [db]
- cuco-core/SoapUiProjects/Party-soapui-project.xml (xml) [db]
- cuco-core/SoapUiProjects/CustomerAssignment-soapui-project.xml (xml) [db] domain:customer
- cuco-core/SoapUiProjects/CustomerAccount-soapui-project.xml (xml) domain:customer
- cuco-core/SoapUiProjects/CustomerInventory-soapui-project.xml (xml) domain:customer
- cuco-core/src/test/resources/logback.xml (xml)
- cuco-core/src/test/resources/ehcache.xml (xml)
- cuco-core/src/test/resources/testApplicationContext-cuco-core.xml (xml)
- cuco-core/src/main/resources/esbstub.properties (properties)
- cuco-core/src/main/resources/log4jdbc.properties (properties) [db]
- cuco-core/src/main/resources/esbstub-t360.properties (properties)
- cuco-core/src/main/resources/at/a1ta/cuco/core/CucoCore.gwt.xml (xml)
- cuco-core/src/main/java/at/a1ta/cuco/core/configuration/MetricsConfiguration.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/PartyModel.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/DualSegment.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/PartyModelFactory.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/AddressLinkData.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/productdetail/ProductDetail.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/seg/MultiPartyMatrixData.java (java)
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/seg/MultiPartyProductGroup.java (java) domain:product
- cuco-core/src/main/java/at/a1ta/cuco/core/shared/model/contactperson/ContactPersonComparator.java (java)


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** mybatis, spring_framework, jpa
- **Design Patterns (top):** repository
- **Inputs/Outputs:** API exposure 0, API consumers 0, DB interactions 69.
- **Key Methods/Functions:** [To be derived in advanced analysis]

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]

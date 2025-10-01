# cuco-cct-core - Backend Layer Requirements

## 1. Overview

Brief purpose within the application for the backend layer.

## 2. Components

### Component Type: dto

- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/MobileSubscriptionCategory.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/FixedLineTelephoneSet.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/MobileSubscription.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/testdtos/FixedLineTelephoneSetConfiguration.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/TariffSocMappings.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/CctAttributeList.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Totals.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/ProductInstance.java (java) domain:product
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/ApproverUserInfo.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/POVHistory.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/POV.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/CctAttribute.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Quote.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Copyable.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/QuoteForFlash.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Opportunity.java (java) domain:opportunity
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/SalesInformation.java (java) domain:sales
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Priceable.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/CCTClearanceRule.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Role.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/SaveInfo.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/QuoteFlashInfo.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/MobileSubscriptionBase.java (java)

### Component Type: service_layer

- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/XsltTest.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/QuoteServiceImplTest.java (java) domain:quote
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/IQuoteDaoTest.java (java) domain:quote
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/DefaultConfigParserTest.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/ICuscoServiceImplTest.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/IOpportunityServiceImplTest.java (java) domain:opportunity
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/IQuoteServiceImplTest.java (java) domain:quote
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/service/impl/ICuscoCustomerContactServiceImplTest.java (java) domain:customer
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/QuoteFlashInfoService.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/QuoteClearanceService.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/QuoteService.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/OpportunityService.java (java) domain:opportunity
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/OpportunityServiceImpl.java (java) domain:opportunity
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/QuoteClearanceServiceImpl.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/QuoteFlashInfoServiceImpl.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/service/impl/QuoteServiceImpl.java (java) domain:quote

### Component Type: unknown

- cuco-cct-core/src/test/resources/configuration.properties (properties) [db]
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/util/CCTClearanceXSLTTester.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/util/ReflectionUtilTest.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/util/ConfigDataGenerator.java (java)
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1cml/v2/shared/A1CMLV2DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1cml/v2/shared/A1CMLV2ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bfw1/v1/shared/BFWV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bfw1/v1/shared/BFWV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v12/shared/ETGTV12ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v12/shared/ETGTV12DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v11/shared/ETGTV11DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v11/shared/ETGTV11ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v10/shared/ETGTV10ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/etgt/v10/shared/ETGTV10DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/marketplace/v1/shared/MarketplaceProductGenerator.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/marketplace/v1/shared/MarketplaceV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/marketplace/v1/shared/MarketplaceV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v6/shared/BpbV6DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v6/shared/BpbV6ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v1/shared/BpbV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v1/shared/BpbV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v7/shared/BpbV7ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bpb/v7/shared/BpbV7DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/daas/v1/shared/DaaSV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/daas/v1/shared/DaaSV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v1/shared/A1bnV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v1/shared/A1BNV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v8/shared/A1BNV8DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v8/shared/A1BNV8ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v9/shared/A1BNV9DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v9/shared/A1BNV9ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v2/shared/A1BNV2DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v2/shared/A1bnV2ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v11/shared/A1BNV11DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v11/shared/A1BNV11ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v10/shared/A1BNV10ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bn/v10/shared/A1BNV10DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v6/shared/A1BIV6DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v6/shared/A1BIV6ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v5/shared/A1BIV5DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v5/shared/A1BIV5ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v4/shared/A1BIV4ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v4/shared/A1BIV4DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v3/shared/A1BIV3DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bi/v3/shared/A1BIV3ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v5/shared/PSHCV5ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v5/shared/PSHCV5DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v4/shared/PSHCV4ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/pshc/v4/shared/PSHCV4DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v1/shared/FibV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v1/shared/FibV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v7/shared/FibV7DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/fib/v7/shared/FibV7ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v1/shared/A1PSV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v1/shared/A1PSV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v2/shared/A1PSV2DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1ps/v2/shared/A1PSV2ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v1/shared/BizkoV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v1/shared/BizkoV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v9/shared/BizkoV9DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/bizko/v9/shared/BizkoV9ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1voip/v1/shared/A1VOIPV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1voip/v1/shared/A1VOIPV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bip/v1/shared/A1BIPV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1bip/v1/shared/A1BIPV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1tvres/v1/shared/A1TVRESV1DefaultConfigurationTest.java (java) domain:product
- cuco-cct-core/src/test/java/at/a1ta/cuco/cct/productoffering/a1tvres/v1/shared/A1TVRESV1ConfigurationSmokeTest.java (java) domain:product
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/XMLUtil.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/ReflectionUtil.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/JaxbDateAdapter.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/util/NonMappableCharacterReplacer.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/Pair.java (java)


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** spring_framework
- **Design Patterns (top):** service_layer
- **Inputs/Outputs:** API exposure 0, API consumers 0, DB interactions 1.
- **Key Methods/Functions:** [To be derived in advanced analysis]

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]

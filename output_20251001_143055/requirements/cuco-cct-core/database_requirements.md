# cuco-cct-core - Database Layer Requirements

## 1. Overview

Brief purpose within the application for the database layer.

## 2. Components

### Component Type: dao

- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/applicationContext-cuco-cct-dao-db.xml (xml) [db]
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-user.xml (xml) [db]
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-productoffering.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-config.xml (xml) [db]
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-opportunity.xml (xml) [db] domain:opportunity
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-POVConfiguration.xml (xml) [db]
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-POVHistory.xml (xml) [db]
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-quoteClearance.xml (xml) [db] domain:quote
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-quote.xml (xml) [db] domain:quote
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-quoteFlashInfo.xml (xml) [db] domain:quote
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-POV.xml (xml) [db]
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/dao/db/sqlmap-salesstage.xml (xml) [db] domain:sales
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/QuoteDao.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/SalesstageDao.java (java) domain:sales
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/POVDao.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/ProductOfferingDao.java (java) domain:product
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/QuoteClearanceDao.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/QuoteFlashInfoDao.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/POVConfigurationDao.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/OpportunityDao.java (java) domain:opportunity
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/ProductOfferingTypeHandler.java (java) [db] domain:product
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/ProductOfferingDaoImpl.java (java) domain:product
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/POVConfigurationDaoImpl.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/SalesstageDaoImpl.java (java) domain:sales
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/OpportunityDaoImpl.java (java) domain:opportunity
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/QuoteDaoImpl.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/POVDaoImpl.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/QuoteClearanceDaoImpl.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/QuoteFlashInfoDaoImpl.java (java) domain:quote
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/dao/db/XMLTypeHandlerCallback.java (java) [db]

### Component Type: dto

- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/RuntimeConfigurable.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/Configurable.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/dto/POVConfiguration.java (java)

### Component Type: service_layer

- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/document.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/documentWithApprover.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/documentEmptySample.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/A1BNV1DefaultConfiguration.xml (xml) [db]
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/bizko-v1-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/pshc-v1-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/bpb-v1-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/a1bn-v2-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/a1cml-v1-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/etgt-v10-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/a1bn-v1-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/expected/fib-v1-expected.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/src/a1bn-v1-test.xml (xml) [db]
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/src/bizko-v1-test.xml (xml) [db]
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/src/fib-v1-test.xml (xml) [db]
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/src/a1bn-v2-test.xml (xml) [db]
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/src/bpb-v1-test.xml (xml) [db]
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/service/impl/src/etgt-v10-test.xml (xml) [db]

### Component Type: unknown

- cuco-cct-core/pom.xml (xml) [db]
- cuco-cct-core/src/test/resources/logback-test.xml (xml)
- cuco-cct-core/src/test/resources/testApplicationContext-cuco-cct-core.xml (xml)
- cuco-cct-core/src/test/resources/ehcache.xml (xml)
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bpbv1-sample-quote-full-adsl.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/etgtv10-sample-quote-full.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bizkov1-sample-quote-full-transfer.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/fibv1-sample-quote-full-transfer.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/a1bnv1-sample-quote-minimal.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bpbv1-sample-quote-full-sdsl.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/a1bnv1-sample-quote-full.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bizkov1-sample-quote-full-isdn.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bpbv1-sample-quote-minimal.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bpbv1-sample-quote-full-transfer.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/etgtv10-sample-quote-minimal.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bizkov1-sample-quote-minimal.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/fibv1-sample-quote-full.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/fibv1-sample-quote-minimal.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/at/a1ta/cuco/cct/productoffering/bizkov1-sample-quote-full-pots.xml (xml) [db] domain:product
- cuco-cct-core/src/test/resources/sampleFiles/a1bn-pdf-generation.xml (xml)
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/CctCore.gwt.xml (xml)
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/applicationContext-cuco-cct-core.xml (xml)
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bfw/v1/server/BFWV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1cml/v1/server/A1CMLV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1cml/v2/server/A1CMLV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/etgt/v12/server/ETGTV12DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/etgt/v11/server/ETGTV11DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/etgt/v10/server/ETGTV10DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/marketplace/v1/server/MARKETPLACEV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v6/server/BPBV6DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v1/server/BPBV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v7/server/BPBV7DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v2/server/BPBV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v5/server/BPBV5DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v4/server/BPBV4DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bpb/v3/server/BPBV3DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/daas/v1/server/DAASV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v6/server/A1BNV6DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v1/server/A1BNV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v8/server/A1BNV8DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v9/server/A1BNV9DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v7/server/A1BNV7DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v2/server/A1BNV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v5/server/A1BNV5DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v4/server/A1BNV4DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v3/server/A1BNV3DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v11/server/A1BNV11DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bn/v10/server/A1BNV10DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v6/server/A1BIV6DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v1/server/A1BIV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v8/server/A1BIV8DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v7/server/A1BIV7DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v2/server/A1BIV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v5/server/A1BIV5DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v4/server/A1BIV4DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bi/v3/server/A1BIV3DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/pshc/v1/server/PSHCV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/pshc/v2/server/PSHCV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/pshc/v5/server/PSHCV5DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/pshc/v4/server/PSHCV4DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/pshc/v3/server/PSHCV3DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v6/server/FIBV6DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v1/server/FIBV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v7/server/FIBV7DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v2/server/FIBV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v5/server/FIBV5DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v4/server/FIBV4DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/fib/v3/server/FIBV3DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1ps/v1/server/A1PSV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1ps/v2/server/A1PSV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v6/server/BIZKOV6DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v1/server/BIZKOV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v8/server/BIZKOV8DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v9/server/BIZKOV9DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v7/server/BIZKOV7DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v2/server/BIZKOV2DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v5/server/BIZKOV5DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v4/server/BIZKOV4DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/bizko/v3/server/BIZKOV3DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/ccs/v1/server/CCSV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1voip/v1/server/A1VOIPV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1bip/v1/server/A1BIPV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/resources/at/a1ta/cuco/cct/productoffering/a1tvres/v1/server/A1TVRESV1DefaultConfiguration.xml (xml) [db] domain:product
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/shared/ConfigurableListSelectorRuntimeConfigurationHelper.java (java)
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/configurationtool/CacheMBean.java (java) [db]
- cuco-cct-core/src/main/java/at/a1ta/cuco/cct/configurationtool/CacheManager.java (java) [db]


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** mybatis, spring_framework
- **Design Patterns (top):** n/a
- **Inputs/Outputs:** API exposure 0, API consumers 0, DB interactions 100.
- **Key Methods/Functions:** [To be derived in advanced analysis]

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]

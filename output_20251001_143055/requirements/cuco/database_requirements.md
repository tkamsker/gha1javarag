# cuco - Database Layer Requirements

## 1. Overview

Brief purpose within the application for the database layer.

## 2. Components

### Component Type: database_script

- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/100_test_deletes_kunde.sql (sql)
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/037_test_deletes_konto.sql (sql)
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/040_test_deletes_rufnummer.sql (sql)
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/050_test_deletes_ansprechpartner.sql (sql)
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/035_test_deletes_bestand.sql (sql)
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/5_test_inserts_bestand.sql (sql) [db]
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/2_test_inserts_ansprechpartner.sql (sql) [db]
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/1_test_inserts_kunde.sql (sql) [db]
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/4_test_inserts_konto.sql (sql) [db]
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/3_test_inserts_rufnummer.sql (sql) [db]

### Component Type: unknown

- cuco/pom.xml (xml) [db]
- cuco/src/main/filters/configuration.prod11-ext.properties (properties) [db]
- cuco/src/main/filters/logback.xml (xml) [db]
- cuco/src/main/filters/configuration.prod11.properties (properties) [db]
- cuco/src/main/filters/configuration.properties (properties) [db]
- cuco/src/main/filters/configuration.e2e11.properties (properties) [db]
- cuco/src/main/filters/web-ntlm.xml (xml)
- cuco/src/main/filters/web-external.xml (xml)
- cuco/src/main/filters/ehcache.xml (xml) [db]
- cuco/src/main/filters/web-internal.xml (xml)
- cuco/src/main/filters/versions.properties (properties)
- cuco/src/main/filters/configuration.t360.properties (properties) [db]
- cuco/src/main/filters/configuration.int11-ext.properties (properties) [db]
- cuco/src/main/filters/configuration.dev11.properties (properties) [db]
- cuco/src/main/filters/configuration.int11.properties (properties) [db]
- cuco/src/main/filters/gwt/PkbStarter.gwt.xml (xml)
- cuco/src/main/filters/gwt/AppStarter.gwt.xml (xml)
- cuco/src/main/filters/gwt/MyCuCoStarter.gwt.xml (xml)
- cuco/src/main/filters/gwt/AdminStarter.gwt.xml (xml)
- cuco/src/main/resources/logback.xml (xml) [db]
- cuco/src/main/resources/configuration.properties (properties) [db]
- cuco/src/main/resources/ehcache.xml (xml) [db]
- cuco/src/main/resources/at/a1ta/cuco/app/starter/AppStarter.gwt.xml (xml)
- cuco/src/main/resources/at/a1ta/cuco/admin/starter/AdminStarter.gwt.xml (xml)
- cuco/src/main/resources/at/a1ta/cuco/mycuco/starter/MyCuCoStarter.gwt.xml (xml)
- cuco/src/main/resources/at/a1ta/pkb/starter/PkbStarter.gwt.xml (xml)
- cuco/src/main/webapp/WEB-INF/web.xml (xml)


## 3. Functionality

- **Main Features:** Heuristic summary based on component classification.
- **Technology Stack (top):** spring_framework, mybatis
- **Design Patterns (top):** n/a
- **Inputs/Outputs:** API exposure 0, API consumers 0, DB interactions 19.
- **Key Methods/Functions:** [To be derived in advanced analysis]

## 4. Dependencies

- [To be cross-linked]

## 5. Notes

- [Business rule nuances]

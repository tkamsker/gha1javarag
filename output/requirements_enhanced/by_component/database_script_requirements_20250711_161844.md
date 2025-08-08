# Database Script Component Requirements

**Generated**: 2025-07-11 16:18:44

**Total files of this component type**: 975

## Distribution Across Layers

- **Unknown**: 938 files
- **Test**: 10 files
- **Persistence**: 7 files
- **Utility**: 3 files
- **Batch Process**: 6 files
- **Data Access**: 3 files
- **Backend Service**: 6 files
- **Configuration**: 2 files

## disable_index.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/disable_index.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to disable and drop indexes for performance optimization during data loading or maintenance operations",
    
    "components": [
        {
            "n...

---

## enable_index.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/enable_index.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database index creation script for customer and related data tables in a dual-schema system (tables suffixed with 1 and 2)",
    "components": [
        {
            "name": "Index ...

---

## 030_insert_custc_indexes.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/030_insert_custc_indexes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for managing indexes on voice usage and transaction tables",
    "components": [
        {
            "name": "CUSTC_INDEXES",
            "type": "datab...

---

## @custc_insert_custc_indexes.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_insert_custc_indexes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to manage indexes for voice usage and transaction tables",
    "components": [
        {
            "name": "CUSTC_INDEXES",
            "type": "databas...

---

## 03_@custc_konto_rufnummer_index.sql

**Path**: `cuco.dbmaintain/sql/00_initialSchema/17_CuCo_V3.3.0/03_@custc_konto_rufnummer_index.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to restructure unique constraints and indexes on KONTO_RUFNUMMER tables",
    
    "components": [
        {
            "name": "KONTO_RUFNUMMER2...

---

## 09_@custc_update_product_offering_index.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/09_@custc_update_product_offering_index.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates product index values for specific product offerings in the cct_productoffering table, establishing a defined ordering sequence",
    "components": [
        {
            "na...

---

## 01_@custc_update_product_offering_index.sql

**Path**: `cuco.dbmaintain/sql/11/59_CuCo_V20.12/01_@custc_update_product_offering_index.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates product index values for specific product offerings in the cct_productoffering table, establishing a defined ordering sequence",
    "components": [
        {
            "na...

---

## 11_@custc_bite_text_for_Indexation.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/11_@custc_bite_text_for_Indexation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update localization text for product browser interface",
    "components": [
        {
            "name": "bite_text",
            "type": "database_t...

---

## 23_@custc_CUCO_LINKS_indexColumn.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/23_@custc_CUCO_LINKS_indexColumn.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a numeric index column to the CUCO_LINKS table for link ordering/sequencing",
    "components": [
        {
            "name": "CUCO_LINKS",
            "type": "database_table...

---

## 02_@custc_indexes.sql

**Path**: `cuco.dbmaintain/sql/09/02_CuCo_V3.11.0/02_@custc_indexes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database index creation script for telephone number tables to optimize queries based on customer ID, account number (BAN), and numbering system",
    "components": [
        {
      ...

---

## 07_@custc_cctReportingIndexes.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/07_@custc_cctReportingIndexes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the cct_quote table to optimize query performance for create_date and last_update fields",
    "components": [
        {
            "name": "cct_quote in...

---

## 100_test_deletes_kunde.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/100_test_deletes_kunde.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data cleanup script that removes test customer records from two related customer tables",
    "components": [
        {
            "name": "delete_script",
            "type": ...

---

## 037_test_deletes_konto.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/037_test_deletes_konto.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data cleanup script that removes test account records from KONTO1 and KONTO2 tables for specific customer IDs",
    "components": [
        {
            "name": "SQL Delete Scr...

---

## 040_test_deletes_rufnummer.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/040_test_deletes_rufnummer.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data cleanup script that removes phone number records for specific test customer IDs from two related tables",
    "components": [
        {
            "name": "Delete Script",...

---

## 050_test_deletes_ansprechpartner.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/050_test_deletes_ansprechpartner.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data cleanup script that removes contact person (Ansprechpartner) records for specific customer IDs from two related tables",
    "components": [
        {
            "name": "...

---

## 035_test_deletes_bestand.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/035_test_deletes_bestand.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data cleanup script that removes records from BESTAND1 and BESTAND2 tables for specific test customer IDs",
    "components": [
        {
            "name": "Delete Script",
  ...

---

## 5_test_inserts_bestand.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/5_test_inserts_bestand.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data insertion script for customer inventory/contract data across dual database tables (BESTAND1 and BESTAND2)",
    
    "components": [
        {
            "name": "BESTAND1...

---

## 2_test_inserts_ansprechpartner.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/2_test_inserts_ansprechpartner.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data insertion script for contact person (Ansprechpartner) records in a customer management system",
    
    "components": [
        {
            "name": "ANSPRECHPARTNER1",
 ...

---

## 1_test_inserts_kunde.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/1_test_inserts_kunde.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data insertion script for customer (KUNDE) database tables with sample customer records",
    "components": [
        {
            "name": "KUNDE1",
            "type": "databa...

---

## 4_test_inserts_konto.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/4_test_inserts_konto.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data insertion script for account (KONTO) tables in a German/Austrian banking system",
    "components": [
        {
            "name": "KONTO1",
            "type": "database_...

---

## 3_test_inserts_rufnummer.sql

**Path**: `cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/3_test_inserts_rufnummer.sql`

**Layer**: Test

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Test data insertion script for telephone number (RUFNUMMER) tables in what appears to be a telecommunications system",
    
    "components": [
        {
            "name": "RUFNUMM...

---

## CUSTC_USER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/CUSTC_USER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation script that sets up tablespaces, users, and permissions for a customer-centric application with separate schemas for application, core, and data warehouse ac...

---

## copy_rufnummer.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_rufnummer.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy data between RUFNUMMER tables while managing constraints",
    "components": [
        {
            "name": "Constraint Disabler",
            "t...

---

## copy_umsatz.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_umsatz.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage UMSATZ (transaction/sales) data between tables with proper constraint and index handling",
    
    "components": [
        {
         ...

---

## copy_voice_nutzung.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_voice_nutzung.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage VOICE_NUTZUNG table data with constraint handling",
    
    "components": [
        {
            "name": "Constraint Management Block...

---

## copy_voice_nutzung_detail.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_voice_nutzung_detail.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage voice usage detail data between tables with constraint handling",
    
    "components": [
        {
            "name": "Constraint Ma...

---

## copy_standort.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_standort.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy data between STANDORT tables while managing constraints",
    "components": [
        {
            "name": "Constraint Management Block 1",
     ...

---

## create_umsatz_supra.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/create_umsatz_supra.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation script for customer transaction data with monthly partitioning",
    "components": [
        {
            "name": "UMSATZ_SUPRA1",
            "type": "data...

---

## copy_internet_nutzung.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_internet_nutzung.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage data between INTERNET_NUTZUNG tables while handling constraints and logging settings",
    
    "components": [
        {
            "...

---

## copy_produkt_hierarchie.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_produkt_hierarchie.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy product hierarchy data between tables",
    "components": [
        {
            "name": "copy_data.load_produkt_hierarchie1",
            "type"...

---

## create_view.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/create_view.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view and synonyms to expose visible products across different schemas with appropriate access controls",
    "components": [
        {
            "name": "V_VISIB...

---

## copy_bestand.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_bestand.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and restructure BESTAND tables with associated constraints and indexes",
    "components": [
        {
            "name": "Constraint Management ...

---

## copy_ansprechpartner.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_ansprechpartner.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to manage constraints and copy data between ANSPRECHPARTNER (contact person) tables",
    
    "components": [
        {
            "name": "constraint_m...

---

## sync_11g210g.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/sync_11g210g.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database synchronization script between Oracle 11g and 10g instances, specifically for user/role management tables",
    
    "components": [
        {
            "name": "Table Del...

---

## copy_konto_rufnummer.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_konto_rufnummer.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage KONTO_RUFNUMMER table data with constraint handling",
    "components": [
        {
            "name": "Constraint Disabler",
        ...

---

## copy_kunde_detail.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_kunde_detail.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy customer detail data between tables while managing constraints",
    "components": [
        {
            "name": "Constraint Disabler",
        ...

---

## get_user_limit.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/get_user_limit.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL utility script to retrieve session limit configuration for the CUSTC database user",
    
    "components": [
        {
            "name": "get_user_limit query",
            "t...

---

## copy_voice_nutzung_gzfz.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_voice_nutzung_gzfz.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage voice usage data between tables with constraint handling",
    
    "components": [
        {
            "name": "Constraint Managemen...

---

## copy_konto.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_konto.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy data between KONTO tables while managing constraints",
    "components": [
        {
            "name": "Constraint Management Block 1",
        ...

---

## drop_tables.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/drop_tables.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database cleanup script to remove views, tables, and synonyms from the CUSTC and CUSTC_DWH schemas",
    "components": [
        {
            "name": "View Cleanup",
            "ty...

---

## copy_umsatz_supra.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_umsatz_supra.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage data between UMSATZ_SUPRA tables while handling constraints and logging settings",
    
    "components": [
        {
            "name...

---

## create_copy_data_package.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/create_copy_data_package.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Generates a dynamic SQL package for data copying operations between tables based on a control table",
    "components": [
        {
            "name": "copy_data package",
         ...

---

## copy_rechnung.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_rechnung.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and rebuild RECHNUNG (invoice) tables with their constraints and indexes",
    "components": [
        {
            "name": "Constraint Managemen...

---

## resend_alerts.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/resend_alerts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A PL/SQL script to resend alerts for table control status by retrieving control data and sending signals via DBMS_ALERT",
    
    "components": [
        {
            "name": "Aler...

---

## copy_mobil_nutzung.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_mobil_nutzung.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage data between MOBIL_NUTZUNG tables while handling constraints",
    "components": [
        {
            "name": "Constraint Management...

---

## compare_dwh_tables.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/compare_dwh_tables.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Compare record counts between production and integration environments for data warehouse tables",
    "components": [
        {
            "name": "Anonymous PL/SQL Block",
        ...

---

## copy_kunde.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_kunde.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy customer (KUNDE) data between tables while managing constraints",
    "components": [
        {
            "name": "constraint_management_block",...

---

## copy_mk_interaktion.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_mk_interaktion.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy and manage data between MK_INTERAKTION tables while handling constraints",
    "components": [
        {
            "name": "Constraint Managemen...

---

## copy_einmal_umsatz.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_einmal_umsatz.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to copy transaction data between tables",
    "components": [
        {
            "name": "copy_data.load_einmal_umsatz1",
            "type": "stored_p...

---

## copy_w11_struktur.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/TOOLS/copy_w11_struktur.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to copy data from w11_struktur1 to w11_struktur2 tables",
    "components": [
        {
            "name": "copy_data.load_w11_struktur1",
            "typ...

---

## Synonyms.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database synonym creation script for data warehouse and operational database access",
    "components": [
        {
            "name": "Database Synonyms",
            "type": "data...

---

## Types.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Types.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script defining a custom type 'role_array' in an Oracle database schema",
    "components": [
        {
            "name": "role_array",
            "type": "oracle_custom_type"...

---

## DO.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/DO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation and maintenance script for a customer management system (CuCo)",
    "components": [
        {
            "name": "Table Scripts",
            "type": "DDL ...

---

## TRG_CUSTC_HEADER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Trigger/TRG_CUSTC_HEADER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database trigger to monitor and signal changes in CUSTC_HEADER table's status_dwh and quit fields",
    "components": [
        {
            "name": "trg_custc_header",
            ...

---

## TRG_DELETE_REPORTING.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Trigger/TRG_DELETE_REPORTING.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database trigger that automatically drops reporting tables when corresponding records are deleted from app_reporting table, specifically for long-running reports",
    
    "componen...

---

## TRG_CUSTC_TABLE_CONTROL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Trigger/TRG_CUSTC_TABLE_CONTROL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database trigger to monitor and signal changes in the CUSTC table control status, facilitating data warehouse synchronization and control operations",
    
    "components": [
      ...

---

## COPY_DATA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/PackageBody/COPY_DATA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Package body for copying and loading data into ansprechpartner1 (contact person) table using PL/SQL bulk operations",
    "components": [
        {
            "name": "copy_data",
 ...

---

## PRINT_OUT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Procedure/PRINT_OUT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A utility procedure for printing long strings to DBMS_OUTPUT with line length control and newline handling",
    
    "components": [
        {
            "name": "print_out",
     ...

---

## EXECUTELONGRUNNINGREPORTINGS.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Procedure/EXECUTELONGRUNNINGREPORTINGS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A stored procedure that executes long-running reporting queries and manages their result tables in an Oracle database",
    
    "components": [
        {
            "name": "execut...

---

## ROLE_ARRAY.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Type/ROLE_ARRAY.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a custom SQL VARRAY type to store an array of role names with a maximum capacity of 10 elements",
    
    "components": [
        {
            "name": "role_array",
       ...

---

## APP_SYS_TRACK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_TRACK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Audit logging table for tracking system events and user actions",
    "components": [
        {
            "name": "app_sys_track",
            "type": "database_table",
           ...

---

## CUCO_MATRIX~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_MATRIX~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the CUCO_MATRIX table, establishing relationships with category, product group, and segment tables",
    "components": [
        {
            "na...

---

## VOICE_NUTZUNG_GZFZ2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_GZFZ2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the VOICE_NUTZUNG_GZFZ2 table to optimize query performance for specific columns",
    "components": [
        {
            "name": "idx_voice_gz2_anlage...

---

## CUCO_SEGMENT~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGMENT~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_segment table by defining segment_id as the primary key",
    "components": [
        {
            "name": "cuco_segment",
            "typ...

---

## MK_INTERAKTION2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MK_INTERAKTION2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the mk_interaktion2 table by defining interact_oid as the primary key column",
    "components": [
        {
            "name": "mk_interaktion2",
 ...

---

## BESTAND2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/BESTAND2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script for storing customer product inventory (voice and internet products) with contract details",
    
    "components": [
        {
            "name": "BE...

---

## CUCO_VERRECHNUNGSART~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VERRECHNUNGSART~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_verrechnungsart table by defining verrechnungsart_id as the primary key",
    "components": [
        {
            "name": "cuco_verrechnun...

---

## RUFNUMMER1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RUFNUMMER1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the RUFNUMMER1 table to optimize query performance for telephone number and customer-related lookups",
    "components": [
        {
            "name": "...

---

## APP_BENUTZER_ROLLE~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER_ROLLE~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for user-role relationships in the application's security/authorization model",
    
    "components": [
        {
            "name": "app_benutzer_r...

---

## CUCO_KUNDE_ERWEITERT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_KUNDE_ERWEITERT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates an extension table for customer (kunde) data to store additional VIP-related information",
    "components": [
        {
            "name": "cuco_kunde_erweitert",
         ...

---

## CUCO_KATEGORIE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_KATEGORIE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table 'cuco_kategorie' for storing category information with basic metadata",
    "components": [
        {
            "name": "cuco_kategorie",
            "type...

---

## KONTO_RUFNUMMER1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO_RUFNUMMER1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing phone numbers associated with customer accounts",
    "components": [
        {
            "name": "konto_rufnummer1",
            "ty...

---

## KUNDE2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KUNDE2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the KUNDE2 table to optimize query performance for customer-related searches",
    "components": [
        {
            "name": "idx_kunde2_firmenbuchnum...

---

## APP_ROLLENGRUPPE_ROLLE~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLENGRUPPE_ROLLE~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key relationships for a role group-role mapping table in an application security/authorization context",
    "components": [
        {
            "name": "app_rollen...

---

## APP_ESB_ACCESS_ASSIGNMENTS~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ESB_ACCESS_ASSIGNMENTS~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a foreign key constraint between app_esb_access_assignments and app_esb_access_parameters tables for ESB access control",
    
    "components": [
        {
            "name...

---

## APP_TAB~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_TAB~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_tab table in a database schema",
    "components": [
        {
            "name": "app_tab",
            "type": "database_table",
         ...

---

## KONTO_RUFNUMMER2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO_RUFNUMMER2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a unique constraint on the konto_rufnummer2 table to ensure unique combinations of kunde_id, konto_id, and rufnummer",
    
    "components": [
        {
            "name": ...

---

## APP_ESB_ACCESS_ASSIGNMENTS~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ESB_ACCESS_ASSIGNMENTS~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a unique constraint to the app_esb_access_assignments table to ensure uniqueness of id and esb_access_parameter_id combinations",
    
    "components": [
        {
            ...

---

## CUCO_ERINNERUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_ERINNERUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the CUCO_ERINNERUNG table in a database schema",
    "components": [
        {
            "name": "CUCO_ERINNERUNG",
            "type": "database_t...

---

## CUCO_GULA~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_GULA~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a foreign key constraint between cuco_gula and cuco_dienstleistung tables to establish referential integrity",
    
    "components": [
        {
            "name": "cuco_gu...

---

## BESTAND1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/BESTAND1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script for storing customer product inventory (voice and internet products) with contract details",
    
    "components": [
        {
            "name": "be...

---

## APP_SYS_MESSAGE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_sys_message table",
    "components": [
        {
            "name": "app_sys_message table",
            "type": "database_table",
        ...

---

## KONTO_RUFNUMMER2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO_RUFNUMMER2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing phone numbers associated with customer accounts",
    "components": [
        {
            "name": "konto_rufnummer2",
            "ty...

---

## CUCO_SEGIMPORT_MATRIX~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_MATRIX~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_segimport_matrix table using prodgrp_id as the key field",
    "components": [
        {
            "name": "cuco_segimport_matrix",
      ...

---

## CUCO_NOTIZ_AENDERUNG~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ_AENDERUNG~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the CUCO_NOTIZ_AENDERUNG table, establishing relationships with CUCO_PRODUKTGRUPPE and CUCO_NOTIZ tables",
    
    "components": [
        {
    ...

---

## APP_APPLIKATION~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_APPLIKATION~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add primary key and unique constraints to the APP_APPLIKATION table",
    
    "components": [
        {
            "name": "APP_APPLIKATION t...

---

## BESTAND1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/BESTAND1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the bestand1 table using the bestand_id column",
    "components": [
        {
            "name": "bestand1_pk",
            "type": "database_const...

---

## EINMAL_UMSATZ1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/EINMAL_UMSATZ1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a primary key constraint for the einmal_umsatz1 table using a composite key of kunde_id and prod_num columns",
    
    "components": [
        {
            "name": "einmal_...

---

## CUCO_BEST_PRODGRP_PROD_HIER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_BEST_PRODGRP_PROD_HIER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for mapping product group hierarchies in the CUCO system",
    "components": [
        {
            "name": "cuco_best_prodgrp_prod_hier",
       ...

---

## UMSATZ1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the umsatz1 table to optimize query performance for customer-related lookups",
    
    "components": [
        {
            "name...

---

## CUCO_UNGUELTIGEVORWAHL~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_UNGUELTIGEVORWAHL~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to add a primary key constraint to the CUCO_UNGUELTIGEVORWAHL table",
    "components": [
        {
            "name": "CUCO_UNGUELTIGEVORWAHL",
            "type": "data...

---

## CUCO_VIP_HISTORY~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_HISTORY~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a foreign key constraint to the cuco_vip_history table linking it to app_benutzer table through benutzer_id",
    "components": [
        {
            "name": "cuco_vip_history...

---

## KONTO1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the konto1 table, establishing unique identification for account records",
    "components": [
        {
            "name": "konto1",
            "t...

---

## APP_ESB_ACCESS_PARAMETERS.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ESB_ACCESS_PARAMETERS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines database table structure for ESB (Enterprise Service Bus) access parameters and connection settings",
    "components": [
        {
            "name": "app_esb_access_parame...

---

## APP_TAB_CONTAINER~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_TAB_CONTAINER~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Establishes foreign key relationships for the app_tab_container table, defining relationships with app_container and app_tab tables",
    
    "components": [
        {
            "...

---

## RECHNUNG1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RECHNUNG1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the konto_id column of the rechnung1 table to optimize query performance for account-related lookups",
    
    "components": [
        {
            "nam...

---

## INTERNET_NUTZUNG2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/INTERNET_NUTZUNG2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a unique constraint to the internet_nutzung2 table to enforce data integrity across multiple customer and contract related columns",
    
    "components": [
        {
         ...

---

## APP_MENU.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_MENU.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines the database table structure for application menu items, representing a hierarchical navigation menu system",
    
    "components": [
        {
            "name": "APP_MENU...

---

## STANDORT1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/STANDORT1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the lokation_id column of the standort1 table to optimize query performance",
    "components": [
        {
            "name": "idx_standort1_lokation_id...

---

## CUCO_PRODUKTGRUPPE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_PRODUKTGRUPPE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key and unique constraints for the CUCO_PRODUKTGRUPPE table in a database schema",
    "components": [
        {
            "name": "CUCO_PRODUKTGRUPPE",
           ...

---

## CUCO_VIP_HISTORY~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_HISTORY~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_vip_history table by defining vip_history_id as the primary key",
    
    "components": [
        {
            "name": "cuco_vip_history",...

---

## CUCO_KUNDE_ERWEITERT~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_KUNDE_ERWEITERT~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to cuco_kunde_erweitert table, establishing unique identification for customer extension records",
    "components": [
        {
            "name": "cuco...

---

## CUCO_DIENSTLEISTUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_DIENSTLEISTUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_dienstleistung table by defining dienstleistung_id as the primary key",
    "components": [
        {
            "name": "cuco_dienstleistu...

---

## APP_SYS_MESSAGE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing system messages/announcements with validity periods and display settings",
    
    "components": [
        {
            "name": "app_...

---

## CUCO_DIENSTLEISTUNGSART~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_DIENSTLEISTUNGSART~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_dienstleistungsart table in a database schema",
    "components": [
        {
            "name": "cuco_dienstleistungsart",
            "ty...

---

## UMSATZ_SUPRA1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ_SUPRA1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a partitioned local index on the umsatz_supra1 table to optimize queries filtering by kunde_id and monat columns",
    
    "components": [
        {
            "name": "idx...

---

## APP_SYS_MESSAGE_ROLLE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE_ROLLE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a junction/mapping table for associating system messages with roles in the application",
    "components": [
        {
            "name": "app_sys_message_rolle",
          ...

---

## CUCO_SEGIMPORT_PATH.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_PATH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing segment import file paths with tracking of last modification timestamps",
    "components": [
        {
            "name": "cuco_segim...

---

## ANSPRECHPARTNER1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/ANSPRECHPARTNER1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the ansprechpartner1 table to optimize query performance for customer contact lookups",
    
    "components": [
        {
        ...

---

## CUCO_SEGIMPORT_MAPPING~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_MAPPING~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the CUCO_SEGIMPORT_MAPPING table, establishing relationships with CUCO_SEGIMPORT_PATH and CUCO_SEGIMPORT_MATRIX tables",
    
    "components": [
...

---

## APP_APPLIKATION.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_APPLIKATION.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script for storing application metadata/configuration",
    "components": [
        {
            "name": "APP_APPLIKATION",
            "type": "database_tab...

---

## APP_EINSTELLUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_EINSTELLUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_einstellung table to ensure unique key values",
    "components": [
        {
            "name": "app_einstellung",
            "type": "dat...

---

## APP_TAB_PORTLET~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_TAB_PORTLET~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_tab_portlet table to ensure uniqueness of portlet-tab combinations",
    
    "components": [
        {
            "name": "app_tab_portlet"...

---

## UMSATZ_SUPRA2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ_SUPRA2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a partitioned database table for storing customer transaction data with monthly partitioning",
    
    "components": [
        {
            "name": "umsatz_supra2",
       ...

---

## MOBIL_NUTZUNG1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MOBIL_NUTZUNG1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing mobile phone usage statistics and billing data",
    "components": [
        {
            "name": "mobil_nutzung1",
            "type": "databa...

---

## CUCO_SEGIMPORT_MAPPING.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_MAPPING.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a mapping table for segment import functionality in the CUCO (Customer Communication) system",
    "components": [
        {
            "name": "cuco_segimport_mapping",
   ...

---

## APP_ROLLENGRUPPE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLENGRUPPE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for managing role groups in an application",
    "components": [
        {
            "name": "APP_ROLLENGRUPPE",
            "type": "database_ta...

---

## APP_ROLLE_AUTH~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLE_AUTH~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for app_rolle_auth table which appears to manage role-based authorization mappings",
    "components": [
        {
            "name": "app_rolle_auth ...

---

## APP_ROLLE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_rolle table in the database schema",
    "components": [
        {
            "name": "app_rolle table",
            "type": "database_table...

---

## APP_IMAGE_SIZE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_IMAGE_SIZE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key and unique constraints for the app_image_size table in a database schema",
    "components": [
        {
            "name": "app_image_size table constraints",
 ...

---

## APP_ROLLENGRUPPE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLENGRUPPE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_rollengruppe table, establishing rg_id as the unique identifier",
    "components": [
        {
            "name": "app_rollengruppe",
     ...

---

## CUCO_RT_CODE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_RT_CODE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the CUCO_RT_CODE table using the prod_num column",
    "components": [
        {
            "name": "CUCO_RT_CODE",
            "type": "database_ta...

---

## APP_REPORTING~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_REPORTING~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to app_reporting table in the database schema",
    "components": [
        {
            "name": "app_reporting",
            "type": "database_table",
 ...

---

## CUSTC_HEADER~CHK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUSTC_HEADER~CHK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a CHECK constraint to the CUSTC_HEADER table to validate status_dwh values",
    
    "components": [
        {
            "name": "CUSTC_HEADER table constraint",
            ...

---

## APP_CONTAINER~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_CONTAINER~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for the app_container table in the database schema",
    
    "components": [
        {
            "name": "app_container table",
            "type": ...

---

## APP_BENUTZER_ROLLE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER_ROLLE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a many-to-many relationship table between users (benutzer) and roles (rolle) for application user role management",
    
    "components": [
        {
            "name": "ap...

---

## RUFNUMMER2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RUFNUMMER2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes for the RUFNUMMER2 table to optimize query performance on frequently accessed columns and combinations",
    "components": [
        {
            "name": "i...

---

## APP_ESB_ACCESS_ASSIGNMENTS.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ESB_ACCESS_ASSIGNMENTS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table for managing ESB access assignments, likely for enterprise service bus access control",
    "components": [
        {
            "name": "app_esb_access_ass...

---

## CUCO_NOTIZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing customer notes/comments with associated metadata in the CUCO (Customer Communication) system",
    "components": [
        {
            "name":...

---

## APP_BENUTZER_EINSTELLUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER_EINSTELLUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Stores user-specific application settings/preferences with sensitivity flags",
    "components": [
        {
            "name": "app_benutzer_einstellung",
            "type": "data...

---

## UMSATZ_SUPRA1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ_SUPRA1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a partitioned database table for storing customer transaction data (SUPRA) with monthly partitioning",
    
    "components": [
        {
            "name": "umsatz_supra1",...

---

## MK_INTERAKTION1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MK_INTERAKTION1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the mk_interaktion1 table by defining interact_oid as the primary key column",
    
    "components": [
        {
            "name": "mk_interaktion...

---

## MOBIL_NUTZUNG2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MOBIL_NUTZUNG2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing mobile usage statistics and billing data for telecommunications customers",
    "components": [
        {
            "name": "MOBIL_NUTZUNG2",
...

---

## APP_MENU~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_MENU~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the app_menu table, establishing hierarchical menu relationships and tab associations",
    
    "components": [
        {
            "name": "ap...

---

## VOICE_NUTZUNG_GZFZ1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_GZFZ1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes for the VOICE_NUTZUNG_GZFZ1 table to optimize query performance on specific columns",
    "components": [
        {
            "name": "idx_voice_gz1_anlage...

---

## KONTO_RUFNUMMER1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO_RUFNUMMER1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a unique constraint on the konto_rufnummer1 table to ensure unique combinations of kunde_id, konto_id, and rufnummer",
    
    "components": [
        {
            "name": ...

---

## CUCO_TEAM.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script for managing team information in the CUCO system",
    "components": [
        {
            "name": "CUCO_TEAM",
            "type": "database_table",...

---

## KUNDE1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KUNDE1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the KUNDE1 table to optimize query performance for customer-related searches",
    "components": [
        {
            "name": "idx_kunde1_firmenbuchnum...

---

## CUCO_DIENSTLEISTUNG~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_DIENSTLEISTUNG~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the CUCO_DIENSTLEISTUNG table, establishing relationships with CUCO_DIENSTLEISTUNGSART and CUCO_VERRECHNUNGSART tables",
    
    "components": [
...

---

## APP_BENUTZER~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for app_benutzer (user/account) table in database schema",
    "components": [
        {
            "name": "app_benutzer",
            "type": "datab...

---

## CUCO_NOTIZ~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the CUCO_NOTIZ table in a database schema",
    "components": [
        {
            "name": "CUCO_NOTIZ",
            "type": "database_table",
   ...

---

## CUCO_SEGIMPORT_MAPPING~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_MAPPING~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key and unique constraints for the cuco_segimport_mapping table used for segment import mapping configurations",
    
    "components": [
        {
            "name"...

---

## CUCO_VIP_HISTORY.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_HISTORY.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a historical tracking table for VIP status changes of customers in the CUCO system",
    "components": [
        {
            "name": "cuco_vip_history",
            "type":...

---

## CUCO_TEAM_USER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM_USER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a many-to-many relationship mapping table between teams and users in the CUCO system",
    
    "components": [
        {
            "name": "cuco_team_user",
            "t...

---

## CUCO_PROTOCOL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_PROTOCOL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for protocol/logging data in the CUCO system",
    "components": [
        {
            "name": "CUCO_PROTOCOL",
            "type": "database_table",
    ...

---

## RUFNUMMER1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RUFNUMMER1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition script for storing telephone number and location information in a customer management system",
    "components": [
        {
            "name": "RUFNUMMER1...

---

## STANDORT2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/STANDORT2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the lokation_id column of the standort2 table to optimize query performance",
    "components": [
        {
            "name": "idx_standort2_lokation_id...

---

## CUCO_BESTAND_PRODUKTGRUPPE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_BESTAND_PRODUKTGRUPPE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for product group inventory/stock management with visibility and ordering controls",
    "components": [
        {
            "name": "cuco_bestan...

---

## INTERNET_NUTZUNG1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/INTERNET_NUTZUNG1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a unique constraint to the internet_nutzung1 table to enforce data integrity across multiple customer and contract related columns",
    
    "components": [
        {
         ...

---

## RECHNUNG2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RECHNUNG2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the konto_id column of the rechnung2 table to optimize query performance for account-related lookups",
    
    "components": [
        {
            "nam...

---

## CUSTC_TABLE_CONTROL~CHK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUSTC_TABLE_CONTROL~CHK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines check constraints for status values in a database table control system that manages data loading and synchronization processes",
    
    "components": [
        {
          ...

---

## APP_REPORTING.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_REPORTING.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing application reporting configurations and queries",
    "components": [
        {
            "name": "app_reporting",
            "type...

---

## CUCO_SEGIMPORT~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_segimport table by defining import_id as the primary key",
    
    "components": [
        {
            "name": "cuco_segimport",
        ...

---

## CUCO_KATEGORIE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_KATEGORIE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_kategorie table by defining kategorie_id as the primary key",
    "components": [
        {
            "name": "cuco_kategorie",
          ...

---

## APP_MENU~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_MENU~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_menu table to ensure unique menu identification",
    "components": [
        {
            "name": "app_menu table",
            "type": "da...

---

## CUCO_SEGIMPORT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for importing segment data with tracking of import metadata",
    "components": [
        {
            "name": "CUCO_SEGIMPORT",
            "type...

---

## ANSPRECHPARTNER2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/ANSPRECHPARTNER2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the ansprechpartner2 table to optimize query performance for customer contact lookups",
    
    "components": [
        {
        ...

---

## APP_SESSION_TRACK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SESSION_TRACK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Tracks application session counts by date for monitoring and analytics purposes",
    
    "components": [
        {
            "name": "app_session_track",
            "type": "dat...

---

## CUSTC_TABLE_CONTROL~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUSTC_TABLE_CONTROL~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a unique constraint to the custc_table_control table to ensure table_name values are unique",
    "components": [
        {
            "name": "custc_table_control",
          ...

---

## UMSATZ_SUPRA2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ_SUPRA2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a partitioned local index on the umsatz_supra2 table to optimize queries filtering by kunde_id and monat columns",
    "components": [
        {
            "name": "idx_umsa...

---

## APP_ROLLENGRUPPE_ROLLE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLENGRUPPE_ROLLE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to app_rollengruppe_rolle table, establishing a composite primary key from rg_id and rolle_id columns",
    
    "components": [
        {
            "na...

---

## UMSATZ2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the umsatz2 table to optimize query performance for customer-related lookups",
    
    "components": [
        {
            "name...

---

## EINMAL_UMSATZ2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/EINMAL_UMSATZ2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a primary key constraint for the einmal_umsatz2 table using a composite key of kunde_id and prod_num columns",
    
    "components": [
        {
            "name": "einmal_...

---

## CUCO_NOTIZ~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the CUCO_NOTIZ table, establishing relationships with CUCO_PRODUKTGRUPPE and CUCO_SEGIMPORT tables",
    
    "components": [
        {
          ...

---

## CUCO_NOTIZ_AENDERUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ_AENDERUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_notiz_aenderung table for tracking note changes",
    "components": [
        {
            "name": "cuco_notiz_aenderung",
            "typ...

---

## APP_TAB_CONTAINER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_TAB_CONTAINER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for managing tab container relationships and positioning in an application interface",
    
    "components": [
        {
            "name": "app_...

---

## APP_CONTAINER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_CONTAINER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for managing application containers/widgets with layout and display properties",
    
    "components": [
        {
            "name": "app_contai...

---

## APP_APPLIKATION_TAB.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_APPLIKATION_TAB.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a join/mapping table that establishes relationships between applications and tabs in a database schema",
    "components": [
        {
            "name": "APP_APPLIKATION_TA...

---

## APP_SYS_MESSAGE_ROLLE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE_ROLLE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for app_sys_message_rolle table to ensure unique combinations of system message and role references",
    
    "components": [
        {
            "n...

---

## APP_EINSTELLUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_EINSTELLUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for application settings/configuration storage",
    "components": [
        {
            "name": "APP_EINSTELLUNG",
            "type": "database_table",
...

---

## APP_SYS_MESSAGE_ROLLE~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE_ROLLE~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the app_sys_message_rolle table, establishing relationships with app_sys_message and app_rolle tables",
    
    "components": [
        {
       ...

---

## RUFNUMMER2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RUFNUMMER2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition script for storing telephone number and location information in a customer/contract context",
    "components": [
        {
            "name": "RUFNUMMER2"...

---

## BESTAND2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/BESTAND2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the bestand2 table, establishing unique identification for records",
    "components": [
        {
            "name": "bestand2_pk",
            "ty...

---

## APP_ROLLENGRUPPE_ROLLE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLENGRUPPE_ROLLE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a join/mapping table for role groups and roles in an application security/authorization context",
    "components": [
        {
            "name": "APP_ROLLENGRUPPE_ROLLE",
...

---

## APP_ESB_ACCESS_PARAMETERS~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ESB_ACCESS_PARAMETERS~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_esb_access_parameters table for ESB (Enterprise Service Bus) access configuration",
    
    "components": [
        {
            "name": "a...

---

## KONTO2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the konto2 table, establishing unique identification for account records",
    "components": [
        {
            "name": "konto2",
            "t...

---

## APP_IMAGE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_IMAGE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_image table in a database schema",
    "components": [
        {
            "name": "app_image table",
            "type": "database_table",...

---

## APP_BENUTZER_EINSTELLUNG~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER_EINSTELLUNG~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a foreign key constraint between app_benutzer_einstellung and app_benutzer tables, establishing a parent-child relationship with cascade delete",
    
    "components": [
   ...

---

## CUCO_NOTIZ_AENDERUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ_AENDERUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Manages change tracking for customer notes/comments in a CRM or customer management system",
    "components": [
        {
            "name": "cuco_notiz_aenderung",
            "ty...

---

## STANDORT1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/STANDORT1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for the standort1 table (location/site table) in a database schema",
    "components": [
        {
            "name": "standort1_pk",
            "typ...

---

## CUCO_VIP_IMPORT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_IMPORT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for importing VIP customer data with transaction amounts and tracking metadata",
    "components": [
        {
            "name": "cuco_vip_import...

---

## RECHNUNG1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RECHNUNG1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the RECHNUNG1 table in a database schema",
    "components": [
        {
            "name": "RECHNUNG1 Table Constraint",
            "type": "DDL c...

---

## INTERNET_NUTZUNG2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/INTERNET_NUTZUNG2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the internet_nutzung2 table to optimize queries based on kunde_id and monat_start_dat columns",
    "components": [
        {
            "name": "idx_int...

---

## CUCO_RT_CODE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_RT_CODE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a reference table structure for product codes with associated attributes like description, one-time sales flag, and duration in months",
    
    "components": [
        {
  ...

---

## CUCO_DIENSTLEISTUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_DIENSTLEISTUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing service/product offerings with pricing and classification information",
    "components": [
        {
            "name": "cuco_dienstl...

---

## CUCO_VIP_HISTORY~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_HISTORY~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the cuco_vip_history table to optimize query performance for customer-related lookups",
    "components": [
        {
            "...

---

## APP_AUTH.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_AUTH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines an authorization/permissions table structure for application-level authentication and authorization",
    "components": [
        {
            "name": "app_auth",
          ...

---

## ANSPRECHPARTNER1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/ANSPRECHPARTNER1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for ansprechpartner1 table (contact person/representative table)",
    "components": [
        {
            "name": "ansprechpartner1_pk",
           ...

---

## CUCO_GULA~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_GULA~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_gula table by defining gula_id as the primary key",
    "components": [
        {
            "name": "cuco_gula",
            "type": "data...

---

## KONTO2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing customer account and billing recipient information in a banking/financial context",
    "components": [
        {
            "name": "KONTO2",
...

---

## MK_INTERAKTION2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MK_INTERAKTION2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing customer interaction records in a marketing/customer service context",
    "components": [
        {
            "name": "mk_interaktio...

---

## APP_BENUTZER_EINSTELLUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER_EINSTELLUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_benutzer_einstellung table to ensure unique user settings combinations",
    
    "components": [
        {
            "name": "app_benutzer...

---

## APP_APPLIKATION_MENU~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_APPLIKATION_MENU~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the app_applikation_menu table, establishing relationships with app_applikation and app_menu tables",
    
    "components": [
        {
         ...

---

## W11_STRUKTUR2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/W11_STRUKTUR2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the w11_struktur2 table using prod_num as the key field",
    "components": [
        {
            "name": "w11_struktur2",
            "type": "dat...

---

## CUCO_SEGMENT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGMENT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition script for customer segmentation data storage",
    "components": [
        {
            "name": "cuco_segment",
            "type": "database_table",
    ...

---

## TOAD_PLAN_TABLE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/TOAD_PLAN_TABLE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a plan table for Oracle's TOAD tool to store execution plan information for SQL query analysis and optimization",
    
    "components": [
        {
            "name": "TOAD...

---

## BESTAND1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/BESTAND1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database index creation script for the BESTAND1 table to optimize query performance on specific columns",
    "components": [
        {
            "name": "idx_bestand1_aon_kund_no"...

---

## CUCO_DIENSTLEISTUNGSART.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_DIENSTLEISTUNGSART.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing service types (Dienstleistungsart) in the CUCO system",
    "components": [
        {
            "name": "cuco_dienstleistungsart",
  ...

---

## CUCO_VIP_IMPORT~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_IMPORT~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a foreign key constraint between cuco_vip_import and app_benutzer tables for user relationships",
    "components": [
        {
            "name": "cuco_vip_import table",
 ...

---

## KONTO1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing customer account and billing recipient information in a banking/financial context",
    
    "components": [
        {
            "name": "KONT...

---

## KONTO1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the KONTO1 table to optimize query performance for KONTO_ID and KUNDE_ID columns",
    "components": [
        {
            "name": "idx_konto1_func",
  ...

---

## MK_INTERAKTION1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MK_INTERAKTION1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing customer interaction records in a marketing/customer service context",
    "components": [
        {
            "name": "mk_interaktio...

---

## APP_PORTLET.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_PORTLET.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for managing application portlets/widgets with their configurations and display settings",
    
    "components": [
        {
            "name": "...

---

## APP_IMAGE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_IMAGE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing application image metadata including file paths and user information",
    "components": [
        {
            "name": "APP_IMAGE",
 ...

---

## APP_TAB.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_TAB.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for application tab/panel configuration storage",
    "components": [
        {
            "name": "app_tab",
            "type": "database_table",
       ...

---

## CUCO_ERINNERUNG~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_ERINNERUNG~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the cuco_erinnerung table to optimize queries involving the this2notiz foreign key relationship",
    
    "components": [
        {
            "name": "...

---

## APP_TAB_PORTLET.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_TAB_PORTLET.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for mapping relationships between tabs and portlets in a web application, likely for UI layout management",
    
    "components": [
        {
    ...

---

## VOICE_NUTZUNG_DETAIL2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_DETAIL2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing detailed voice usage records with monthly partitioning",
    
    "components": [
        {
            "name": "voice_nutzung_detail2",
       ...

---

## MOBIL_NUTZUNG2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MOBIL_NUTZUNG2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the mobil_nutzung2 table to optimize queries filtering by kunde_id and rufnummer columns",
    
    "components": [
        {
            "name": "idx_mob...

---

## CUCO_SEGIMPORT_PATH~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_PATH~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_segimport_path table, establishing path_id as the unique identifier",
    "components": [
        {
            "name": "cuco_segimport_path...

---

## VOICE_NUTZUNG1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a local partitioned index on the kunde_id column of the voice_nutzung1 table for optimizing customer-related queries",
    "components": [
        {
            "name": "idx_...

---

## KUNDE_DETAIL2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KUNDE_DETAIL2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a unique constraint to the kunde_detail2 table to ensure unique kunde_id values",
    "components": [
        {
            "name": "kunde_detail2",
            "type": "databas...

---

## APP_SYS_MESSAGE~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the app_sys_message table for optimizing queries based on valid_start and valid_end date ranges",
    
    "components": [
        {
            "name": "...

---

## CUCO_VIP_IMPORT~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VIP_IMPORT~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_vip_import table by defining import_id as the primary key",
    "components": [
        {
            "name": "cuco_vip_import",
           ...

---

## APP_BENUTZER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script for user management (app_benutzer) storing basic user information including login credentials and department details",
    
    "components": [
       ...

---

## CUCO_TEAM_USER~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM_USER~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the cuco_team_user table, establishing relationships between users and teams",
    "components": [
        {
            "name": "cuco_team_user",...

---

## RUFNUMMER1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RUFNUMMER1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a primary key constraint on the rufnummer1 table for telephone number management",
    "components": [
        {
            "name": "rufnummer1",
            "type": "databa...

---

## APP_CONTAINER_PORTLET.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_CONTAINER_PORTLET.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a join/mapping table for managing relationships between application containers and portlets with sequence ordering",
    "components": [
        {
            "name": "app_co...

---

## VOICE_NUTZUNG_DETAIL1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_DETAIL1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing detailed voice usage records with monthly partitioning",
    
    "components": [
        {
            "name": "voice_nutzung_detail1",
       ...

---

## VOICE_NUTZUNG_DETAIL1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_DETAIL1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a local partitioned index on the kunde_id column of the voice_nutzung_detail1 table for optimizing customer-related voice usage queries",
    
    "components": [
        {
 ...

---

## MK_INTERAKTION2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MK_INTERAKTION2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the mk_interaktion2 table to optimize query performance for customer-related lookups",
    
    "components": [
        {
         ...

---

## APP_ROLLE~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLE~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Establishes a foreign key relationship between app_rolle and app_applikation tables for application role management",
    
    "components": [
        {
            "name": "app_roll...

---

## PRODUKT_HIERARCHIE1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/PRODUKT_HIERARCHIE1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the produkt_hierarchie1 table using the ssa_produkt_id column",
    
    "components": [
        {
            "name": "produkt_hierarchie1",
       ...

---

## KUNDE2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KUNDE2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add primary key and unique constraints to the KUNDE2 table",
    "components": [
        {
            "name": "KUNDE2 Table Constraints",
    ...

---

## APP_AUTH~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_AUTH~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Establishes a foreign key relationship between app_auth and app_applikation tables for application authentication",
    
    "components": [
        {
            "name": "app_auth",...

---

## CUCO_SEGIMPORT_MATRIX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_SEGIMPORT_MATRIX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing segment import matrix data, likely used for customer segmentation or product grouping",
    "components": [
        {
            "name...

---

## KONTO_RUFNUMMER2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO_RUFNUMMER2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the konto_rufnummer2 table to optimize query performance for customer-related lookups",
    
    "components": [
        {
        ...

---

## CUCO_UNGUELTIGEVORWAHL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_UNGUELTIGEVORWAHL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table to store invalid area codes (telephone prefixes) with descriptions",
    "components": [
        {
            "name": "cuco_ungueltigevorwahl",
            ...

---

## CUCO_RT_PRODGRP.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_RT_PRODGRP.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a relation/mapping table between product groups and RT codes in the CUCO system",
    "components": [
        {
            "name": "cuco_rt_prodgrp",
            "type": "da...

---

## APP_SYS_MESSAGE_VIEWED~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE_VIEWED~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the app_sys_message_viewed table, establishing relationships with app_sys_message and app_benutzer tables",
    
    "components": [
        {
   ...

---

## APP_ROLLE_AUTH.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLE_AUTH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a many-to-many relationship table between application roles and authorizations",
    "components": [
        {
            "name": "app_rolle_auth",
            "type": "data...

---

## BESTAND2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/BESTAND2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the BESTAND2 table to optimize query performance for customer and contract-related lookups",
    "components": [
        {
            "name": "idx_bestan...

---

## CUCO_TEAM_USER~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM_USER~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_team_user table defining a composite key from team_id and user_id columns",
    
    "components": [
        {
            "name": "cuco_tea...

---

## CUCO_GULA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_GULA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for customer-related data storage, appears to be tracking customer contact/phone information and associated service costs",
    
    "components": [
       ...

---

## APP_SYS_MESSAGE_VIEWED.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_SYS_MESSAGE_VIEWED.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Stores user message viewing history for system messages in the application",
    "components": [
        {
            "name": "app_sys_message_viewed",
            "type": "database...

---

## W11_STRUKTUR1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/W11_STRUKTUR1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the w11_struktur1 table using prod_num as the key field",
    "components": [
        {
            "name": "w11_struktur1",
            "type": "dat...

---

## VOICE_NUTZUNG_GZFZ2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_GZFZ2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for tracking voice usage data with business/leisure time classification for customer billing",
    
    "components": [
        {
            "name...

---

## KONTO2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the KONTO2 table to optimize query performance for KONTO_ID and KUNDE_ID columns",
    "components": [
        {
            "name": "idx_konto2_func",
  ...

---

## APP_ROLLE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script defining an application role entity for user role management",
    "components": [
        {
            "name": "APP_ROLLE",
            "type": "data...

---

## CUCO_RT_PRODGRP~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_RT_PRODGRP~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the CUCO_RT_PRODGRP table, establishing relationships with CUCO_PRODUKTGRUPPE and CUCO_RT_CODE tables",
    
    "components": [
        {
       ...

---

## APP_PORTLET~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_PORTLET~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_portlet table in a database schema",
    "components": [
        {
            "name": "app_portlet",
            "type": "database_table",
 ...

---

## CUCO_NOTIZ~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_NOTIZ~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the cuco_notiz table to optimize foreign key lookups for produktgruppe relationships",
    
    "components": [
        {
            "name": "fk_notiz_pr...

---

## INTERNET_NUTZUNG1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/INTERNET_NUTZUNG1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database indexes on the internet_nutzung1 table to optimize query performance for kunde_id and monat_start_dat columns",
    "components": [
        {
            "name": "id...

---

## RECHNUNG2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RECHNUNG2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the RECHNUNG2 table in a database schema",
    "components": [
        {
            "name": "RECHNUNG2_PK",
            "type": "database_constraint...

---

## CUCO_PROTOCOL~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_PROTOCOL~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to the cuco_protocol table in the database schema",
    
    "components": [
        {
            "name": "cuco_protocol",
            "type": "database_...

---

## APP_APPLIKATION_TAB~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_APPLIKATION_TAB~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key relationships for the app_applikation_tab table, establishing relationships with app_applikation and app_tab tables",
    
    "components": [
        {
         ...

---

## STANDORT2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/STANDORT2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for the standort2 table in a database schema",
    "components": [
        {
            "name": "standort2_pk",
            "type": "primary_key_const...

---

## CUCO_BEST_PRODGRP_PROD_HIER~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_BEST_PRODGRP_PROD_HIER~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a foreign key constraint between cuco_best_prodgrp_prod_hier and cuco_bestand_produktgruppe tables for maintaining referential integrity in product group hierarchy",
    
   ...

---

## VOICE_NUTZUNG_GZFZ1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_GZFZ1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for tracking voice usage during business and leisure hours for customer billing and analysis",
    
    "components": [
        {
            "name...

---

## ANSPRECHPARTNER2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/ANSPRECHPARTNER2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for ansprechpartner2 table (contact person/representative table)",
    "components": [
        {
            "name": "ansprechpartner2_pk",
           ...

---

## CUCO_VERRECHNUNGSART.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_VERRECHNUNGSART.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing billing/accounting types (Verrechnungsart) in the CUCO system",
    "components": [
        {
            "name": "cuco_verrechnungsart...

---

## VOICE_NUTZUNG1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a partitioned database table for storing voice usage/call records for customers with monthly partitioning",
    
    "components": [
        {
            "name": "voice_nutz...

---

## MK_INTERAKTION1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MK_INTERAKTION1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the mk_interaktion1 table to optimize query performance for customer-related lookups",
    
    "components": [
        {
         ...

---

## VOICE_NUTZUNG_DETAIL2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG_DETAIL2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a partitioned local index on the kunde_id column of the voice_nutzung_detail2 table for optimizing customer-based queries on voice usage details",
    
    "components": [
  ...

---

## CUCO_TEAM_DIENSTLEISTUNG~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM_DIENSTLEISTUNG~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines foreign key constraints for the cuco_team_dienstleistung table, establishing relationships between teams and services",
    
    "components": [
        {
            "name":...

---

## PRODUKT_HIERARCHIE1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/PRODUKT_HIERARCHIE1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for product hierarchy management with multiple levels of product categorization",
    "components": [
        {
            "name": "produkt_hierar...

---

## RUFNUMMER2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/RUFNUMMER2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a primary key constraint on the rufnummer2 table for telephone number management",
    "components": [
        {
            "name": "rufnummer2_pk",
            "type": "dat...

---

## CUCO_ERINNERUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_ERINNERUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for reminder/notification management in the CUCO system",
    "components": [
        {
            "name": "CUCO_ERINNERUNG",
            "type": "database...

---

## CUCO_TEAM~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to the cuco_team table in the database schema",
    "components": [
        {
            "name": "cuco_team",
            "type": "database_table",
     ...

---

## APP_APPLIKATION_MENU.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_APPLIKATION_MENU.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a join/mapping table for application menu structure, likely managing the relationship between applications and their menu items with ordering",
    
    "components": [
     ...

---

## CUCO_BESTAND_PRODUKTGRUPPE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_BESTAND_PRODUKTGRUPPE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the cuco_bestand_produktgruppe table by defining bestand_produktgruppe_id as the primary key",
    "components": [
        {
            "name": "cuc...

---

## W11_STRUKTUR2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/W11_STRUKTUR2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table 'w11_struktur2' for storing product structure information with timestamps and action codes",
    "components": [
        {
            "name": "w11_struktur2...

---

## UMSATZ2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table 'umsatz2' for storing customer transaction and revenue data with timestamps",
    "components": [
        {
            "name": "umsatz2",
            "type"...

---

## KONTO_RUFNUMMER1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KONTO_RUFNUMMER1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the kunde_id column of the konto_rufnummer1 table to optimize query performance for customer-related lookups",
    
    "components": [
        {
        ...

---

## EINMAL_UMSATZ1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/EINMAL_UMSATZ1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store one-time transaction data for customers with product-specific details",
    "components": [
        {
            "name": "einmal_umsatz1",
        ...

---

## APP_ROLLE_AUTH~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLE_AUTH~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Establishes foreign key relationships for the app_rolle_auth table, defining many-to-many relationships between roles and authorizations",
    "components": [
        {
            "...

---

## APP_BENUTZER~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a unique index on the app_benutzer table for case-insensitive login lookups",
    "components": [
        {
            "name": "app_benutzer_login_idx",
            "type": ...

---

## KUNDE1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KUNDE1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script that adds primary key and unique constraints to the KUNDE1 table",
    "components": [
        {
            "name": "KUNDE1 Table Constraints",
 ...

---

## PRODUKT_HIERARCHIE2~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/PRODUKT_HIERARCHIE2~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the produkt_hierarchie2 table using the ssa_produkt_id column",
    "components": [
        {
            "name": "produkt_hierarchie2",
            ...

---

## VOICE_NUTZUNG2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a partitioned database table for storing voice usage/call records with monthly segmentation",
    "components": [
        {
            "name": "voice_nutzung2",
            ...

---

## MOBIL_NUTZUNG1~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/MOBIL_NUTZUNG1~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the mobil_nutzung1 table to optimize queries filtering by kunde_id and rufnummer columns",
    
    "components": [
        {
            "name": "idx_mob...

---

## CUCO_ERINNERUNG~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_ERINNERUNG~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a foreign key constraint between CUCO_ERINNERUNG and CUCO_NOTIZ tables in a database schema",
    "components": [
        {
            "name": "CUCO_ERINNERUNG",
           ...

---

## CUCO_TEAM_DIENSTLEISTUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_TEAM_DIENSTLEISTUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a many-to-many relationship table between teams and services (dienstleistung) in the CUCO system",
    "components": [
        {
            "name": "cuco_team_dienstleistung...

---

## PRODUKT_HIERARCHIE2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/PRODUKT_HIERARCHIE2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a product hierarchy table structure for storing product categorization data with multiple levels",
    "components": [
        {
            "name": "produkt_hierarchie2",
  ...

---

## APP_EINSTELLUNG~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_EINSTELLUNG~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a unique index on the app_einstellung table for app_id and key columns",
    "components": [
        {
            "name": "app_einstellungen_pk",
            "type": "databa...

---

## CUCO_MATRIX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_MATRIX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing matrix relationships between product groups, segments, and categories with ordering information",
    "components": [
        {
       ...

---

## APP_CONTAINER_PORTLET~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_CONTAINER_PORTLET~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Establishes foreign key relationships for the app_container_portlet table, defining associations with app_container and app_portlet tables",
    
    "components": [
        {
      ...

---

## APP_IMAGE_SIZE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_IMAGE_SIZE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table schema for storing application image size configurations",
    "components": [
        {
            "name": "app_image_size",
            "type": "database_...

---

## APP_BENUTZER_ROLLE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_BENUTZER_ROLLE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a primary key constraint for the app_benutzer_rolle table which appears to manage user role associations",
    "components": [
        {
            "name": "app_benutzer_rol...

---

## DBMAINTAIN_SCRIPTS.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/DBMAINTAIN_SCRIPTS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database version control tracking table to maintain script execution history",
    "components": [
        {
            "name": "dbmaintain_scripts",
            "type": "database_t...

---

## W11_STRUKTUR1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/W11_STRUKTUR1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table structure for storing product-related data with timestamps and action codes",
    "components": [
        {
            "name": "w11_struktur1",
            ...

---

## CUCO_PRODUKTGRUPPE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/CUCO_PRODUKTGRUPPE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table schema for product groups (Produktgruppe) in the CUCO system",
    "components": [
        {
            "name": "cuco_produktgruppe",
            "type": "d...

---

## UMSATZ1.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/UMSATZ1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table 'umsatz1' for storing customer transaction and revenue data with timestamps",
    "components": [
        {
            "name": "umsatz1",
            "type"...

---

## APP_ROLLENGRUPPE~FK.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_ROLLENGRUPPE~FK.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Establishes a foreign key relationship between app_rollengruppe and app_applikation tables for application role group management",
    
    "components": [
        {
            "nam...

---

## EINMAL_UMSATZ2.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/EINMAL_UMSATZ2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store one-time transaction data for customers with product-specific details",
    "components": [
        {
            "name": "einmal_umsatz2",
        ...

---

## APP_AUTH~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/APP_AUTH~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the app_auth table for authentication/authorization management",
    
    "components": [
        {
            "name": "app_auth table",
           ...

---

## KUNDE_DETAIL1~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/KUNDE_DETAIL1~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a unique constraint to the kunde_detail1 table to ensure unique kunde_id values",
    "components": [
        {
            "name": "kunde_detail1",
            "type": "databas...

---

## VOICE_NUTZUNG2~INX.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Table/VOICE_NUTZUNG2~INX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a partitioned local index on the kunde_id column of the voice_nutzung2 table to optimize customer-based queries",
    "components": [
        {
            "name": "idx_voice...

---

## V_W11_STRUKTUR.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_W11_STRUKTUR.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified interface to access W11_STRUKTUR table data",
    "components": [
        {
            "name": "v_w11_struktur",
            "type...

---

## V_ANSPRECHPARTNER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_ANSPRECHPARTNER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition that provides a read-only representation of contact person (Ansprechpartner) information for customers",
    "components": [
        {
            "name": "v...

---

## V_KONTO_RUFNUMMER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_KONTO_RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified access layer for account (konto) and phone number (rufnummer) relationships",
    "components": [
        {
            "name": "v_...

---

## V_UMSATZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_UMSATZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified interface for accessing sales/revenue data from the UMSATZ table",
    "components": [
        {
            "name": "v_umsatz",
  ...

---

## V_RUFNUMMER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view 'v_rufnummer' that provides a structured representation of telephone number related data including contract, customer, and location information",
    
    "co...

---

## V_MOBIL_NUTZUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_MOBIL_NUTZUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition for mobile usage tracking and billing data aggregation",
    "components": [
        {
            "name": "v_mobil_nutzung",
            "type": "database_v...

---

## APP_V_STANDORT_RUFNUMMER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/APP_V_STANDORT_RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that joins location (standort) and phone number (rufnummer) information for customer data access",
    "components": [
        {
            "name": "APP_V_ST...

---

## V_PRODUKT_HIERARCHIE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_PRODUKT_HIERARCHIE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a hierarchical representation of products with multiple levels of categorization",
    "components": [
        {
            "name": "v_produkt_...

---

## V_MK_INTERAKTION.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_MK_INTERAKTION.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a read-only abstraction layer over the MK_INTERAKTION table, likely for marketing interaction data",
    
    "components": [
        {
        ...

---

## V_BESTAND.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_BESTAND.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition that provides a read-only abstraction layer over the 'bestand' table, likely representing customer contract or service inventory data",
    
    "components"...

---

## V_STANDORT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_STANDORT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition that provides a simplified interface for accessing location/site data from the STANDORT table",
    "components": [
        {
            "name": "v_standort...

---

## V_UMSATZ_SUPRA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_UMSATZ_SUPRA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified access layer to the umsatz_supra table, exposing specific columns for sales/transaction data",
    
    "components": [
        {
 ...

---

## V_EINMAL_UMSATZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_EINMAL_UMSATZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified access layer to the EINMAL_UMSATZ table, exposing one-time transaction data for customers",
    
    "components": [
        {
    ...

---

## V_INTERNET_NUTZUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_INTERNET_NUTZUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified interface for internet usage data of customers",
    "components": [
        {
            "name": "v_internet_nutzung",
          ...

---

## V_VOICE_NUTZUNG_GZFZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_VOICE_NUTZUNG_GZFZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified interface for voice usage data with time window information",
    "components": [
        {
            "name": "v_voice_nutzung_gz...

---

## V_KUNDE_DETAIL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_KUNDE_DETAIL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition that provides a detailed customer information overview including product usage, contact history, and customer status",
    
    "components": [
        {
   ...

---

## V_VISIBLE_PRODUCTS.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_VISIBLE_PRODUCTS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that filters visible products based on product hierarchy and group relationships",
    "components": [
        {
            "name": "v_visible_products",
   ...

---

## V_KONTO.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_KONTO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition that provides a read-only abstraction layer over the konto (account) table with customer-related information",
    "components": [
        {
            "nam...

---

## V_VOICE_NUTZUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_VOICE_NUTZUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides a simplified interface for voice usage data, mapping directly to the VOICE_NUTZUNG table",
    
    "components": [
        {
            "name"...

---

## V_INTERNET_NUTZUNG_AGGREGATED.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_INTERNET_NUTZUNG_AGGREGATED.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Aggregates internet usage data by customer and month, providing summarized metrics for volume, costs and duration",
    "components": [
        {
            "name": "v_internet_nutz...

---

## V_RECHNUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_RECHNUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition that provides a simplified interface for querying invoice (rechnung) data",
    "components": [
        {
            "name": "v_rechnung",
            "type...

---

## V_KUNDE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_KUNDE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database view definition for customer (kunde) data providing a consolidated read-only view of customer information",
    "components": [
        {
            "name": "v_kunde",
    ...

---

## V_VOICE_NUTZUNG_DETAIL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/View/V_VOICE_NUTZUNG_DETAIL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that provides detailed voice usage information for customer contracts",
    "components": [
        {
            "name": "v_voice_nutzung_detail",
          ...

---

## SEQ_APP_BENUTZER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_BENUTZER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for application users (BENUTZER)",
    "components": [
        {
            "name": "seq_app_benutzer",
            "ty...

---

## CUSTC_META_MODEL_SEQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/CUSTC_META_MODEL_SEQ.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for the customer meta model entities",
    "components": [
        {
            "name": "custc_meta_model_seq...

---

## SEQ_CUCO_NOTIZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_NOTIZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for CUCO_NOTIZ (notes/notifications) table",
    "components": [
        {
            "name": "seq_cuco_notiz...

---

## SEQ_APP_CONTAINER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_CONTAINER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for application containers",
    "components": [
        {
            "name": "seq_app_container",
            "type": ...

---

## SEQ_CUCO_VIP_IMPORT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_VIP_IMPORT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for VIP import operations with specific increment and range settings",
    "components": [
        {
            "name": "seq_cuco_vip_import",
...

---

## SEQ_CUCO_GULA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_GULA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers in the CUCO (Customer Contract) system",
    "components": [
        {
            "name": "seq_cuco_gula",
            ...

---

## SEQ_APP_REPORTING.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_REPORTING.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence for application reporting ID generation in the database",
    "components": [
        {
            "name": "seq_app_reporting",
            "type": "database_sequ...

---

## SEQ_APP_ROLLE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_ROLLE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence for application role IDs in the database",
    "components": [
        {
            "name": "seq_app_rolle",
            "type": "database_sequence",
            ...

---

## SEQ_CUCO_ERINNERUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_ERINNERUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for CUCO_ERINNERUNG (reminder) entities",
    "components": [
        {
            "name": "seq_cuco_erinnerung",
     ...

---

## SEQ_APP_PORTLET.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_PORTLET.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for application portlets",
    "components": [
        {
            "name": "seq_app_portlet",
            "type": "dat...

---

## SEQ_APP_IMAGE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_IMAGE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for application images",
    "components": [
        {
            "name": "seq_app_image",
            "type"...

---

## SEQ_CUCO_DIENSTLEISTUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_DIENSTLEISTUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence for generating unique identifiers for the CUCO_DIENSTLEISTUNG (service/performance) table in the database",
    "components": [
        {
            "name": "seq_...

---

## SEQ_CUCO_NOTIZ_AENDERUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_NOTIZ_AENDERUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for tracking changes to notes (notiz_aenderung) in the CUCO system",
    "components": [
        {
            "name": "seq_cuco_notiz_aenderung",
       ...

---

## SEQ_CUCO_SEGIMPORT_MAPPING.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_SEGIMPORT_MAPPING.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for CUCO segment import mapping records",
    "components": [
        {
            "name": "seq_cuco_segimpor...

---

## SEQ_APP_AUTH.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_AUTH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for application authorization ID generation",
    "components": [
        {
            "name": "seq_app_auth",
            "type": "database_sequence",
 ...

---

## CUCO_SEQ_PROTOCOL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/CUCO_SEQ_PROTOCOL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique protocol identifiers",
    "components": [
        {
            "name": "cuco_seq_protocol",
            "type": "databas...

---

## SEQ_CUCO_UNGUELTIGEVORWAHL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_UNGUELTIGEVORWAHL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for invalid area codes (ungueltige vorwahl) in the CUCO system",
    "components": [
        {
            "name": "seq_...

---

## SEQ_APP_ROLLENGRUPPE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_ROLLENGRUPPE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for application role groups",
    "components": [
        {
            "name": "seq_app_rollengruppe",
            "typ...

---

## SEQ_APP_SYS_MESSAGE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_SYS_MESSAGE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for application system messages",
    "components": [
        {
            "name": "seq_app_sys_message",
   ...

---

## LOGGINGSEQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/LOGGINGSEQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for logging functionality, used to generate unique identifiers for log entries",
    "components": [
        {
            "name": "loggingseq",...

---

## SEQ_CUCO_VIP_HISTORY.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_VIP_HISTORY.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence for VIP history records in the CUCO (Customer Core) system",
    "components": [
        {
            "name": "seq_cuco_vip_history",
            "type": "databas...

---

## SEQ_CUCO_TEAM.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_TEAM.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence for generating unique team IDs in the CUCO system",
    "components": [
        {
            "name": "seq_cuco_team",
            "type": "database_sequence",
   ...

---

## SEQ_CUCO_PRODUKTGRUPPE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_PRODUKTGRUPPE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for product groups (PRODUKTGRUPPE) in the CUCO system",
    "components": [
        {
            "name": "seq_cuco_prod...

---

## SEQ_CUCO_SEGIMPORT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_SEGIMPORT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for CUCO segment import records",
    "components": [
        {
            "name": "seq_cuco_segimport",
    ...

---

## SEQ_CUCO_DIENSTLEISTUNGSART.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_DIENSTLEISTUNGSART.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for service types (Dienstleistungsart) in the CUCO system",
    "components": [
        {
            "name": "seq_cuco_...

---

## SEQ_APP_MENU.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_MENU.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence for generating unique identifiers for application menu items",
    "components": [
        {
            "name": "seq_app_menu",
            "type": "database_sequ...

---

## SEQ_CUCO_SEGIMPORT_PATH.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_SEGIMPORT_PATH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a sequence in Oracle database for generating unique identifiers for CUCO segment import paths",
    "components": [
        {
            "name": "seq_cuco_segimport_path",
 ...

---

## SEQ_APP_TAB.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_APP_TAB.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for an application table",
    "components": [
        {
            "name": "seq_app_tab",
            "type": "databas...

---

## SEQ_CUCO_BESTAND_PRODUKTGRUPPE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Sequence/SEQ_CUCO_BESTAND_PRODUKTGRUPPE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database sequence for generating unique identifiers for the CUCO_BESTAND_PRODUKTGRUPPE table",
    "components": [
        {
            "name": "seq_cuco_bestand_produktgr...

---

## TOOLS_COMMON.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Package/TOOLS_COMMON.sql`

**Layer**: Utility

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A utility package for email handling and logging operations in an Oracle database environment",
    
    "components": [
        {
            "name": "tools_common",
            "ty...

---

## LOAD_DWH_DATA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Package/LOAD_DWH_DATA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Package definition for loading data warehouse (DWH) data with multiple load procedures for different business entities",
    "components": [
        {
            "name": "load_dwh_d...

---

## COPY_DATA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Package/COPY_DATA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Package for managing data copying operations between database tables, likely for ETL or data migration purposes",
    "components": [
        {
            "name": "copy_data",
     ...

---

## CUSTC_APP.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Grant/CUSTC_APP.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database permission script granting access rights to CUSTC_APP user for various application tables",
    "components": [
        {
            "name": "CUSTC_APP",
            "type"...

---

## CUSTC_DWH.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Grant/CUSTC_DWH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database permission management script granting specific access rights to the CUSTC_DWH user/role for various customer and product-related tables in a data warehouse context",
    "co...

---

## PUBLIC.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC/Grant/PUBLIC.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Grant database permissions to PUBLIC role for the TOAD plan table",
    "components": [
        {
            "name": "PUBLIC Role Grant",
            "type": "database_permission",
...

---

## 072_create_trigger.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/072_create_trigger.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database trigger management script for customer data control and reporting system",
    "components": [
        {
            "name": "trg_custc_header",
            "type": "databas...

---

## 093_insert_app_einstellung_prod.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/093_insert_app_einstellung_prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script to populate application settings table with initial production values",
    
    "components": [
        {
            "name": "APP_EINSTELLUNG",
      ...

---

## 012_create_pkb_views4custc_app.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/012_create_pkb_views4custc_app.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database views for PKB (Product Knowledge Base) data access and grants select permissions to CUSTC_APP user",
    
    "components": [
        {
            "name": "v_pkb_de...

---

## 010_create_db_link_10g_prod.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/010_create_db_link_10g_prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database link creation script for connecting to CUSTC production database systems",
    "components": [
        {
            "name": "CUSTC_10G_PROD",
            "type": "database_...

---

## 085_copy_from_11g_INT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/085_copy_from_11g_INT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to disable foreign key constraints on APP_ and CUCO_ tables, likely for data migration or maintenance purposes",
    
    "components": [
        {
      ...

---

## 065_executelongrunningreportings.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/065_executelongrunningreportings.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A stored procedure that executes long-running reporting queries and manages their result tables in a database",
    
    "components": [
        {
            "name": "executelongrun...

---

## 025_insert_custc_table_control.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/025_insert_custc_table_control.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for configuring table control parameters in the CUSTC_TABLE_CONTROL table, which manages table maintenance operations",
    
    "components": [
      ...

---

## 020_insert_custc_header.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/020_insert_custc_header.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script to populate the CUSTC_HEADER table with initial configuration data",
    
    "components": [
        {
            "name": "CUSTC_HEADER Table Initial...

---

## 035_create_print_out.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/035_create_print_out.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A utility stored procedure for printing long strings to DBMS_OUTPUT with line length control and newline handling",
    
    "components": [
        {
            "name": "print_out"...

---

## 090_copy_from_10g_prod.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/090_copy_from_10g_prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to disable foreign key constraints on APP_ and CUCO_ tables, likely for data migration or maintenance purposes",
    
    "components": [
        {
      ...

---

## 075_create_del_old_data_job.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/075_create_del_old_data_job.sql`

**Layer**: Batch Process

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a scheduled database maintenance job to automatically delete old data from tables based on configured retention periods",
    
    "components": [
        {
            "name...

---

## 095_check_and_fix_sequences.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/095_check_and_fix_sequences.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to check and fix sequence values by aligning them with the maximum primary key values in their respective tables",
    
    "components": [
        {
    ...

---

## 094_insert_app_esb_xxx.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/094_insert_app_esb_xxx.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for ESB (Enterprise Service Bus) access parameters across different environments (DEV, INT, PROD)",
    
    "components": [
        {
            "name...

---

## 005_create_db_link_11g_int.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/005_create_db_link_11g_int.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database link between Oracle databases for cross-database access in a CUSTC environment",
    "components": [
        {
            "name": "CUSTC_11G_INT",
            "ty...

---

## 080_create_main_alert_job.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/080_create_main_alert_job.sql`

**Layer**: Batch Process

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to initialize and start a main alert job process",
    "components": [
        {
            "name": "LOAD_DATA.START_MAIN_ALERT",
            "type": "st...

---

## 055_create_load_dwh_package.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/055_create_load_dwh_package.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Dynamically generates a PL/SQL package for loading data warehouse tables based on table control metadata",
    
    "components": [
        {
            "name": "load_dwh_data packa...

---

## 100_create_statistics.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/100_create_statistics.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to gather statistics on tables in the CUSTC schema, handling both regular and versioned tables",
    
    "components": [
        {
            "name": "S...

---

## 060_create_load_dwh_data.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/ROLLOUT/060_create_load_dwh_data.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Oracle PL/SQL package for loading data warehouse tables with ETL procedures for various business entities",
    "components": [
        {
            "name": "load_dwh_data",
       ...

---

## Synonyms.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database synonym creation script for a data warehouse environment, establishing aliases for various customer and product-related tables",
    "components": [
        {
            "n...

---

## Types.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Types.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL Type definitions script for CUSTC_DWH schema in CuCo database version 3.0.0.0",
    "components": [],
    "data_structures": [],
    "business_rules": [],
    "dependencies": ["D...

---

## DO.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/DO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation and maintenance script for a customer and communications data warehouse",
    "components": [
        {
            "name": "Table Scripts",
            "typ...

---

## MK_INTERAKTION~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/MK_INTERAKTION~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the mk_interaktion table in a database schema",
    "components": [
        {
            "name": "mk_interaktion",
            "type": "database_tab...

---

## MOBIL_NUTZUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/MOBIL_NUTZUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for mobile usage tracking and billing data in a data warehouse context",
    "components": [
        {
            "name": "MOBIL_NUTZUNG",
            "typ...

---

## STANDORT~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/STANDORT~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the 'standort' (location) table using composite keys kunde_id and lokation_id",
    
    "components": [
        {
            "name": "standort",
  ...

---

## VOICE_NUTZUNG_GZFZ~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/VOICE_NUTZUNG_GZFZ~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the VOICE_NUTZUNG_GZFZ table in a data warehouse schema",
    "components": [
        {
            "name": "VOICE_NUTZUNG_GZFZ",
            "type":...

---

## KONTO.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/KONTO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition script for storing customer account (konto) information in a data warehouse context",
    
    "components": [
        {
            "name": "KONTO table",
...

---

## PRODUKT_HIERARCHIE.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/PRODUKT_HIERARCHIE.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a product hierarchy table structure in a data warehouse environment for storing product categorization and classification data",
    "components": [
        {
            "na...

---

## KUNDE_DETAIL~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/KUNDE_DETAIL~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the kunde_detail table, establishing unique identification for customer details",
    "components": [
        {
            "name": "kunde_detail",
 ...

---

## VOICE_NUTZUNG_DETAIL~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/VOICE_NUTZUNG_DETAIL~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to voice_nutzung_detail table in a data warehouse schema",
    "components": [
        {
            "name": "voice_nutzung_detail",
            "type": "...

---

## MK_INTERAKTION.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/MK_INTERAKTION.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing customer interaction/contact records in a data warehouse context",
    "components": [
        {
            "name": "mk_interaktion",
...

---

## RECHNUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/RECHNUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to the 'rechnung' (invoice) table in a database schema",
    "components": [
        {
            "name": "rechnung",
            "type": "database_table...

---

## KUNDE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/KUNDE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the 'kunde' (customer) table in a database schema",
    "components": [
        {
            "name": "kunde table",
            "type": "database_ta...

---

## VOICE_NUTZUNG~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/VOICE_NUTZUNG~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to voice_nutzung table in a data warehouse schema",
    "components": [
        {
            "name": "voice_nutzung",
            "type": "database_table...

---

## EINMAL_UMSATZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/EINMAL_UMSATZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store one-time sales/transaction data for customers with product information",
    "components": [
        {
            "name": "einmal_umsatz",
        ...

---

## VOICE_NUTZUNG_DETAIL.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/VOICE_NUTZUNG_DETAIL.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing detailed voice usage/call records for customer telecommunications data in a data warehouse context",
    
    "components": [
        {...

---

## RUFNUMMER~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/RUFNUMMER~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the 'rufnummer' table in a database schema",
    "components": [
        {
            "name": "rufnummer table",
            "type": "database_table...

---

## ANSPRECHPARTNER~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/ANSPRECHPARTNER~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for the ansprechpartner (contact person) table in a customer data warehouse schema",
    
    "components": [
        {
            "name": "ansprechpa...

---

## KONTO~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/KONTO~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to the 'konto' table in a database schema",
    "components": [
        {
            "name": "konto table",
            "type": "database_table",
       ...

---

## EINMAL_UMSATZ~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/EINMAL_UMSATZ~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines primary key constraint for einmal_umsatz table in a data warehouse schema",
    "components": [
        {
            "name": "einmal_umsatz",
            "type": "database_t...

---

## VOICE_NUTZUNG.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/VOICE_NUTZUNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing voice usage/call records for customer contracts",
    "components": [
        {
            "name": "voice_nutzung",
            "type"...

---

## BESTAND.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/BESTAND.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table creation script for storing customer product inventory (bestand) data in a data warehouse environment",
    
    "components": [
        {
            "name": "bestand...

---

## KONTO_RUFNUMMER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/KONTO_RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines a database table structure for storing phone numbers associated with customer accounts in a data warehouse context",
    "components": [
        {
            "name": "konto_...

---

## W11_STRUKTUR.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/W11_STRUKTUR.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table 'w11_struktur' for storing product structure information in a data warehouse context",
    "components": [
        {
            "name": "w11_struktur",
    ...

---

## PRODUKT_HIERARCHIE~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/PRODUKT_HIERARCHIE~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the produkt_hierarchie table in a data warehouse schema",
    "components": [
        {
            "name": "produkt_hierarchie",
            "type":...

---

## KONTO_RUFNUMMER~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/KONTO_RUFNUMMER~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the konto_rufnummer table in a database schema",
    "components": [
        {
            "name": "konto_rufnummer",
            "type": "database_t...

---

## BESTAND~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/BESTAND~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds primary key constraint to the 'bestand' table in a database schema",
    "components": [
        {
            "name": "bestand table",
            "type": "database_table",
   ...

---

## UMSATZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/UMSATZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition for storing customer sales/revenue data in a data warehouse context",
    "components": [
        {
            "name": "umsatz",
            "type": "datab...

---

## UMSATZ_SUPRA.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/UMSATZ_SUPRA.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store customer transaction data (SUPRA) with timestamp tracking",
    "components": [
        {
            "name": "umsatz_supra",
            "type": "d...

---

## VOICE_NUTZUNG_GZFZ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/VOICE_NUTZUNG_GZFZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store voice usage data segmented by business hours and free time periods for customer tracking",
    
    "components": [
        {
            "name": "V...

---

## RUFNUMMER.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database table definition script for storing telephone number and location information in a customer/contract context",
    "components": [
        {
            "name": "RUFNUMMER",...

---

## W11_STRUKTUR~UNQ.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Table/W11_STRUKTUR~UNQ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds a primary key constraint to the w11_struktur table using prod_num column",
    "components": [
        {
            "name": "w11_struktur",
            "type": "database_table"...

---

## DWH_IMPORT.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Package/DWH_IMPORT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Package for controlling and managing data warehouse (DWH) loading processes",
    "components": [
        {
            "name": "dwh_import",
            "type": "oracle_package",
  ...

---

## CUSTC.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_DWH/Grant/CUSTC.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database permission management script granting CRUD operations to CUSTC user on customer and usage-related tables in a data warehouse environment",
    "components": [
        {
    ...

---

## Synonyms.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_APP/Synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database synonym creation script for application schema access layer, providing alias mappings to CUSTC schema objects",
    "components": [
        {
            "name": "Database S...

---

## Types.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_APP/Types.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Empty or missing SQL file - unable to analyze actual content",
    "components": [],
    "data_structures": [],
    "business_rules": [],
    "dependencies": [],
    
    "file_class...

---

## DO.sql

**Path**: `cuco.dbmaintain/SchemaCreation/01_CuCo_V3.0.0.0/CUSTC_APP/DO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema maintenance script that executes synonym and type definitions and compiles the schema objects",
    
    "components": [
        {
            "name": "DO.sql",
     ...

---

## 03_@custc_roles.sql

**Path**: `cuco.dbmaintain/sql/04/02_CuCo_V3.4.0/03_@custc_roles.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script for customer contact (CuCo) system defining user roles and permissions",
    
    "components": [
        {
            "name": "BITE_ROLE table",
...

---

## 04_@custc_users.sql

**Path**: `cuco.dbmaintain/sql/04/02_CuCo_V3.4.0/04_@custc_users.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script to populate user and role data for IT department staff members",
    "components": [
        {
            "name": "BITE_USER",
            "type": "da...

---

## 02_@custc_auths.sql

**Path**: `cuco.dbmaintain/sql/04/02_CuCo_V3.4.0/02_@custc_auths.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for inserting authorization/permission records into the BITE_AUTH table, defining feature-level access controls",
    
    "components": [
        {
            "name": "B...

---

## @custc_cctReporting.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_cctReporting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates reporting views for CCT (Customer Contract Tool) data with customer, quote, and opportunity information",
    "components": [
        {
            "name": "v_cct_report",
  ...

---

## @custc_cct_text.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_cct_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating and maintaining localized UI text labels related to A1 IP Voice services",
    
    "components": [
        {
            "name":...

---

## @custc_load_dwh_data.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_load_dwh_data.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Data warehouse (DWH) loading package that manages ETL operations for various business entities",
    "components": [
        {
            "name": "load_dwh_data",
            "type"...

---

## @custc_triggers.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_triggers.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database trigger definitions for monitoring and managing customer data changes and search index updates",
    "components": [
        {
            "name": "trg_custc_header",
      ...

---

## @custc_menu_lead.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_menu_lead.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to update menu configuration for quote overview functionality in the BITE_MENU table",
    
    "components": [
        {
            "name": "Menu Definition XML",
      ...

---

## @custc_salesInfoReporting.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_salesInfoReporting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database views for sales information reporting, specifically focusing on customer notes and related task information",
    
    "components": [
        {
            "name": ...

---

## @custc_dataCleanup.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_dataCleanup.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to clean up old logs by deleting records older than 1 year from CUCO_LOGS table",
    
    "components": [
        {
            "name": "Log Cleanup Scri...

---

## @custc_visitreport.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_visitreport.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for product configuration data in a visit report system",
    "components": [
        {
            "name": "SI_VI_SBS_PRODUCT table",
            "typ...

---

## @custc_loggingEvents.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_loggingEvents.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for logging events configuration",
    "components": [
        {
            "name": "bite_loggingevent",
            "type": "database_table",
       ...

---

## @custc_menu.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_menu.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to define and insert menu configuration for a customer portal interface into BITE_MENU table",
    
    "components": [
        {
            "name": "Menu Definition XML"...

---

## @custc_menu_pkb.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_menu_pkb.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to update menu configuration for PKB (Probably Knowledge Base) by inserting XML menu definition into bite_menu table",
    
    "components": [
        {
            "name...

---

## @custc_digital_selling_note_view.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_digital_selling_note_view.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that transforms XML-structured digital selling note data into a relational format for easier querying",
    
    "components": [
        {
            "name":...

---

## @rep_salesInfoReporting.sql

**Path**: `cuco.dbmaintain/sql/repeat/@rep_salesInfoReporting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for sales information reporting views, providing a layer of abstraction for accessing customer reporting data",
    "components": [
        {
            "n...

---

## @custc_procedures.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_procedures.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Oracle PL/SQL stored procedure to trigger Solr index updates for phone and party cores via HTTP requests",
    
    "components": [
        {
            "name": "call_solr_for_updat...

---

## @custc_reports.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_reports.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for managing reporting queries in a customer reporting system",
    "components": [
        {
            "name": "APP_REPORTING table management",
            "type": "da...

---

## @custc_package_tools_common.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_package_tools_common.sql`

**Layer**: Utility

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Oracle PL/SQL package providing email configuration and utility functions for a system named CUCO",
    
    "components": [
        {
            "name": "tools_common",
           ...

---

## @custc_menu_insert.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_menu_insert.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to insert/update menu configuration data in XML format for a customer portal interface",
    "components": [
        {
            "name": "menuDefinition",
            "t...

---

## @custc_load_data.sql

**Path**: `cuco.dbmaintain/sql/repeat/@custc_load_data.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Oracle PL/SQL package for managing data warehouse (DWH) loading processes with status tracking and table management",
    
    "components": [
        {
            "name": "CUSTC.lo...

---

## @app_cctReporting.sql

**Path**: `cuco.dbmaintain/sql/repeat/@app_cctReporting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for CCT (Customer Care Tool) reporting views to provide abstracted access to reporting data across different business units",
    "components": [
        {
...

---

## @rep_cctReporting.sql

**Path**: `cuco.dbmaintain/sql/repeat/@rep_cctReporting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for CCT (Customer Contract Tracking) reporting views to provide simplified access to reporting data structures",
    "components": [
        {
            "...

---

## @custc_settings.sql

**Path**: `cuco.dbmaintain/sql/repeat/settings/@custc_settings.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for email notification settings in the Customer Cockpit application",
    
    "components": [
        {
            "name": "BITE_SETTING table",
     ...

---

## @custc_cronjobs_#prod.sql

**Path**: `cuco.dbmaintain/sql/repeat/cronjobs/@custc_cronjobs_#prod.sql`

**Layer**: Batch Process

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for scheduling periodic jobs/tasks in a customer service system",
    
    "components": [
        {
            "name": "bite_cronjob table",
         ...

---

## @custc_cronjobs_#dev.sql

**Path**: `cuco.dbmaintain/sql/repeat/cronjobs/@custc_cronjobs_#dev.sql`

**Layer**: Batch Process

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for configuring scheduled jobs (cronjobs) in a development environment",
    
    "components": [
        {
            "name": "bite_cronjob table",
 ...

---

## @custc_cronjobs_#int.sql

**Path**: `cuco.dbmaintain/sql/repeat/cronjobs/@custc_cronjobs_#int.sql`

**Layer**: Batch Process

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for scheduling system cron jobs with specific timing patterns",
    
    "components": [
        {
            "name": "bite_cronjob table",
          ...

---

## @custc_esb_assignments_#int.sql

**Path**: `cuco.dbmaintain/sql/repeat/esb/@custc_esb_assignments_#int.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for ESB (Enterprise Service Bus) access parameters and assignments in different environments (DEV, INT)",
    "components": [
        {
            "name": "BITE...

---

## @custc_esb_assignments_#dev.sql

**Path**: `cuco.dbmaintain/sql/repeat/esb/@custc_esb_assignments_#dev.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for ESB (Enterprise Service Bus) access parameters in development environment",
    "components": [
        {
            "name": "BITE_ESB_ACCESS_PARAMETERS",
 ...

---

## @custc_esb_assignments_#e2e.sql

**Path**: `cuco.dbmaintain/sql/repeat/esb/@custc_esb_assignments_#e2e.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for ESB (Enterprise Service Bus) access parameters and assignments in a development environment",
    
    "components": [
        {
            "name": "BITE_ES...

---

## @custc_esb_assignments_#prod.sql

**Path**: `cuco.dbmaintain/sql/repeat/esb/@custc_esb_assignments_#prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for ESB (Enterprise Service Bus) access parameters and assignments in different environments",
    
    "components": [
        {
            "name": "BITE_ESB_A...

---

## @custc_role_authz_#prod.sql

**Path**: `cuco.dbmaintain/sql/repeat/authorization/@custc_role_authz_#prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Defines role-based authorization mappings for CUCO CCT KeyUser role in the system",
    "components": [
        {
            "name": "BITE_ROLE_AUTH",
            "type": "database_...

---

## @custc_role_authz_#int.sql

**Path**: `cuco.dbmaintain/sql/repeat/authorization/@custc_role_authz_#int.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for role-based authorization configuration, specifically assigning CCT (Customer Care Tool) default role permissions",
    
    "components": [
        {
            "name...

---

## 02_@custc_daas_activation.sql

**Path**: `cuco.dbmaintain/sql/11/48_CuCo_V19.11/02_@custc_daas_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to set up Device as a Service (DaaS) product offering configuration",
    "components": [
        {
            "name": "Product Offering Insert",
            "type":...

---

## 04_@custc_etgt_delete_not_finalized_quotes_lower_v10.sql

**Path**: `cuco.dbmaintain/sql/11/48_CuCo_V19.11/04_@custc_etgt_delete_not_finalized_quotes_lower_v10.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to delete non-finalized quotes from ETGT system versions lower than V10",
    
    "components": [
        {
            "name": "Quote Cleanup Procedure"...

---

## 01_@custc_daas_admin_ui.sql

**Path**: `cuco.dbmaintain/sql/11/48_CuCo_V19.11/01_@custc_daas_admin_ui.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for Device as a Service (DaaS) admin UI text content and role permissions",
    
    "components": [
        {
            "name": "Role Authorization",...

---

## 05_@custc_a1bi_update.sql

**Path**: `cuco.dbmaintain/sql/11/48_CuCo_V19.11/05_@custc_a1bi_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update customer contract text information in BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table maintenance",
  ...

---

## 03_@custc_bpb_v6_cleanup.sql

**Path**: `cuco.dbmaintain/sql/11/48_CuCo_V19.11/03_@custc_bpb_v6_cleanup.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database cleanup and text configuration script for A1 Backup Mobile Pro contract duration settings",
    "components": [
        {
            "name": "BITE_TEXT",
            "type"...

---

## 04_@app_cuco_kums_skz_shop.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/04_@app_cuco_kums_skz_shop.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for a KUMS shop table, providing an alias for cross-schema access",
    "components": [
        {
            "name": "cuco_kums_skz_shop",
            "ty...

---

## 06_@custc_etgtv2.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/06_@custc_etgtv2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database insertion script for ETGT V2 configuration in the CuCo system's point of view (POV) table",
    
    "components": [
        {
            "name": "cct_pov",
            "ty...

---

## 07_@custc_drop_old_seg_tables.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/07_@custc_drop_old_seg_tables.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database cleanup script to remove legacy segment-related tables and associated data structures from the CuCo system",
    "components": [
        {
            "name": "Database Clea...

---

## 02_@custc_bite_user.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/02_@custc_bite_user.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to refactor user-related foreign key relationships and data structures across multiple tables",
    
    "components": [
        {
            "name": "bite...

---

## 01_@custc_a1bnv2.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/01_@custc_a1bnv2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database insertion script for adding a configuration record to the cct_pov table, likely related to customer/contract configuration",
    
    "components": [
        {
            "...

---

## 03_@custc_cuco_kums_skz_shop.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/03_@custc_cuco_kums_skz_shop.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table for managing shop supervision/support relationships with associated permissions",
    "components": [
        {
            "name": "cuco_kums_skz_shop",
   ...

---

## 05_@custc_cct_pov_updates.sql

**Path**: `cuco.dbmaintain/sql/11/01_CuCo-V5.1.0/05_@custc_cct_pov_updates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database update script to modify PDF template association for a specific CCT POV configuration",
    
    "components": [
        {
            "name": "cct_pov",
            "type":...

---

## 01_@custc_a1bnv5.sql

**Path**: `cuco.dbmaintain/sql/11/07_CuCo_V15.11/01_@custc_a1bnv5.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Operation...

---

## 05_@custc_bite_auth_A1Coach_Update.sql

**Path**: `cuco.dbmaintain/sql/11/30_CuCo_V18.04.01/05_@custc_bite_auth_A1Coach_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization settings for A1Coach link functionality by updating BITE authentication and role mappings",
    
    "components": [
        {
            "na...

---

## 01_@custc_bite_text_ProductBrowser_Update.sql

**Path**: `cuco.dbmaintain/sql/11/30_CuCo_V18.04.01/01_@custc_bite_text_ProductBrowser_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in the BITE_TEXT table for product browser UI labels",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "data...

---

## 02_@dwh_mk_interaktion.sql

**Path**: `cuco.dbmaintain/sql/11/30_CuCo_V18.04.01/02_@dwh_mk_interaktion.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a CLOB column for storing interaction notes in the MK_INTERAKTION table",
    
    "components": [
        {
            "name": "MK_INTERAKTION",...

---

## 06_@custc_bite_text_searchViewValidationStrings.sql

**Path**: `cuco.dbmaintain/sql/11/30_CuCo_V18.04.01/06_@custc_bite_text_searchViewValidationStrings.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script to update validation patterns for user ID search fields in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table...

---

## 04_@custc_bite_text_fibv6.sql

**Path**: `cuco.dbmaintain/sql/11/30_CuCo_V18.04.01/04_@custc_bite_text_fibv6.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries for contract change type enumerations in the BITE_TEXT table, specifically for FIB V6 contract changes",
    
    "components": [
        {
   ...

---

## 03_@custc_mk_interaktion.sql

**Path**: `cuco.dbmaintain/sql/11/30_CuCo_V18.04.01/03_@custc_mk_interaktion.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add CLOB columns for interaction notes and create a view for MK_INTERAKTION tables",
    
    "components": [
        {
            "name": "MK...

---

## 04_@custc_a1bn_v11_text.sql

**Path**: `cuco.dbmaintain/sql/11/76_Cuco_V28.10/04_@custc_a1bn_v11_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update a URL link text in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table",
            "type": "database...

---

## 02_@custc_a1bi_v6_text.sql

**Path**: `cuco.dbmaintain/sql/11/76_Cuco_V28.10/02_@custc_a1bi_v6_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for inserting localized text/labels related to IP packet configuration and router settings",
    
    "components": [
        {
            "n...

---

## 03_@custc_a1bip_v1_text.sql

**Path**: `cuco.dbmaintain/sql/11/76_Cuco_V28.10/03_@custc_a1bip_v1_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating a yearly service fee label in multiple languages",
    
    "components": [
        {
            "name": "BITE_TEXT table operat...

---

## 01_@custc_add_a1bi_v6.sql

**Path**: `cuco.dbmaintain/sql/11/76_Cuco_V28.10/01_@custc_add_a1bi_v6.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update A1BI V6 product offering version configuration in CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Operatio...

---

## 01_@custc_bizkov2.sql

**Path**: `cuco.dbmaintain/sql/11/03_CuCo-V5.4.0/01_@custc_bizkov2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering versions (POV) for BIZKO business internet service with promotional periods",
    
    "components": [
        {
            "nam...

---

## 02_@custc_fibv2.sql

**Path**: `cuco.dbmaintain/sql/11/03_CuCo-V5.4.0/02_@custc_fibv2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering versions (POV) for FIB V2 product with different promotional periods",
    
    "components": [
        {
            "name": "CC...

---

## 01_@custc_a1bi_bussiness_firewall_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/01_@custc_a1bi_bussiness_firewall_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to configure business firewall feature authorization and role mappings",
    "components": [
        {
            "name": "BITE_AUTH",
            "type": "database_...

---

## 08_@custc_brian_cee_order_dao_#int.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/08_@custc_brian_cee_order_dao_#int.sql`

**Layer**: Data Access

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for setting up ESB access assignments and system settings for Brian CEE Order integration",
    "components": [
        {
            "name": "BITE_ESB_...

---

## 02_@custc_a1bi_add_quote_text_bussiness_firewall.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/02_@custc_a1bi_add_quote_text_bussiness_firewall.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text labels for Business Firewall UI components in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
    ...

---

## 05_@custc_a1bnv11_add_summary_section_mobile_subscription_texts.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/05_@custc_a1bnv11_add_summary_section_mobile_subscription_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for mobile subscription summary section in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": ...

---

## 09_@custc_brian_cee_order_dao_#prod.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/09_@custc_brian_cee_order_dao_#prod.sql`

**Layer**: Data Access

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for setting up ESB access assignments and system settings for Brian Cee Order functionality in production environment",
    
    "components": [
       ...

---

## 04_@custc_a1bnv10_add_summary_section_mobile_subscription_texts.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/04_@custc_a1bnv10_add_summary_section_mobile_subscription_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for mobile subscription summary section in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": ...

---

## 10_@custc_a1bi_add_quote_summary_text_bussiness_firewall.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/10_@custc_a1bi_add_quote_summary_text_bussiness_firewall.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update business firewall-related text labels in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table operation",
         ...

---

## 03_@custc_a1bip_admin_quote_text_show_business_firewall.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/03_@custc_a1bip_admin_quote_text_show_business_firewall.sql`

**Layer**: Backend Service

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script to update text labels for Business Internet Professional (BIP) section in the administration interface",
    
    "components": [
        {
            ...

---

## 11_@custc_gucci_buddy_auth.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/11_@custc_gucci_buddy_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for setting up Gucci Buddy authorization permissions and role assignments",
    
    "components": [
        {
            "name": "BITE_AUTH",
            "type": "d...

---

## 06_@custc_esb_asmp_environment.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/06_@custc_esb_asmp_environment.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for ESB (Enterprise Service Bus) access parameters across different environments (DEV, INT, PROD)",
    "components": [
        {
            "name": "BITE_ESB_A...

---

## 07_@custc_brian_cee_order_dao_#dev.sql

**Path**: `cuco.dbmaintain/sql/11/65_CuCo_V21.09/07_@custc_brian_cee_order_dao_#dev.sql`

**Layer**: Data Access

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for setting up ESB access assignments and system settings for Brian Cee Order functionality",
    
    "components": [
        {
            "name": "BI...

---

## 01_@custc_etgtv6.sql

**Path**: `cuco.dbmaintain/sql/11/12_CuCo_V16.06/01_@custc_etgtv6.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Product Offering Version (POV) records for ETGT product",
    "components": [
        {
            "name": "CCT_POV Table",
            "type":...

---

## 02_@custc_bizcov4.sql

**Path**: `cuco.dbmaintain/sql/11/12_CuCo_V16.06/02_@custc_bizcov4.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operations",
 ...

---

## 04_@custc_bpbv2.sql

**Path**: `cuco.dbmaintain/sql/11/12_CuCo_V16.06/04_@custc_bpbv2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating Product Offering Version (POV) records in the CCT_POV table, specifically handling BPB (Business Product Bundle) version transitions",
    
 ...

---

## 03_@custc_pshcv1.sql

**Path**: `cuco.dbmaintain/sql/11/12_CuCo_V16.06/03_@custc_pshcv1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for adding Public Sector Health Care product offering and version configuration",
    
    "components": [
        {
            "name": "Product Offer...

---

## 04_@custc_marketing_product__add_text.sql

**Path**: `cuco.dbmaintain/sql/11/61_CuCo_V21.04/04_@custc_marketing_product__add_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for marketing product UI labels in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "dat...

---

## 01_@custc_add_a1bi_v5.sql

**Path**: `cuco.dbmaintain/sql/11/61_CuCo_V21.04/01_@custc_add_a1bi_v5.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product offering version (POV) data for A1BI V5 product in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV T...

---

## 02_@custc_a1bi_v5_text.sql

**Path**: `cuco.dbmaintain/sql/11/61_CuCo_V21.04/02_@custc_a1bi_v5_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for managing text entries in the BITE_TEXT table, specifically for customer-facing text configurations related to A1 Business Internet services",
    
    "components": [
...

---

## 03_@custc_a1bip_update_admin_quote_text.sql

**Path**: `cuco.dbmaintain/sql/11/61_CuCo_V21.04/03_@custc_a1bip_update_admin_quote_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates localized text entries in the BITE_TEXT table for admin configurable list selector UI components with German translations",
    
    "components": [
        {
            "na...

---

## 01_@custc_bite_text_Merlin4Business.sql

**Path**: `cuco.dbmaintain/sql/11/35_CuCo_V18.07.2/01_@custc_bite_text_Merlin4Business.sql`

**Layer**: Backend Service

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels in BITE_TEXT table for customer communication templates",
    
    "components": [
        {
            "name": "BITE_TEXT table ma...

---

## 03_@custc_Auth_Assignment.sql

**Path**: `cuco.dbmaintain/sql/11/35_CuCo_V18.07.2/03_@custc_Auth_Assignment.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization permissions for quote viewing functionality",
    "components": [
        {
            "name": "bite_auth",
            "type": "database_tab...

---

## 04_@custc_numberOfTemplatesError_Label.sql

**Path**: `cuco.dbmaintain/sql/11/35_CuCo_V18.07.2/04_@custc_numberOfTemplatesError_Label.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update error message text for template number validation in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table Operation...

---

## 06_@custc_bite_text_admin_textUpdates.sql

**Path**: `cuco.dbmaintain/sql/11/35_CuCo_V18.07.2/06_@custc_bite_text_admin_textUpdates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating localized UI text entries in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT",
            "ty...

---

## 05_@custc_numberOfTemplatesError_UpdatedLabel.sql

**Path**: `cuco.dbmaintain/sql/11/35_CuCo_V18.07.2/05_@custc_numberOfTemplatesError_UpdatedLabel.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update error message text for template number validation",
    
    "components": [
        {
            "name": "BITE_TEXT table operations",
            "type":...

---

## 02_@custc_Auth_Product_Browser_Additional_Info_Icon.sql

**Path**: `cuco.dbmaintain/sql/11/35_CuCo_V18.07.2/02_@custc_Auth_Product_Browser_Additional_Info_Icon.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing authorization settings and text resources for a product browser interface",
    
    "components": [
        {
            "name": "Authorization Managem...

---

## 03_@custc_a1bi_v8_cleanup.sql

**Path**: `cuco.dbmaintain/sql/11/84_CuCo_V24.08/03_@custc_a1bi_v8_cleanup.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database cleanup script to remove a specific UI configuration field (showProfessionalPaketField) from calcTool.A1BI",
    "components": [
        {
            "name": "calcTool.A1BI...

---

## 01_@custc_add_a1bi_v8.sql

**Path**: `cuco.dbmaintain/sql/11/84_CuCo_V24.08/01_@custc_add_a1bi_v8.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Point of View (POV) records for A1BI V8 product offering",
    "components": [
        {
            "name": "CCT_POV Table Operations",
       ...

---

## 02_@custc_a1bi_v8_text.sql

**Path**: `cuco.dbmaintain/sql/11/84_CuCo_V24.08/02_@custc_a1bi_v8_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for internationalization/localization of UI labels and messages related to IP packet and router configurations",
    
    "components": [
    ...

---

## 04_@custc_bite_text_A1BN_ETGT_Update.sql

**Path**: `cuco.dbmaintain/sql/11/31_CuCo_V18.05.1/04_@custc_bite_text_A1BN_ETGT_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and tooltips for business tariff plans in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table Updates"...

---

## 01_@custc_bite_text_ProductBrowser_Update.sql

**Path**: `cuco.dbmaintain/sql/11/31_CuCo_V18.05.1/01_@custc_bite_text_ProductBrowser_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text content in the BITE_TEXT table for product browser UI labels",
    
    "components": [
        {
            "name": "BITE_TEXT Table",
  ...

---

## 02_@custc_bite_text_ProductBrowser_InsuranceBroker.sql

**Path**: `cuco.dbmaintain/sql/11/31_CuCo_V18.05.1/02_@custc_bite_text_ProductBrowser_InsuranceBroker.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text entries for an insurance product browser interface, specifically for insurance broker-related UI elements",
    
    "components": [
     ...

---

## 06_@custc_bite_text_ProductBrowser_InsuranceBrokerNew.sql

**Path**: `cuco.dbmaintain/sql/11/31_CuCo_V18.05.1/06_@custc_bite_text_ProductBrowser_InsuranceBrokerNew.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for product browser insurance broker related labels in German language",
    
    "components": [
        {
            "nam...

---

## 05_@custc_bite_text_staticInformation_DateType.sql

**Path**: `cuco.dbmaintain/sql/11/31_CuCo_V18.05.1/05_@custc_bite_text_staticInformation_DateType.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update static text information for date value label in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table op...

---

## 03_@custc_bite_text_staticInformation_DateType.sql

**Path**: `cuco.dbmaintain/sql/11/31_CuCo_V18.05.1/03_@custc_bite_text_staticInformation_DateType.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update static text information for date value labels in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table O...

---

## 01_@custc_a1bnv4.sql

**Path**: `cuco.dbmaintain/sql/11/04_CuCo-V5.5.0/01_@custc_a1bnv4.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering version data in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operations",
            "type":...

---

## 02_@custc_a1bnv3.sql

**Path**: `cuco.dbmaintain/sql/11/02_CuCo-V5.2.0/02_@custc_a1bnv3.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CuCo system",
    "components": [
        {
            "name": "CCT_POV Table Operations",
   ...

---

## 01_@custc_update_role_bite_tables.sql

**Path**: `cuco.dbmaintain/sql/11/02_CuCo-V5.2.0/01_@custc_update_role_bite_tables.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update role names and relationships across multiple BITE system tables while maintaining referential integrity",
    
    "components": [
        {
     ...

---

## 01_@custc_bite_text_search_OneTV.sql

**Path**: `cuco.dbmaintain/sql/11/29_CuCo_V18.03.02/01_@custc_bite_text_search_OneTV.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text search labels and validation messages for OneTV user interface",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "type"...

---

## 05_@custc_bite_text_PRODtexts_updated.sql

**Path**: `cuco.dbmaintain/sql/11/29_CuCo_V18.03.02/05_@custc_bite_text_PRODtexts_updated.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for updating text labels and messages in the BITE_TEXT table, primarily focused on SIM card tariff-related content and UI labels",
    
    "components": [
        {
...

---

## 02_@custc_bite_text_search_BvkUserId.sql

**Path**: `cuco.dbmaintain/sql/11/29_CuCo_V18.03.02/02_@custc_bite_text_search_BvkUserId.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for BVK user search functionality in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "d...

---

## 03_@custc_bite_text_a1TvRes_InternetTvTab.sql

**Path**: `cuco.dbmaintain/sql/11/29_CuCo_V18.03.02/03_@custc_bite_text_a1TvRes_InternetTvTab.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text labels and translations for an Internet/TV service interface, specifically for A1 TV residential customer portal",
    
    "components": [
        ...

---

## 04_@custc_bite_text_adminHeader_update.sql

**Path**: `cuco.dbmaintain/sql/11/29_CuCo_V18.03.02/04_@custc_bite_text_adminHeader_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update system message header text in BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table Operation",
            ...

---

## 04_@custc_bite_text_newProductOverview.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/04_@custc_bite_text_newProductOverview.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to populate localized text labels for a product overview interface in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "ty...

---

## 01_@custc_alter_attribute_newColumns.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/01_@custc_alter_attribute_newColumns.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add TEXT_VALUE and VALID_VALUES columns to existing attribute-related tables",
    
    "components": [
        {
            "name": "si_attri...

---

## 08_@custc_bite_text_newProductBrowserTableView.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/08_@custc_bite_text_newProductBrowserTableView.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for product overview UI labels and messages",
    "components": [
        {
            "name": "BITE_TEXT",
            "ty...

---

## 06_@custc_newProductBrowser_role.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/06_@custc_newProductBrowser_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script that adds a new role for product browser functionality",
    "components": [
        {
            "name": "BITE_ROLE",
            "type": "databa...

---

## 09_@custc_bite_text_updateCalcTool.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/09_@custc_bite_text_updateCalcTool.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for contract change types and additional options information related to A1 Dual Power Pro service",
    
    "components": [...

---

## 07_@custc_bite_text_update_tooltipChange.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/07_@custc_bite_text_update_tooltipChange.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates tooltip text values in the BITE_TEXT database table for various internet speed options across different product configurations",
    "components": [
        {
            "na...

---

## 02_@custc_bite_txt_comboboxAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/02_@custc_bite_txt_comboboxAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update combo box text values in the BITE_TEXT table for sales information display",
    
    "components": [
        {
            "name": "BITE_TEXT T...

---

## 03_@custc_bite_text_Dual_Power_BPB.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/03_@custc_bite_text_Dual_Power_BPB.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localized text entries for Dual Power BPB (Business Product Bundle) additional options in German language",
    
    "components": [
        {
            "...

---

## 05_@custc_bite_text_update_BPB.sql

**Path**: `cuco.dbmaintain/sql/11/20_CuCo_V17.07/05_@custc_bite_text_update_BPB.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for contract change types related to Dual Power upgrades and downgrades",
    
    "components": [
        {
            "na...

---

## 01_@custc_a1psv2_texts.sql

**Path**: `cuco.dbmaintain/sql/11/72_CuCo_V22.06/01_@custc_a1psv2_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text labels and tooltips for voucher code functionality in the A1PS system",
    "components": [
        {
            "name": "BITE_TEXT",
            "typ...

---

## 02_@custc_etgtv12_texts.sql

**Path**: `cuco.dbmaintain/sql/11/72_CuCo_V22.06/02_@custc_etgtv12_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for ETGT tariff promotion labels",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_table",
      ...

---

## 03_@custc_gamificationMessages.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/03_@custc_gamificationMessages.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and manages a database table for storing gamification messages and user interactions with those messages",
    
    "components": [
        {
            "name": "GAMIFICATIO...

---

## 05_@custc_bite_text_GamificationEmailRegexValidationUiTextEditable.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/05_@custc_bite_text_GamificationEmailRegexValidationUiTextEditable.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script to update email validation regex pattern in BITE_TEXT table for contact person form validation",
    
    "components": [
        {
            "name": ...

---

## 07_@custc_bite_text_cct_NewContactPersonTexts.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/07_@custc_bite_text_cct_NewContactPersonTexts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localized text entries for contact person related UI labels in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            ...

---

## 06_@custc_bite_text_A1BNv8_ETGTv10_New_Daten_Fields.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/06_@custc_bite_text_A1BNv8_ETGTv10_New_Daten_Fields.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text labels and tooltips for A1 data package offerings in multiple versions (A1BNv8 and ETGTv10)",
    
    "components": [
        {
            "name":...

---

## 08_@custc_bite_text_ETGTv10_New_Handygarantie_Field.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/08_@custc_bite_text_ETGTv10_New_Handygarantie_Field.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates text labels in BITE_TEXT table for mobile phone insurance categories with German translations",
    
    "components": [
        {
            "name": "BITE_TEXT",
          ...

---

## 01_@custc_pshcv4_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/01_@custc_pshcv4_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) Calculation Tool, specifically for PSHC v4 product, focusing on text label configurations",
    
    "components": [
     ...

---

## 02_@custc_pshcv4_activation.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/02_@custc_pshcv4_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update Point of View (POV) configurations for PSHC product version management",
    
    "components": [
        {
            "name": "CCT_POV Table Ope...

---

## 04_@custc_bite_text_ETGT_V10_XmasPromo_Update.sql

**Path**: `cuco.dbmaintain/sql/11/25_CuCo_V18.01.01/04_@custc_bite_text_ETGT_V10_XmasPromo_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels in BITE_TEXT table, replacing Christmas promotion related labels with generic promotion labels",
    
    "components": [
        {
            ...

---

## 06_@custc_a1bnv11_text_festnetzNummernKonfiguration.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/06_@custc_a1bnv11_text_festnetzNummernKonfiguration.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels for Festnetz (landline) number configuration in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_T...

---

## 03_@custc_cuco_Links_dataUpdate_#prod.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/03_@custc_cuco_Links_dataUpdate_#prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update contract summary link information in the CUCO_LINKS table",
    "components": [
        {
            "name": "CUCO_LINKS Table Operation",
    ...

---

## 01_@custc_cuco_Links_dataUpdate_#dev.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/01_@custc_cuco_Links_dataUpdate_#dev.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update contract summary link configuration in CUCO_LINKS table",
    
    "components": [
        {
            "name": "CUCO_LINKS Table Operation",
 ...

---

## 05_@custc_a1bnv11_texts.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/05_@custc_a1bnv11_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for customer configuration labels in German language",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
       ...

---

## 04_@custc_bite_role_auth_update_Links.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/04_@custc_bite_role_auth_update_Links.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update authorization settings and text resources for the Links portlet in the CuCo system",
    
    "components": [
        {
            "name": "Authorization M...

---

## 02_@custc_cuco_Links_dataUpdate_#int.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/02_@custc_cuco_Links_dataUpdate_#int.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update contract summary link configuration in CUCO_LINKS table",
    
    "components": [
        {
            "name": "CUCO_LINKS Table Operation",
 ...

---

## 07_@custc_productbrowser_table_pagesize.sql

**Path**: `cuco.dbmaintain/sql/11/67_CuCo_V21.11/07_@custc_productbrowser_table_pagesize.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script to set the page size for product browser table view in the BITE_SETTING table",
    
    "components": [
        {
            "name": "BITE_SETTING",
          ...

---

## 06_@custc_update_vbm_custc_table_control_flags.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/06_@custc_update_vbm_custc_table_control_flags.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update control flags for VBM-related tables in the custc_table_control configuration",
    
    "components": [
        {
            "name": "custc_ta...

---

## 01_@custc_SI_History_table.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/01_@custc_SI_History_table.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a history notes table for storing SI (Service Item) related historical information with indexing and access permissions",
    
    "components": [
        {
            "name...

---

## 05_@custc_alter_todoGroup_creator_note_size.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/05_@custc_alter_todoGroup_creator_note_size.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter the size of the CREATOR_NOTE_TEXT column in the SI_TODO_GROUP_NOTE table to accommodate larger text content",
    
    "components": [
        {
            "name": "SI_TODO_GR...

---

## 02_@app_SI_History_Synonym.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/02_@app_SI_History_Synonym.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for SI_HISTORY_NOTE table, providing an alias to access the table from a different schema (custc)",
    "components": [
        {
            "name": "SI_H...

---

## 04_@custc_etgtv8.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/04_@custc_etgtv8.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Product Offering Version (POV) records for ETGT product versions",
    
    "components": [
        {
            "name": "CCT_POV Table Operati...

---

## 03_@custc_alter_historyNote_add_historyNoteId.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/03_@custc_alter_historyNote_add_historyNoteId.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter the si_history_note table to add a new numeric column history_note_id",
    "components": [
        {
            "name": "si_history_note table",
            "type": "database...

---

## 07_@custc_bite_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/16_CuCo_V17.03/07_@custc_bite_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for populating the BITE_TEXT table with localized text content and tooltips",
    
    "components": [
        {
            "name": "bite_text",
     ...

---

## 02_@custc_update_a1bi_v5_text.sql

**Path**: `cuco.dbmaintain/sql/11/63_CuCo_V21.06/02_@custc_update_a1bi_v5_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating text configurations in BITE_TEXT table related to A1 business information",
    "components": [
        {
            "name": "BITE_TEXT Tabl...

---

## 01_@custc_update_a1bip_v1_text.sql

**Path**: `cuco.dbmaintain/sql/11/63_CuCo_V21.06/01_@custc_update_a1bip_v1_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text localization update script for connection type enumerations",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_table",
     ...

---

## 05_@custc_bite_text_MVP_Productbrowser_PLZ.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/05_@custc_bite_text_MVP_Productbrowser_PLZ.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels for product overview address display in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT tabl...

---

## 02_@custc_bite_text_productbrowser.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/02_@custc_bite_text_productbrowser.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text labels (internationalization/localization) in the BITE_TEXT table for a product browser interface",
    
    "components": [
        {
          ...

---

## 07_@custc_bite_text_Merlin4Business.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/07_@custc_bite_text_Merlin4Business.sql`

**Layer**: Backend Service

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels for contract duration options in the BITE_TEXT table, specifically for A1 Backup Mobile Pro service",
    
    "components": [
     ...

---

## 01_@custc_bite_text_and_Auths_MVP_Productbrowser.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/01_@custc_bite_text_and_Auths_MVP_Productbrowser.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script for setting up authorization and text configurations for a product browser feature",
    
    "components": [
        {
            "name": "BITE_TEXT",
   ...

---

## 04_@custc_bite_text_Merlin4Business.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/04_@custc_bite_text_Merlin4Business.sql`

**Layer**: Backend Service

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text entries in the BITE_TEXT table, specifically for contract change types and contract duration labels",
    
    "components": [
        {
 ...

---

## 03_@custc_bite_text_admin_textUpdates.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/03_@custc_bite_text_admin_textUpdates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating mobile phone insurance and router configuration labels/info in the BITE_TEXT table",
    
    "components": [
        {
         ...

---

## 06_@custc_bite_text_MVP_Productbrowser.sql

**Path**: `cuco.dbmaintain/sql/11/34_CuCo_V18.07.1/06_@custc_bite_text_MVP_Productbrowser.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and tooltips for product browser interface in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "t...

---

## 03_@custc_a1biV1_activation.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/03_@custc_a1biV1_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update A1BI V1 product offering version configuration in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation",
            "...

---

## 01_@custc_a1biV1.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/01_@custc_a1biV1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering data for A1 Business Internet service",
    "components": [
        {
            "name": "Product Offering Management",
        ...

---

## 04_@custc_bite_text_a1bi_V1_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/04_@custc_bite_text_a1bi_V1_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for text/label configurations related to A1 Business Internet (A1BI) product in the CuCo (Customer Configuration) system",
    
    "components": [
        ...

---

## 07_@custc_bite_text_a1bn_basic_package_pur.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/07_@custc_bite_text_a1bn_basic_package_pur.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localization text entries for a basic package feature related to PUR (Purchase) functionality",
    "components": [
        {
            "name": "BITE_TEXT...

---

## 10_@custc_bite_text_admin_textUpdates2.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/10_@custc_bite_text_admin_textUpdates2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating customer-facing text labels and messages in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Ta...

---

## 06_@custc_bite_text_A1_Marketplace.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/06_@custc_bite_text_A1_Marketplace.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels for A1 Marketplace product browser interface",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_t...

---

## 02_@custc_role_auth_update.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/02_@custc_role_auth_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates role-based authorization configuration for A1 Business Internet quote feature",
    "components": [
        {
            "name": "bite_role_auth",
            "type": "datab...

---

## 09_@custc_bite_text_admin_textUpdates.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/09_@custc_bite_text_admin_textUpdates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update tooltip text entries for language channel configurations in the BITE_TEXT table, specifically for NUVS migration customers",
    
    "components": [
      ...

---

## 05_@custc_bite_text_A1_Connect_Plus.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/05_@custc_bite_text_A1_Connect_Plus.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for A1 Connect Plus UI components in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "d...

---

## 08_@custc_bite_text_FIB_BIZKO_BPB_PSHC_A1BI_oanGpon.sql

**Path**: `cuco.dbmaintain/sql/11/36_CuCo_V18.08.1/08_@custc_bite_text_FIB_BIZKO_BPB_PSHC_A1BI_oanGpon.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text entries related to OAN GPON configuration across multiple modules (FIB, BIZKO, BPB)",
    "components": [
        {
            "name": "B...

---

## 05_@custc_etgtv5.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/05_@custc_etgtv5.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update Point of View (POV) records for ETGT product versions",
    "components": [
        {
            "name": "CCT_POV Table Operations",
            ...

---

## 07_@custc_pov_history.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/07_@custc_pov_history.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and configures a history table for Point of View (POV) data with user tracking and timestamps",
    "components": [
        {
            "name": "CCT_POV_HISTORY",
         ...

---

## 03_@custc_lead.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/03_@custc_lead.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema definition for managing lead/prospect contact information in a customer management system",
    "components": [
        {
            "name": "lead table",
          ...

---

## 12_@custc_addRolesForNC.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/12_@custc_addRolesForNC.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to add role definitions for non-customer (NC) functionality in the system",
    
    "components": [
        {
            "name": "bite_role table",
            "typ...

---

## 01_@custc_a1bnv6.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/01_@custc_a1bnv6.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operations",
 ...

---

## 10_@custc_alterLead_addUserFields.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/10_@custc_alterLead_addUserFields.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add user-related fields to the lead table with corresponding indexes",
    
    "components": [
        {
            "name": "lead table modif...

---

## 13_@app_lead_pov_history_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/13_@app_lead_pov_history_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for lead and POV (Point of View) history tables and sequences in the CUSTC schema",
    "components": [
        {
            "name": "lead synonym",
      ...

---

## 02_@custc_cct_a1cmlv2.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/02_@custc_cct_a1cmlv2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating Product Offering Version (POV) records in the CCT system",
    
    "components": [
        {
            "name": "CCT_POV Table",
          ...

---

## 06_@custc_role_prod_conf_admin.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/06_@custc_role_prod_conf_admin.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script that adds a product deployment owner role to the system",
    "components": [
        {
            "name": "bite_role",
            "type": "datab...

---

## 08_@custc_cct_opportunity_lead_id.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/08_@custc_cct_opportunity_lead_id.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add lead tracking capability to opportunities by adding a LEAD_ID column and corresponding index",
    
    "components": [
        {
            "nam...

---

## 09_@custc_alterLead.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/09_@custc_alterLead.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add lead-customer merge tracking capabilities",
    "components": [
        {
            "name": "lead table modification",
            "type"...

---

## 11_@custc_alterLead_addMergeByUserFields.sql

**Path**: `cuco.dbmaintain/sql/11/10_CuCo_V16.03/11_@custc_alterLead_addMergeByUserFields.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add tracking fields for lead merging operations",
    
    "components": [
        {
            "name": "lead table",
            "type": "database_t...

---

## 01_@custc_pshcv4_update.sql

**Path**: `cuco.dbmaintain/sql/11/47_CuCo_V19.10/01_@custc_pshcv4_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating text labels and enums in the CuCo Calculation Tool for PSHC product version 4",
    
    "components": [
        {
            "name": "BITE_...

---

## 03_@custc_bite_text_productbrowser_update.sql

**Path**: `cuco.dbmaintain/sql/11/47_CuCo_V19.10/03_@custc_bite_text_productbrowser_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and translations in the BITE_TEXT table for a product browser interface, focusing on regional promotion-related UI elements",
    
    "componen...

---

## 02_@custc_a1biv3_update.sql

**Path**: `cuco.dbmaintain/sql/11/47_CuCo_V19.10/02_@custc_a1biv3_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating text entries related to A1 Business Internet (A1BI) calculation tool version 3",
    
    "components": [
        {
            "name": "bite...

---

## 04_@custc_update_trx_validationerror.sql

**Path**: `cuco.dbmaintain/sql/11/47_CuCo_V19.10/04_@custc_update_trx_validationerror.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates validation error message text in the bite_text table for a specific transaction validation key",
    
    "components": [
        {
            "name": "bite_text",
         ...

---

## 05_@dwh_VBM_CUSTC_DWH.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/05_@dwh_VBM_CUSTC_DWH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation for a VBM (Value-Based Management) system focusing on product scoring and feedback management",
    
    "components": [
        {
            "name": "VBM_P...

---

## 12_@custc_USERSHOPASSIGNMENT.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/12_@custc_USERSHOPASSIGNMENT.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to manage user-shop assignments, establishing a many-to-many relationship between users and shops",
    
    "components": [
        {
            "name": "C...

---

## 16_@custc_grant_usershopassignments.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/16_@custc_grant_usershopassignments.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database permission management script granting CRUD operations access to specific tables for a customer application user",
    
    "components": [
        {
            "name": "GRA...

---

## 07_@app_VBM_CUSTC_APP.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/07_@app_VBM_CUSTC_APP.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database synonym creation script for VBM (Value-Based Management) related tables in the CUSTC schema",
    "components": [
        {
            "name": "Database Synonyms",
        ...

---

## 10_@app_Appointments_Synonym.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/10_@app_Appointments_Synonym.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for appointment notes table, providing an alternative name for accessing the table across different schemas",
    "components": [
        {
            "na...

---

## 18_@custc_ToDoGroup_table.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/18_@custc_ToDoGroup_table.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and configures a todo group note tracking system with database tables and relationships",
    "components": [
        {
            "name": "SI_TODO_GROUP_NOTE",
            ...

---

## 17_@app_synonyms_for_usershopassignments.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/17_@app_synonyms_for_usershopassignments.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for user shop assignment tables to provide alias access to tables in the CUSTC schema",
    "components": [
        {
            "name": "CUCO_USERSHOPASSI...

---

## 04_@custc_bpbv3.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/04_@custc_bpbv3.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating Product Offering Version (POV) records in the CuCo system",
    "components": [
        {
            "name": "CCT_POV Table",
            "t...

---

## 11_@custc_ANSPRECHPARTNER_CUCO.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/11_@custc_ANSPRECHPARTNER_CUCO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store contact person (Ansprechpartner) information for customers in the CuCo system, with local storage and no DWH synchronization",
    
    "components"...

---

## 06_@custc_VBM_CUSTC.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/06_@custc_VBM_CUSTC.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema definition for a Value-Based Management (VBM) system tracking products, scoring, and feedback",
    "components": [
        {
            "name": "Product Management"...

---

## 19_@app_ToDoGroup_Synonym.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/19_@app_ToDoGroup_Synonym.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for a todo group note table, providing an alternative name for accessing the table across different schemas",
    "components": [
        {
            "na...

---

## 02_@custc_fibv4.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/02_@custc_fibv4.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Product Offering Version (POV) records for FIB (Business Internet) product",
    
    "components": [
        {
            "name": "CCT_POV Tab...

---

## 09_@custc_Appointments_table.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/09_@custc_Appointments_table.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table for storing appointment notes with communication details and establishes related permissions",
    
    "components": [
        {
            "name": "si_app...

---

## 08_@custc_VBM_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/08_@custc_VBM_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms in CUSTC schema for VBM (Value-Based Management) related tables in CUSTC_DWH schema, enabling cross-schema access to VBM data objects",
    "components": [
...

---

## 01_@custc_a1bnv8.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/01_@custc_a1bnv8.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to manage product offering versions (POV) in the CCT_POV table, specifically handling A1BN version transitions",
    
    "components": [
        {
      ...

---

## 03_@custc_bizcov6.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/03_@custc_bizcov6.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operations",
 ...

---

## 15_@custc_CUCO_USERASSIGNMENTLOGS.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/15_@custc_CUCO_USERASSIGNMENTLOGS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a logging table to track user shop assignment activities",
    "components": [
        {
            "name": "CUCO_USERSHOPASSIGNMENTLOGS",
            "type": "database_tabl...

---

## 13_@app_CUCO_ANSPRECHPARTNER_additionalChanges.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/13_@app_CUCO_ANSPRECHPARTNER_additionalChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym CUCO_ANSPRECHPARTNER that points to CUSTC.CUCO_ANSPRECHPARTNER table/view",
    "components": [
        {
            "name": "CUCO_ANSPRECHPARTNER",
     ...

---

## 14_@custc_alter_sbs_product_nots.sql

**Path**: `cuco.dbmaintain/sql/11/15_CuCo_V17.02/14_@custc_alter_sbs_product_nots.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter table script to add a contact person reference column to the SBS product notes table",
    
    "components": [
        {
            "name": "si_vi_sbs_product_note",
        ...

---

## 01_@custc_bite_text_admin_textUpdates.sql

**Path**: `cuco.dbmaintain/sql/11/41_CuCo_V19.02.1/01_@custc_bite_text_admin_textUpdates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating business-related labels and tooltips in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT T...

---

## 03_@custc_bite_text_GFP1000_update.sql

**Path**: `cuco.dbmaintain/sql/11/41_CuCo_V19.02.1/03_@custc_bite_text_GFP1000_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries for internet speed options (1000 Mbit/s) in multiple product configurations",
    
    "components": [
        {
            "name": "BITE_TEXT...

---

## 02_@custc_bite_text_M4BDualPower_PSHC.sql

**Path**: `cuco.dbmaintain/sql/11/41_CuCo_V19.02.1/02_@custc_bite_text_M4BDualPower_PSHC.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localization text entries for Dual Power configuration options in a PSHC (presumably Power/Smart Home Control) system",
    
    "components": [
        {
 ...

---

## 09_@custc_bite_text_A1_mobile_internet_BUS_tarif_name_change.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/09_@custc_bite_text_A1_mobile_internet_BUS_tarif_name_change.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates text labels for A1 Mobile Internet Business tariff names in the BITE_TEXT table, changing them to simplified S, M, L designations",
    
    "components": [
        {
       ...

---

## 07_@custc_bite_text_ETGT_V10_XmasPromo.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/07_@custc_bite_text_ETGT_V10_XmasPromo.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localized text entries for a promotional UI component in the ETGT V10 Christmas Promotion feature",
    
    "components": [
        {
            "name": "...

---

## 01_@custc_fibv6_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/01_@custc_fibv6_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for customer configuration tool (CuCo) text labels and UI elements for FIB v6 product",
    
    "components": [
        {
            "name": "BITE_TEXT ta...

---

## 06_@custc_bizkov8_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/06_@custc_bizkov8_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) tool's text labels and configurations specific to Business Kombi V8 product",
    
    "components": [
        {
         ...

---

## 02_@custc_fibV6_activation.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/02_@custc_fibV6_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to activate FIB V6 product offering variant and deactivate FIB V5",
    "components": [
        {
            "name": "CCT_POV table operations",
          ...

---

## 05_@custc_bizkoV8_activation.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/05_@custc_bizkoV8_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update BIZKO product offering versions by activating V8 and deactivating V7",
    
    "components": [
        {
            "name": "CCT_POV Table Opera...

---

## 04_@custc_bpbV5_activation.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/04_@custc_bpbV5_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update BPB (Business Product Bundle) version configurations in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation...

---

## 03_@custc_bpbv5_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/03_@custc_bpbv5_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) tool text labels, specifically for BPB (Breitband Pro Business) v5 product configuration",
    
    "components": [
      ...

---

## 08_@custc_si_note_finalize_flag.sql

**Path**: `cuco.dbmaintain/sql/11/24_CuCo_V17.11/08_@custc_si_note_finalize_flag.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification and text resource management for note finalization functionality",
    "components": [
        {
            "name": "si_note table",
            "type":...

---

## 03_@custc_customer_worthclass.sql

**Path**: `cuco.dbmaintain/sql/11/50_CuCo_V20.03/03_@custc_customer_worthclass.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels for customer worth class tiering in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT",
      ...

---

## 01_@custc_add_mobile_signature_auth.sql

**Path**: `cuco.dbmaintain/sql/11/50_CuCo_V20.03/01_@custc_add_mobile_signature_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage mobile view authorization feature by updating authentication records",
    
    "components": [
        {
            "name": "BITE_AUTH table",
           ...

---

## 02_@custc_mobile_signature_text.sql

**Path**: `cuco.dbmaintain/sql/11/50_CuCo_V20.03/02_@custc_mobile_signature_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text entries related to customer cockpit permissions and signature functionality in multiple languages",
    "components": [
        {
            "name"...

---

## 02_@custc_etgtv3.sql

**Path**: `cuco.dbmaintain/sql/11/06_CuCo_V15.08/02_@custc_etgtv3.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering version (POV) data for ETGT V3 and deprecate ETGT V2",
    
    "components": [
        {
            "name": "CCT_POV table oper...

---

## 01_@custc_cct_a1cml.sql

**Path**: `cuco.dbmaintain/sql/11/06_CuCo_V15.08/01_@custc_cct_a1cml.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for A1 Cloud Managed LAN product offering configuration",
    "components": [
        {
            "name": "cct_productoffering",
            "type": ...

---

## 01_@custc_add_a1ps_v2.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/01_@custc_add_a1ps_v2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update A1PS V2 product offering variant (POV) configuration in CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Op...

---

## 03_@custc_a1voip_text.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/03_@custc_a1voip_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text labels/messages in multiple languages for a VoIP/telephony system interface",
    "components": [
        {
            "name": "BITE_TEXT",
       ...

---

## 05_@custc_a1bn_v9_text.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/05_@custc_a1bn_v9_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text resource management script for customer configuration module (CuCo) containing localized text entries",
    
    "components": [
        {
            "name": "bite_tex...

---

## 06_@custc_marketplace.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/06_@custc_marketplace.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating marketplace-related display text configurations and PDF template settings",
    "components": [
        {
            "name": "CCT_POV",
    ...

---

## 07_@custc_cct_texts.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/07_@custc_cct_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content maintenance script for updating and inserting localized text entries in the BITE_TEXT table, primarily focused on marketplace product-related labels and tooltip...

---

## 02_@custc_a1ps_v2_text.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/02_@custc_a1ps_v2_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text localization script for A1 Payment Service customer interface, inserting German language text labels and messages",
    "components": [
        {
            "name": "B...

---

## 04_@custc_add_a1bn_v9.sql

**Path**: `cuco.dbmaintain/sql/11/54_CuCo_V20.07/04_@custc_add_a1bn_v9.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Product Offering Version (POV) data for A1BN V9 product",
    "components": [
        {
            "name": "CCT_POV Table Operation",
         ...

---

## 01_@custc_a1psV1.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/01_@custc_a1psV1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering and POV (Point of View) data for A1PS V1 payment system",
    "components": [
        {
            "name": "Data Cleanup",
     ...

---

## 09_@custc_a1ps_v1biteText_updation.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/09_@custc_a1ps_v1biteText_updation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for payment card and transaction-related UI elements in a multilingual system",
    
    "components": [
        {
            "name": "BITE_TEX...

---

## 05_@custc_role_auth_update.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/05_@custc_role_auth_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates role-based authorization mappings for CCT (Customer Care Tool) feature access, specifically for new quote functionality A1PS",
    
    "components": [
        {
            ...

---

## 06_@custc_QuoteClearance_Bite_TextChanges.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/06_@custc_QuoteClearance_Bite_TextChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update menu text for Quote Validation Configuration in the admin interface",
    
    "components": [
        {
            "name": "BITE_TEXT",
      ...

---

## 04_@custc_bite_text_a1ps_V1_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/04_@custc_bite_text_a1ps_V1_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for A1 Payment Service (A1PS) text configurations in multiple languages",
    "components": [
        {
            "name": "bite_text",
            "type":...

---

## 03_@custc_a1psV1_activation.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/03_@custc_a1psV1_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product offering variant (POV) data for A1PS V1 product in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV T...

---

## 08_@custc_herbspromo_text.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/08_@custc_herbspromo_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and tooltips for business tariff plans in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table Operatio...

---

## 02_@custc_role_auth_update.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/02_@custc_role_auth_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update role-based authorization for A1 Payment quote feature",
    
    "components": [
        {
            "name": "bite_role_auth",
            "type": "databa...

---

## 07_@custc_myOpportunities_filtername_correction.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/07_@custc_myOpportunities_filtername_correction.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels/translations in the BITE_TEXT table for opportunity-related UI elements and filters",
    
    "components": [
        {
            "name": "BI...

---

## 10_@custc_bite_text_admin_textUpdates.sql

**Path**: `cuco.dbmaintain/sql/11/39_CuCo_V18.10.1/10_@custc_bite_text_admin_textUpdates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for updating text content in BITE_TEXT table with localized German messages for various UI components and tooltips",
    
    "components": [
        {
            "n...

---

## 02_@custc_gucci_oneCockpitTab_auth.sql

**Path**: `cuco.dbmaintain/sql/11/74_Cuco_V26.08/02_@custc_gucci_oneCockpitTab_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to add authorization configuration for OneCockpit product link tab visibility",
    
    "components": [
        {
            "name": "BITE_AUTH",
            "type": "au...

---

## 01_@custc_cuco_Links_oneCockpit_#int.sql

**Path**: `cuco.dbmaintain/sql/11/74_Cuco_V26.08/01_@custc_cuco_Links_oneCockpit_#int.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update a link configuration for 'One Cockpit' in the CUCO_LINKS table",
    
    "components": [
        {
            "name": "CUCO_LINKS Table Operat...

---

## 01_@custc_cuco_Links_oneCockpit_#prod.sql

**Path**: `cuco.dbmaintain/sql/11/74_Cuco_V26.08/01_@custc_cuco_Links_oneCockpit_#prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update a link configuration for 'One Cockpit' in the CUCO_LINKS table",
    
    "components": [
        {
            "name": "CUCO_LINKS Table Operat...

---

## 01_@custc_cuco_Links_oneCockpit_#dev.sql

**Path**: `cuco.dbmaintain/sql/11/74_Cuco_V26.08/01_@custc_cuco_Links_oneCockpit_#dev.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update a link configuration for 'One Cockpit' in the CUCO_LINKS table",
    
    "components": [
        {
            "name": "CUCO_LINKS Table Operat...

---

## 01_@custc_a1bipv1_texts.sql

**Path**: `cuco.dbmaintain/sql/11/73_Cuco_V25.07/01_@custc_a1bipv1_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text labels and information messages related to Last Mile ID and Business Case functionality in multiple modules",
    
    "components": [
        {
...

---

## 04_@custc_QuoteClearanceChanges_AuthChanges.sql

**Path**: `cuco.dbmaintain/sql/11/37_CuCo_V18.09.1/04_@custc_QuoteClearanceChanges_AuthChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for role and authorization management related to quote validation functionality",
    "components": [
        {
            "name": "Role Management",
            "ty...

---

## 01_@custc_mariposa_new_datamodel.sql

**Path**: `cuco.dbmaintain/sql/11/37_CuCo_V18.09.1/01_@custc_mariposa_new_datamodel.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation script for a Customer Contract (CuCo) management system focusing on approval hierarchies, clearance rules, and product templates",
    
    "components": [
 ...

---

## 02_@app_mariposa_new_datamodel_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/37_CuCo_V18.09.1/02_@app_mariposa_new_datamodel_synonyms.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for customer configuration tables, providing alias access to tables in the CUSTC schema",
    "components": [
        {
            "name": "Database Synony...

---

## 05_@custc_mariposa_Bite_TextChanges.sql

**Path**: `cuco.dbmaintain/sql/11/37_CuCo_V18.09.1/05_@custc_mariposa_Bite_TextChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for updating text translations and validation patterns in the BITE_TEXT table, focusing on sales stage statuses and form validation messages in German",
    
    "com...

---

## 03_@custc_QuoteClearance_Bite_TextChanges.sql

**Path**: `cuco.dbmaintain/sql/11/37_CuCo_V18.09.1/03_@custc_QuoteClearance_Bite_TextChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for updating text/label configurations in the BITE_TEXT table, primarily focused on organizational structure and quote validation UI elements",
    
    "components":...

---

## 01_@custc_a1bi5_texts.sql

**Path**: `cuco.dbmaintain/sql/11/70_CuCo_V22.04/01_@custc_a1bi5_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text labels and error messages related to IP packet configuration in a business internet and OAN (Optical Access Network) system",
    
    "components":...

---

## 09_@custc_digital_selling_note.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/09_@custc_digital_selling_note.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a digital selling note table and grants database permissions for the CUCO application",
    
    "components": [
        {
            "name": "si_vi_ds_note",
            "t...

---

## 05_@custc_etgtV11_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/05_@custc_etgtV11_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for CuCo Calculation Tool (etgt v11) that populates localization text entries for mobile internet tariff labels and descriptions",
    
    "components...

---

## 12_@custc_daas_pdftemplate.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/12_@custc_daas_pdftemplate.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates PDF template configuration for DaaS (Device as a Service) offering in the CuCo system",
    "components": [
        {
            "name": "CCT_POV",
            "type": "data...

---

## 04_@custc_etgt_remove_texts_lower_v10.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/04_@custc_etgt_remove_texts_lower_v10.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to remove legacy text entries from BITE_TEXT table for versions 2 through 9 of cct_etgt system",
    
    "components": [
        {
            "name": "B...

---

## 10_@app_si_ds_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/10_@app_si_ds_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for a data source note view, providing an alias for cross-schema access",
    "components": [
        {
            "name": "si_vi_ds_note",
            "t...

---

## 11_@custc_digital_selling_text.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/11_@custc_digital_selling_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for digital selling categories in a multilingual/localization system",
    
    "components": [
        {
            "name": "BITE_TEXT table ...

---

## 01_@custc_add_daas_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/01_@custc_add_daas_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization for Device as a Service (DaaS) feature in the CuCo system by updating role and authentication entries",
    
    "components": [
        {
   ...

---

## 07_@custc_cct_update.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/07_@custc_cct_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating customer-facing labels and descriptions in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
  ...

---

## 03_@custc_daas_admin_ui.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/03_@custc_daas_admin_ui.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text/labels for a marketing product administration interface in German language",
    "components": [
        {
            "name": "BITE_TEXT",
     ...

---

## 08_@custc_add_digital_selling_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/08_@custc_add_digital_selling_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to set up authorization and roles for Digital Selling feature in the CuCo system",
    "components": [
        {
            "name": "bite_auth",
            "type": ...

---

## 02_@custc_daas_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/02_@custc_daas_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for Device as a Service (DaaS) text configurations and labels in a multi-language support system",
    
    "components": [
        {
            "name": "B...

---

## 06_@custc_etgtV11_activation.sql

**Path**: `cuco.dbmaintain/sql/11/49_CuCo_V20.02/06_@custc_etgtV11_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update ETGT V11 point of view (POV) configuration in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation",
     ...

---

## 04_@custc_a1bn_v11_text.sql

**Path**: `cuco.dbmaintain/sql/11/62_CuCo_V21.05/04_@custc_a1bn_v11_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for maintaining text labels and descriptions in the BITE_TEXT table, specifically for customer configuration texts with prefix 'cct_a1bn_v11_'",
    
    "components": [
 ...

---

## 05_@custc_update_pshc_v5_text.sql

**Path**: `cuco.dbmaintain/sql/11/62_CuCo_V21.05/05_@custc_update_pshc_v5_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text localization script for updating customer communication texts related to PSHC v5 module",
    
    "components": [
        {
            "name": "BITE_TEXT table",
    ...

---

## 03_@custc_add_a1bn_v11.sql

**Path**: `cuco.dbmaintain/sql/11/62_CuCo_V21.05/03_@custc_add_a1bn_v11.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product offering version (POV) data for A1BN V11 in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Op...

---

## 01_@custc_add_pshc_v5.sql

**Path**: `cuco.dbmaintain/sql/11/62_CuCo_V21.05/01_@custc_add_pshc_v5.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Product Offering Version (POV) records for PSHC V5 configuration",
    "components": [
        {
            "name": "CCT_POV Table Operations",...

---

## 02_@custc_pshc_v5_text.sql

**Path**: `cuco.dbmaintain/sql/11/62_CuCo_V21.05/02_@custc_pshc_v5_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text localization/configuration script for inserting UI text labels and enums related to OAN GPON and A1 Dame Arzt features",
    
    "components": [
        {
            ...

---

## 05_@custc_mariposa_Part4_clearance_history.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/05_@custc_mariposa_Part4_clearance_history.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a historical tracking table for clearance records with associated permissions",
    "components": [
        {
            "name": "CCT_CLEARANCE_HISTORY",
            "type":...

---

## 02_@custc_mariposa_pov_add_validation_xslt.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/02_@custc_mariposa_pov_add_validation_xslt.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Adds an XMLTYPE column for XSLT validation to an existing database table",
    "components": [
        {
            "name": "cct_pov table",
            "type": "database_table",
  ...

---

## 04_@app_mariposa_Part4_clearance_history2.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/04_@app_mariposa_Part4_clearance_history2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for clearance history table, providing an alias for cross-schema access",
    "components": [
        {
            "name": "CCT_CLEARANCE_HISTORY",
      ...

---

## 01_@custc_mariposa_Part4_Bite_TextChanges.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/01_@custc_mariposa_Part4_Bite_TextChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and tooltips in the BITE_TEXT table for quote widget status indicators in German language",
    
    "components": [
        {
            "name...

---

## 07_@custc_mariposa_Part3_Bie_TextChanges2.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/07_@custc_mariposa_Part3_Bie_TextChanges2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for clearance status messages in a quote clearance workflow system",
    "components": [
        {
            "name": "BITE_TEXT",
            ...

---

## 06_@custc_authAndDBChanges.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/06_@custc_authAndDBChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for role management and schema modification in CCT (Customer Care Tool) system",
    "components": [
        {
            "name": "Role Management",
    ...

---

## 10_@custc_texts_OrgStructureImport_2.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/10_@custc_texts_OrgStructureImport_2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text entries in the BITE_TEXT table, specifically for organization structure import functionality",
    
    "components": [
        {
        ...

---

## 09_@custc_texts_OrgStructureImport.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/09_@custc_texts_OrgStructureImport.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text messages related to organization structure import functionality in German language",
    "components": [
        {
            "name": "BITE_TEXT",
...

---

## 08_@custc_initialDataForProductIdentifiers.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/08_@custc_initialDataForProductIdentifiers.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Initial data setup script for product templates and tabs in a customer configuration system",
    "components": [
        {
            "name": "CCT_PRODUCT_TEMPLATE",
            "t...

---

## 03_@custc_mariposa_Part3_Bite_TextChanges.sql

**Path**: `cuco.dbmaintain/sql/11/38_CuCo_V18.09.2/03_@custc_mariposa_Part3_Bite_TextChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for updating text labels and messages in a multilingual clearance/approval system, specifically German translations",
    
    "components": [
        {
            "...

---

## 01_@custc_a1tvResV1.sql

**Path**: `cuco.dbmaintain/sql/11/28_CuCo_V18.03.01/01_@custc_a1tvResV1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to insert product offering and product offering variant (POV) data for A1 TV Kombi residential service",
    
    "components": [
        {
            "name": "Produ...

---

## 02_@custc_role_auth_update.sql

**Path**: `cuco.dbmaintain/sql/11/28_CuCo_V18.03.01/02_@custc_role_auth_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to update role-based authorization mappings for CCT (Customer Care Tool) features",
    
    "components": [
        {
            "name": "bite_role_auth",
            "t...

---

## 03_@custc_bite_text_a1tvRes_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/28_CuCo_V18.03.01/03_@custc_bite_text_a1tvRes_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for A1TV residential product text configurations in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
  ...

---

## 05_@custc_bite_text_bvk_BillableUser.sql

**Path**: `cuco.dbmaintain/sql/11/28_CuCo_V18.03.01/05_@custc_bite_text_bvk_BillableUser.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update UI text labels for billable user information in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table",
...

---

## 04_@custc_a1tvResV1_activation.sql

**Path**: `cuco.dbmaintain/sql/11/28_CuCo_V18.03.01/04_@custc_a1tvResV1_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update Product Offering Version (POV) data for A1TV Residential service",
    "components": [
        {
            "name": "CCT_POV table operations",
           ...

---

## 09_@custc_bite_text_for_A1GoNetwork_SimPur_Tariffs.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/09_@custc_bite_text_for_A1GoNetwork_SimPur_Tariffs.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update customer-facing text labels for A1 Go Network SIM card tariff plans in the bite_text table",
    
    "components": [
        {
            "name": "bite_te...

---

## 08_@custc_bite_text_for_price_panel.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/08_@custc_bite_text_for_price_panel.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage UI text/labels for price panel and SIM tariff descriptions in German language",
    
    "components": [
        {
            "name": "bite_text",
        ...

---

## 04_@custc_bite_text_productBrowser.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/04_@custc_bite_text_productBrowser.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing product-related text labels and translations in a multilingual application",
    "components": [
        {
            "name": "BITE_TEXT",
            "...

---

## 01_@custc_bite_text_update.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/01_@custc_bite_text_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels in the BITE_TEXT table for customer communication templates",
    
    "components": [
        {
            "name": "BITE_TEXT tabl...

---

## 05_@custc_bite_text_update2.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/05_@custc_bite_text_update2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels in the BITE_TEXT table for various product summary sections with German translations",
    "components": [
        {
            "name": "BITE_T...

---

## 02_@custc_etgtv9.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/02_@custc_etgtv9.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for inserting localized text entries for a Customer Communication (CuCo) Calculation Tool, specifically for the 'etgt' product version 9",
    
    "components": [
       ...

---

## 07_@app_cct_tariff_soc_mappings_table_Synonym.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/07_@app_cct_tariff_soc_mappings_table_Synonym.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for CCT_TARIFF_SOC_MAPPINGS table, providing an alias to access the table from custc schema",
    "components": [
        {
            "name": "CCT_TARIFF...

---

## 06_@custc_cct_tariff_soc_mappings_table.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/06_@custc_cct_tariff_soc_mappings_table.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and populates a mapping table between tariff SOCs (Service Offering Codes) and product pricing IDs in a telecommunications system",
    
    "components": [
        {
       ...

---

## 03_@custc_etgtv9_activation.sql

**Path**: `cuco.dbmaintain/sql/11/17_CuCo_V17.04/03_@custc_etgtv9_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering version data for ETGT V9 activation and deactivate ETGT V8",
    "components": [
        {
            "name": "CCT_POV table ope...

---

## 01_@custc_a1voip_v11_text.sql

**Path**: `cuco.dbmaintain/sql/11/77_Cuco_V29.11/01_@custc_a1voip_v11_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for A1 VoIP related labels and error messages",
    
    "components": [
        {
            "name": "BITE_TEXT table operations",
         ...

---

## 05_@custc_daas.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/05_@custc_daas.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for text labels related to Device as a Service (DaaS) product offerings",
    "components": [
        {
            "name": "BITE_TEXT",
            "ty...

---

## 02_@custc_marketplace_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/02_@custc_marketplace_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for marketplace quote text labels and configurations in a multilingual system",
    "components": [
        {
            "name": "BITE_TEXT",
        ...

---

## 03_@custc_quoteflashinfo.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/03_@custc_quoteflashinfo.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation for a quote flash notification system with role-based access control",
    "components": [
        {
            "name": "cuco_quote_flash",
            "typ...

---

## 07_@custc_text_updates.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/07_@custc_text_updates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating localization/label entries in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations...

---

## 01_@custc_add_marketplace.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/01_@custc_add_marketplace.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script to set up Marketplace product configuration and related authorization settings",
    
    "components": [
        {
            "name": "Authorization ...

---

## 04_@app_quoteflashinfo.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/04_@app_quoteflashinfo.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for quote flash-related tables and sequences in the CUCO (Customer Contract) system",
    "components": [
        {
            "name": "cuco_quote_flash",
...

---

## 06_@custc_a1biv3_add_aktion.sql

**Path**: `cuco.dbmaintain/sql/11/52_CuCo_V20.05/06_@custc_a1biv3_add_aktion.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script to add action-related text labels and settings for the CuCo calculation tool",
    
    "components": [
        {
            "name": "BITE_TEXT",
     ...

---

## 01_@custc_ccs_v1_text.sql

**Path**: `cuco.dbmaintain/sql/11/85_CuCO_V24.09/01_@custc_ccs_v1_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for customer communication service configurations and business rules",
    "components": [
        {
            "name": "BITE_TEXT",
        ...

---

## 01_@custc_a1bnv11_texts.sql

**Path**: `cuco.dbmaintain/sql/11/66_CuCo_V21.10/01_@custc_a1bnv11_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for customer configuration UI labels and messages",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
          ...

---

## 02_@custc_a1bn_backup_mobile_change_texts.sql

**Path**: `cuco.dbmaintain/sql/11/66_CuCo_V21.10/02_@custc_a1bn_backup_mobile_change_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels related to 'Backup Mobile' functionality in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations"...

---

## 08_@custc_bite_text_ProductBrowser_RenameFremdnetz.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/08_@custc_bite_text_ProductBrowser_RenameFremdnetz.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels in the BITE_TEXT table, specifically renaming a product browser OAN status label",
    
    "components": [
        {
            "n...

---

## 06_@custc_bite_text_ProductBrowser_StyleUpdate.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/06_@custc_bite_text_ProductBrowser_StyleUpdate.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates styling configuration for product browser OAN status display in the BITE_TEXT configuration table",
    
    "components": [
        {
            "name": "BITE_TEXT",
      ...

---

## 03_@custc_bite_text_productBrowser_excelExport.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/03_@custc_bite_text_productBrowser_excelExport.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels for product browser foreign network header in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEX...

---

## 09_@custc_bite_text_ChangesFromAdmin.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/09_@custc_bite_text_ChangesFromAdmin.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and messages in the BITE_TEXT table for a customer-facing application",
    "components": [
        {
            "name": "BITE_TEXT Table Opera...

---

## 01_@custc_bite_text_ProductBrowser_Update.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/01_@custc_bite_text_ProductBrowser_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates text labels and styling for product browser interface related to foreign network status",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "...

---

## 02_@custc_bite_text_A1TVRES_Internetschutz.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/02_@custc_bite_text_A1TVRES_Internetschutz.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing text entries related to A1 Internet protection service options and configurations in the BITE_TEXT table",
    
    "components": [
        {
           ...

---

## 04_@custc_bite_text_productBrowser_geoCallNumber.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/04_@custc_bite_text_productBrowser_geoCallNumber.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels in BITE_TEXT table for product browser and geo call number related UI elements",
    "components": [
        {
            "name": "BITE_TEXT",
...

---

## 07_@custc_bite_text_A1BNV8_Sprachkanale_Update.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/07_@custc_bite_text_A1BNV8_Sprachkanale_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update language channel label text in BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT table",
            "type": "datab...

---

## 05_@custc_bite_text_A1BNV8_Sprachkanale.sql

**Path**: `cuco.dbmaintain/sql/11/32_CuCo_V18.05.2/05_@custc_bite_text_A1BNV8_Sprachkanale.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing multilingual text entries related to audio channel configurations (Sprachkanäle/Language Channels) in a localization/configuration system",
    
    "com...

---

## 10_@custc_bite_text_newProductOverview_changeNames.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/10_@custc_bite_text_newProductOverview_changeNames.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels for product overview display in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations"...

---

## 04_@custc_mobile_nutzung.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/04_@custc_mobile_nutzung.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add data usage tracking fields for mobile services and create a view",
    
    "components": [
        {
            "name": "MOBIL_NUTZUNG1",...

---

## 09_@custc_bite_text_for_dataUsageTable.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/09_@custc_bite_text_for_dataUsageTable.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text values in BITE_TEXT table for data usage display configuration",
    
    "components": [
        {
            "name": "BITE_TEXT table ma...

---

## 08_@custc_bite_text_splitWlan_vpnDailUp_labelInUberblick.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/08_@custc_bite_text_splitWlan_vpnDailUp_labelInUberblick.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for Split-WLAN and VPN-Dialup features in both FIB v5 and BIZKO v7 systems",
    
    "components": [
        {
            "name": "BITE_TEXT",...

---

## 06_@custc_bite_text_UiChangeableTextChanges.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/06_@custc_bite_text_UiChangeableTextChanges.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database content management script for updating UI text labels in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_t...

---

## 03_@dwh_mobile_nutzung.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/03_@dwh_mobile_nutzung.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter the MOBIL_NUTZUNG table to add new columns for tracking mobile data usage metrics",
    "components": [
        {
            "name": "MOBIL_NUTZUNG",
            "type": "data...

---

## 05_@custc_newProductBrowserTableView_AdminSettings_Corrections.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/05_@custc_newProductBrowserTableView_AdminSettings_Corrections.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for product browser table view admin settings in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "t...

---

## 01_@custc_bite_text_fibv5_for_splitWlan_vpnDailUp.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/01_@custc_bite_text_fibv5_for_splitWlan_vpnDailUp.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text labels and tooltips for Split-WLAN and VPN dial-up functionality in multiple display contexts (UI and PDF)",
    
    "components": [
        {
       ...

---

## 07_@custc_bite_text_ProductEntries.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/07_@custc_bite_text_ProductEntries.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing product-related text entries in a multilingual text management system (BITE_TEXT table)",
    "components": [
        {
            "name": "BITE_TEXT Ta...

---

## 02_@custc_bite_text_bizkov7_for_splitWlan_vpnDailUp.sql

**Path**: `cuco.dbmaintain/sql/11/21_CuCo_V17.08/02_@custc_bite_text_bizkov7_for_splitWlan_vpnDailUp.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for Split-WLAN and VPN dial-up configuration labels and tooltips in multiple languages",
    
    "components": [
        {
            "name":...

---

## 01_@custc_etgt_v12_text.sql

**Path**: `cuco.dbmaintain/sql/11/81_CuCo_V24.02/01_@custc_etgt_v12_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text labels related to A1 business mobile products and services",
    "components": [
        {
            "name": "BITE_TEXT Table Operations...

---

## 03_@custc_add_etgt_v12.sql

**Path**: `cuco.dbmaintain/sql/11/56_CuCo_V20.09/03_@custc_add_etgt_v12.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Point of View (POV) records for ETGT V12 configuration in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Ta...

---

## 05_@custc_AddMeinA1BusinessRegistration_text.sql

**Path**: `cuco.dbmaintain/sql/11/56_CuCo_V20.09/05_@custc_AddMeinA1BusinessRegistration_text.sql`

**Layer**: Backend Service

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for Mein A1 Business Registration across different product variants in the BITE_TEXT table",
    
    "components": [
        {
            "nam...

---

## 04_@custc_etgt_v12_text.sql

**Path**: `cuco.dbmaintain/sql/11/56_CuCo_V20.09/04_@custc_etgt_v12_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text localization script for customer configuration module (CuCo) that manages text entries for a tariff/bundle management interface",
    
    "components": [
        {
   ...

---

## 01_@custc_add_a1bi_v4.sql

**Path**: `cuco.dbmaintain/sql/11/56_CuCo_V20.09/01_@custc_add_a1bi_v4.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product offering version data for A1BI V4 in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Operation...

---

## 02_@custc_a1bi_v4_text.sql

**Path**: `cuco.dbmaintain/sql/11/56_CuCo_V20.09/02_@custc_a1bi_v4_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for inserting and updating localized text entries for a business internet service configuration interface",
    "components": [
        {
            "name": "BITE_TE...

---

## 06_@custc_etgt_v12_report.sql

**Path**: `cuco.dbmaintain/sql/11/56_CuCo_V20.09/06_@custc_etgt_v12_report.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to insert a reporting query for ETGT V12 discount offers analysis over a 31-day period into APP_REPORTING table",
    
    "components": [
        {
            "name": "A...

---

## 10_@custc_etgt_v12_missing_text.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/10_@custc_etgt_v12_missing_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to insert localized text for activation costs label in German",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "d...

---

## 05_@custc_a1bip_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/05_@custc_a1bip_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for text labels and messages related to A1 Business Internet Professional (BIP) quote system",
    
    "components": [
        {
            "name": "BITE_...

---

## 08_@custc_a1bip_admin_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/08_@custc_a1bip_admin_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for text labels/messages related to A1 Business Internet Professional administration interface",
    
    "components": [
        {
            "name":...

---

## 06_@custc_add_a1bip_v1.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/06_@custc_add_a1bip_v1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product offering and point of view (POV) data for A1 Cloud Communication Service",
    
    "components": [
        {
            "name": "CCT_P...

---

## 04_@custc_a1bip_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/04_@custc_a1bip_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for A1 Business Internet Professional (A1BIP) product offering text configurations",
    
    "components": [
        {
            "name": "BITE_TEXT ...

---

## 01_@custc_add_bpb_v7.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/01_@custc_add_bpb_v7.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update BPB V7 product offering version data in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation",
           ...

---

## 11_@custc_a1bip_clearance_rules.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/11_@custc_a1bip_clearance_rules.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for setting up product tab attributes and sections for A1 Business Internet Professional offering",
    
    "components": [
        {
            "name...

---

## 02_@custc_bpb_v7_text.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/02_@custc_bpb_v7_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text resource configuration script for customer communication module (CuCo) containing localized text entries for a business product bundle (BPB) version 7",
    
    "compo...

---

## 07_@custc_a1bip_admin_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/07_@custc_a1bip_admin_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for setting up role-based authorization for A1 Business Internet Professional administration and business firewall features",
    
    "components": [
        {
          ...

---

## 03_@custc_add_a1bip_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/58_CuCo_V20.11/03_@custc_add_a1bip_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization for A1 Business Internet Professional quote creation feature",
    
    "components": [
        {
            "name": "bite_auth",
           ...

---

## 01_@custc_a1voip_a1bn_oan_gpon.sql

**Path**: `cuco.dbmaintain/sql/11/64_CuCo_V21.07/01_@custc_a1voip_a1bn_oan_gpon.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for updating text labels related to OAN-GPON in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT Table Operations...

---

## 02_@custc_a1bi_v5_update_text.sql

**Path**: `cuco.dbmaintain/sql/11/64_CuCo_V21.07/02_@custc_a1bi_v5_update_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content maintenance script for updating and deleting customer communication text entries",
    "components": [
        {
            "name": "BITE_TEXT",
            "t...

---

## 05_@custc_etgtv7.sql

**Path**: `cuco.dbmaintain/sql/11/14_CuCo_V16.11/05_@custc_etgtv7.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update Product Offering Version (POV) records for ETGT product",
    "components": [
        {
            "name": "CCT_POV table",
            "type": "...

---

## 02_@custc_bizcov5.sql

**Path**: `cuco.dbmaintain/sql/11/14_CuCo_V16.11/02_@custc_bizcov5.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operations",
 ...

---

## 01_@custc_a1bnv7.sql

**Path**: `cuco.dbmaintain/sql/11/14_CuCo_V16.11/01_@custc_a1bnv7.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating Point of View (POV) records in the CuCo system",
    "components": [
        {
            "name": "CCT_POV Table",
            "type": "data...

---

## 03_@custc_fibv3.sql

**Path**: `cuco.dbmaintain/sql/11/14_CuCo_V16.11/03_@custc_fibv3.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update Product Offering Version (POV) records for FIB (Business Internet) service",
    
    "components": [
        {
            "name": "CCT_POV Tab...

---

## 04_@custc_pshcv2.sql

**Path**: `cuco.dbmaintain/sql/11/14_CuCo_V16.11/04_@custc_pshcv2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to manage Point of View (POV) configurations for PSHC V2 product offering",
    "components": [
        {
            "name": "CCT_POV Table Operations",
...

---

## 07_@custc_bite_role_auth_all_updated.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/07_@custc_bite_role_auth_all_updated.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for initializing and updating role-based authorization data in the BITE system",
    
    "components": [
        {
            "name": "bite_auth",
            "type": "d...

---

## 03_@custc_View_For_CuCo_LOGS.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/03_@custc_View_For_CuCo_LOGS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view for data warehouse access to customer logs, specifically filtering for 'party loaded' events",
    
    "components": [
        {
            "name": "V_CUCO_...

---

## 06_@custc_bite_text_ChineseWall.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/06_@custc_bite_text_ChineseWall.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update error message text for Chinese Wall functionality in customer context",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "typ...

---

## 01_@custc_bite_text_FIBv6_BIZKOv8_RouterInfoLabel.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/01_@custc_bite_text_FIBv6_BIZKOv8_RouterInfoLabel.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update router configuration information text in BITE_TEXT table for FIBv6 and BIZKOv8 components",
    
    "components": [
        {
            "name": "BITE_TEX...

---

## 04_@custc_bite_text_User_Admin_Segment.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/04_@custc_bite_text_User_Admin_Segment.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text labels related to user administration segment functionality",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": ...

---

## 02_@custc_CUCO_LOGS_Updates_For_Party_Loaded.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/02_@custc_CUCO_LOGS_Updates_For_Party_Loaded.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add logging capabilities for password viewing and party loading events",
    
    "components": [
        {
            "name": "CUCO_LOGS",
         ...

---

## 05_@custc_bite_text_New_AdminScreens.sql

**Path**: `cuco.dbmaintain/sql/11/27_CuCo_V18.02.01/05_@custc_bite_text_New_AdminScreens.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels for admin team management screens in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": ...

---

## 10_@custc_bpbV6_a1biv3_deactivation.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/10_@custc_bpbV6_a1biv3_deactivation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update validity dates for BPB and A1BI product versions in CCT_POV table, effectively managing product version lifecycles",
    
    "components": [
  ...

---

## 08_@custc_bite_invoiceWidget_removeUnused.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/08_@custc_bite_invoiceWidget_removeUnused.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to remove unused configuration entry for Gucci invoice widget URL from BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT...

---

## 12_@custc_widget_loading_error.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/12_@custc_widget_loading_error.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update error message text for widget loading in German language",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "type...

---

## 07_@custc_bpbV6_activation.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/07_@custc_bpbV6_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update BPB (Business Product Bundle) version configurations in CCT_POV table, transitioning from V5 to V6",
    
    "components": [
        {
          ...

---

## 01_@custc_fibv7_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/01_@custc_fibv7_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Communication) tool's text labels and configurations for FIB (Festnetz-Internet Business) v7 product",
    
    "components": [
        {...

---

## 09_@custc_widget_loading_error.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/09_@custc_widget_loading_error.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update error message text for widget loading in multiple languages",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "datab...

---

## 11_@custc_bite_auth_old_widget_auth.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/11_@custc_bite_auth_old_widget_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization settings for old billing widget content view permissions",
    "components": [
        {
            "name": "BITE_AUTH Management",
         ...

---

## 05_@custc_a1biv3_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/05_@custc_a1biv3_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) Calculation Tool text labels, specifically for A1BI v3 product configuration",
    
    "components": [
        {
        ...

---

## 02_@custc_fibV7_activation.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/02_@custc_fibV7_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update FIB (Business Internet) product version from V6 to V7 in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table...

---

## 03_@custc_bite_auth_widget_gateway.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/03_@custc_bite_auth_widget_gateway.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authentication permissions for Gucci widgets content access in the BITE system",
    
    "components": [
        {
            "name": "BITE Authentication...

---

## 06_@custc_bpbV6_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/06_@custc_bpbV6_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) tool text labels, specifically for BPB (Breitband Pro Business) v6 product configuration",
    
    "components": [
      ...

---

## 04_@custc_a1biv3_activation.sql

**Path**: `cuco.dbmaintain/sql/11/46_CuCo_V19.09.1/04_@custc_a1biv3_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update A1BI (A1 Business Internet) product offering version configurations",
    "components": [
        {
            "name": "CCT_POV",
            "ty...

---

## 01_@custc_pshc_v5_text.sql

**Path**: `cuco.dbmaintain/sql/11/80_CuCo_V24.01/01_@custc_pshc_v5_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels related to mobile backup functionality in a customer communication system",
    "components": [
        {
            "name": "BITE_TEXT",
     ...

---

## 03_@custc_a1bip_admin_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/59_CuCo_V20.12/03_@custc_a1bip_admin_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for admin quote text labels related to Business Internet Professional (BIP) configuration",
    "components": [
        {
            "name": "BITE_TEX...

---

## 02_@custc_a1bip_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/59_CuCo_V20.12/02_@custc_a1bip_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text initialization script for customer communication/configuration labels in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "t...

---

## 09_@custc_bizcov3.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/09_@custc_bizcov3.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating product offering version (POV) records in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Operation...

---

## 06_@app_admin_emails_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/06_@app_admin_emails_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for team email-related tables and sequences in the CUSTC schema",
    "components": [
        {
            "name": "si_sc_team_email",
            "type": ...

---

## 02_@custc_si_vi_sc_product_history.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/02_@custc_si_vi_sc_product_history.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a history table for tracking product notes with audit information",
    "components": [
        {
            "name": "si_sc_product_history",
            "type": "database_t...

---

## 08_@custc_alter_quote_table.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/08_@custc_alter_quote_table.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter the cct_quote table to add a new column for sales conversion note ID",
    "components": [
        {
            "name": "cct_quote",
            "type": "database_table",
    ...

---

## 01_@custc_si_vi_sbs_product.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/01_@custc_si_vi_sbs_product.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a note classification column to the si_vi_sbs_product table",
    
    "components": [
        {
            "name": "si_vi_sbs_product",
        ...

---

## 07_@custc_admin_team_email.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/07_@custc_admin_team_email.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script to populate team email configurations for a customer contact system",
    "components": [
        {
            "name": "si_sc_team_email",
           ...

---

## 05_@custc_admin_emails.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/05_@custc_admin_emails.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema definition for team email management system with user associations",
    "components": [
        {
            "name": "si_sc_team_email",
            "type": "databa...

---

## 03_@custc_si_vi_sc_sales_conv_note.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/03_@custc_si_vi_sc_sales_conv_note.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table for storing sales conversation notes and related sequences with appropriate access grants",
    "components": [
        {
            "name": "si_sc_sales_co...

---

## 10_@custc_alter_sales_conv.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/10_@custc_alter_sales_conv.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter table si_sc_sales_conv_note to add a date tracking column for last reminder mail sent",
    
    "components": [
        {
            "name": "si_sc_sales_conv_note",
        ...

---

## 04_@app_salesConv_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/05_CuCo_V15.05/04_@app_salesConv_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for sales conversion related tables and sequences in the CuCo application",
    "components": [
        {
            "name": "sales_conversion_synonyms",
 ...

---

## 01_@custc_bizkoV9_activation.sql

**Path**: `cuco.dbmaintain/sql/11/44_CuCo_V19.06.1/01_@custc_bizkoV9_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering version (POV) records for BIZKO service, transitioning from V8 to V9",
    
    "components": [
        {
            "name": "CC...

---

## 02_@custc_bizkov9_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/44_CuCo_V19.06.1/02_@custc_bizkov9_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) tool's text labels and configurations specific to 'bizko v9' product",
    
    "components": [
        {
            "nam...

---

## 02_@custc_cuco_common_cm_buddy_text.sql

**Path**: `cuco.dbmaintain/sql/11/60_Cuco_V21.02/02_@custc_cuco_common_cm_buddy_text.sql`

**Layer**: Utility

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries for CM Buddy related UI labels in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
       ...

---

## 01_@custc_cuco_cm_buddy_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/60_Cuco_V21.02/01_@custc_cuco_cm_buddy_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to set up role-based authorization for CM Buddy functionality by creating necessary role and permission entries",
    "components": [
        {
            "name": "BITE_R...

---

## 01_@custc_pshcv1.sql

**Path**: `cuco.dbmaintain/sql/11/13_CuCo_V16.09/01_@custc_pshcv1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database update script to modify PDF template configuration for PSHC V1 product offering",
    "components": [
        {
            "name": "cct_pov",
            "type": "database_...

---

## 03_@custc_cct_approver_idx.sql

**Path**: `cuco.dbmaintain/sql/11/53_CuCo_V20.06/03_@custc_cct_approver_idx.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database index on the USER_ID column of the CCT_APPROVER_HIERARCHY table to optimize query performance for user-based lookups",
    
    "components": [
        {
         ...

---

## 01_@custc_quoteflashinfo_view.sql

**Path**: `cuco.dbmaintain/sql/11/53_CuCo_V20.06/01_@custc_quoteflashinfo_view.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification for quote flash view functionality and adding localization text entries",
    
    "components": [
        {
            "name": "cuco_quote_flash_viewed...

---

## 02_@custc_marketplace_text.sql

**Path**: `cuco.dbmaintain/sql/11/53_CuCo_V20.06/02_@custc_marketplace_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for marketplace sale type display texts in German language",
    "components": [
        {
            "name": "BITE_TEXT Ta...

---

## 06_@custc_bite_text_a1network_label.sql

**Path**: `cuco.dbmaintain/sql/11/33_CuCo_V18.06.1/06_@custc_bite_text_a1network_label.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for A1 Network-related UI elements in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table operations",...

---

## 04_@custc_bite_text_updateETGTV10.sql

**Path**: `cuco.dbmaintain/sql/11/33_CuCo_V18.06.1/04_@custc_bite_text_updateETGTV10.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update business product text labels and tooltips in the BITE_TEXT table for A1 Go Network business packages",
    
    "components": [
        {
            "name"...

---

## 01_@custc_bite_text_MVP.sql

**Path**: `cuco.dbmaintain/sql/11/33_CuCo_V18.06.1/01_@custc_bite_text_MVP.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text entries in the BITE_TEXT table for CuCo application",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
    ...

---

## 02_@custc_bite_text_MVP_updateETGTV10.sql

**Path**: `cuco.dbmaintain/sql/11/33_CuCo_V18.06.1/02_@custc_bite_text_MVP_updateETGTV10.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text entries in BITE_TEXT table for ETGT V10 minimum contract period configurations",
    
    "components": [
        {
            "name": "BI...

---

## 05_@custc_bite_text_bundleToggle.sql

**Path**: `cuco.dbmaintain/sql/11/33_CuCo_V18.06.1/05_@custc_bite_text_bundleToggle.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels for bundle mode toggle functionality in product browser",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": ...

---

## 03_@custc_bite_text_etgtv10.sql

**Path**: `cuco.dbmaintain/sql/11/33_CuCo_V18.06.1/03_@custc_bite_text_etgtv10.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localized text entries in the BITE_TEXT table, specifically for A1 mobile service configurations and tooltips",
    
    "components": [
        {
      ...

---

## 04_@custc_bite_text_new_contact_person_view.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/04_@custc_bite_text_new_contact_person_view.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage UI text labels and tooltips for a contact person management interface in German language",
    
    "components": [
        {
            "name": "BITE_TEXT...

---

## 02_@custc_bite_text_A1_Net_Flex_Cube_Tariffs.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/02_@custc_bite_text_A1_Net_Flex_Cube_Tariffs.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text labels and tooltips for A1 Flex Cube Internet tariffs in a localization/internationalization table",
    
    "components": [
        {
            "na...

---

## 03_@custc_ansprechPartnerStatus.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/03_@custc_ansprechPartnerStatus.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script for contact partner (Ansprechpartner) management system",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "look...

---

## 06_@custc_bite_text_update_with_admin_changes.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/06_@custc_bite_text_update_with_admin_changes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels related to security package offerings in the BITE_TEXT table, specifically updating German language promotional and contract period text",
    
...

---

## 07_@app_ansprechPartner_grants.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/07_@app_ansprechPartner_grants.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database synonym creation script for customer contact (Ansprechpartner) related tables",
    "components": [
        {
            "name": "ANSPRECHPARTNER_STATUS",
            "type...

---

## 05_@custc_bite_text_new_product_browser_view_UiTextEditable.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/05_@custc_bite_text_new_product_browser_view_UiTextEditable.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels in the BITE_TEXT table for product browser view customization",
    
    "components": [
        {
            "name": "BITE_TEXT",
         ...

---

## 01_@custc_bite_text_A1_mobile_internet_BUS_tarif_name_change.sql

**Path**: `cuco.dbmaintain/sql/11/23_CuCo_V17.10/01_@custc_bite_text_A1_mobile_internet_BUS_tarif_name_change.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates text labels for A1 Mobile Internet business tariff names in the BITE_TEXT table, changing them to 'Net Cube' naming convention",
    
    "components": [
        {
          ...

---

## 01_@custc_pshcv5_texts.sql

**Path**: `cuco.dbmaintain/sql/11/71_CuCo_V22.05/01_@custc_pshcv5_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for managing IP Voice text labels and messages in a customer communication system",
    
    "components": [
        {
            "name": "BITE_TEXT Ta...

---

## 03_@custc_a1voipV1_ChangeRequest_Changes.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/03_@custc_a1voipV1_ChangeRequest_Changes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for managing text labels and messages in a VoIP system, specifically handling German language text entries",
    
    "components": [
        {
        ...

---

## 06_@custc_bite_text_admin_update.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/06_@custc_bite_text_admin_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for product overview loading messages in German language",
    
    "components": [
        {
            "name": "BITE_TEXT...

---

## 02_@custc_bite_text_a1bi_V2_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/02_@custc_bite_text_a1bi_V2_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for customer communication tool (CuCo) text labels, specifically for A1BI product version 2",
    
    "components": [
        {
            "name": "bite_t...

---

## 04_@custc_bite_text_admin_update.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/04_@custc_bite_text_admin_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for managing localized text entries in a BITE_TEXT table, specifically for VoIP and business integration related UI labels",
    
    "components": [
  ...

---

## 07_@custc_bite_auth_update.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/07_@custc_bite_auth_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update authorization roles and permissions by removing a legacy product overview permission and adding new product browser admin permissions to multiple roles",
  ...

---

## 01_@custc_a1biV2_activation.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/01_@custc_a1biV2_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update A1BI (A1 Business Internet) product offering version configurations",
    "components": [
        {
            "name": "CCT_POV table operations"...

---

## 08_@custc_bite_text_myCuco_defect.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/08_@custc_bite_text_myCuco_defect.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text entries for MyCuCo customer-related error messages",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "type"...

---

## 05_@custc_A1BI_IPVOICE_clearanceAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/05_@custc_A1BI_IPVOICE_clearanceAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for managing IP Voice product attributes in the CCT (Customer Care Tool) system",
    
    "components": [
        {
            "name": "CCT_PRODUCT_TAB_...

---

## 09_@custc_bite_PROBLEM-53258.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/09_@custc_bite_PROBLEM-53258.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to increase comment field length and update error message text",
    
    "components": [
        {
            "name": "CCT_CLEARANCE_HISTORY",
        ...

---

## 10_@custc_bite_miscellaneous.sql

**Path**: `cuco.dbmaintain/sql/11/43_CuCo_V19.03.2/10_@custc_bite_miscellaneous.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for updating PDF template configurations and business text labels in the CUCO system",
    
    "components": [
        {
            "name": "CCT_POV Upd...

---

## 02_@custc_bite_invoiceWidget.sql

**Path**: `cuco.dbmaintain/sql/11/45_CuCo_V19.06.2/02_@custc_bite_invoiceWidget.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for setting up Gucci invoice widget URL in BITE system",
    
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_table"...

---

## 01_@custc_loadDWHControl.sql

**Path**: `cuco.dbmaintain/sql/11/45_CuCo_V19.06.2/01_@custc_loadDWHControl.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update deletion interval configuration for the UMSATZ table in data warehouse control settings",
    
    "components": [
        {
            "name":...

---

## 04_@custc_bite_text_admin_update.sql

**Path**: `cuco.dbmaintain/sql/11/45_CuCo_V19.06.2/04_@custc_bite_text_admin_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating localized UI text labels and enum values in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TE...

---

## 03_@custc_bite_auth_invoiceWidget.sql

**Path**: `cuco.dbmaintain/sql/11/45_CuCo_V19.06.2/03_@custc_bite_auth_invoiceWidget.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization settings for GUCCI billing content widget in the BITE system",
    
    "components": [
        {
            "name": "BITE Authorization Mana...

---

## 08_@custc_bite_text_for_PSHC_SNG.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/08_@custc_bite_text_for_PSHC_SNG.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to populate localization text entries for mobile connection sizes in a municipality context",
    "components": [
        {
            "name": "BITE_TEXT",
         ...

---

## 12_@custc_pshc_role.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/12_@custc_pshc_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script that adds a new role for PSHC Quote Creation functionality",
    
    "components": [
        {
            "name": "BITE_ROLE",
            "type"...

---

## 06_@custc_bite_text_New_SNOM_Telephones.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/06_@custc_bite_text_New_SNOM_Telephones.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries for SNOM telephone models and related configurations in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT...

---

## 05_@custc_bite_text_SBS_Note_TitleSection.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/05_@custc_bite_text_SBS_Note_TitleSection.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels for note title sections in a visit report system",
    "components": [
        {
            "name": "bite_text",
            "type": "databa...

---

## 04_@custc_bite_text_for_PSHC_SNS.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/04_@custc_bite_text_for_PSHC_SNS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing localization text entries related to PSHC (Presumably Product/Service Handling Configuration) SNS module, specifically handling connection-related text l...

---

## 02_@custc_pshcv3_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/02_@custc_pshcv3_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) Calc Tool, specifically for PSHC v3 product, setting up UI text labels and configurations",
    
    "components": [
     ...

---

## 03_@custc_bite_text_for_WLAN_Schule.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/03_@custc_bite_text_for_WLAN_Schule.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text labels related to WLAN school configuration, focusing on text localization and configuration data",
    
    "components": [
        {
          ...

---

## 01_@custc_pshcv3_activation.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/01_@custc_pshcv3_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to activate PSHC V3 product offering variant and deactivate PSHC V2",
    "components": [
        {
            "name": "CCT_POV table operations",
        ...

---

## 10_@custc_bite_text_discount_validation_messages.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/10_@custc_bite_text_discount_validation_messages.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage validation error messages for percentage and absolute discount values in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_...

---

## 09_@custc_bite_text_for_gdpr_update_doc.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/09_@custc_bite_text_for_gdpr_update_doc.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates text entries in BITE_TEXT table related to GDPR/data protection portal view texts",
    "components": [
        {
            "name": "BITE_TEXT Table",
            "type": "...

---

## 07_@custc_bite_text_gdpr_show_eve_status.sql

**Path**: `cuco.dbmaintain/sql/11/18_CuCo_V17.05/07_@custc_bite_text_gdpr_show_eve_status.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Manages GDPR-related text content for party/customer data display, specifically EVE (Einwilligungserklärung/Consent Declaration) status texts in German",
    
    "components": [
   ...

---

## 03_@custc_add_bfw_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/03_@custc_add_bfw_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage role-based authorization for Business Firewall quote creation feature",
    
    "components": [
        {
            "name": "bite_role_auth",
           ...

---

## 07_@custc_bfw_admin_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/07_@custc_bfw_admin_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to configure authorization and role mappings for A1 Business Firewall administration in the BITE system",
    
    "components": [
        {
            "name": "BITE_AUTH...

---

## 09_@custc_bfw_pdf_template.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/09_@custc_bfw_pdf_template.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates PDF template configuration for Business Firewall (BFW) product variant in CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV",
            "type"...

---

## 10_@custc_bfw_clearance_rules.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/10_@custc_bfw_clearance_rules.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for setting up product tab attributes and sections for Business Firewall (BFW) clearance rules",
    
    "components": [
        {
            "name": ...

---

## 01_@custc_add_a1bn_v10.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/01_@custc_add_a1bn_v10.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product offering version data for A1BN V10 in the CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation",
 ...

---

## 06_@custc_add_bfw_v1.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/06_@custc_add_bfw_v1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to set up Business Firewall (BFW) V1 product offering configuration",
    
    "components": [
        {
            "name": "Product Offering Setup",
     ...

---

## 08_@custc_bfw_admin_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/08_@custc_bfw_admin_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for initializing/updating text labels and menu items in the Business Firewall administration interface",
    
    "components": [
        {
            "name": "BITE_TEXT"...

---

## 05_@custc_bfw_quote_text_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/05_@custc_bfw_quote_text_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for text labels/translations in a Business Firewall quote system",
    
    "components": [
        {
            "name": "bite_text",
            "type": "...

---

## 04_@custc_bfw_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/04_@custc_bfw_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for Business Firewall (BFW) product offering text configurations",
    
    "components": [
        {
            "name": "BITE_TEXT table operations",...

---

## 02_@custc_a1bn_v10_text.sql

**Path**: `cuco.dbmaintain/sql/11/57_CuCo_V20.10/02_@custc_a1bn_v10_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text resource configuration script for customer communication module (CuCo) containing localized German text labels and messages",
    
    "components": [
        {
       ...

---

## 03_@custc_add_ccs_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/83_CuCo_V24.06/03_@custc_add_ccs_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage role-based authorization for Cloud Communication Service (CCS) features",
    "components": [
        {
            "name": "Authorization Management",
    ...

---

## 02_@custc_ccs_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/83_CuCo_V24.06/02_@custc_ccs_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for CCS (Cloud Communication Service) product offering text configurations",
    
    "components": [
        {
            "name": "BITE_TEXT table op...

---

## 05_@custc_a1bn_servicefee.sql

**Path**: `cuco.dbmaintain/sql/11/83_CuCo_V24.06/05_@custc_a1bn_servicefee.sql`

**Layer**: Backend Service

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration update script to enable mobile service fee functionality for A1BN calculation tool",
    
    "components": [
        {
            "name": "BITE_SETTING",
   ...

---

## 04_@custc_add_ccs_texts.sql

**Path**: `cuco.dbmaintain/sql/11/83_CuCo_V24.06/04_@custc_add_ccs_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localization text entries for a CCS (Customer Communication System) interface",
    "components": [
        {
            "name": "BITE_TEXT table operation...

---

## 01_@custc_add_ccs_v1.sql

**Path**: `cuco.dbmaintain/sql/11/83_CuCo_V24.06/01_@custc_add_ccs_v1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product offering and point-of-view (POV) configurations for Cloud Communication Service",
    
    "components": [
        {
            "name": "...

---

## 02_@custc_new_role.sql

**Path**: `cuco.dbmaintain/sql/11/08_CuCo_V16.02/02_@custc_new_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script to add a new ZVERA Pilot role for the CUCO system",
    "components": [
        {
            "name": "BITE_ROLE table insert",
            "type":...

---

## 01_@custc_etgtv4.sql

**Path**: `cuco.dbmaintain/sql/11/08_CuCo_V16.02/01_@custc_etgtv4.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update ETGT (Electronic Trading) product offering version data in CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table O...

---

## 02_@custc_a1bi_v7_text.sql

**Path**: `cuco.dbmaintain/sql/11/79_Cuco_V23.01/02_@custc_a1bi_v7_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for internationalization/localization of UI labels and messages related to IP packet and router configurations",
    
    "components": [
    ...

---

## 01_@custc_add_a1bi_v7.sql

**Path**: `cuco.dbmaintain/sql/11/79_Cuco_V23.01/01_@custc_add_a1bi_v7.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update A1BI V7 product offering version configuration in CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table Operatio...

---

## 04_@custc_daas_additional_notes_setting.sql

**Path**: `cuco.dbmaintain/sql/11/51_CuCo_V20.04/04_@custc_daas_additional_notes_setting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script to set a feature flag for DaaS additional notes functionality in the calculation tool",
    
    "components": [
        {
            "name": "BITE_SETTING",
  ...

---

## 03_@custc_text_updates.sql

**Path**: `cuco.dbmaintain/sql/11/51_CuCo_V20.04/03_@custc_text_updates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels in BITE_TEXT table for a customer-facing device management interface",
    "components": [
        {
            "name": "BITE_TEXT Table Update...

---

## 01_@custc_daas_quote_text.sql

**Path**: `cuco.dbmaintain/sql/11/51_CuCo_V20.04/01_@custc_daas_quote_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing multilingual text labels for a Device-as-a-Service (DaaS) application interface",
    
    "components": [
        {
            "name": "BITE_TEXT",
   ...

---

## 02_@custc_clearance_texts.sql

**Path**: `cuco.dbmaintain/sql/11/51_CuCo_V20.04/02_@custc_clearance_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing clearance-related text messages in multiple languages for a customer quote system",
    "components": [
        {
            "name": "BITE_TEXT",
      ...

---

## 04_@dwh_rufnummer.sql

**Path**: `cuco.dbmaintain/sql/11/11_CuCo_V16.05/04_@dwh_rufnummer.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a CPI_STATUS column to the rufnummer table",
    
    "components": [
        {
            "name": "rufnummer table",
            "type": "databa...

---

## 02_@custc_kunde.sql

**Path**: `cuco.dbmaintain/sql/11/11_CuCo_V16.05/02_@custc_kunde.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add CPI_STATUS column to customer tables and create a view",
    
    "components": [
        {
            "name": "kunde1",
            "type...

---

## 03_@custc_rufnummer.sql

**Path**: `cuco.dbmaintain/sql/11/11_CuCo_V16.05/03_@custc_rufnummer.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add CPI_STATUS column to rufnummer tables and create a view",
    
    "components": [
        {
            "name": "rufnummer1",
            ...

---

## 06_@custc_bestand.sql

**Path**: `cuco.dbmaintain/sql/11/11_CuCo_V16.05/06_@custc_bestand.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script that adds a CPI_STATUS column to bestand tables and creates a view",
    
    "components": [
        {
            "name": "bestand1",
          ...

---

## 01_@dwh_kunde.sql

**Path**: `cuco.dbmaintain/sql/11/11_CuCo_V16.05/01_@dwh_kunde.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a CPI status tracking column to the customer table",
    
    "components": [
        {
            "name": "kunde table",
            "type": "da...

---

## 05_@dwh_bestand.sql

**Path**: `cuco.dbmaintain/sql/11/11_CuCo_V16.05/05_@dwh_bestand.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a CPI status tracking column to the 'bestand' table",
    
    "components": [
        {
            "name": "bestand table",
            "type": ...

---

## 01_@custc_a1bip_admin_quote_text_confirm_mcd.sql

**Path**: `cuco.dbmaintain/sql/11/68_CuCo_V21.12/01_@custc_a1bip_admin_quote_text_confirm_mcd.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels in the BITE_TEXT table for administrative confirmation labels",
    
    "components": [
        {
            "name": "BITE_TEXT Ta...

---

## 10_@custc_missing_clearanceAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/10_@custc_missing_clearanceAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update product attributes for A1 Business Internet services in the CCT_PRODUCT_TAB_ATTRIBUTE table",
    
    "components": [
        {
            "na...

---

## 07_@custc_bite_text_New_Product_Overview_SubscriptionTypes.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/07_@custc_bite_text_New_Product_Overview_SubscriptionTypes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels for product overview subscription types in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "t...

---

## 08_@custc_A1VOIP_clearanceAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/08_@custc_A1VOIP_clearanceAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for managing product attributes related to A1 VOIP service configurations",
    
    "components": [
        {
            "name": "CCT_PRODUCT_TAB_ATTRIB...

---

## 02_@custc_a1voipV1_activation.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/02_@custc_a1voipV1_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage A1VOIP V1 product offering version (POV) configuration in the CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation",
 ...

---

## 04_@custc_role_auth_update.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/04_@custc_role_auth_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update role-based authorization for A1 VoIP quote feature",
    "components": [
        {
            "name": "bite_role_auth",
            "type": "database_table...

---

## 11_@custc_missing_biteScript.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/11_@custc_missing_biteScript.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update VOIP call number type configurations in BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table operation",
  ...

---

## 03_@custc_bite_text_a1voip_V1_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/03_@custc_bite_text_a1voip_V1_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for A1VOIP product text configurations in a bite_text table",
    "components": [
        {
            "name": "bite_text table operations",
            "t...

---

## 05_@custc_role_auth_updateRole.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/05_@custc_role_auth_updateRole.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates role-based authorization mappings for A1VOIP feature in the CCT system",
    "components": [
        {
            "name": "bite_role_auth",
            "type": "database_tab...

---

## 09_@custc_productOverviewLoadingMessages.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/09_@custc_productOverviewLoadingMessages.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage loading message texts for product overview functionality in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "ty...

---

## 01_@custc_a1voipV1.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/01_@custc_a1voipV1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for managing A1VOIP V1 product offering configurations",
    "components": [
        {
            "name": "Product Offering Maintenance",
            "ty...

---

## 06_@custc_bite_text_New_Product_Overview.sql

**Path**: `cuco.dbmaintain/sql/11/42_CuCo_V19.02.2/06_@custc_bite_text_New_Product_Overview.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script for managing text content and authorization settings in a product overview feature",
    "components": [
        {
            "name": "Authorization Management",
        ...

---

## 01_@custc_bite_text_NPS.sql

**Path**: `cuco.dbmaintain/sql/11/22_CuCo_V17.09/01_@custc_bite_text_NPS.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for NPS (Net Promoter Score) related UI labels and messages in a customer portal",
    
    "components": [
        {
            "name": "BITE...

---

## 03_@custc_bite_text_update_with_admin_changes.sql

**Path**: `cuco.dbmaintain/sql/11/22_CuCo_V17.09/03_@custc_bite_text_update_with_admin_changes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and tooltips in the BITE_TEXT table for A1 Business Glasfaser Power product configurations",
    
    "components": [
        {
            "nam...

---

## 02_@custc_bite_text_gamification.sql

**Path**: `cuco.dbmaintain/sql/11/22_CuCo_V17.09/02_@custc_bite_text_gamification.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing gamification-related text content in the BITE_TEXT table, specifically for A1 Sales Hero game interface texts",
    
    "components": [
        {
      ...

---

## 02_@custc_creditLimit_texts.sql

**Path**: `cuco.dbmaintain/sql/11/75_Cuco_V27.09/02_@custc_creditLimit_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text localization update script for credit limit label",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_table",
            "de...

---

## 01_@custc_creditlimit_auth.sql

**Path**: `cuco.dbmaintain/sql/11/75_Cuco_V27.09/01_@custc_creditlimit_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to add credit limit display authorization feature and assign it to superuser role",
    
    "components": [
        {
            "name": "BITE_AUTH",
            "t...

---

## 02_@custc_posInfo.sql

**Path**: `cuco.dbmaintain/sql/11/82_CuCo_V24.04/02_@custc_posInfo.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text resource management for POS (Point of Sale) related UI labels",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_table",
   ...

---

## 01_@custc_a1bi_v7_text.sql

**Path**: `cuco.dbmaintain/sql/11/82_CuCo_V24.04/01_@custc_a1bi_v7_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating business internet service labels in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
         ...

---

## 04_@custc_cct_text_updates.sql

**Path**: `cuco.dbmaintain/sql/11/55_CuCo_V20.08/04_@custc_cct_text_updates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for router configuration and IP packet related UI labels and information messages in German language",
    
    "components"...

---

## 02_@custc_a1ps_v2_add_text.sql

**Path**: `cuco.dbmaintain/sql/11/55_CuCo_V20.08/02_@custc_a1ps_v2_add_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels and identifiers in BITE_TEXT table for Alipay terminal pricing related UI elements",
    
    "components": [
        {
            "name": "BIT...

---

## 01_@custc_a1bi_v3_add_text.sql

**Path**: `cuco.dbmaintain/sql/11/55_CuCo_V20.08/01_@custc_a1bi_v3_add_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating localized UI labels related to IP packet configurations",
    "components": [
        {
            "name": "BITE_TEXT",
        ...

---

## 03_@custc_marketing_product_text.sql

**Path**: `cuco.dbmaintain/sql/11/55_CuCo_V20.08/03_@custc_marketing_product_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text/label translations in a marketing product module, specifically handling German language entries",
    
    "components": [
        {
            ...

---

## 06_@custc_a1bn_marketplace_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/06_@custc_a1bn_marketplace_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to configure authorization and role permissions for A1BN Marketplace feature in Business Network",
    
    "components": [
        {
            "name": "BITE_AUTH",...

---

## 03_@custc_add_etgt_v12_marketplace_texts.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/03_@custc_add_etgt_v12_marketplace_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localization text entries for a marketplace feature in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",...

---

## 05_@custc_add_a1bn_v11_marketplace_texts.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/05_@custc_add_a1bn_v11_marketplace_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localization text entries for a marketplace feature in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",...

---

## 02_@custc_a1bi_marketplace_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/02_@custc_a1bi_marketplace_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to configure authorization and role mappings for Business Marketplace feature in A1BI system",
    
    "components": [
        {
            "name": "BITE_AUTH",
   ...

---

## 01_@custc_add_a1bi_v5_marketplace_texts.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/01_@custc_add_a1bi_v5_marketplace_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text labels and translations for a marketplace feature in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operation...

---

## 07_@custc_admin_copy_marketplace_products_texts.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/07_@custc_admin_copy_marketplace_products_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for marketplace product cloning functionality in the admin interface",
    "components": [
        {
            "name": "BITE_TEXT",
         ...

---

## 04_@custc_etgt_marketplace_role_auth.sql

**Path**: `cuco.dbmaintain/sql/11/69_CuCo_V21.12.2/04_@custc_etgt_marketplace_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to configure marketplace feature authorization and role assignments for ETGT system",
    
    "components": [
        {
            "name": "BITE_AUTH",
            ...

---

## 02_@custc_bite_text_for_GFP_300_A1BN.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/02_@custc_bite_text_for_GFP_300_A1BN.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for A1BN Gigaspeed product configurations and tooltips",
    
    "components": [
        {
            "name": "BITE_TEXT T...

---

## 12_@custc_etgtv10_activation.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/12_@custc_etgtv10_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update Product Offering Version (POV) records for ETGT product version management",
    
    "components": [
        {
            "name": "CCT_POV Table...

---

## 04_@custc_bizkov7_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/04_@custc_bizkov7_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) Calc Tool text labels and configurations specific to Business Kombi v7 product",
    
    "components": [
        {
      ...

---

## 09_@custc_bpbV4_activation.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/09_@custc_bpbV4_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update BPB (Business Product Bundle) version configurations in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation...

---

## 11_@custc_etgtv10_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/11_@custc_etgtv10_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo Calculation Tool's text labels and enumerations for the etgt v10 product",
    
    "components": [
        {
            "name": "BITE_TEXT Table ...

---

## 13_@custc_newProductBrowserTableView_AdminSettings.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/13_@custc_newProductBrowserTableView_AdminSettings.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for product browser table view settings and related admin interface text labels",
    
    "components": [
        {
            "name": "BITE_TEXT Tabl...

---

## 08_@custc_bpbv4_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/08_@custc_bpbv4_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for CuCo (Customer Configuration) tool text labels, specifically for BPB (Breitband Pro Business) v4 product configuration",
    
    "components": [
      ...

---

## 01_@custc_etgt_VoiceButler.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/01_@custc_etgt_VoiceButler.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text entries for A1 Voice Butler service options in a localization/configuration table",
    
    "components": [
        {
            "name": "BITE_TEXT t...

---

## 14_@custc_bite_text_update_for_RLAH.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/14_@custc_bite_text_update_for_RLAH.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to remove RLAH (Roam Like At Home) related text entries from the bite_text table",
    "components": [
        {
            "name": "bite_text table",
  ...

---

## 10_@custc_bite_text_fiber_product_300_BPB.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/10_@custc_bite_text_fiber_product_300_BPB.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update BITE_TEXT table with ADSL speed product descriptions and labels for A1 Breitband Pro Business products",
    
    "components": [
        {
            "nam...

---

## 03_@custc_bizkoV7_activation.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/03_@custc_bizkoV7_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update BIZKO product offering versions by activating V7 and deactivating V6",
    
    "components": [
        {
            "name": "CCT_POV Table Opera...

---

## 07_@custc_fibV5_activation.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/07_@custc_fibV5_activation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update FIB (Business Internet) product version from V4 to V5 in the CCT_POV table",
    
    "components": [
        {
            "name": "CCT_POV Table...

---

## 05_@custc_bizusatzoptionenv2_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/05_@custc_bizusatzoptionenv2_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for business add-on options (Zusatzoptionen) text labels in a customer configuration tool",
    
    "components": [
        {
            "name": "BITE_TEX...

---

## 06_@custc_fibv5_initialization.sql

**Path**: `cuco.dbmaintain/sql/11/19_CuCo_V17.06/06_@custc_fibv5_initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for customer configuration tool (CuCo) text labels and UI elements for FIB (Festnetz-Internet Business) v5 product",
    
    "components": [
        {
    ...

---

## 03_@custc_LOGS_CUCO.sql

**Path**: `cuco.dbmaintain/sql/11/26_CuCo_V18.01.02/03_@custc_LOGS_CUCO.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a logging table for customer access tracking with associated permissions and synonyms",
    
    "components": [
        {
            "name": "cuco_logs",
            "type"...

---

## 05_@custc_bite_text_update_with_admin_changes.sql

**Path**: `cuco.dbmaintain/sql/11/26_CuCo_V18.01.02/05_@custc_bite_text_update_with_admin_changes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text entries in BITE_TEXT table for tooltip and label configurations, primarily related to security package and unavailable action messages",
    
    "comp...

---

## 01_@custc_bite_text_Mobile_Password.sql

**Path**: `cuco.dbmaintain/sql/11/26_CuCo_V18.01.02/01_@custc_bite_text_Mobile_Password.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script for managing UI text/label configurations in multiple languages for a mobile password management interface",
    
    "components": [
        {
            "name": "B...

---

## 04_@custc_bite_text_BIZKOV8_MissingText.sql

**Path**: `cuco.dbmaintain/sql/11/26_CuCo_V18.01.02/04_@custc_bite_text_BIZKOV8_MissingText.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database text content management script for updating business-related text labels in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operatio...

---

## 02_@custc_update_bite_text_Mobile_Password.sql

**Path**: `cuco.dbmaintain/sql/11/26_CuCo_V18.01.02/02_@custc_update_bite_text_Mobile_Password.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text messages and roles related to mobile password functionality",
    "components": [
        {
            "name": "BITE_TEXT Updates",
            "type"...

---

## 01_@custc_bite_CMSYS-9442.sql

**Path**: `cuco.dbmaintain/sql/11/78_Cuco_V30.12/01_@custc_bite_CMSYS-9442.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration update script to modify BITE_SETTING table entry for hiding legacy panels in VBM NBO feature",
    
    "components": [
        {
            "name": "BITE_SET...

---

## 02_@custc_daas_quote_text-initialization.sql

**Path**: `cuco.dbmaintain/sql/11/78_Cuco_V30.12/02_@custc_daas_quote_text-initialization.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL initialization script for text labels and messages in a DaaS (Device as a Service) quoting system, specifically handling German language content",
    
    "components": [
      ...

---

## 01_@custc_add_daas_v2.sql

**Path**: `cuco.dbmaintain/sql/11/78_Cuco_V30.12/01_@custc_add_daas_v2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update DaaS (Device as a Service) product offering versions in CCT_POV table",
    "components": [
        {
            "name": "CCT_POV Table Operation...

---

## 01_@custc_bite_text_Mariposa_Miscellaneous.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/01_@custc_bite_text_Mariposa_Miscellaneous.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script for text localization and clearance rules configuration",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_tab...

---

## 20_@custc_bite_text_missingSql.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/20_@custc_bite_text_missingSql.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text labels in BITE_TEXT table for customer communication",
    
    "components": [
        {
            "name": "BITE_TEXT Table Operation",
...

---

## 12_@custc_cuco_Links_dataUpdate.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/12_@custc_cuco_Links_dataUpdate.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update external link configurations in the CUCO_LINKS table for A1 Telekom's internal systems and tools",
    
    "components": [
        {
          ...

---

## 10_@custc_OrgStructureImport_Update.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/10_@custc_OrgStructureImport_Update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema update script for organization structure import functionality and related text messages",
    
    "components": [
        {
            "name": "CCT_APPROVER_HIERARC...

---

## 04_@custc_bite_text_Mariposa_Miscellaneous.2.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/04_@custc_bite_text_Mariposa_Miscellaneous.2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database localization text maintenance script for updating UI text labels in German language",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "dat...

---

## 25_@custc_Mariposa_additionalAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/25_@custc_Mariposa_additionalAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product attributes for Public Sector Health Care (PSHC) offerings in the CCT_PRODUCT_TAB_ATTRIBUTE table",
    
    "components": [
        {
    ...

---

## 15_@custc_V_MOBIL_NUTZUNG_ScriptUpdate.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/15_@custc_V_MOBIL_NUTZUNG_ScriptUpdate.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view for mobile usage tracking and billing data aggregation",
    "components": [
        {
            "name": "v_mobil_nutzung",
            "type": "database_vi...

---

## 17_@custc_bite_text_a1bi_AktionGrundpaket.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/17_@custc_bite_text_a1bi_AktionGrundpaket.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage localized text entries for action package offer types in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT",
            "t...

---

## 21_@custc_Mariposa_additionalAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/21_@custc_Mariposa_additionalAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update product attributes for mobile tariffs in the CCT_PRODUCT_TAB_ATTRIBUTE table",
    
    "components": [
        {
            "name": "CCT_PRODUCT...

---

## 22_@custc_ViewUpdatesForProductNutzungs.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/22_@custc_ViewUpdatesForProductNutzungs.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and updates database views for customer phone number formatting and usage tracking (mobile and internet)",
    
    "components": [
        {
            "name": "V_RUFNUMMER...

---

## 09_@custc_Mariposa_CUCO_LINKS_datamodel.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/09_@custc_Mariposa_CUCO_LINKS_datamodel.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table for storing BUE (Business Unit Entity) links with associated metadata and grants access permissions",
    
    "components": [
        {
            "name": ...

---

## 03_@custc_emailDomainChange_updateTableColumns.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/03_@custc_emailDomainChange_updateTableColumns.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update email domain from 'a1telekom.at' to 'a1.at' across multiple tables",
    
    "components": [
        {
            "name": "Email Domain Update S...

---

## 02_@custc_emaildomainchange_updateDBEntries_text.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/02_@custc_emaildomainchange_updateDBEntries_text.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update email domain configurations and team email settings for the CuCo system",
    
    "components": [
        {
            "name": "Text Configura...

---

## 08_@custc_bite_role_auth_update_MariposaLinks.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/08_@custc_bite_role_auth_update_MariposaLinks.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update authorization and role mappings for BSNotes Links functionality in CuCo Mariposa system",
    
    "components": [
        {
            "name": "bite_auth"...

---

## 24_@custc_bite_text_Mariposa_Mail_Process.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/24_@custc_bite_text_Mariposa_Mail_Process.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage error message texts in BITE_TEXT table for quote clearance process",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "dat...

---

## 13_@custc_bite_text_for_dataUsageTable.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/13_@custc_bite_text_for_dataUsageTable.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database maintenance script to update text values in BITE_TEXT table for data usage zone display configuration",
    
    "components": [
        {
            "name": "BITE_TEXT Tab...

---

## 18_@custc_CUCO_LINKS_update.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/18_@custc_CUCO_LINKS_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a numeric product index column to the CCT_PRODUCTOFFERING table",
    
    "components": [
        {
            "name": "CCT_PRODUCTOFFERING",
  ...

---

## 16_@custc_V_INTERNET_NUTZUNG_ScriptUpdate.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/16_@custc_V_INTERNET_NUTZUNG_ScriptUpdate.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view that transforms internet usage data with specific volume and duration calculations based on date conditions",
    "components": [
        {
            "name"...

---

## 05_@custc_missed_Mariposa_authAndRoleGrp.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/05_@custc_missed_Mariposa_authAndRoleGrp.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to configure role-based access control (RBAC) for CCT Superuser role by setting up authorizations and role group mappings",
    
    "components": [
       ...

---

## 11_@app_mariposa_new_datamodel_synonyms.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/11_@app_mariposa_new_datamodel_synonyms.sql`

**Layer**: Persistence

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym to provide an alias for the CUCO_LINKS table in the custc schema",
    "components": [
        {
            "name": "CUCO_LINKS",
            "type": "dat...

---

## 06_@custc_Mariposa_additionalAttributes.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/06_@custc_Mariposa_additionalAttributes.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for updating product attributes and localized text entries in a customer configuration system",
    
    "components": [
        {
            "name": "...

---

## 19_@custc_CUCO_LINKS_updateData.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/19_@custc_CUCO_LINKS_updateData.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates product index values for specific product offerings in the CCT_PRODUCTOFFERING table, appears to be a data migration or reordering script",
    "components": [
        {
    ...

---

## 07_@custc_bite_text_update_Links.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/07_@custc_bite_text_update_Links.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels in the BITE_TEXT table for menu items and UI components",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "da...

---

## 14_@custc_bite_text_Mariposa_Miscellaneous.3.sql

**Path**: `cuco.dbmaintain/sql/11/40_CuCo_V18.11.1/14_@custc_bite_text_Mariposa_Miscellaneous.3.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database content management script for updating UI text labels in multiple languages",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "database_ta...

---

## 18_@custc_visitreport_update.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/18_@custc_visitreport_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add new columns to the si_vi_sbs_product table for visit report functionality",
    
    "components": [
        {
            "name": "si_vi_s...

---

## 07_@custc_cct_bizko.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/07_@custc_cct_bizko.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for product offering and product offering variant (POV) data in the CuCo (Customer Configuration) system",
    
    "components": [
        {
         ...

---

## 14_@custc_cuco_country.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/14_@custc_cuco_country.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database table to store country information with ISO codes and German names, with appropriate access permissions",
    "components": [
        {
            "name": "cuco_c...

---

## 09_@custc_visitreport_update.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/09_@custc_visitreport_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script for visit report product management system",
    "components": [
        {
            "name": "si_vi_sbs_product",
            "type": "database_...

---

## 06_@custc_migration.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/06_@custc_migration.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script for customer contact (CuCo) system notes and reminders data transformation",
    
    "components": [
        {
            "name": "Note Migration Cursor",...

---

## 03_@custc_segNew.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/03_@custc_segNew.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema definition for customer segmentation and task management system",
    "components": [
        {
            "name": "si_attribute_config",
            "type": "databa...

---

## 04_@custc_visitreport.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/04_@custc_visitreport.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation script for a customer visit report system focusing on organizational units, products, and notes",
    "components": [
        {
            "name": "si_vi_sb...

---

## 16_@custc_visitreport_update.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/16_@custc_visitreport_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script for customer contact and visit report system",
    "components": [
        {
            "name": "si_vi_sbs_product_note",
            "type": "da...

---

## 10_@custc_cuco_standard_address.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/10_@custc_cuco_standard_address.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and modifies database schema for standardized address handling, including a new address table and modifications to existing task table",
    
    "components": [
        {
  ...

---

## 17_@custc_si_attribute_config_alter.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/17_@custc_si_attribute_config_alter.sql`

**Layer**: Configuration

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Alter the si_attribute_config table to add a segments column with default value 'all'",
    
    "components": [
        {
            "name": "si_attribute_config",
            "typ...

---

## 05_@app_si_note_synonyms.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/05_@app_si_note_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for SI (Strategic Intelligence) related tables and sequences in the CUCO system",
    "components": [
        {
            "name": "SI Note Synonyms",
    ...

---

## 01_@custc_cct_fib.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/01_@custc_cct_fib.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for product offerings and product offering variants (POV) related to Festnetz Internet Business service",
    
    "components": [
        {
          ...

---

## 11_@app_cuco_standard_address.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/11_@app_cuco_standard_address.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for standard address related database objects, providing an abstraction layer for accessing customer address data",
    "components": [
        {
          ...

---

## 02_@custc_cct_bpb.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/02_@custc_cct_bpb.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for product offering and product offering variant (POV) data in the CuCo system",
    
    "components": [
        {
            "name": "cct_productof...

---

## 08_@custc_cct_etgt_update.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/08_@custc_cct_etgt_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database update script to modify PDF template configuration for ETGT V1 customer offer document",
    "components": [
        {
            "name": "cct_pov",
            "type": "da...

---

## 19_@custc_attribute_config_initfill.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/19_@custc_attribute_config_initfill.sql`

**Layer**: Configuration

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script to populate attribute configuration table with predefined customer feedback and visit report attributes",
    
    "components": [
        {
          ...

---

## 13_@custc_cuco_standard_address_update.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/13_@custc_cuco_standard_address_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a customer ID column to the standard address table",
    
    "components": [
        {
            "name": "cuco_standard_address",
            "...

---

## 15_@app_cuco_country.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/15_@app_cuco_country.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database synonym for the cuco_country table, providing an alias to access the table in the custc schema",
    "components": [
        {
            "name": "cuco_country",
...

---

## 22_@custc_visitreport_role.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/22_@custc_visitreport_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script for visit report access permissions",
    "components": [
        {
            "name": "bite_role",
            "type": "database_table",
        ...

---

## 21_@custc_segNewRoleMigration.sql

**Path**: `cuco.dbmaintain/sql/10/01_CuCo_V5.0.0/21_@custc_segNewRoleMigration.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to update role-based access control (RBAC) system by adding new roles and migrating users from legacy SEG roles to new role structure",
    
    "components...

---

## 02_@custc_kunde.sql

**Path**: `cuco.dbmaintain/sql/09/04_CuCo_V3.13.0/02_@custc_kunde.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add customer support office fields and create a view",
    "components": [
        {
            "name": "kunde1",
            "type": "databas...

---

## 01_@dwh_kunde.sql

**Path**: `cuco.dbmaintain/sql/09/04_CuCo_V3.13.0/01_@dwh_kunde.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add new customer-related fields to the 'kunde' table in a data warehouse environment",
    
    "components": [
        {
            "name": "...

---

## 01_@custc_PaST_setup_for_ADX.sql

**Path**: `cuco.dbmaintain/sql/09/02_CuCo_V3.11.0/01_@custc_PaST_setup_for_ADX.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database setup script for ADX mobile billing configuration, modifying billing types and valid area codes",
    
    "components": [
        {
            "name": "CUCO_VERRECHNUNGSAR...

---

## 01_@custc_changeUuserColumns.sql

**Path**: `cuco.dbmaintain/sql/09/06_CuCo_V4.0.1/01_@custc_changeUuserColumns.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to standardize user-related column lengths and trim whitespace from existing values",
    
    "components": [
        {
            "name": "Sche...

---

## 03_@custc_custc_adjustments_for_mail_sending.sql

**Path**: `cuco.dbmaintain/sql/09/01_CuCo_V3.8.0/03_@custc_custc_adjustments_for_mail_sending.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for email server settings in the CuCo system",
    "components": [
        {
            "name": "CUSTC_ADJUSTMENTS",
            "type": "database_tabl...

---

## 02_@custc_bite_portlet_conf_grants.sql

**Path**: `cuco.dbmaintain/sql/09/01_CuCo_V3.8.0/02_@custc_bite_portlet_conf_grants.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database permission configuration script that grants access rights and creates a synonym for the BITE_PORTLET_CONF table",
    "components": [
        {
            "name": "BITE_POR...

---

## 05_@custc_salesinformation_fixed_xpaths_in_update.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/05_@custc_salesinformation_fixed_xpaths_in_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Updates sales information fields in cct_quote table by extracting values from XML content using specific XPaths",
    
    "components": [
        {
            "name": "SQL Update S...

---

## 06_@custc_totals_update.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/06_@custc_totals_update.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification and data migration script for cost totals in quotes system",
    "components": [
        {
            "name": "Schema Modification",
            "type":...

---

## 03_@custc_cct_etgt.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/03_@custc_cct_etgt.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database initialization script for product offerings and product offering variants (POV) in the CuCo system",
    
    "components": [
        {
            "name": "cct_productoffer...

---

## 04_@custc_role.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/04_@custc_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role definition script for MyCuco application's quote viewing permissions",
    
    "components": [
        {
            "name": "bite_role",
            "type": "database...

---

## 02_@custc_salesinformation.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/02_@custc_salesinformation.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification and data migration script for customer quote sales information",
    "components": [
        {
            "name": "cct_quote table modification",
      ...

---

## 01_@custc_cct_sequenceResetJob.sql

**Path**: `cuco.dbmaintain/sql/09/07_CuCo_V4.1.0/01_@custc_cct_sequenceResetJob.sql`

**Layer**: Batch Process

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates and configures a scheduled Oracle database job to reset a quote number sequence annually",
    
    "components": [
        {
            "name": "QuoteNumberResetJob",
     ...

---

## 03_@custc_dwh_reporting_view.sql

**Path**: `cuco.dbmaintain/sql/09/03_CuCo_V3.12.0/03_@custc_dwh_reporting_view.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a reporting view to track customer data loading events in the CUCO system, excluding specific user activities",
    
    "components": [
        {
            "name": "V_REP_...

---

## 02_@custc_product_tree_user_role.sql

**Path**: `cuco.dbmaintain/sql/09/03_CuCo_V3.12.0/02_@custc_product_tree_user_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database migration script to assign the ROLE_CUCO_PRODUCT_TREE role to users who currently have ROLE_CUCO_PRODUCT_BROWSER role",
    
    "components": [
        {
            "name"...

---

## 01_@custc_product_tree_role.sql

**Path**: `cuco.dbmaintain/sql/09/03_CuCo_V3.12.0/01_@custc_product_tree_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role insertion script for CuCo Product Tree functionality based on Customer Inventory",
    
    "components": [
        {
            "name": "BITE_ROLE",
            "type...

---

## 03_@app_cct_synonyms.sql

**Path**: `cuco.dbmaintain/sql/09/05_CuCo_V4.0.0/03_@app_cct_synonyms.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates database synonyms for CCT (Customer Configuration Tool) tables and sequences in a database schema",
    "components": [
        {
            "name": "Database Synonyms",
   ...

---

## 01_@custc_cct_creates.sql

**Path**: `cuco.dbmaintain/sql/09/05_CuCo_V4.0.0/01_@custc_cct_creates.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation script for a Customer Contract (CuCo) system managing product offerings, quotes and opportunities",
    
    "components": [
        {
            "name": "P...

---

## 02_@custc_cct_role.sql

**Path**: `cuco.dbmaintain/sql/09/05_CuCo_V4.0.0/02_@custc_cct_role.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script for CuCo Calculator Tool that inserts a default role",
    "components": [
        {
            "name": "bite_role",
            "type": "database...

---

## 02_@custc_mycucoperformance.sql

**Path**: `cuco.dbmaintain/sql/08/01_CuCo_V3.4.0/02_@custc_mycucoperformance.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema creation and modification script for customer data management and performance tracking",
    "components": [
        {
            "name": "kunde_gesamt",
           ...

---

## 01_@custc_roles.sql

**Path**: `cuco.dbmaintain/sql/08/03_CuCo_V3.7.0/01_@custc_roles.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database role configuration script that adds premium partner roles for the CuCo system",
    
    "components": [
        {
            "name": "bite_role table",
            "type":...

---

## 02_@custc_bite_auth.sql

**Path**: `cuco.dbmaintain/sql/08/04_CuCo_V3.8.0/02_@custc_bite_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage authorization entries in BITE_AUTH table, defining system access permissions and link authorizations",
    "components": [
        {
            "name": "BI...

---

## 03_@custc_bite_auth.sql

**Path**: `cuco.dbmaintain/sql/08/04_CuCo_V3.8.0/03_@custc_bite_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database authorization configuration script that inserts a new tariff guide authorization record",
    "components": [
        {
            "name": "BITE_AUTH",
            "type": ...

---

## 05_@custc_kunde_gesamt.sql

**Path**: `cuco.dbmaintain/sql/08/02_CuCo_V3.5.0/05_@custc_kunde_gesamt.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification script to add churn risk tracking capability for mobile customers",
    
    "components": [
        {
            "name": "kunde_gesamt table modificati...

---

## 02_@custc_RUFNUMMER1.sql

**Path**: `cuco.dbmaintain/sql/08/02_CuCo_V3.5.0/02_@custc_RUFNUMMER1.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a churn risk indicator column for mobile numbers",
    "components": [
        {
            "name": "rufnummer1",
            "type": "database_t...

---

## 01_@dwh_RUFNUMMER.sql

**Path**: `cuco.dbmaintain/sql/08/02_CuCo_V3.5.0/01_@dwh_RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a churn risk indicator column for mobile numbers",
    "components": [
        {
            "name": "rufnummer",
            "type": "database_ta...

---

## 03_@custc_RUFNUMMER2.sql

**Path**: `cuco.dbmaintain/sql/08/02_CuCo_V3.5.0/03_@custc_RUFNUMMER2.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database schema modification to add a churn risk indicator column for mobile numbers",
    "components": [
        {
            "name": "rufnummer2",
            "type": "database_t...

---

## 04_@custc_V_RUFNUMMER.sql

**Path**: `cuco.dbmaintain/sql/08/02_CuCo_V3.5.0/04_@custc_V_RUFNUMMER.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Creates a database view 'v_rufnummer' that provides a structured view of telephone number related data including customer, contract, and technical details",
    "components": [
     ...

---

## 02_@custc_a1coachsetting.sql

**Path**: `cuco.dbmaintain/sql/06/01_CuCo_V3.4.0/02_@custc_a1coachsetting.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script to update external link settings by removing InfoCorner link and adding A1 Coach link",
    
    "components": [
        {
            "name": "bite_set...

---

## @custc_settings_#int.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/@custc_settings_#int.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for email notification settings in a test/integration environment",
    
    "components": [
        {
            "name": "BITE_SETTING Table Operation...

---

## @custc_settings_#t360.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/@custc_settings_#t360.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for email notification settings and templates in a customer cockpit application",
    
    "components": [
        {
            "name": "BITE_SETTING T...

---

## @custc_settings_#prod.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/@custc_settings_#prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database configuration script for email notification settings in a customer cockpit application",
    
    "components": [
        {
            "name": "BITE_SETTING Table Operation...

---

## @custc_settings_#dev.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/@custc_settings_#dev.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Development environment configuration script for email notification settings and URL configurations in the BITE system",
    
    "components": [
        {
            "name": "BITE_...

---

## 02_@custc_update_sequences.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/02_@custc_update_sequences.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "A database maintenance script that updates sequence values in Oracle database tables to align with existing maximum primary key values",
    
    "components": [
        {
          ...

---

## 01_@custc_start_main_alert_#prod.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/01_@custc_start_main_alert_#prod.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Post-processing SQL script to initialize alert processing and update customer header status",
    
    "components": [
        {
            "name": "LOAD_DATA",
            "type": ...

---

## @custc_settings_#e2e.sql

**Path**: `cuco.dbmaintain/sql/postprocessing/@custc_settings_#e2e.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Configuration script for email settings and templates in a customer cockpit application",
    "components": [
        {
            "name": "BITE_SETTING Table",
            "type": ...

---

## 02_@custc_add_daas_role_auth.sql

**Path**: `cuco.dbmaintain/sql/25/01_CuCO_V25.02/02_@custc_add_daas_role_auth.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "SQL script to manage DaaS (Device as a Service) role-based authorization by adding special price group permissions",
    "components": [
        {
            "name": "Role Authoriza...

---

## 01_@custc_A1_Family_text.sql

**Path**: `cuco.dbmaintain/sql/25/01_CuCO_V25.02/01_@custc_A1_Family_text.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update UI text labels related to A1 Family feature in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT",
            "type": "dat...

---

## 03_@custc_add_ccs_menu_texts.sql

**Path**: `cuco.dbmaintain/sql/25/01_CuCO_V25.02/03_@custc_add_ccs_menu_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update menu text entries for Cloud Communication Service in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations",
 ...

---

## 02_@custc_add_infotext_label.sql

**Path**: `cuco.dbmaintain/sql/25/02_CuCO_V25.03/02_@custc_add_infotext_label.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update marketing product info text label in the BITE_TEXT table",
    
    "components": [
        {
            "name": "BITE_TEXT table operation",
            "...

---

## 04_@custc_change_label.sql

**Path**: `cuco.dbmaintain/sql/25/02_CuCO_V25.03/04_@custc_change_label.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database content update script for modifying text labels and tariff information in the BITE_TEXT table",
    "components": [
        {
            "name": "BITE_TEXT Table Operations...

---

## 03_@custc_add_a1bnv11_texts.sql

**Path**: `cuco.dbmaintain/sql/25/02_CuCO_V25.03/03_@custc_add_a1bnv11_texts.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to manage text labels and messages for a customer interface, specifically related to IP packet configurations and dual power 5G services",
    
    "components": [
  ...

---

## 01_@custc_add_ccs_voicemail_label.sql

**Path**: `cuco.dbmaintain/sql/25/02_CuCO_V25.03/01_@custc_add_ccs_voicemail_label.sql`

**Layer**: Unknown

**Primary Purpose**: Analysis parsing failed

**Detailed Purpose**: {
    "purpose": "Database script to update text labels for voicemail-related UI elements in the CCS (Customer Communication System) module",
    
    "components": [
        {
            "name": "BI...

---


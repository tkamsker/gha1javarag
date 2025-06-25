# Requirements Document: Database Layer

## 1. Overview
Analysis of database layer components and functionality

## 2. Components
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/100_test_deletes_kunde.sql (SQL script)
  - Purpose: SQL script to delete test customer records from the database
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/037_test_deletes_konto.sql (SQL script)
  - Purpose: Delete test account data from KONTO1 and KONTO2 tables for specific test customer IDs
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/040_test_deletes_rufnummer.sql (SQL script)
  - Purpose: Delete test phone number data from RUFNUMMER1 and RUFNUMMER2 tables for specific test customer IDs
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/050_test_deletes_ansprechpartner.sql (SQL script)
  - Purpose: Delete test contact person data from ANSPRECHPARTNER1 and ANSPRECHPARTNER2 tables for specific test customer IDs
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/035_test_deletes_bestand.sql (SQL script)
  - Purpose: Delete test data from BESTAND1 and BESTAND2 tables for specific customer IDs
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/5_test_inserts_bestand.sql (SQL script)
  - Purpose: Insert test data into BESTAND1 and BESTAND2 tables
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/2_test_inserts_ansprechpartner.sql (SQL script)
  - Purpose: Insert test contact person data into ANSPRECHPARTNER1 table
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/1_test_inserts_kunde.sql (SQL script)
  - Purpose: Insert test customer data into KUNDE tables for testing purposes
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/4_test_inserts_konto.sql (SQL script)
  - Purpose: Insert test account data into KONTO tables for testing purposes
- cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/3_test_inserts_rufnummer.sql (SQL script)
  - Purpose: Insert test phone number data into RUFNUMMER tables for testing purposes

## 3. Functionality
### Main Features
- Delete test account data from KONTO1 and KONTO2 tables for specific test customer IDs
- SQL script to delete test customer records from the database
- Delete test contact person data from ANSPRECHPARTNER1 and ANSPRECHPARTNER2 tables for specific test customer IDs
- Delete test data from BESTAND1 and BESTAND2 tables for specific customer IDs
- Delete test phone number data from RUFNUMMER1 and RUFNUMMER2 tables for specific test customer IDs
- Insert test phone number data into RUFNUMMER tables for testing purposes
- Insert test contact person data into ANSPRECHPARTNER1 table
- Insert test data into BESTAND1 and BESTAND2 tables
- Insert test account data into KONTO tables for testing purposes
- Insert test customer data into KUNDE tables for testing purposes

### Data Structures
#### kunde1
Fields:
- kunde_id
Relationships:
- Paired with kunde2 table
#### kunde2
Fields:
- kunde_id
Relationships:
- Paired with kunde1 table
#### KONTO1
Fields:
- kunde_id
Relationships:
- References customer table via kunde_id
#### KONTO2
Fields:
- kunde_id
Relationships:
- References customer table via kunde_id
#### RUFNUMMER1
Fields:
- kunde_id
Relationships:
- References customer table via kunde_id
#### RUFNUMMER2
Fields:
- kunde_id
Relationships:
- References customer table via kunde_id
#### ANSPRECHPARTNER1
Fields:
- KUNDE_ID
Relationships:
- References customer table via KUNDE_ID
#### ANSPRECHPARTNER2
Fields:
- KUNDE_ID
Relationships:
- References customer table via KUNDE_ID
#### BESTAND1
Fields:
- kunde_id
Relationships:
- References customer records
#### BESTAND2
Fields:
- kunde_id
Relationships:
- References customer records
#### BESTAND1/BESTAND2
Fields:
- BESTAND_ID
- KUNDE_ID
- VERTRAG_ID
- RUFNUMMER
- AON_KUNDENNUMMER_ID
- KONTO_ID
Relationships:
- Links to customer records
- Links to contract records
- Links to account records
#### ANSPRECHPARTNER1
Fields:
- KUNDE_ID
- KONTAKT_ROLLE_ID
- HAUPTANPRECHPARTNER_JN
- ROLLE_BEI_TA_BES
- ROLLE_BEIM_KUNDEN_BES
- ANREDE_BES
- TITEL_BES
- NAME
- ADRESSE_2ZEILIG_1
- ADRESSE_2ZEILIG_2
- GEBURTS_DAT
- MOBIL_BES
- RUFNUMMER_TAG_BES
- RUFNUMMER_ABEND_BES
- FAX_BES
- EMAIL_BES
- AKTION_CD
- ANLAGE_TS
- QUELLE_CD
Relationships:
- Links to customer records
#### KUNDE1
Fields:
- HEADER_ID
- KUNDE_ID
- SEG_CD
- KUNDE_TYP_CD
- TITEL_BES
- GESCHLECHT_CD
- ANREDE_BES
- KUNDE_VORNAME
- KUNDE_NAM
- STAAT_CD
- ORT
- PLZ
- STRASSE
- HAUSNUMMER
- GEBURT_DAT
- FIRMENBUCHNUMMER
Relationships:
- Primary table for customer data
#### KONTO1
Fields:
- KUNDE_ID
- KONTO_ID
- ANREDE_BES
- TITEL_BES
- KUNDE_NAM
- ADRESSE_2ZEILIG_1
- ADRESSE_2ZEILIG_2
- MEDIUM_BES
- AKTION_CD
- ANLAGE_TS
- BAN_ID
- BEN_ID
- AKTIV_CD
Relationships:
- References KUNDE table through KUNDE_ID
#### RUFNUMMER1
Fields:
- VERTRAG_ID
- KUNDE_ID
- LKZ
- ONKZ
- TN_NUM
- RUFNUMMERNSYSTEM_CD
Relationships:
- References KUNDE table through KUNDE_ID
- References contract through VERTRAG_ID

### Key Methods/Functions
#### CustomerDeleteScript
Description: Removes test customer records from kunde1 and kunde2 tables
#### delete_konto_data
Description: Removes test account records for customer IDs in 999999991-999999994 range
#### delete_rufnummer_data
Description: Removes test phone number records for customer IDs in 999999991-999999994 range
#### delete_ansprechpartner_data
Description: Removes test contact person records for customer IDs in 999999991-999999994 range
#### delete_statements
Description: Series of DELETE statements to remove test customer records
#### insert_statements
Description: Inserts test records with customer, contract, and account details
#### insert_statements
Description: Inserts test contact person records with detailed personal information
#### KUNDE1
Description: Primary customer information table containing personal and business details
#### KONTO1
Description: Account information table with billing and contact details
#### RUFNUMMER1
Description: Phone number information table containing number details and assignments

## 4. Dependencies
- KUNDE tables must exist
- RUFNUMMER1 and RUFNUMMER2 tables must exist
- BESTAND1 table
- Contract table
- ANSPRECHPARTNER1 and ANSPRECHPARTNER2 tables must exist
- Customer table
- Contact role definitions
- Account table structure must be defined
- Phone number table structure must be defined
- Account table
- Customer table structure must be defined
- Database schema must exist
- Customer table must exist
- Contract tables must exist
- BESTAND2 table
- KONTO1 and KONTO2 tables must exist

## 5. Business Rules
- Test customer records must be deleted from both kunde1 and kunde2 tables
- Customer IDs in test data range from 999999991 upwards
- Test accounts must be removed from both KONTO1 and KONTO2 tables
- Test phone numbers must be removed from both RUFNUMMER1 and RUFNUMMER2 tables
- Test contact persons must be removed from both ANSPRECHPARTNER1 and ANSPRECHPARTNER2 tables
- Test data cleanup for customer IDs in range 999999991-999999994
- Test data follows specific ID pattern (9999999xx)
- Contact person records include mandatory personal and contact information
- Uses specific date format for GEBURTS_DAT (birth date)
- Customer records must include basic identification and contact information
- Accounts must be linked to a customer and include address information
- Phone numbers must be associated with a customer and contract
- Phone numbers follow specific format with country code (LKZ), area code (ONKZ), and number (TN_NUM)


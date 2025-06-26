# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/5_test_inserts_bestand.sql

5_test_inserts_bestand.sql
1. Purpose: Populates test data into BESTAND1 and BESTAND2 tables
2. User interactions: None - administrative/test script
3. Data handling:
   - Inserts records with predefined test values
   - Fields: BESTAND_ID, KUNDE_ID, VERTRAG_ID, RUFNUMMER, AON_KUNDENNUMMER_ID, KONTO_ID
4. Business rules:
   - Uses specific ID ranges for test data (99999999x)
   - Maintains parallel records in both BESTAND1 and BESTAND2
   - Phone numbers follow Austrian format (43 xxxx)
5. Dependencies:
   - Tables BESTAND1 and BESTAND2 must exist
   - Referenced IDs must be unique
   - Must run before any tests using this data
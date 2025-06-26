# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/2_test_inserts_ansprechpartner.sql

2_test_inserts_ansprechpartner.sql
1. Purpose: Creates test contact person records in ANSPRECHPARTNER1 table
2. User interactions: None - administrative/test script
3. Data handling:
   - Inserts detailed contact information
   - Includes personal data (name, address, contact details)
   - Handles dates (GEBURTS_DAT)
4. Business rules:
   - Contact roles defined by KONTAKT_ROLLE_ID
   - HAUPTANPRECHPARTNER_JN flag for primary contact status
   - Austrian address format
   - Includes audit fields (AKTION_CD, ANLAGE_TS, QUELLE_CD)
5. Dependencies:
   - ANSPRECHPARTNER1 table must exist
   - Referenced KUNDE_ID must match other test data
   - KONTAKT_ROLLE_ID must be valid
   - Should run in sequence with other test data scripts (numbered 2_)
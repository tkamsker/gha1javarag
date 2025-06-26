# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/4_test_inserts_konto.sql

4_test_inserts_konto.sql
1. Purpose: Populates account (KONTO) tables with test data
2. Data handling:
- Stores account information linked to customers
- Maintains billing/contact information
- Tracks account status and creation details

3. Business rules:
- Each account has unique KONTO_ID
- Links to customer via KUNDE_ID
- Supports multiple address lines
- Tracks account activity status (AKTIV_CD)
- Records creation timestamp (ANLAGE_TS)

4. Dependencies:
- Requires valid KUNDE_ID from KUNDE tables
- May link to billing/authorization systems (BAN_ID, BEN_ID)
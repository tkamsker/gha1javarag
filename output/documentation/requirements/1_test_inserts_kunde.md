# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/1_test_inserts_kunde.sql

1_test_inserts_kunde.sql
1. Purpose: Populates the KUNDE (Customer) tables with test data for customer records
2. Data handling:
- Stores comprehensive customer profile information
- Includes personal details, address info, and business-related data
- Maintains both individual and business customer records

3. Business rules:
- Customers have unique KUNDE_ID
- Multiple contact methods supported (phone numbers, email)
- Supports different customer types (indicated by KUNDE_TYP_CD)
- VIP status tracking (VIP_JN field)
- Regional and team assignments tracked

4. Dependencies:
- Primary table for customer information
- Referenced by other tables (KONTO, RUFNUMMER) via KUNDE_ID
# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/037_test_deletes_konto.sql

037_test_deletes_konto.sql
1. Purpose: Cleanup script to remove test account data from KONTO1 and KONTO2 tables
2. User interactions: None - backend database maintenance script
3. Data handling:
   - Deletes account records based on specific kunde_id values
   - Targets test customer IDs in 999999xxx range
   - Operates on dual table structure (KONTO1 and KONTO2)
4. Business rules:
   - Maintains data integrity by removing test accounts
   - Uses predefined test customer IDs
5. Dependencies:
   - Requires existence of KONTO1 and KONTO2 tables
   - Must be executed before test data insertion
   - Related to customer (kunde) data structure
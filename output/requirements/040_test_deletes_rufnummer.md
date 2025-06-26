# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/040_test_deletes_rufnummer.sql

040_test_deletes_rufnummer.sql
1. Purpose: Cleanup script to remove test phone number data from RUFNUMMER1 and RUFNUMMER2 tables
2. User interactions: None - backend database maintenance script
3. Data handling:
   - Deletes phone number records based on specific kunde_id values
   - Targets test customer IDs in 999999xxx range
   - Operates on dual table structure (RUFNUMMER1 and RUFNUMMER2)
4. Business rules:
   - Maintains data integrity by removing test phone numbers
   - Uses predefined test customer IDs
5. Dependencies:
   - Requires existence of RUFNUMMER1 and RUFNUMMER2 tables
   - Must be executed before test data insertion
   - Related to customer (kunde) data structure
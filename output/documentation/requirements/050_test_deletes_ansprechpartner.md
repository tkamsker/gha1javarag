# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/050_test_deletes_ansprechpartner.sql

050_test_deletes_ansprechpartner.sql
1. Purpose: Cleanup script to remove test contact person data from ANSPRECHPARTNER1 and ANSPRECHPARTNER2 tables
2. User interactions: None - backend database maintenance script
3. Data handling:
   - Deletes contact person records based on specific KUNDE_ID values
   - Targets test customer IDs in 999999xxx range
   - Operates on dual table structure (ANSPRECHPARTNER1 and ANSPRECHPARTNER2)
4. Business rules:
   - Maintains data integrity by removing test contact persons
   - Uses predefined test customer IDs
5. Dependencies:
   - Requires existence of ANSPRECHPARTNER1 and ANSPRECHPARTNER2 tables
   - Must be executed before test data insertion
   - Related to customer (kunde) data structure

Common Patterns:
- All files follow similar naming convention (xxx_test_deletes_[entity].sql)
- All use dual table structure (Table1 and Table2)
- All reference same test customer IDs
- All are part of test data management system
- Execution order appears to be managed by filename numbering (037, 040, 050)
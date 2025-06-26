# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/100_test_deletes_kunde.sql

100_test_deletes_kunde.sql
1. Purpose: Test data cleanup script for customer records
- Removes test customer records from database
- Maintains data integrity in test environment

2. User Interactions:
- No direct user interactions
- Used by testing framework/administrators

3. Data Handling:
- Deletes customer records from kunde1 and kunde2 tables
- Targets specific test customer IDs (999999991-999999994)
- Sequential deletion from multiple tables

4. Business Rules:
- Must maintain referential integrity
- Follows specific customer ID pattern for test data
- Requires deletion from both kunde1 and kunde2 tables

5. Dependencies:
- Depends on existence of kunde1 and kunde2 tables
- Requires matching customer IDs across tables
- Must be executed in proper sequence with other test data scripts
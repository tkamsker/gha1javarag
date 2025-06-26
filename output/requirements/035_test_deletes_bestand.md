# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/deletes/035_test_deletes_bestand.sql

035_test_deletes_bestand.sql
1. Purpose: Cleanup script to remove test data from BESTAND1 and BESTAND2 tables
2. User interactions: None - administrative/test script
3. Data handling:
   - Deletes records based on specific kunde_id values (999999991-999999994)
   - Affects two tables: BESTAND1 and BESTAND2
4. Business rules:
   - Records must be deleted from both tables for data consistency
   - Uses specific test kunde_id values in 999999xxx range
5. Dependencies:
   - Must run after test data has been used
   - Tables BESTAND1 and BESTAND2 must exist
   - Referenced kunde_id values must match test data
# Requirements Analysis: cuco/src/main/resources/at/a1ta/cuco/service/sql/testdata/inserts/3_test_inserts_rufnummer.sql

3_test_inserts_rufnummer.sql
1. Purpose: Populates phone number (RUFNUMMER) tables with test data
2. Data handling:
- Stores telephone number information
- Links numbers to contracts and customers

3. Business rules:
- Numbers structured with country code (LKZ), area code (ONKZ), and number (TN_NUM)
- Each number linked to specific contract (VERTRAG_ID) and customer (KUNDE_ID)
- Supports different numbering systems (RUFNUMMERNSYSTEM_CD)

4. Dependencies:
- Requires valid KUNDE_ID from KUNDE tables
- Requires valid VERTRAG_ID (contract ID)
- Part of larger telecommunications service system

Common Characteristics:
- All files are part of test data setup
- Maintain data in multiple versions of tables (numbered suffixes)
- Support a telecommunications/customer service system
- Follow strict data structure and relationship rules
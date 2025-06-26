# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/VbmProductsDao.java

VbmProductsDao.java
1. Purpose: Interface for managing VBM (Value-Based Management) product data access operations
2. User Interactions:
- Allows querying VBM products based on customer criteria
- Handles product details and decline reasons

3. Data Handling:
- Retrieves lists of VBM products
- Manages product details and decline reasons
- Supports filtering by customer ID, product name, time period, and scoring

4. Business Rules:
- Products can be filtered by scoring total
- Results can be limited to maximum count
- Supports period-based queries (monthYearPeriod)

5. Dependencies:
- Relies on VBMProduct, VBMProductDetails, and VBMDeclineReason DTOs
- Part of core DAO layer
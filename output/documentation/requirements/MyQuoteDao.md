# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/dao/db/MyQuoteDao.java

MyQuoteDao.java
1. Purpose: Interface for managing sales opportunities and quotes
2. User interactions:
   - Loading opportunities with filtering
   - Searching opportunities
   - Handling sales info overview
3. Data handling:
   - Returns SearchResult<MyOpportunity> for opportunity queries
   - Handles OpportunityFilter parameters
   - Manages sales information data
4. Business rules:
   - Supports filtering between customer/non-customer opportunities
   - Integrates with sales info overview functionality
5. Dependencies:
   - bite.core.shared.dto.SearchResult
   - cuco.core.shared.dto packages
   - Sales info related components
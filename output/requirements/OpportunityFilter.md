# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/OpportunityFilter.java

OpportunityFilter.java
1. Purpose and functionality:
- Defines filtering criteria for opportunity/quote searches
- Implements different filter types for viewing opportunities (ALL, MYQUOTES, MYAPPROVINGS, MYCUSTOMERS)
- Provides constants for various search parameters

2. User interactions:
- Users can filter opportunities based on:
  - Quote number
  - Filter type
  - Party ID
  - First/Last name
  - Date ranges
  - Status

3. Data handling:
- Uses enums for filter types
- Contains static constants for field names
- Likely used as a DTO for search/filter requests

4. Business rules:
- Supports different view contexts (all quotes, my quotes, pending approvals, customer-specific)
- Implements filtering based on business-relevant parameters

5. Dependencies:
- Requires Date utility
- Likely used by search/query services
- Part of the core DTO package
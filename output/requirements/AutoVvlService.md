# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/AutoVvlService.java

AutoVvlService.java
1. Purpose and functionality:
- Interface defining services for retrieving automatic VVL (likely contract/subscription) information
- Provides methods to fetch VVL info using either call number or BAN (Billing Account Number)

2. User interactions:
- No direct user interactions - service interface layer
- Used by other components to retrieve VVL information

3. Data handling:
- Returns AutoVvlInfo objects containing VVL-related data
- Accepts CallNumber objects and String BAN numbers as input parameters

4. Business rules:
- Must support lookup by both call number and BAN number
- Implements separation of concerns by isolating VVL retrieval logic

5. Dependencies:
- Depends on AutoVvlInfo DTO
- Depends on CallNumber DTO
- Likely integrated with billing/subscription systems
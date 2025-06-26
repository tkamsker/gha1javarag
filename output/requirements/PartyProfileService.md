# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/PartyProfileService.java

PartyProfileService.java
1. Purpose and functionality:
- Interface defining services for retrieving party/user profile information
- Provides methods to fetch different types of user profiles (Party, BVK, OneTV)

2. User interactions:
- No direct user interactions - service layer interface
- Used by other components to retrieve profile data

3. Data handling:
- Returns PartyProfileInfo objects for party queries
- Returns String data for BVK and OneTV user queries
- Read-only operations (no data modification methods)

4. Business rules:
- Requires valid partyId for party profile retrieval
- Separate handling for different user types (Party, BVK, OneTV)

5. Dependencies:
- Depends on PartyProfileInfo DTO
- Likely implemented by service classes
- Used by controllers or other services needing profile data
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/PartyCustomerLoyaltyService.java

PartyCustomerLoyaltyService.java
1. Purpose: Interface defining service for retrieving customer loyalty information for a party
2. User Interactions: None directly - service layer interface
3. Data Handling:
   - Retrieves PartyCustomerLoyaltyInfo based on partyId
   - Uses long type for party identification
4. Business Rules:
   - Requires valid partyId to retrieve loyalty information
5. Dependencies:
   - PartyCustomerLoyaltyInfo DTO
   - Core service component
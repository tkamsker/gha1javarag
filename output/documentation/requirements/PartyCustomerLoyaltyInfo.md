# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyCustomerLoyaltyInfo.java

PartyCustomerLoyaltyInfo.java
1. Purpose and functionality:
- Manages customer loyalty information for a party
- Tracks the status of loyalty data loading and processing
- Implements Serializable for data transfer

2. Data handling:
- Defines status constants for different states:
  - ERROR (99)
  - LOADING (-1)
  - NOT_RECEIVED (98)
  - LOADED (0)
- Maintains status tracking and customer status flags

3. Business rules:
- Status must be one of the predefined constants
- Supports state management for loyalty information loading
- Default state is LOADING (-1)

4. Dependencies and relationships:
- Part of the party profile management system
- Used in customer loyalty tracking and processing
- Integrated with customer data management systems
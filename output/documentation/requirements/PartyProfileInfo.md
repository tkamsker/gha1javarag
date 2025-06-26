# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyProfileInfo.java

PartyProfileInfo.java
1. Purpose and functionality:
- Manages party (user/organization) profile information
- Handles profile loading states and status tracking
- Provides serializable profile data structure

2. Data handling:
- Implements Serializable interface
- Uses ArrayList for data collections
- Defines status constants (ERROR, LOADING, NOT_RECEIVED, LOADED)

3. Business rules:
- Status codes define profile states:
  - ERROR (99): Error state
  - LOADING (-1): Profile loading
  - NOT_RECEIVED (98): Data not yet received
  - LOADED: Successfully loaded

4. Dependencies:
- Core DTO component
- Likely integrated with party/profile management systems
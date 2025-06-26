# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/MyFlashInfo.java

MyFlashInfo.java

1. Purpose and functionality:
- Extends FlashInfo class to store flash message information with additional party-specific details
- Used for system notifications or messages with associated party context

2. User interactions:
- No direct user interactions; serves as a data transfer object

3. Data handling:
- Manages two main fields: partyId (Long) and creatorName (String)
- Implements Serializable for data transfer/persistence
- Standard getter/setter methods for field access

4. Business rules:
- Must maintain inheritance relationship with FlashInfo
- PartyId and creatorName can be null (no validation constraints shown)

5. Dependencies:
- Extends FlashInfo class
- Implements Serializable interface
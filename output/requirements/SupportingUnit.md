# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SupportingUnit.java

SupportingUnit.java
1. Purpose: Represents a support unit entity with status tracking capabilities
2. User Interactions: Status monitoring and support unit information retrieval
3. Data Handling:
   - Implements Serializable
   - Maintains status codes as constants
   - Stores support unit details (SKZ text and support name)
4. Business Rules:
   - Defines status constants:
     - ERROR (99)
     - LOADING (-1)
     - NOT_RECEIVED (98)
     - LOADED (0)
   - Default status is LOADING
5. Dependencies:
   - Java Serializable interface
   - Likely integrated with support/service management system
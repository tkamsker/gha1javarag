# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CustomerBlock.java

CustomerBlock.java
1. Purpose: Represents a block or group of customer data
2. User Interactions: None directly - data container
3. Data Handling:
   - Implements Serializable
   - Contains fields:
     - id (long)
     - name (String)
     - count (long)
     - imported (boolean)
     - data (String)
     - flashInfo (FlashInfo)
   - Standard getter/setter methods
4. Business Rules:
   - Default id is -1
   - Tracks import status
   - Maintains customer block metadata
5. Dependencies:
   - FlashInfo class
   - Serializable interface
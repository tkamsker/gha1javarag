# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/YNBooleanTypeHandler.java

YNBooleanTypeHandler.java
1. Purpose: Custom iBATIS type handler that converts between Java Boolean values and database 'Y'/'N' character representations
2. User interactions: None - purely data layer functionality
3. Data handling:
   - Converts Boolean true → 'Y' and false → 'N' for database storage
   - Converts 'Y' → Boolean true and 'N' → Boolean false when reading from database
   - Handles null values
4. Business rules:
   - Only 'Y' maps to true, all other non-null values map to false
   - Preserves null values in both directions
5. Dependencies:
   - Requires iBATIS SQL mapping framework
   - Implements TypeHandlerCallback interface
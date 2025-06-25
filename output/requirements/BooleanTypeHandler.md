# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/dao/util/BooleanTypeHandler.java

BooleanTypeHandler.java
1. Purpose: Custom iBATIS type handler for converting between Java Boolean values and database numeric (1/0) representations
2. User interactions: None - data layer functionality
3. Data handling:
   - Converts Boolean true → "1" and false → "0" for database storage
   - Converts "1" → Boolean true and "0" → Boolean false when reading
   - Handles null values
4. Business rules:
   - Uses "1" to represent true and "0" to represent false
   - Defined constants TRUE_STRING and likely FALSE_STRING
   - Preserves null values
5. Dependencies:
   - iBATIS framework
   - Implements TypeHandlerCallback interface

Common themes across these files:
- All are data layer utilities for type conversion
- Part of the iBATIS database mapping framework
- Handle null value preservation
- Follow similar implementation patterns
- No direct user interaction
- Focus on data type conversion and representation
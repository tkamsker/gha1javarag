# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/MetaDataEntryType.java

MetaDataEntryType.java
1. Purpose and functionality:
- Defines enumerated types for metadata entries
- Supports various data type classifications
- Maps types to numeric values

2. User interactions:
- No direct user interactions
- Used for system-level type classification

3. Data handling:
- Defines 9 different entry types:
  - STRING(1), LONG(2), BOOLEAN(3)
  - DATE_TIME(4), DECIMAL(5)
  - LKMS_ID(6)
  - MBIT(7), KBIT(8), MB(9)
- Each type has an associated integer value

4. Business rules:
- Each type has a unique numeric identifier
- Supports specific measurement units (MBIT, KBIT, MB)
- Includes special type for LKMS_ID

5. Dependencies:
- No external dependencies
- Used by other components for metadata type classification
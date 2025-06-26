# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/NetworkProvider.java

NetworkProvider.java
1. Purpose: Defines an enumeration of network service providers with associated values and labels
2. User Interactions: Used for display and selection of network providers in UI
3. Data Handling:
   - Stores provider code (value) and display name (label)
   - Provides getter methods for both properties
4. Business Rules:
   - Three defined providers: A1 (T), ANB (A), and COMBINED (C)
   - Each provider must have both a value code and display label
5. Dependencies:
   - Used by other components requiring network provider information
   - Part of the usagedata DTO package
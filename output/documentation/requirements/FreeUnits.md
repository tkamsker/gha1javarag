# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/freeunits/FreeUnits.java

FreeUnits.java
1. Purpose and functionality:
- Manages free units/quotas for services (likely telecommunications)
- Handles different unit types (minutes, seconds, milliseconds)
- Serializable DTO for free units data

2. Data handling:
- Defines constants for different unit types (MIN, SEC, MSEC)
- Likely handles conversion between different time units
- Implements Serializable for data transfer

3. Business rules:
- Standardized unit definitions
- Specific handling for different time-based measurements
- Conversion rules between units must be maintained

4. Dependencies:
- Uses BigInteger for precise numerical calculations
- Core component for quota/usage tracking systems
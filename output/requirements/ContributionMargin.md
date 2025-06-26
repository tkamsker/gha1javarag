# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/ContributionMargin.java

ContributionMargin.java
1. Purpose and functionality:
- Manages contribution margin calculations for tariffs
- Provides indicator-based margin classification
- Includes special handling for unknown margins

2. User interactions:
- No direct user interactions, serves as a calculation model

3. Data handling:
- Implements Serializable
- Manages price and indicator data
- Handles unknown/special cases
- Uses List for data storage

4. Business rules:
- Supports different margin indicators
- Provides immutable UNKNOWN instance
- Handles special cases for margin calculations

5. Dependencies:
- Depends on Price class
- Uses ArrayList for data management
- Part of the larger tariff calculation system

Common themes across files:
- All implement Serializable for data transfer
- Part of a larger tariff management system
- Focus on pricing and financial calculations
- Strong emphasis on data integrity and null safety
- Clear separation of concerns between tariff components
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoComponentProductPrice.java

CuCoComponentProductPrice.java
1. Purpose: Manages pricing information for component products including tax rates and indexation details
2. Data handling:
- Stores price information using CuCoPrice objects
- Tracks base price and current price
- Manages tax rates using BigDecimal for precision
- Handles indexation status and start dates
3. Business rules:
- Must maintain both base price and current price
- Supports price indexation with status tracking
- Includes tax rate calculations
4. Dependencies:
- Extends CuCoProductPriceBase
- Uses IndexationStatus enum
- Relies on CuCoPrice class for price representation
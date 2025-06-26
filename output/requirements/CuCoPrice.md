# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CuCoPrice.java

CuCoPrice.java
1. Purpose and functionality:
- Represents a price structure with currency units and amount
- Simple DTO (Data Transfer Object) for price information
- Implements Serializable for data transfer/persistence

2. User interactions:
- No direct user interactions
- Used as a data container in price-related operations

3. Data handling:
- Stores two fields:
  - units (String): Represents currency or measurement units
  - amount (BigDecimal): Stores the numerical value
- Provides standard getter/setter methods

4. Business rules:
- Uses BigDecimal for precise monetary calculations
- No validation rules implemented in this class

5. Dependencies:
- java.math.BigDecimal
- java.io.Serializable
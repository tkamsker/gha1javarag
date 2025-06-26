# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ProductOfferingTypeHandler.java

ProductOfferingTypeHandler.java
1. Purpose: Custom type handler for ProductOffering objects in iBatis SQL mapping
2. Data handling:
- Handles conversion between database and Java ProductOffering objects
- Implements JDBC parameter setting and result set handling
3. Business rules:
- Must properly map database fields to ProductOffering object properties
4. Dependencies:
- Extends iBatis BaseTypeHandler
- Depends on ProductOffering class
- Uses JDBC interfaces (PreparedStatement, ResultSet, CallableStatement)
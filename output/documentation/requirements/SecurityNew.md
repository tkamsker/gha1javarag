# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/SecurityNew.java

SecurityNew.java
1. Purpose and functionality:
- Extends SecurityBase class to handle new security product offerings
- Represents security-related digital selling products and their pricing
- Specifically handles A1 Cyber Protection products (single and family variants)

2. Data handling:
- Uses boolean flags to track product selection status
- Stores pricing information using BigDecimal for accuracy
- Implements XML serialization via JAXB annotations

3. Business rules:
- Maintains separate pricing for single and family protection products
- Requires price tracking for each security product option
- Inherits base security product functionality from SecurityBase

4. Dependencies:
- Extends SecurityBase
- Uses javax.xml.bind annotations
- Requires BigDecimal for price handling
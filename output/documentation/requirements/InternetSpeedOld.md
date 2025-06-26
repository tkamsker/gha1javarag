# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedOld.java

InternetSpeedOld.java
1. Purpose and functionality:
- Represents legacy internet speed configuration
- Extends InternetSpeedBase with additional virus protection features
- Handles pricing and protection options for internet services

2. Data handling:
- Inherits base internet speed properties
- Manages virus protection status (boolean)
- Handles virus protection pricing (BigDecimal)

3. Business rules:
- Optional virus protection feature
- Price association with protection service
- XML-based data representation

4. Dependencies:
- Extends InternetSpeedBase
- Uses BigDecimal for precise pricing
- JAXB annotations for XML handling
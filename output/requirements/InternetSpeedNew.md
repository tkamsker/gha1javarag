# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetSpeedNew.java

InternetSpeedNew.java
1. Purpose and functionality:
- Manages new internet speed product offerings and related protections
- Extends InternetSpeedBase for core internet speed functionality
- Handles A1 Internet Protection feature configuration

2. Data handling:
- Stores product name information
- Manages boolean flag for A1 Internet Protection status
- Uses XML annotations for data mapping

3. Business rules:
- Must integrate with existing internet speed base functionality
- Supports A1-specific internet protection features
- Requires proper product naming conventions

4. Dependencies:
- Extends InternetSpeedBase class
- Requires javax.xml.bind annotations
- Uses BigDecimal for any pricing-related data
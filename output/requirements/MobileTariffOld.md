# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariffOld.java

MobileTariffOld.java
1. Purpose: Represents legacy mobile tariff information in the digital selling system
2. User interactions: Used to display and manage old/legacy tariff plans
3. Data handling:
   - XML serialization support
   - Stores tariff values and pricing information
   - Implements serialization (serialVersionUID)
4. Business rules:
   - Extends MobileTariffBase for common tariff functionality
   - Maintains legacy tariff information
5. Dependencies:
   - Extends MobileTariffBase
   - Uses JAXB annotations for XML handling
   - Requires BigDecimal for pricing calculations
   - Implements Serializable interface

Common Patterns:
- All classes are part of the digital selling module
- XML serialization is used throughout
- Proper decimal handling for financial calculations
- Inheritance is used for base functionality
- Clear separation between new and old/legacy implementations
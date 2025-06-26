# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/MobileTariffNew.java

MobileTariffNew.java

1. Purpose and functionality:
- Represents a new mobile tariff configuration in a digital selling system
- Extends MobileTariffBase class to inherit common tariff properties
- Handles tariff-specific values and pricing information

2. Data handling:
- Uses XML binding annotations for data serialization/deserialization
- Stores tariff value as String
- Handles BigDecimal values for precise monetary calculations
- Implements Serializable for object persistence

3. Business rules:
- Must extend MobileTariffBase for consistent tariff handling
- Requires proper serialization handling
- Values must follow specific format/precision requirements (implied by BigDecimal usage)

4. Dependencies:
- Extends MobileTariffBase
- Uses javax.xml.bind annotations
- Requires java.math.BigDecimal for calculations
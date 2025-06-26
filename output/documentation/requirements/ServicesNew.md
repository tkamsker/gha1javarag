# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/ServicesNew.java

ServicesNew.java
1. Purpose: Represents new service offerings in the digital selling system, extending ServicesBase
2. User interactions: Captures service selections and pricing information
3. Data handling:
   - Uses XML binding for data serialization
   - Stores boolean flags for service activation
   - Manages pricing using BigDecimal for accuracy
4. Business rules:
   - Tracks A1 Initial Setup service status and pricing
   - Extends ServicesBase for common service functionality
5. Dependencies:
   - Extends ServicesBase
   - Uses JAXB annotations for XML handling
   - Requires BigDecimal for price calculations
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PointOfSaleInfo.java

PointOfSaleInfo.java
1. Purpose and functionality:
- Represents information about a point of sale/dealer location
- Manages dealer contact and location details
- Tracks status of the point of sale

2. Data handling:
- Stores dealer identification (dealerId)
- Maintains contact information (email, phone)
- Includes physical address through StandardAddress object
- Status tracking with integer field

3. Business rules:
- Has a LOADING status constant
- Requires dealer identification and contact details
- Address information is structured through separate class

4. Dependencies:
- Java Serializable interface
- CommonUtils from at.a1ta.bite.core
- StandardAddress class dependency
- Integrated with dealer management system
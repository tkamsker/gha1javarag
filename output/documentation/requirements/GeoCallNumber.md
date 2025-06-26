# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/GeoCallNumber.java

GeoCallNumber.java
1. Purpose and functionality:
- Represents geographical telephone numbers
- Stores and manages phone number components
- Provides structured format for telecom data

2. User interactions:
- No direct user interactions; data container

3. Data handling:
- Stores three string components:
  - countryCode: international dialing code
  - onkz: area code
  - tnum: telephone number
- Implements Serializable

4. Business rules:
- Maintains phone number format separation
- Supports international number formatting

5. Dependencies:
- No external class dependencies
- Java Serializable interface
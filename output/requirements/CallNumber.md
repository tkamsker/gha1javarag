# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/CallNumber.java

CallNumber.java
1. Purpose: Represents a phone number with country code, area code (onkz) and local number components
2. User interactions: None directly - data structure only
3. Data handling:
   - Stores phone number components (countryCode, onkz, tnum)
   - Implements Serializable for data transfer
   - Provides getters/setters for all fields
4. Business rules:
   - Phone numbers must be structured in 3 parts
   - Supports GWT parsing through default constructor
5. Dependencies:
   - Java Serializable interface
   - Used by subscription/account management systems
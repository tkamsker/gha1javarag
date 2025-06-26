# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/Price.java

Price.java
1. Purpose: Represents a price entity with gross and net values
2. User interactions: None directly - used as a data structure
3. Data handling:
   - Stores float values for gross and net prices
   - Implements Serializable for data transfer
   - Provides getters/setters for both fields
4. Business rules:
   - Allows null values for both gross and net
   - No validation rules implemented
5. Dependencies:
   - Java Serializable interface
   - Likely used by tariff-related classes
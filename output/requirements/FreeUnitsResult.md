# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/freeunits/FreeUnitsResult.java

FreeUnitsResult.java
1. Purpose and functionality:
- Data transfer object for representing free units/minutes information
- Tracks usage and availability of communication units (likely phone minutes)
- Supports pulse unit tracking functionality

2. Data handling:
- Stores basic unit information (name, description)
- Tracks numerical values for minutes (maximum, used, unused)
- Implements Serializable for data transfer
- Uses BigInteger for precise numerical calculations

3. Business rules:
- Minutes tracking must maintain consistency (used + unused = maximum)
- Pulse unit flag indicates special unit type handling
- All numerical values must be non-negative

4. Dependencies:
- Java Serializable interface
- java.math.BigInteger for numerical precision
- Likely used by billing or usage monitoring systems
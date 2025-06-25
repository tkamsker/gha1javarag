# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/usagedata/VoiceUsage.java

VoiceUsage.java
1. Purpose: Represents voice call usage data with associated metadata
2. Data handling:
- Stores call details including date, duration, fees, zone info
- Implements Serializable for data transfer/persistence
- Standard getter/setter methods for all fields

3. Business rules:
- Must track call duration and connection fees
- Requires zone and time type classification
- Provider information must be maintained

4. Dependencies:
- Java Date utility
- Serializable interface
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Turnover.java

Turnover.java
1. Purpose: Represents financial turnover data with two types (TA and MK)
2. User interactions: None directly - data transfer object
3. Data handling:
   - Stores party ID, month, and financial metrics
   - Implements Serializable for data transfer
   - Tracks turnover and margin for both TA and MK types
4. Business rules:
   - Two distinct turnover types: TA and MK
   - Each type has associated turnover and margin values
   - Requires party ID and month tracking
5. Dependencies:
   - java.io.Serializable
   - java.util.Date
   - Used by financial reporting/tracking systems
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/BRKAccountInfo.java

BRKAccountInfo.java
1. Purpose: Data transfer object for BRK (likely Broker) account information
2. Data handling:
- Stores account details: number, status, name, handling fee
- Implements Serializable for data transfer
3. Business rules:
- All fields are accessible via getters/setters
- Account information must be maintainable
4. Dependencies:
- Standalone class implementing Serializable
- Part of product DTO package
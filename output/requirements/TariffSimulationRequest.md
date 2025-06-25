# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffSimulationRequest.java

TariffSimulationRequest.java
1. Purpose: Handles requests for tariff simulations, allowing users to evaluate different tariff options
2. User interactions:
- Accepts phone number and billing account information for tariff simulation
- Supports different simulation types via SimulationType enum

3. Data handling:
- Implements Serializable for data transfer
- Contains PhoneNumberStructure and BillingAccountNumber objects
- Manages tariff simulation parameters

4. Business rules:
- Must have valid phone number format
- Requires valid billing account information
- Simulation type must be specified

5. Dependencies:
- Depends on PhoneNumberStructure and BillingAccountNumber DTOs
- Uses SimulationType from mobilkom.bit.tariffguide
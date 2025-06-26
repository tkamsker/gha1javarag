# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/UsageDataService.java

UsageDataService.java
1. Purpose: Interface for managing usage data across different telecommunication services
2. User interactions: No direct user interactions - service layer interface
3. Data handling:
   - Retrieves fixed line numbers for a party ID
   - Handles different usage types (Internet, Mobile, Voice)
   - Works with NetworkProvider data
4. Business rules:
   - Organizes usage data by party ID
   - Separates usage by service type (inet, mobile, voice)
5. Dependencies:
   - Uses DTOs: InetUsage, MobileUsage, VoiceUsage
   - Relies on NetworkProvider entity
   - Part of cuco-core module
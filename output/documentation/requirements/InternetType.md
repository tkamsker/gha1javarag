# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/digitalselling/InternetType.java

InternetType.java
1. Purpose: Defines enumeration of available internet connection types
2. User interactions: Used for selection of internet connection type
3. Data handling: Simple enum with two values:
   - WIRE (Leitung/Line-based)
   - MOBILE (Mobil/Mobile-based)
4. Business rules:
   - Restricts internet type selection to only these two options
   - Used for categorizing internet service offerings
5. Dependencies:
   - Used by other digital selling components
   - Part of visit report system
   - Likely referenced in service configuration or order processing

Common Themes:
- All files are part of the digital selling visit report system
- Focus on data structure and transfer
- XML-centric architecture
- Clear separation of concerns between different service types
- Multilingual support (German/English comments)
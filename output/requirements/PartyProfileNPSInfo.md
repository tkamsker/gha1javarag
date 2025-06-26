# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartyProfileNPSInfo.java

PartyProfileNPSInfo.java
1. Purpose and functionality:
- Manages Net Promoter Score (NPS) information for party profiles
- Stores scoring data and related metrics
- Implements Serializable for data transfer

2. Data handling:
- Manages three main data elements:
  - scoringType: Type of NPS scoring
  - scoringValue: Actual NPS score
  - scoringDate: When the scoring was performed
- Includes GWT parsing support

3. Business rules:
- Must maintain scoring history with dates
- Supports different types of scoring methods
- Requires proper date formatting for scoring dates

4. Dependencies and relationships:
- Integrated with GWT framework
- Part of the customer feedback and satisfaction tracking system
- Related to party profile management
- Used in customer experience analytics
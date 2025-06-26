# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/PartySearch.java

PartySearch.java
1. Purpose and functionality:
- Data transfer object for searching party/customer information
- Encapsulates search criteria for party lookup operations
- Implements Serializable for data transfer across systems

2. User interactions:
- Used as search parameters input structure
- Supports searching by personal details and address information

3. Data handling:
- Contains basic personal identifiers (id, leadId)
- Personal information (firstName, lastName, birthDate)
- Address details (postcode, city, village, street, country)
- All fields appear to be String except birthDate (Date)

4. Business rules:
- Flexible search structure allowing partial or complete search criteria
- Supports both personal and address-based searches

5. Dependencies:
- Java Date utility
- Serializable interface implementation
- Core component of party/customer search functionality
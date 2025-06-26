# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyCustomersService.java

MyCustomersService.java

1. Purpose and functionality:
- Interface for customer management services
- Handles customer metrics and information
- Focuses on support user operations

2. User interactions:
- Support user access to customer information
- Customer metrics retrieval

3. Data handling:
- Returns customer counts
- Processes CustomerFilter for searches
- Manages Party information
- Returns SearchResult data structure

4. Business rules:
- Support user specific access
- Churn tracking functionality
- Customer filtering capabilities

5. Dependencies:
- SearchResult from bite.core framework
- CustomerFilter DTO
- Party DTO
- Map and List collections for data handling

Each service component appears to be part of a larger customer relationship management system, with clear separation of concerns between flash notifications, quote management, and customer service functionalities.
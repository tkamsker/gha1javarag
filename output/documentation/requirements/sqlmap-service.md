# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-service.xml

sqlmap-service.xml
1. Purpose and functionality:
- iBatis SQL mapping configuration for Service-related database operations
- Defines data mapping between database and Service DTOs
- Implements caching using ehcache for service data

2. User interactions:
- No direct user interactions - backend configuration file

3. Data handling:
- Maps Service database tables to Service DTOs
- Implements read-only caching for service data
- Likely handles CRUD operations for service entities

4. Business rules:
- Uses read-only cache indicating service data is relatively static
- Cache flush interval suggests periodic data refresh requirements

5. Dependencies:
- Depends on iBatis framework
- Uses ehcache provider for caching
- References Service DTO classes from core.shared.dto package
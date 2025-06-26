# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-contactPerson.xml

sqlmap-contactPerson.xml
1. Purpose and functionality:
- Defines SQL mapping for contact person management
- Implements caching strategy for contact person data
- Handles CRUD operations for contact person records

2. Data handling:
- Uses iBatis SQL mapping framework
- Implements ehcache caching with 3-hour flush interval
- Cache size limited to 1000 entries
- Read-only cache configuration
- Non-serialized cache storage

3. Business rules:
- Contact information must be cached for performance
- Cache invalidation occurs every 3 hours
- Read-only access to cached data

4. Dependencies and relationships:
- Relies on iBatis framework
- Depends on ehcache provider
- Integrated with contact person domain model
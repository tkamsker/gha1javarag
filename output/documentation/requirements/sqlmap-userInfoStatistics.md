# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-userInfoStatistics.xml

sqlmap-userInfoStatistics.xml
1. Purpose: Manages SQL mappings for user information statistics tracking and caching
2. Data handling:
- Uses iBatis SQL mapping framework
- Implements caching via ehcache with 1-minute flush interval
- Maps to UserInfoStatistics DTO class
3. Business rules:
- Read-only cache implementation
- Short cache lifetime (1 min) suggests frequently updated statistics
4. Dependencies:
- Relies on ehcacheProvider
- Depends on UserInfoStatistics DTO class
- Part of the core DAO layer
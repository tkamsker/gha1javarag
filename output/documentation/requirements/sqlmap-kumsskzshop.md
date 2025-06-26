# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-kumsskzshop.xml

sqlmap-kumsskzshop.xml
1. Purpose: Manages KUMS SKZ shop data mapping and caching configuration
2. Data Handling:
- Uses ehcache provider for caching
- 1-hour cache flush interval
- Read-only cache implementation
- Maps to KumsSkzShop DTO class
3. Business Rules:
- Shop data requires more frequent updates (1hr cache)
- Optimized for read operations
4. Dependencies:
- iBatis framework dependency
- ehcache system
- References at.a1ta.bite.core.shared.dto.KumsSkzShop class
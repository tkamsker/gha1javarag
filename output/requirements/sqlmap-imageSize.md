# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-imageSize.xml

sqlmap-imageSize.xml
1. Purpose: Manages image size configurations and caching
2. Data handling:
- Implements caching for image size data using ehcache
- Cache configured for 3-hour refresh interval
- Supports up to 1000 cached entries
3. Business rules:
- Read-only cache implementation
- No serialization of cached objects
- Cache refreshes every 3 hours automatically
4. Dependencies:
- Requires ehcacheProvider
- Part of image processing subsystem
- Integrated with iBatis framework
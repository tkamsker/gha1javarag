# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-usageData.xml

sqlmap-usageData.xml
1. Purpose: Manages database operations for usage data tracking, likely for voice/telecom services
2. Data Handling:
- Implements caching using ehcache provider
- 3-hour cache flush interval
- Cache size limit of 1000 entries
- Read-only cache configuration
- Non-serialized cache storage

3. Business Rules:
- Cache invalidation every 3 hours ensures relatively fresh data
- Read-only nature suggests data is primarily for reporting/analysis

4. Dependencies:
- Requires iBatis SQL mapping framework
- Depends on ehcache provider
- Likely interfaces with voice usage tracking systems
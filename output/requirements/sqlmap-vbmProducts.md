# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-vbmProducts.xml

sqlmap-vbmProducts.xml
1. Purpose: Manages SQL mappings for VBM (Virtual Business Manager) products
2. Data handling:
   - Uses iBatis SQL mapping framework
   - Implements caching via ehcache
   - Cache configuration: 1000 entries, 1-minute flush interval
   - Read-only cache with no serialization
3. Business rules:
   - Product data is cached for performance
   - Cache invalidation occurs every minute
4. Dependencies:
   - Requires iBatis framework
   - Uses ehcacheProvider
   - Integrates with VBM product database tables
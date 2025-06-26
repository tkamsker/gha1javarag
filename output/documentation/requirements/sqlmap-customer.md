# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-customer.xml

sqlmap-customer.xml
1. Purpose: Manages customer-related database operations and opportunity tracking
2. Data handling:
   - Uses iBatis SQL mapping framework
   - Implements type aliases for Opportunity class
   - Includes caching mechanism via ehcache
3. Business rules:
   - Handles customer opportunity data
   - Maintains relationship between customers and opportunities
4. Dependencies:
   - Requires iBatis framework
   - Depends on at.a1ta.cuco.cct.shared.dto.Opportunity class
   - Uses EhCacheController for caching
   - Integrates with customer database tables
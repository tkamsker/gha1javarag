# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/AggregatedInventoryProductGroupUsage.java

AggregatedInventoryProductGroupUsage.java
1. Purpose: Represents aggregated usage data for inventory product groups with associated parties
2. Data handling:
   - Extends InventoryProductGroupUsage
   - Manages a list of Party objects
   - Provides methods to get/set and add parties
3. Business rules:
   - Lazy initialization of parties list when adding first party
   - Null check before adding new parties
4. Dependencies:
   - Extends InventoryProductGroupUsage class
   - Uses Party class
   - Java ArrayList implementation
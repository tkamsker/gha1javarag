# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/tariff/TariffLists.java

TariffLists.java
1. Purpose: Manages collections of tariffs, separating all tariffs from recommended ones
2. User interactions: None directly - used as a data container
3. Data handling:
   - Maintains two List<Tariff> collections
   - Implements Serializable
   - Provides getters/setters with null safety (returns empty lists)
4. Business rules:
   - Returns empty lists instead of null for safety
   - Allows separate management of recommended vs all tariffs
5. Dependencies:
   - Tariff class
   - Java Collections
   - Java Serializable interface
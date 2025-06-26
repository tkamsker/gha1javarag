# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InventoryProductGroup.java

InventoryProductGroup.java
1. Purpose: Represents a grouping of inventory products with visibility and ordering controls
2. User Interactions: None directly - serves as a data transfer object
3. Data Handling:
   - Stores: id (Long), name (String), order (int), visible (boolean), anb (boolean)
   - Implements Serializable for data transfer/persistence
   - Provides getter/setter methods for all fields
4. Business Rules:
   - Groups must have unique IDs
   - Groups can be made visible/invisible
   - Groups have a specific display order
   - Special handling for "anb" flag (purpose needs clarification)
5. Dependencies:
   - Java Serializable interface
   - Likely used in inventory management system
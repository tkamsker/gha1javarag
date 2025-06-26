# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/customerequipment/EquipmentConsignee.java

EquipmentConsignee.java
1. Purpose: Represents a consignee (recipient) for equipment delivery/management
2. User interactions: Used as a data transfer object for displaying and managing equipment consignee information
3. Data handling:
   - Stores personal/business contact information (name, address, etc.)
   - Implements Serializable for data transfer
   - Contains basic identifier and summary fields
4. Business rules:
   - Requires unique ID and partyId for identification
   - Supports structured address format (title, name1, name2, plz, city, street)
5. Dependencies:
   - Core Java Serializable interface
   - Used by other equipment management components
   - Parent class for DummyEquipmentConsignee
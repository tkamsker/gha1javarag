# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/NodeHelper.java

NodeHelper.java
1. Purpose and functionality:
- Utility class providing helper methods for node operations
- Specifically handles party node relationships and navigation
- Facilitates node type checking and casting

2. Data handling:
- No direct data storage
- Handles node type conversions
- Manages node relationship traversal

3. Business rules:
- Implements logic for identifying and retrieving PartyNodes
- Enforces node hierarchy navigation rules
- Validates parent-child relationships

4. Dependencies:
- Depends on Node interface/class
- Uses PartyNode class
- References ProductType enum from DefaultProductNode
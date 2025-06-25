# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/product/SAPPhysicalResourceNode.java

SAPPhysicalResourceNode.java
1. Purpose: Represents a node in a physical resource hierarchy from SAP systems, extending BaseNode class
2. Data handling:
- Stores text description of the resource node
- Contains equipment attributes via MetaData object
- Implements Serializable for object persistence/transfer
3. Business rules:
- Must extend BaseNode functionality
- Text and equipment attributes can be retrieved/set
4. Dependencies:
- Extends BaseNode
- Uses MetaData class for equipment attributes
- Part of product DTO package
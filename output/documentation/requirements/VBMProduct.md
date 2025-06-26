# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/nbo/VBMProduct.java

VBMProduct.java
1. Purpose and functionality:
- Represents a product in the VBM (likely Value-Based Management) system
- Serves as a data transfer object (DTO) for product information
- Implements Serializable for data transmission

2. Data handling:
- Stores core product attributes: customerId, productId, monthYearPeriod
- Contains party information through Party object
- Manages scoring total and product details
- Implements standard Java serialization

3. Business rules:
- Must maintain association with a customer (customerId)
- Requires unique product identification (productId)
- Includes temporal tracking (monthYearPeriod)
- Incorporates scoring mechanism

4. Dependencies and relationships:
- Depends on Party class
- Contains VBMProductDetails
- Part of the NBO (Next Best Offer) subsystem
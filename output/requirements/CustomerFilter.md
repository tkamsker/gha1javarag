# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CustomerFilter.java

CustomerFilter.java
1. Purpose and functionality:
- Provides filtering capabilities for customer data
- Handles VIP and turnover region filtering
- Supports customer segmentation

2. User interactions:
- Likely used in search/filter interfaces for customer management
- Supports VIP customer identification

3. Data handling:
- Uses KeyValuePair for filter criteria
- Integrates with VBMProductDetails
- Handles DualSegment data

4. Business rules:
- Special handling for VIP customers
- Turnover region-based filtering
- Customer segmentation logic

5. Dependencies:
- bite.core.shared.dto.KeyValuePair
- cuco.core.shared.dto.nbo.VBMProductDetails
- cuco.core.shared.model.DualSegment
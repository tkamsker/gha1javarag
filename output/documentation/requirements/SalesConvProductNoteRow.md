# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesConvProductNoteRow.java

SalesConvProductNoteRow.java
1. Purpose and functionality:
- Represents a product-specific row in sales conversations
- Tracks product details and sales status
- Manages product-related metrics

2. Data handling:
- Stores product identifiers and categories
- Tracks quote status and turnover quantities
- Manages contact counts and assignments

3. Business rules:
- Must link to predecessor notes (if applicable)
- Requires product categorization
- Tracks quote status and assignment types
- Maintains contact count metrics

4. Dependencies:
- Product management system
- Quote management system
- Sales assignment system

Common themes across files:
- Part of a larger sales management system
- Hierarchical structure for different types of sales information
- Strong focus on tracking and categorization
- Integration with multiple business processes (sales, communication, product management)
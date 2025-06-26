# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/Customer.java

Customer.java
1. Purpose: Core customer entity representation extending Person class
2. Data handling:
- Manages business-related customer attributes
- Integrates with Solr search through @Field annotations
3. Business rules:
- Tracks business rules and segments
- Handles business volume metrics
- Maintains customer-specific data
4. Dependencies:
- Extends Person class
- Apache Solr client
- VBMProduct class for product relationships
- Date and List utilities
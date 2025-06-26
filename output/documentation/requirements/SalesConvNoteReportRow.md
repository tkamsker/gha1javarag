# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/SalesConvNoteReportRow.java

SalesConvNoteReportRow.java
1. Purpose and functionality:
- Represents a row in a sales conversation note report
- Stores sales conversation tracking and reporting data
- Manages campaign and customer relationship information

2. User interactions:
- Used in reporting interfaces
- Tracks user modifications through lastModUser

3. Data handling:
- Contains identifiers (siNoteId, campaignId, customerId)
- Manages temporal data using Date objects
- Maintains relationship with BiteUser for modification tracking

4. Business rules:
- Links sales notes with campaigns
- Tracks conversation history through predecessorSiNoteId
- Maintains modification audit trail

5. Dependencies:
- BiteUser from bite.core package
- Java Date utility
- List interface for collections
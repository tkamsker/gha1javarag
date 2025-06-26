# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/salesinfo/visitreport/sbs/SBSNote.java

SBSNote.java
1. Purpose: Represents a structured note entity for Small Business Solutions visit reports
2. User interactions: Captures and manages visit report data
3. Data handling:
   - Extends core note functionality
   - Manages lists of attributes, contact persons
   - Handles appointment and sales information
4. Business rules:
   - Inherits from base note classes (AppointmentNote, SalesInfoNote)
   - Organizes todo groups and contact information
   - Maintains business-specific attributes
5. Dependencies:
   - Depends on core DTO classes (Attribute, ContactPerson)
   - Part of sales information system
   - Related to appointment and todo management
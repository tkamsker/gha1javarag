# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/SalesConvEmailData.java

SalesConvEmailData.java
1. Purpose and functionality:
- Data transfer object for email communication in sales conversations
- Encapsulates email message details and attachments
- Implements Serializable for data transfer

2. Data handling:
- Stores basic email components: sender, recipient, subject, message
- Manages attachment URLs through a Map structure
- Includes partyId for customer/conversation identification

3. Business rules:
- All fields appear to be required for a complete email
- Attachments are optional (Map can be empty)
- Uses String format for all basic fields

4. Dependencies:
- Java Serializable interface
- Java Map interface for attachments
- No complex external dependencies
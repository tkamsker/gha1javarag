# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/FlashInfoBase.java

FlashInfoBase.java
1. Purpose and functionality:
- Represents a flash message/notification system base class
- Manages displayable notifications or alerts in the system
- Supports both regular notifications and popup messages

2. Data handling:
- Stores notification metadata including ID, title, text
- Tracks active status and popup display mode
- Maintains list of roles for access control
- Records whether notification has been viewed

3. Business rules:
- Each flash message must have unique ID
- Can be configured as active/inactive
- Can be set as popup or regular notification
- Access can be restricted by roles
- Viewing status is trackable

4. Dependencies:
- Depends on Role class from bite.core security package
- Implements Serializable for data transfer
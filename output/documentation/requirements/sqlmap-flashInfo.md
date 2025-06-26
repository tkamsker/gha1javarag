# Requirements Analysis: cuco-core/src/main/resources/at/a1ta/cuco/core/dao/db/sqlmap-flashInfo.xml

sqlmap-flashInfo.xml
1. Purpose: Manages flash information/notifications system

2. User Interactions:
- Displays flash messages/notifications
- Manages user-specific notifications
- Role-based notification handling

3. Data Handling:
- Maps FlashInfo and MyFlashInfo DTOs
- Role-based data filtering
- Notification state management

4. Business Rules:
- Role-based access control
- Notification lifecycle management
- User-specific notification rules

5. Dependencies:
- iBatis framework
- FlashInfo and MyFlashInfo DTOs
- Role management system
- Core notification system integration

All three files are iBatis SQL mapping configurations, forming part of the data access layer for different functional areas of the application. They follow similar structural patterns but serve distinct business purposes within the system.
# Requirements Analysis: administration.ui/src/main/java/at/a1ta/cuco/admin/ui/common/client/event/SelectRolesEvent.java

SelectRolesEvent.java
1. Purpose: Handles role selection events in the administration interface
2. User Interactions: Triggered when users/administrators select roles
3. Data Handling:
   - Manages List<Role> collection
   - Initializes with CuCoEventType.SELECT_ROLES event type
4. Business Rules:
   - Must handle multiple role selections
   - Implements event type specification for role selection
5. Dependencies:
   - Depends on bite.core.shared.dto.security.Role
   - Extends framework.ui.client.event.PortletEvent
   - Uses CuCoEventType enumeration
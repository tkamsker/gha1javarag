# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/CrmAuthenticationInfo.java

CrmAuthenticationInfo.java
1. Purpose and functionality:
- Manages authentication status and credentials for CRM system access
- Tracks different states of authentication (LOADING, ERROR, NOT_RECEIVED, LOADED)
- Stores password information

2. User interactions:
- No direct user interactions, serves as a data transport object

3. Data handling:
- Implements Serializable for data transfer
- Maintains authentication status and password information
- Uses status constants for state management

4. Business rules:
- Status codes defined for different states:
  * LOADING (-1): Authentication in progress
  * ERROR (99): Authentication failed
  * NOT_RECEIVED (98): No authentication attempt made
  * LOADED (0): Successfully authenticated
- Default status is LOADING

5. Dependencies:
- Java Serializable interface
- Used by authentication-related services
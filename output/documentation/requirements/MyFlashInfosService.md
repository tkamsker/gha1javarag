# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/mycuco/MyFlashInfosService.java

MyFlashInfosService.java

1. Purpose and functionality:
- Interface defining services for handling flash information alerts
- Manages flash info retrieval for agents
- Handles party/participant information related to flash infos

2. User interactions:
- Allows agents to retrieve their flash info notifications
- Enables access to party information associated with flash infos

3. Data handling:
- Returns List<FlashInfo> for agent-specific flash information
- Returns List<Party> for party information
- Uses FilterCollection for query filtering
- Processes agent identification via uuser string

4. Business rules:
- Access restricted to specific agents
- Filtering capabilities for flash info retrieval
- Association between flash infos and parties

5. Dependencies:
- Depends on FlashInfo DTO
- Depends on Party DTO
- Uses FilterCollection from bite.core framework
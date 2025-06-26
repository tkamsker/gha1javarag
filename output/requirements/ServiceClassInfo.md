# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ServiceClassInfo.java

ServiceClassInfo.java
1. Purpose and functionality:
- Represents service class information in the system
- Manages service class status and descriptive text
- Defines constants for different service states (ERROR, LOADING)

2. User interactions:
- No direct user interactions, serves as a data transfer object

3. Data handling:
- Implements Serializable for data transfer
- Stores service class as integer value
- Maintains service class description as text

4. Business rules:
- Predefined service class states:
  - SERVICE_CLASS_ERROR = 99
  - SERVICE_CLASS_LOADING = -1
- Default state is SERVICE_CLASS_LOADING

5. Dependencies:
- Java Serializable interface
- Used by other components requiring service class information
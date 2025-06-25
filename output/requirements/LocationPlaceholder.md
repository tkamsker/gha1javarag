# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/LocationPlaceholder.java

LocationPlaceholder.java
1. Purpose: A placeholder class for Location objects, providing default/empty location values
2. User interactions: None directly - used internally
3. Data handling:
   - Extends Location class
   - Implements Serializable
   - Sets default values (id=-1, locationId="-1")
4. Business rules:
   - Used when a null/empty location needs to be represented
5. Dependencies:
   - Extends at.a1ta.bite.data.clarify.shared.dto.Location
   - Implements Serializable
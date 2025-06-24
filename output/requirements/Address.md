# Requirements Analysis: src/main/java/com/bittercode/model/Address.java

src/main/java/com/bittercode/model/Address.java
### 1. Purpose and Functionality
- Represents a user's address in the application.
- Contains fields for street, city, state, country, pin code, and phone number.

### 2. User Interactions (if applicable)
- Users interact with this class indirectly when providing or updating their address during registration or profile management.
- Developers use this class to handle address data across different layers of the application.

### 3. Data Handling
- Fields:
  - `addressLine1`, `addressLine2`: Strings for street details.
  - `city`, `state`, `country`: Strings representing geographical locations.
  - `pinCode`: Long representing the postal code.
  - `phone`: String representing the phone number associated with the address.
- Methods:
  - Getters and setters for all fields.

### 4. Business Rules
- Address validation may be required based on country-specific formats.
- Pin codes must be valid for the given country.
- Phone numbers may need to follow specific formatting rules.

### 5. Dependencies and Relationships
- Implements `Serializable` for object persistence or network transmission.
- May be used in conjunction with `User` class to store user addresses.
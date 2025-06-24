# Requirements Analysis: src/main/java/com/bittercode/model/UserRole.java

UserRole.java
### Purpose and Functionality:
An enum defining roles (`CUSTOMER`, `SELLER`) to control user access levels within the application.

### User Interactions:
Directly influences user permissions, affecting what actions users can perform post-login. Users interact based on their assigned role.

### Data Handling:
Roles are stored in the database (likely linked to user records) and retrieved during authentication to determine access rights.

### Business Rules:
- `CUSTOMER` can view products and checkout.
- `SELLER` can manage inventory and orders.

### Dependencies and Relationships:
Depends on authentication modules for role assignment. Related to UsersDBConstants if roles are stored as a column in the users table, affecting user interactions across features like product management or order processing.
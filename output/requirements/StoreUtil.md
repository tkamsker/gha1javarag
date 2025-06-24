# Requirements Analysis: src/main/java/com/bittercode/util/StoreUtil.java

src/main/java/com/bittercode/util/StoreUtil.java
### 1. Purpose and Functionality
- The `StoreUtil` class serves as a utility file containing commonly used methods for user authentication and session management in a web application.
- It provides functionality to check if a user is logged in with a specific role, which is essential for access control.

### 2. User Interactions (if applicable)
- Users interact indirectly through the application's login mechanism and subsequent access checks.
- The `isLoggedIn` method ensures that users can only access features or pages for which they have the required permissions.

### 3. Data Handling
- Handles session data stored in `HttpSession`.
- Manages user roles to determine if a user has the necessary permissions for specific actions.

### 4. Business Rules
- Users must be authenticated and have the correct role to access certain features or pages.
- The application enforces security policies by checking user roles before allowing access.

### 5. Dependencies and Relationships
- Depends on `HttpServletRequest` and `HttpSession` from the Servlet API for session management.
- References `UserRole` from the model package, indicating a dependency on the application's user role enumeration.

---
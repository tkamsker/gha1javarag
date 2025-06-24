# Requirements Analysis: src/main/java/com/bittercode/util/DBUtil.java

src/main/java/com/bittercode/util/DBUtil.java
### 1. Purpose and Functionality  
This utility class manages database connections. It initializes a connection using configurations from `DatabaseConfig` and provides methods for interacting with the database.

### 2. User Interactions  
- No direct user interaction; it is used internally by other components like `CustomerRegisterServlet`.

### 3. Data Handling  
- Establishes a database connection during class initialization.
- Provides static methods to retrieve or close connections.
- Handles exceptions related to database operations and throws custom `StoreException` for error handling.

### 4. Business Rules  
- Ensure that the database connection is properly initialized and maintained.
- Handle database exceptions gracefully and propagate them as custom exceptions.

### 5. Dependencies and Relationships  
- Depends on `DatabaseConfig` for database configuration settings.
- Uses JDBC classes (`Connection`, `DriverManager`) for database operations.
- Thrown exceptions are caught and handled by other components like `CustomerRegisterServlet`.
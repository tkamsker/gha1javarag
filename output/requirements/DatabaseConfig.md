# Requirements Analysis: src/main/java/com/bittercode/util/DatabaseConfig.java

src/main/java/com/bittercode/util/DatabaseConfig.java
### 1. Purpose and Functionality  
This utility class reads and stores database configuration settings from the `application.properties` file. It provides static access to these configurations throughout the application.

### 2. User Interactions  
- No direct user interaction; it operates behind the scenes to provide database connection details.

### 3. Data Handling  
- Loads properties from `application.properties` during class initialization.
- Stores configuration values (e.g., driver name, URL, username, password) in a static `Properties` object.

### 4. Business Rules  
- Ensure that all required database configuration properties are present and valid.
- Throw exceptions if the configuration file is missing or corrupted.

### 5. Dependencies and Relationships  
- Uses Java IO classes for reading files.
- Provides configuration data to other components like `DBUtil`.

---
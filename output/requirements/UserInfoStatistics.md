# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/UserInfoStatistics.java

UserInfoStatistics.java
1. Purpose: Data transfer object for aggregating user-related statistics and metrics
2. User Interactions: Read-only consumption of statistics through getter methods
3. Data Handling:
   - Stores integer counts for various metrics
   - Implements Serializable for data transfer
4. Business Rules:
   - Tracks 5 key metrics:
     - Number of customers
     - Number of expiring bindings
     - Number of quotes
     - Number of tasks
     - Number of open todos
5. Dependencies:
   - Java Serializable interface
   - Likely used by dashboard or reporting components
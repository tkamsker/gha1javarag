# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/KumsCustomerInfo.java

KumsCustomerInfo.java
1. Purpose and functionality:
- Represents customer VIP status information
- Tracks customer status changes

2. Data handling:
- Stores VIP status as Integer
- Maintains last change date as String
- Implements basic getter/setter pattern

3. Business rules:
- VIP status is represented as numeric levels
- Change dates must be tracked
- Status changes are auditable through date tracking

4. Dependencies:
- Implements Serializable for data transfer
- Standalone class with no external dependencies
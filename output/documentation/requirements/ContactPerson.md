# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/ContactPerson.java

ContactPerson.java
1. Purpose: Represents a contact person associated with a customer in the system
2. Data handling:
- Extends Person class
- Stores contact information including:
  - Customer ID and role
  - Phone numbers (day, fax, mobile)
  - Email address
  - Contact status (main contact flag)
  - Personal ID
3. Business rules:
- Can be designated as main contact (boolean flag)
- Must be associated with a customer (customerId)
4. Dependencies:
- Extends Person class
- Depends on BiteUser from bite.core package
- Implements serializable for data transfer
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/InvoiceService.java

InvoiceService.java
1. Purpose and functionality:
- Interface for invoice management operations
- Handles invoice data retrieval and mobile invoice download functionality
- Manages clearing accounts and invoice relationships

2. User interactions:
- Provides functionality for invoice download
- Likely integrated with user-facing invoice management features

3. Data handling:
- Manages ClearingAccount and Invoice data structures
- Returns LinkedHashMap of ClearingAccounts grouped by party IDs
- Handles invoice download link generation

4. Business rules:
- Supports multiple party IDs for invoice data retrieval
- Maintains relationship between invoices and clearing accounts
- Specific business logic for mobile invoice handling

5. Dependencies:
- Uses ClearingAccount and Invoice DTOs
- Part of core service layer
- Likely integrates with financial/billing systems
- ArrayList and LinkedHashMap from Java Collections Framework
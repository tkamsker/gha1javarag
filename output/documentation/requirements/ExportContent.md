# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/export/ExportContent.java

ExportContent.java
1. Purpose and functionality:
- Defines an interface for handling content export formatting
- Provides methods to set formatters at different levels (type, column, row, content)
- Manages data organization and formatting for export operations

2. User interactions:
- No direct user interactions; used programmatically

3. Data handling:
- Allows adding rows of data
- Supports clearing content
- Manages formatting rules for different data types and structures

4. Business rules:
- Hierarchical formatting system (type, column, row, content levels)
- Flexible formatter assignment
- Data organization must follow row-based structure

5. Dependencies and relationships:
- Depends on Formater interface
- Used by export implementations
- Core interface for export functionality
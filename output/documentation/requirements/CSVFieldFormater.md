# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/export/CSVFieldFormater.java

CSVFieldFormater.java
1. Purpose: Formats individual fields for CSV export according to RFC4180 standards
2. User Interactions: None - utility class
3. Data Handling:
- Handles field-level CSV formatting
- Manages field separators and escaping
4. Business Rules:
- Default separator is semicolon (;)
- Alternative RFC4180 separator is comma (,)
- Must properly escape special characters
5. Dependencies:
- Part of export package
- Implements Formater interface
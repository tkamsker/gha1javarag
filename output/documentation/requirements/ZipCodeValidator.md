# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/ZipCodeValidator.java

ZipCodeValidator.java
1. Purpose and functionality:
- Validates postal/zip code format
- Ensures zip codes meet length and character requirements
- Provides flexible validation that accepts blank values

2. User interactions:
- No direct user interface
- Used as a validation component in form processing

3. Data handling:
- Accepts string input for zip code validation
- Returns boolean validation result
- Handles null/blank input gracefully

4. Business rules:
- Valid zip codes must be 4-5 digits long
- Must contain only numeric characters
- Blank/null values are considered valid
- No country-specific validation rules implemented

5. Dependencies:
- Depends on CommonValidator utility class
- Used by higher-level validation processes
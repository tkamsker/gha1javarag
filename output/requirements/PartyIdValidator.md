# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/validator/PartyIdValidator.java

PartyIdValidator.java
1. Purpose: Validates party identification numbers
2. User Interactions: Used during party ID input validation
3. Data Handling:
   - Validates string input
   - Handles blank values
   - Checks for specific format requirements
4. Business Rules:
   - Accepts blank values as valid
   - Valid party IDs must be either:
     - A valid lead search format
     - Exactly 9 digits long
   - Uses CommonValidator for digit checking
5. Dependencies:
   - Relies on CommonValidator class
   - Used in party/customer identification workflows

Note: The PartyIdValidator implementation appears to be truncated in the provided code, so there may be additional validation rules not visible in the preview.
# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/NotesFilter.java

NotesFilter.java
1. Purpose: Filter criteria definition for querying/filtering notes in the system
2. User Interactions:
   - Used to filter notes based on user preferences
   - Supports search/filtering functionality
3. Data Handling:
   - Manages filter criteria for notes including:
     - User ID
     - Last modification date
     - Note type
4. Business Rules:
   - Supports filtering by specific criteria constants
   - Integrates with sales info notes and todo status
5. Dependencies:
   - SalesInfoNoteType enum
   - ToDoStatus enum
   - Requires Date handling
   - Used in note management functionality
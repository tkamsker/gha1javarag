package at.a1ta.cuco.core.service.mycuco;

import java.util.List;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.shared.dto.ToDoNotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

public interface MyToDoNotesService {

  SearchResult<SalesInfoNote> loadMyToDoNotes(ToDoNotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad);

}

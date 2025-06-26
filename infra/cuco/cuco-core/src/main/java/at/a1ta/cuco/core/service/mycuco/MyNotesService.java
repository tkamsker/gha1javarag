package at.a1ta.cuco.core.service.mycuco;

import java.util.List;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.shared.dto.NotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

public interface MyNotesService {

  SearchResult<SalesInfoNote> loadMyNotes(NotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad);
}

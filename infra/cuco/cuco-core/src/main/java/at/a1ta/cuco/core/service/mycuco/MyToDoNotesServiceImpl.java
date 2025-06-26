package at.a1ta.cuco.core.service.mycuco;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyToDoNotesDao;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.shared.dto.ToDoNotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

@Service
public class MyToDoNotesServiceImpl implements MyToDoNotesService {

  private MyToDoNotesDao myToDoNotesDao;
  @Autowired
  @Qualifier("cucoCustomerDao")
  PartyDao partyDao;

  @Override
  public SearchResult<SalesInfoNote> loadMyToDoNotes(ToDoNotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    SearchResult<SalesInfoNote> notes = myToDoNotesDao.loadMyToDoNotes(filter, salesInfoNoteTypesToLoad);
    for (SalesInfoNote note : notes) {
      note.setParty(partyDao.loadParty(note.getPartyId()));
    }
    return notes;
  }

  @Autowired
  public void setMyToDoNotesDao(MyToDoNotesDao myToDoNotesDao) {
    this.myToDoNotesDao = myToDoNotesDao;
  }
}

package at.a1ta.cuco.core.service.mycuco;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyNotesDao;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.shared.dto.NotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

@Service
public class MyNotesServiceImpl implements MyNotesService {

  MyNotesDao myNotesDao;

  @Autowired
  @Qualifier("cucoCustomerDao")
  PartyDao partyDao;

  @Override
  public SearchResult<SalesInfoNote> loadMyNotes(NotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    SearchResult<SalesInfoNote> notes = myNotesDao.loadMyNotes(filter, salesInfoNoteTypesToLoad);
    for (SalesInfoNote note : notes) {
      note.setParty(partyDao.loadParty(note.getPartyId()));
    }
    return notes;
  }

  @Autowired
  public void setNotesDao(MyNotesDao myNotesDao) {
    this.myNotesDao = myNotesDao;
  }

}

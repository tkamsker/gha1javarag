package at.a1ta.cuco.core.dao.db.impl;

import java.util.ArrayList;
import java.util.List;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyNotesDao;
import at.a1ta.cuco.core.shared.dto.NotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class MyNotesDaoImplTest {

  @Autowired
  MyNotesDao myNotesDao;

  @Test
  public void testAll() {
    List<SalesInfoNoteType> salesInfoNoteTypesToLoad = new ArrayList<SalesInfoNoteType>();
    salesInfoNoteTypesToLoad.add(SalesInfoNoteType.SI_SIMPLE_NOTE);
    salesInfoNoteTypesToLoad.add(SalesInfoNoteType.SI_COMPETITOR_NOTE);

    NotesFilter filter = new NotesFilter();
    filter.setReminderOperator(null);
    filter.setUserId(36668);
    SearchResult<SalesInfoNote> searchResult = myNotesDao.loadMyNotes(filter, salesInfoNoteTypesToLoad);

    ArrayList<SalesInfoNote> results = searchResult.getResults();
    Assert.assertTrue(results.size() > 0);
  }

  @Test
  public void testEqual() {

    List<SalesInfoNoteType> salesInfoNoteTypesToLoad = new ArrayList<SalesInfoNoteType>();
    salesInfoNoteTypesToLoad.add(SalesInfoNoteType.SI_SIMPLE_NOTE);
    salesInfoNoteTypesToLoad.add(SalesInfoNoteType.SI_COMPETITOR_NOTE);

    NotesFilter filter = new NotesFilter();
    filter.setReminderOperator("=");
    filter.setUserId(36668);
    SearchResult<SalesInfoNote> searchResult = myNotesDao.loadMyNotes(filter, salesInfoNoteTypesToLoad);

    ArrayList<SalesInfoNote> results = searchResult.getResults();
    Assert.assertTrue(results.size() > 0);
  }
}

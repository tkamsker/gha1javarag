package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyNotesDao;
import at.a1ta.cuco.core.shared.dto.NotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

public class MyNotesDaoImpl extends AbstractDao implements MyNotesDao {

  @Autowired
  private SettingService settingService;

  private static final String SEARCH_RESULT_LIMIT_SETTING_KEY = "mycuco.table.searchresult.limit";

  @SuppressWarnings("unchecked")
  @Override
  public SearchResult<SalesInfoNote> loadMyNotes(NotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    Map<String, Object> params = createParams(filter, salesInfoNoteTypesToLoad);
    SearchResult<SalesInfoNote> result = (SearchResult<SalesInfoNote>) performLimitedListQuery("MyNotes.LoadMyNotes", params, settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
    return result;
  }

  private Map<String, Object> createParams(NotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("modDate", filter.getLastModDate());
    params.put("creator", filter.getCreator() != null ? filter.getCreator().toLowerCase() : null);
    params.put("lastModifier", filter.getLastModifier() != null ? filter.getLastModifier().toLowerCase() : null);
    params.put("assignee", filter.getAssignee() != null ? filter.getAssignee().toLowerCase() : null);
    params.put("noteText", filter.getNoteText() != null ? filter.getNoteText().toLowerCase() : null);
    params.put("noteType", filter.getNoteType());
    params.put("reminderOperator", filter.getReminderOperator().isEmpty() ? null : filter.getReminderOperator());
    params.put("userId", filter.getUserId());
    params.put("partyId", filter.getPartyId());
    params.put("firstname", filter.getFirstname());
    params.put("lastname", filter.getLastname());
    params.put("salesInfoNoteTypesToLoad", salesInfoNoteTypesToLoad);
    return params;
  }
}

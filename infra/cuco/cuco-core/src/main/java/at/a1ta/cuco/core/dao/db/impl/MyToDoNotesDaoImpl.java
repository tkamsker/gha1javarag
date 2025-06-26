package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyToDoNotesDao;
import at.a1ta.cuco.core.shared.dto.ToDoNotesFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;

public class MyToDoNotesDaoImpl extends AbstractDao implements MyToDoNotesDao {
  @Autowired
  private SettingService settingService;

  private static final String SEARCH_RESULT_LIMIT_SETTING_KEY = "mycuco.table.searchresult.limit";

  @SuppressWarnings("unchecked")
  @Override
  public SearchResult<SalesInfoNote> loadMyToDoNotes(ToDoNotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    Map<String, Object> params = createParams(filter, salesInfoNoteTypesToLoad);
    SearchResult<SalesInfoNote> result = (SearchResult<SalesInfoNote>) performLimitedListQuery("VisitReport.getOpenToDoGroupNotesForUser", params,
        settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
    return result;
  }

  private Map<String, Object> createParams(ToDoNotesFilter filter, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("userId", filter.getUserId());
    params.put("partyId", filter.getPartyId());
    params.put("groupName", filter.getGroupName());
    params.put("groupStatus", filter.getGroupStatus());
    params.put("salesInfoNoteTypesToLoad", salesInfoNoteTypesToLoad);
    return params;
  }
}

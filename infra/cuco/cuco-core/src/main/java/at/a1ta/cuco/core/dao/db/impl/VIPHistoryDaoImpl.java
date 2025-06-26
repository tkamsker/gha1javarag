package at.a1ta.cuco.core.dao.db.impl;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.VIPHistoryDao;
import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;

public class VIPHistoryDaoImpl extends AbstractDao implements VIPHistoryDao {

  @Override
  public List<VIPHistoryEntry> getVIPHistory(Long customerId) {
    return performListQuery("VIPHistory.GetVIPHistory", customerId);
  }

  @Override
  public List<VIPHistoryEntry> getVIPHistory(Date from, Date to, String searchTerm, String vipStatus) {
    Map<String, Object> map = new HashMap<String, Object>(3);
    map.put("from", from);
    map.put("to", to);
    map.put("searchTerm", searchTerm != null ? searchTerm.trim() : "");
    if (!"ALL".equals(vipStatus)) {
      map.put("vipStatus", (vipStatus != null && !vipStatus.isEmpty()) ? Integer.parseInt(vipStatus) : null);
    }

    return performListQuery("VIPHistory.SearchVIPHistory", map);
  }

  @Override
  public void saveVIPHistory(VIPHistoryEntry vipHistory) {
    executeInsert("VIPHistory.SaveVIPHistory", vipHistory);
  }
}

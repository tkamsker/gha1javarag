package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.Date;
import java.util.List;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;

@RemoteServiceRelativePath("cuco/vipHistory.rpc")
public interface VIPHistoryServlet extends RemoteService {
  public List<VIPHistoryEntry> getVIPHistory(Date from, Date to, String searchTerm, String vipStatus);
}

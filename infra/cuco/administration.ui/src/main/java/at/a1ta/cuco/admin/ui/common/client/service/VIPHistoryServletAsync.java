package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.Date;
import java.util.List;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;

public interface VIPHistoryServletAsync {
  void getVIPHistory(Date from, Date to, String searchTerm, String vipStatus, AsyncCallback<List<VIPHistoryEntry>> callback);
}

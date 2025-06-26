package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

@RemoteServiceRelativePath("cuco/systemTracking.rpc")
public interface SystemTrackingServlet extends RemoteService {
  public ArrayList<BaseModelData> loadAnalysis4logon();

  public ArrayList<BaseModelData> loadAnalysis4customerRequest();

  public ArrayList<BaseModelData> loadDetails4date(String date, String uuser);
}

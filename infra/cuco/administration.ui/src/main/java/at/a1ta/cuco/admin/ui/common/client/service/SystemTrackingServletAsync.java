package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.google.gwt.user.client.rpc.AsyncCallback;

public interface SystemTrackingServletAsync {
  public void loadAnalysis4logon(AsyncCallback<ArrayList<BaseModelData>> callback);

  public void loadAnalysis4customerRequest(AsyncCallback<ArrayList<BaseModelData>> callback);

  public void loadDetails4date(String date, String uuser, AsyncCallback<ArrayList<BaseModelData>> callback);
}

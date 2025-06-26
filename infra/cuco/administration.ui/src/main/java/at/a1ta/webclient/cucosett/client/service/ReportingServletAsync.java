package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;
import java.util.HashMap;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.bean.Reporting;

public interface ReportingServletAsync {
  public void getAllReportings(AsyncCallback<ArrayList<Reporting>> callback);

  public void executeReporting(Long id, AsyncCallback<ArrayList<HashMap<String, Object>>> callback);

  public void exportReportAsExcel(Long id, AsyncCallback<String> callback);
}

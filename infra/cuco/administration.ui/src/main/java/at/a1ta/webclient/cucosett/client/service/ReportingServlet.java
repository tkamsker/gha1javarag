package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;
import java.util.HashMap;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.bean.Reporting;

@RemoteServiceRelativePath("cuco/reporting.rpc")
public interface ReportingServlet extends RemoteService {
  public ArrayList<Reporting> getAllReportings();

  public ArrayList<HashMap<String, Object>> executeReporting(Long id) throws ReportingException;

  public String exportReportAsExcel(Long id) throws ReportingException;
}

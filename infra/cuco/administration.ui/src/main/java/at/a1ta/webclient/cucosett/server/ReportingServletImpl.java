package at.a1ta.webclient.cucosett.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.lang3.exception.ExceptionUtils;
import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.cuco.core.bean.File;
import at.a1ta.cuco.core.bean.Reporting;
import at.a1ta.cuco.core.service.ReportingService;
import at.a1ta.cuco.ui.common.server.util.SessionUtil;
import at.a1ta.webclient.cucosett.client.service.ReportingException;
import at.a1ta.webclient.cucosett.client.service.ReportingServlet;

@WebServlet(name = "reporting", urlPatterns = {"/admin/cuco/reporting.rpc"})
public class ReportingServletImpl extends SpringRemoteServiceServlet implements ReportingServlet {
  @Autowired
  private ReportingService reportingService;

  @Override
  public ArrayList<Reporting> getAllReportings() {
    return new ArrayList<Reporting>(reportingService.getAllReportings());
  }

  @Override
  public ArrayList<HashMap<String, Object>> executeReporting(Long id) throws ReportingException {
    try {
      return new ArrayList<HashMap<String, Object>>(reportingService.executeReporting(id));
    } catch (Exception b) {
      throw new ReportingException(ExceptionUtils.getStackTrace(b));
    }
  }

  @Override
  public String exportReportAsExcel(Long id) throws ReportingException {
    try {
      File file = reportingService.exportReportAsExcel(id);
      return SessionUtil.saveFile(getSession(), file);
    } catch (Exception b) {
      throw new ReportingException(ExceptionUtils.getStackTrace(b));
    }
  }
}

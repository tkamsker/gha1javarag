package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;
import java.util.List;

import org.apache.commons.lang.time.FastDateFormat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.util.ParseUtils;
import at.a1ta.bite.ui.server.servlet.AuthenticationServlet;
import at.a1ta.cuco.admin.ui.common.client.service.VIPHistoryServlet;
import at.a1ta.cuco.core.export.CSVFieldFormater;
import at.a1ta.cuco.core.export.CSVRowFormater;
import at.a1ta.cuco.core.export.DateFormater;
import at.a1ta.cuco.core.export.TableContent;
import at.a1ta.cuco.core.service.PartyService;
import at.a1ta.cuco.core.service.VIPHistoryService;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;
import at.a1ta.cuco.core.shared.dto.VipExport;

@Component
@WebServlet(name = "vipHistory", urlPatterns = {"/admin/cuco/vipHistory.rpc"})
public class VIPHistoryServletImpl extends AuthenticationServlet implements VIPHistoryServlet {
  private static final Logger logger = LoggerFactory.getLogger(VIPHistoryServletImpl.class);

  private static final FastDateFormat sdf = FastDateFormat.getInstance(VipExport.EXPORT_DATE_FILE_PATTERN);

  @Autowired
  private VIPHistoryService vipHistoryService;
  @Autowired
  private PartyService customerService;

  @Override
  public List<VIPHistoryEntry> getVIPHistory(Date from, Date to, String searchTerm, String vipStatus) {
    return vipHistoryService.getVIPHistory(from, to, searchTerm, vipStatus);
  }

  @Override
  protected void doGet(final HttpServletRequest req, final HttpServletResponse resp) throws ServletException, IOException {
    final String action = req.getParameter("action");
    if (action != null && VipExport.EXPORT_ACTION_CSV_BY_SEARCH.equals(action)) {
      Date fromDate = null;
      Date toDate = null;
      String reporter = null;
      String vipStatus = null;
      if (req.getParameter(VipExport.SEARCH_FROM) != null) {
        fromDate = ParseUtils.parseDate(req.getParameter(VipExport.SEARCH_FROM), VipExport.SERIALIZATION_DATE_PATTERN, null);
      }
      if (req.getParameter(VipExport.SEARCH_TO) != null) {
        toDate = ParseUtils.parseDate(req.getParameter(VipExport.SEARCH_TO), VipExport.SERIALIZATION_DATE_PATTERN, null);
      }
      if (req.getParameter(VipExport.SEARCH_REPORTER) != null) {
        reporter = req.getParameter(VipExport.SEARCH_REPORTER);
      }
      if (req.getParameter(VipExport.SEARCH_VIP_STATUS) != null) {
        vipStatus = req.getParameter(VipExport.SEARCH_VIP_STATUS);
      }

      logger.debug("Creating VIP History export file.");
      writeExportFile(resp, getVIPHistory(fromDate, toDate, reporter, vipStatus));
    } else {
      super.doGet(req, resp);
    }
  }

  private void writeExportFile(final HttpServletResponse resp, final List<VIPHistoryEntry> importHistory) throws IOException {
    final String timestampStr = sdf.format(new Date());
    final String fileName = "VipExport_" + timestampStr + VipExport.EXPORT_CSV_EXT;
    resp.setHeader("Content-Disposition", "attachment; filename=" + fileName);
    resp.setContentType(VipExport.EXPORT_CSV_CONTENT_TYPE);

    // write servlet response stream
    final PrintWriter writer = resp.getWriter();
    writer.write(getExportFileContent(importHistory));
    writer.flush();
    writer.close();
  }

  private String getExportFileContent(final List<VIPHistoryEntry> importHistory) {
    final TableContent c = new TableContent();
    c.setColumnFormater(0, VipExport.EXPORT_ROW_TITLES.length - 1, new CSVFieldFormater());
    c.setTypeFormater(Date.class, new DateFormater(VipExport.EXPORT_DATE_PATTERN, ""));
    c.setRowFormater(new CSVRowFormater());

    // Header
    c.addRow(VipExport.EXPORT_ROW_TITLES);

    // Rows
    for (VIPHistoryEntry history : importHistory) {
      Long customerId = history.getCustomerId();
      Party cust = customerService.get(customerId);
      Integer newStatus = history.getNewStatus();
      String reporter = history.getReported();
      Date created = history.getCreated();

      if (cust == null) {
        logger.warn("Cannot export VIP History. Customer " + customerId + " doesn't exist.");
        continue;
      }

      c.addRow(customerId, cust.getTitle(), cust.getLastname(), cust.getFirstname(), newStatus, reporter, created, cust.getBusinessSegment(), cust.getPoBox(), cust.getCity(), cust.getStreet(), cust.getHousenumber(), cust.getEMailAddress(), cust.getBirthdate(), cust.getGender(), cust.getCommercialSector());
    }
    return c.asString();
  }

}

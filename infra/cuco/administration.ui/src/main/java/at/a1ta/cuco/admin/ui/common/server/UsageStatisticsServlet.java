/*
 * Copyright 2009 - 2013 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.dto.TimeSpan;
import at.a1ta.bite.core.server.service.UserTrackingService;
import at.a1ta.bite.core.server.util.UsageStatistics;
import at.a1ta.bite.ui.server.servlet.CommonAuthenticationServlet;
import at.a1ta.cuco.core.shared.dto.Auth;

@Component
public class UsageStatisticsServlet extends CommonAuthenticationServlet {
  private static final long serialVersionUID = 1L;
  private static final Logger logger = LoggerFactory.getLogger(UsageStatisticsServlet.class);
  private static final String REQUEST_PARAM_END = "end";
  private static final String REQUEST_PARAM_START = "start";
  private static final String DATE_FORMAT_PATTERN = "MM-yyyy";

  private UserTrackingService trackingService;

  @Override
  protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    super.service(request, response);
    if (!hasAuthority(Auth.CONTENT_USERTRACKING)) {
      forbidden();
      return;
    }
    TimeSpan timeSpan = getReportTimeSpan(request);
    prepareContentHeader(response);
    writeWorkbook(createUsageReport(timeSpan), response.getOutputStream());
    response.flushBuffer();
  }

  private void prepareContentHeader(HttpServletResponse response) {
    response.setHeader("Content-Disposition", "attachment;filename=UsageReport_" + new Date().getTime() + ".xls");
    response.setContentType("application/vnd.ms-excel");
  }

  private TimeSpan getReportTimeSpan(HttpServletRequest request) {
    SimpleDateFormat sdf = new SimpleDateFormat(DATE_FORMAT_PATTERN);
    TimeSpan span = null;
    try {
      span = TimeSpan.startingAt(sdf.parse(request.getParameter(REQUEST_PARAM_START))).to(sdf.parse(request.getParameter(REQUEST_PARAM_END)));
    } catch (ParseException e) {
      throw new IllegalArgumentException(e);
    }
    return span;
  }

  private HSSFWorkbook createUsageReport(TimeSpan span) {
    UsageStatistics stats = new UsageStatistics(this.trackingService);
    return stats.generateUsageReport(span);
  }

  private void writeWorkbook(HSSFWorkbook workbook, OutputStream stream) {
    try {
      workbook.write(stream);
      stream.flush();
    } catch (IOException e) {
      StringWriter stack = new StringWriter();
      e.printStackTrace(new PrintWriter(stack));
      logger.debug("IOException: " + stack.toString());
    }
  }

  @Autowired
  public void setTrackingService(UserTrackingService trackingService) {
    this.trackingService = trackingService;
  }
}

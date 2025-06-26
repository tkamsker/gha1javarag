package at.a1ta.webclient.cucosett.client.service;

import com.google.gwt.core.client.GWT;

public class SettingsServiceLocator {

  private static CreditTypeServletAsync creditTypeServlet;

  private static ChargingTypeServletAsync chargingTypeServlet;

  private static TeamServletAsync teamServlet;

  private static AuthServletAsync authServlet;

  private static IbatisServletAsync ibatisServlet;

  private static ReportingServletAsync reportingServlet;

  public static AuthServletAsync getAuthorityServlet() {
    if (authServlet == null) {
      authServlet = GWT.create(AuthServlet.class);
    }
    return authServlet;
  }

  public static CreditTypeServletAsync getCreditTypeServlet() {
    if (creditTypeServlet == null) {
      creditTypeServlet = GWT.create(CreditTypeServlet.class);
    }
    return creditTypeServlet;
  }

  public static TeamServletAsync getTeamServlet() {
    if (teamServlet == null) {
      teamServlet = GWT.create(TeamServlet.class);
    }
    return teamServlet;
  }

  public static ChargingTypeServletAsync getChargingTypeServlet() {
    if (chargingTypeServlet == null) {
      chargingTypeServlet = GWT.create(ChargingTypeServlet.class);
    }
    return chargingTypeServlet;
  }

  public static IbatisServletAsync getIbatisServlet() {
    if (ibatisServlet == null) {
      ibatisServlet = GWT.create(IbatisServlet.class);
    }
    return ibatisServlet;
  }

  public static ReportingServletAsync getReportingServlet() {
    if (reportingServlet == null) {
      reportingServlet = GWT.create(ReportingServlet.class);
    }
    return reportingServlet;
  }
}

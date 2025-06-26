package at.a1ta.cuco.admin.ui.common.client.service;

import com.google.gwt.core.client.GWT;

public final class CommonServiceLocator {

  private static SystemTrackingServletAsync systemTrackingServlet;
  private static UserRoleServletAsync roleServlet;
  private static ServiceServletAsync serviceServlet;
  private static UnknownAreaCodeServletAsync unknownAreaCode;
  private static VIPHistoryServletAsync vipHistoryServlet;
  private static UserShopAssignmentServletAsync userShopAssignmentServlet;

  private CommonServiceLocator() {}

  public static SystemTrackingServletAsync getSystemTrackingServlet() {
    if (systemTrackingServlet == null) {
      systemTrackingServlet = GWT.create(SystemTrackingServlet.class);
    }
    return systemTrackingServlet;
  }

  public static UserRoleServletAsync getRoleServlet() {
    if (roleServlet == null) {
      roleServlet = GWT.create(UserRoleServlet.class);
    }
    return roleServlet;
  }

  public static ServiceServletAsync getServiceServlet() {
    if (serviceServlet == null) {
      serviceServlet = GWT.create(ServiceServlet.class);
    }
    return serviceServlet;
  }

  public static UnknownAreaCodeServletAsync getUnknownAreaCodeServlet() {
    if (unknownAreaCode == null) {
      unknownAreaCode = GWT.create(UnknownAreaCodeServlet.class);
    }
    return unknownAreaCode;
  }

  public static VIPHistoryServletAsync getVIPHistoryServlet() {
    if (vipHistoryServlet == null) {
      vipHistoryServlet = GWT.create(VIPHistoryServlet.class);
    }
    return vipHistoryServlet;
  }

  public static UserShopAssignmentServletAsync getUserShopAssignmentServlet() {
    if (userShopAssignmentServlet == null) {
      userShopAssignmentServlet = GWT.create(UserShopAssignmentServlet.class);
    }
    return userShopAssignmentServlet;
  }

}

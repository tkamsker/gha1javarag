package at.a1ta.cuco.admin.ui.common.client.bundle;

import com.google.gwt.core.client.GWT;

import at.a1ta.cuco.admin.ui.common.client.bundle.configuration.CuCoConfiguration;

public class AdminUI {
  public static final AdminCommonTextPool ADMINCOMMONTEXTPOOL = GWT.create(AdminCommonTextPool.class);

  public static final CuCoConfiguration CONFIG = new CuCoConfiguration();
}

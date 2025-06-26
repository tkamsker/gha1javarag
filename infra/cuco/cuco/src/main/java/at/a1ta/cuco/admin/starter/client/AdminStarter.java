package at.a1ta.cuco.admin.starter.client;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.bite.core.shared.dto.LocalSettingPool;
import at.a1ta.bite.core.shared.dto.SettingPool;
import at.a1ta.bite.core.shared.dto.TextPool;
import at.a1ta.bite.ui.client.BiteEntryPoint;
import at.a1ta.cuco.ui.common.shared.ApplicationId;

import com.extjs.gxt.ui.client.GXT;
import com.extjs.gxt.ui.client.util.Theme;
import com.google.gwt.core.client.GWT;

public class AdminStarter extends BiteEntryPoint {
  private static final String DEFAULT_CSS = "styles/gxt-gray.css";

  @Override
  protected List<Class<?>> getDataPools() {
    ArrayList<Class<?>> pools = new ArrayList<Class<?>>();
    pools.add(TextPool.class);
    pools.add(SettingPool.class);
    pools.add(LocalSettingPool.class);
    return pools;
  }

  @Override
  protected String getApplicationId() {
    return ApplicationId.ADMIN.toString();
  }

  @Override
  protected void beforeLoad() {
    Theme.GRAY.set("file", GWT.getModuleBaseURL() + DEFAULT_CSS);
    GXT.setDefaultTheme(Theme.GRAY, true);
  }
}

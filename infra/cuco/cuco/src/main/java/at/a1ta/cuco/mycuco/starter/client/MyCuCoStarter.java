package at.a1ta.cuco.mycuco.starter.client;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.bite.core.shared.dto.LocalSettingPool;
import at.a1ta.bite.core.shared.dto.SettingPool;
import at.a1ta.bite.core.shared.dto.StartupConfiguration;
import at.a1ta.bite.core.shared.dto.TextPool;
import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessagePool;
import at.a1ta.bite.ui.client.BiteEntryPoint;
import at.a1ta.cuco.ui.common.shared.ApplicationId;

import com.google.gwt.user.client.Window.Location;

public class MyCuCoStarter extends BiteEntryPoint {
  @Override
  protected List<Class<?>> getDataPools() {
    ArrayList<Class<?>> pools = new ArrayList<Class<?>>();
    pools.add(TextPool.class);
    pools.add(SettingPool.class);
    pools.add(LocalSettingPool.class);
    pools.add(SystemMessagePool.class);
    return pools;
  }

  @Override
  protected void beforeLoad() {
    String impersonation = Location.getParameter("iun");
    StartupConfiguration.getInstance().setImpersonation(impersonation);
  }

  @Override
  protected String getApplicationId() {
    return ApplicationId.MYCUCO.toString();
  }
}

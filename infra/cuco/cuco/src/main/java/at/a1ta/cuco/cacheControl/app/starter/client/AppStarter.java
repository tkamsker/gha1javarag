package at.a1ta.cuco.app.starter.client;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.bite.core.shared.dto.LocalSettingPool;
import at.a1ta.bite.core.shared.dto.SettingPool;
import at.a1ta.bite.core.shared.dto.TextPool;
import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessagePool;
import at.a1ta.bite.ui.client.BiteEntryPoint;
import at.a1ta.cuco.ui.common.shared.LocationHelper;
import at.a1ta.pkb.bean.bean.TouchpointPool;
import at.a1ta.pkb.ui.common.client.nbo.NBOOverviewView;
import at.a1ta.pkb.ui.common.client.nbo.NBOPortletView;

public class AppStarter extends BiteEntryPoint {
  @Override
  protected List<Class<?>> getDataPools() {
    ArrayList<Class<?>> pools = new ArrayList<Class<?>>();
    pools.add(TextPool.class);
    pools.add(SettingPool.class);
    pools.add(TouchpointPool.class);
    pools.add(LocalSettingPool.class);
    pools.add(SystemMessagePool.class);
    return pools;
  }

  @Override
  protected String getApplicationId() {
    return LocationHelper.getApplicationIdForCurrentPage();
  }

  @Override
  protected void beforeLoad() {
    NBOPortletView.exportPortletStaticMethod();
    NBOOverviewView.exportOverviewStaticMethod();
  }
}

package at.a1ta.pkb.starter.client;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.bite.core.shared.dto.LocalSettingPool;
import at.a1ta.bite.core.shared.dto.SettingPool;
import at.a1ta.bite.core.shared.dto.TextPool;
import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessagePool;
import at.a1ta.bite.ui.client.BiteEntryPoint;
import at.a1ta.cuco.ui.common.shared.ApplicationId;
import at.a1ta.pkb.bean.bean.TouchpointPool;

public class PkbStarter extends BiteEntryPoint {
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
    return ApplicationId.PKB.toString();
  }
}

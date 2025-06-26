package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.dao.db.UserInfoStatisticsDao;
import at.a1ta.cuco.core.shared.dto.UserInfoStatistics;
import org.springframework.beans.factory.annotation.Autowired;

public class UserInfoStatisticsDaoImpl extends AbstractDao implements UserInfoStatisticsDao {

  private static final String BINDING_TIMERANGE_3 = "mycuco.binding.timerange3.days";
  private static final String REMINDER_TIMERANGE_3 = "mycuco.reminders.timerange3.days";
  private SettingService settingService;

  @Override
  public UserInfoStatistics getUserInfoStatistics(String uUser) {
    HashMap<String, Object> params = new HashMap<String, Object>();
    params.put("uuser", uUser.toLowerCase());
    params.put("bindingDayLimit", settingService.getIntValue(BINDING_TIMERANGE_3));
    params.put("reminderDayLimit", settingService.getIntValue(REMINDER_TIMERANGE_3));
    return (UserInfoStatistics) performObjectQuery("UserInfoStats.getStats", params);
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

}

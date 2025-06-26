package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.dao.db.CucoLogsDao;

public class CucoLogsDaoImpl extends AbstractDao implements CucoLogsDao {
  @Autowired
  private SettingService settingService;

  private static final String PARTYLOADED_PASSWORDTYPE = "-";
  private static final String PASSWORDVIEW_LOGTYPE = "Password Viewed By Agent";

  @Override
  public void insertLogEntryForPartyLoaded(Long kundeId, String name, String userId, String ban, String logType) {
    final Map<String, Object> params = new HashMap<String, Object>();
    params.put("kunde_id", kundeId);
    params.put("name", name);
    params.put("user_id", userId);
    params.put("passwordType", settingService.getValueOrDefault("cucoLogsPartyLoadedPasswordType", PARTYLOADED_PASSWORDTYPE));
    params.put("ban", ban);
    params.put("log_Type", logType);
    executeInsert("CucoLogs.InsertLogEntry", params);
  }

  @Override
  public void insertLogEntryForViewPassword(Long kundeId, String name, String userId, String passwordType, String ban) {
    final Map<String, Object> params = new HashMap<String, Object>();
    params.put("kunde_id", kundeId);
    params.put("name", name);
    params.put("user_id", userId);
    params.put("passwordType", passwordType);
    params.put("ban", ban);
    params.put("log_Type", settingService.getValueOrDefault("cucoLogsPasswordViewLogType", PASSWORDVIEW_LOGTYPE));
    executeInsert("CucoLogs.InsertLogEntry", params);
  }

}
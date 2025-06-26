package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.shared.dto.Setting;
import at.a1ta.cuco.core.dao.db.SettingsEditorDAO;

public class SettingsEditorDAOImpl extends AbstractDao implements SettingsEditorDAO {

  @Override
  public List<Setting> getSettings() {
    return performListQuery("cucoSettings.getSettings");
  }

  @Override
  public void updateSetting(Setting setting) {
    executeUpdate("cucoSettings.updateSetting", setting);
  }

  @Override
  public List<Setting> searchSetting(String value) {
    return performListQuery("cucoSettings.searchSetting", value);
  }

}

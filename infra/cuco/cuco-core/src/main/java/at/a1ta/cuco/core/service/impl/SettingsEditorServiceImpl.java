package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.shared.dto.Setting;
import at.a1ta.cuco.core.dao.db.SettingsEditorDAO;
import at.a1ta.cuco.core.service.SettingsEditorService;

@Service
public class SettingsEditorServiceImpl implements SettingsEditorService {

  @Autowired
  private SettingsEditorDAO settingsEditorDAO;

  @Override
  public List<Setting> getSettings() {
    return settingsEditorDAO.getSettings();
  }

  @Override
  public void updateSetting(Setting setting) {
    settingsEditorDAO.updateSetting(setting);
  }

  @Override
  public List<Setting> searchText(String text) {
    return settingsEditorDAO.searchSetting(text);
  }

}

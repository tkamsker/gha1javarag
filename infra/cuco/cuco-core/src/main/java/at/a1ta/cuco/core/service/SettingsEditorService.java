package at.a1ta.cuco.core.service;

import java.util.List;

import at.a1ta.bite.core.shared.dto.Setting;

public interface SettingsEditorService {

  // select
  public List<Setting> getSettings();

  // update
  public void updateSetting(Setting setting);

  // search
  public List<Setting> searchText(String text);

}

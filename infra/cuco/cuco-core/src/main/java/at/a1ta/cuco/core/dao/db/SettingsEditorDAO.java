package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.bite.core.shared.dto.Setting;

public interface SettingsEditorDAO {

  List<Setting> getSettings();

  void updateSetting(Setting setting);

  List<Setting> searchSetting(String value);

}
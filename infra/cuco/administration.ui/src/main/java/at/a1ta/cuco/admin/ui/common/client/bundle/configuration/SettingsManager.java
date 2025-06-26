package at.a1ta.cuco.admin.ui.common.client.bundle.configuration;

import java.util.Map;

public class SettingsManager {
  private static Map<String, String> settings;

  public static void setSettings(Map<String, String> settings) {
    SettingsManager.settings = settings;
  }

  public String readString(String key) {
    return settings.get(key);
  }

  private Integer readInteger(String key) {
    String val = settings.get(key);
    return new Integer(Integer.parseInt(val));
  }

  public int readInt(String key) {
    return readInteger(key).intValue();
  }
}

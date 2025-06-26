package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class CucoLogs implements Serializable {
  private Long kundeId;
  private String name;
  private Long userId;
  private String passwordType;
  private Long ban;
  private String LogType;

  public Long getKundeId() {
    return kundeId;
  }

  public void setKundeId(Long kundeId) {
    this.kundeId = kundeId;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public Long getUserId() {
    return userId;
  }

  public void setUserId(Long userId) {
    this.userId = userId;
  }

  public String getPasswordType() {
    return passwordType;
  }

  public void setPasswordType(String passwordType) {
    this.passwordType = passwordType;
  }

  public Long getBan() {
    return ban;
  }

  public void setBan(Long ban) {
    this.ban = ban;
  }

  public String getLogType() {
    return LogType;
  }

  public void setLogType(String logType) {
    LogType = logType;
  }

}
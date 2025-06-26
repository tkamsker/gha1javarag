package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class UserShopAssignmentLogLine implements Serializable {
  
  private String userName;
  private String logText;
  
  public UserShopAssignmentLogLine()
  {
    this.userName = "";
    this.logText = "";
  }
  
  public UserShopAssignmentLogLine(String userName, String logText) {
    this.userName = userName; 
    this.logText = logText;
  }
  
  public String getUsername() {
    return userName;
  }
  public void setUsername(String username) {
    this.userName = username;
  }
  public String getLogText() {
    return logText;
  }
  public void setLogtext(String logText) {
    this.logText = logText;
  }  
}

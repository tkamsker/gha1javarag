package at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote;

import java.io.Serializable;

public class TeamEmailAdminGroup implements Serializable {

  private Integer id;
  private String teamName;
  private String teamEmail;
  private String userList;
  private Boolean isDefault;

  public TeamEmailAdminGroup() {

  }

  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
  }

  public String getTeamName() {
    return teamName;
  }

  public void setTeamName(String teamName) {
    this.teamName = teamName;
  }

  public String getTeamEmail() {
    return teamEmail;
  }

  public void setTeamEmail(String teamEmail) {
    this.teamEmail = teamEmail;
  }

  public String getUserList() {
    return userList;
  }

  public void setUserList(String userList) {
    this.userList = userList;
  }

  public boolean isDefault() {
    return isDefault;
  }

  public void setDefault(boolean isDefault) {
    this.isDefault = isDefault;
  }

}

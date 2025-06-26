package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class CrmAuthenticationInfo implements Serializable {

  private static final long serialVersionUID = 1L;

  public static final int ERROR = 99;
  public static final int LOADING = -1;
  public static final int NOT_RECEIVED = 98;
  public static final int LOADED = 0;

  private int status = LOADING;
  private String password;
  private String ban;

  public CrmAuthenticationInfo() {
    // default constructor to support GWT parsing
  }

  public CrmAuthenticationInfo(int status) {
    this.status = status;
  }

  public int getStatus() {
    return status;
  }

  public void setStatus(int staus) {
    this.status = staus;
  }

  public String getPassword() {
    return password;
  }

  public void setPassword(String password) {
    this.password = password;
  }

  public String getBan() {
    return ban;
  }

  public void setBan(String ban) {
    this.ban = ban;
  }

}

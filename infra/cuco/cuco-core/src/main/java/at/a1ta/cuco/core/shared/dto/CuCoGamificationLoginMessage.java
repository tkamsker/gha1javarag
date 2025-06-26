package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class CuCoGamificationLoginMessage implements Serializable {

  private static final long serialVersionUID = 1L;
  private String messageType;
  private String id;
  private String pswd;
  private String sessionKey;

  public String getMessageType() {
    return messageType;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getPswd() {
    return pswd;
  }

  public void setPswd(String pswd) {
    this.pswd = pswd;
  }

  public void setMessageType(String messageType) {
    this.messageType = messageType;
  }

  public String getSessionKey() {
    return sessionKey;
  }

  public void setSessionKey(String sessionKey) {
    this.sessionKey = sessionKey;
  }

}

package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class CrmAuthenticationPasswordInfo implements Serializable {
  private static final long serialVersionUID = 1L;

  private String value;
  private String type;

  public CrmAuthenticationPasswordInfo() {}

  public String getValue() {
    return value;
  }

  public void setValue(String value) {
    this.value = value;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public CrmAuthenticationPasswordInfo(String value, String string) {

    this.value = value;
    this.type = string;
  }

  public String getPassword() {
    return getValue();
  }
}

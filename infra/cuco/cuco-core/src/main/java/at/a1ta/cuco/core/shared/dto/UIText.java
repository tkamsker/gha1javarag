package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class UIText implements Serializable {

  private String key; 
  private String value;
  
  public UIText() {
    key = new String();
    value = new String();
  }
  
  public UIText(String key, String value)
  {
    this.key = key;
    this.value = value;
  }
  
  public String getKey() {
    return key;
  }
  
  public void setKey(String key) {
    this.key = key;
  }
  
  public String getValue() {
    return value;
  }
  
  public void setValue(String value) {
    this.value = value;
  }
  
}

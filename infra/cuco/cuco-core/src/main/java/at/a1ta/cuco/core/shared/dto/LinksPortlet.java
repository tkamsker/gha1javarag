package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class LinksPortlet implements Serializable {
  private static final long serialVersionUID = 1L;
  private String key;
  private String text;
  private String url;
  private Auth requiredAuthority;;

  public String getKey() {
    return key;
  }

  public void setKey(String key) {
    this.key = key;
  }

  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public Auth getRequiredAuthority() {
    return requiredAuthority;
  }

  public void setRequiredAuthority(Auth requiredAuthority) {
    this.requiredAuthority = requiredAuthority;
  }
}

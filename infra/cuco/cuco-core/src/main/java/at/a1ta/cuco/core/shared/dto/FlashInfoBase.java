package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.List;

import at.a1ta.bite.core.shared.dto.security.Role;

public class FlashInfoBase implements Serializable {
  private long id = -1;
  private String title;
  private String text;
  private boolean active;
  private boolean popup;
  private List<Role> roles;
  private boolean viewed;

  public FlashInfoBase() {
    super();
  }

  public FlashInfoBase(long id, String title, String text, boolean active, boolean popup, List<Role> roles, boolean viewed) {
    super();
    this.id = id;
    this.title = title;
    this.text = text;
    this.active = active;
    this.popup = popup;
    this.roles = roles;
    this.viewed = viewed;
  }

  public long getId() {
    return id;
  }

  public void setId(long id) {
    this.id = id;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public boolean isActive() {
    return active;
  }

  public void setActive(boolean active) {
    this.active = active;
  }

  public boolean isPopup() {
    return popup;
  }

  public void setPopup(boolean popup) {
    this.popup = popup;
  }

  public List<Role> getRoles() {
    return roles;
  }

  public void setRoles(List<Role> roles) {
    this.roles = roles;
  }

  public boolean isViewed() {
    return viewed;
  }

  public void setViewed(boolean viewed) {
    this.viewed = viewed;
  }

}

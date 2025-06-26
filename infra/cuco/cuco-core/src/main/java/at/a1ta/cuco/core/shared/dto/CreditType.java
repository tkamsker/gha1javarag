package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class CreditType implements Serializable {
  private Long id;
  private String name;
  private String description;
  private Boolean active;

  public CreditType() {}

  public CreditType(String name, String description, Boolean active) {
    super();
    this.name = name;
    this.description = description;
    this.active = active;
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public Boolean getActive() {
    return active;
  }

  public void setActive(Boolean active) {
    this.active = active;
  }
}

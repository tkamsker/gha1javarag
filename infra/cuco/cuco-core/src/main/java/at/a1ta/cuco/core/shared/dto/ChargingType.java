package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class ChargingType implements Serializable {

  private static final Long MOBILE_CHARGING_TYPE = 3L;

  private Long id;
  private String name;
  private String description;

  public ChargingType() {}

  public ChargingType(Long id) {
    this.id = id;
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

  public boolean isMobileChargingType() {
    return MOBILE_CHARGING_TYPE.equals(id);
  }
}

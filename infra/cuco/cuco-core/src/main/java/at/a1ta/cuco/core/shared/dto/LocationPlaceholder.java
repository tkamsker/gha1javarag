package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

import at.a1ta.bite.data.clarify.shared.dto.Location;

public class LocationPlaceholder extends Location implements Serializable {
  public LocationPlaceholder() {
    setId(-1l);
    setLocationId("-1");
  }
}

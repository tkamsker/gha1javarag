package at.a1ta.cuco.core.shared.dto.product;

import at.a1ta.cuco.core.shared.dto.product.Location.LocationType;

public class LocationNode extends BaseNode {

  private Location location;

  public Location getLocation() {
    return location;
  }

  public void setLocation(Location location) {
    this.location = location;
  }

  @Override
  public String getText() {
    return location.getAddress();
  }

  public String getFullText() {
    return location.getAddress();
  }

  public LocationType getLocationTypeFormLocation() {
    return null != location ? location.getLocationType() : null;
  }

}

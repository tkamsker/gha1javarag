package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class Location implements Serializable {

  public enum LocationType {
    MOBILE, FIXED, HYBRID
  }

  private long partyId;
  private String locationId;
  private String address;
  private String city;
  private String street;
  private String poBox;
  private Coordinates coordinates;
  private LocationType locationType;

  public boolean hasCoordinates() {
    return coordinates != null;
  }

  public Coordinates getCoordinates() {
    return coordinates;
  }

  public void setCoordinates(Coordinates coordinates) {
    this.coordinates = coordinates;
  }

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public String getLocationId() {
    return locationId;
  }

  public void setLocationId(String locationId) {
    this.locationId = locationId;
  }

  public String getAddress() {
    return address;
  }

  public void setAddress(String address) {
    this.address = address;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getCity() {
    return city;
  }

  public void setStreet(String street) {
    this.street = street;
  }

  public String getStreet() {
    return street;
  }

  public void setPoBox(String poBox) {
    this.poBox = poBox;
  }

  public String getPoBox() {
    return poBox;
  }

  public LocationType getLocationType() {
    return locationType;
  }

  public void setLocationType(LocationType locationType) {
    this.locationType = locationType;
  }

}

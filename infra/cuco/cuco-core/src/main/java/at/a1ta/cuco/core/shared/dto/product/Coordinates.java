package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class Coordinates implements Serializable {

  private double longitude;
  private double latitude;

  public Coordinates() {}

  public Coordinates(double longitude, double latitude) {
    this.longitude = longitude;
    this.latitude = latitude;
  }

  public double getLongitude() {
    return longitude;
  }

  public void setLongitude(double longitude) {
    this.longitude = longitude;
  }

  public double getLatitude() {
    return latitude;
  }

  public void setLatitude(double latitude) {
    this.latitude = latitude;
  }
}

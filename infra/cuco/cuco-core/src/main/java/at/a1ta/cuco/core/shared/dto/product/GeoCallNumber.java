package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class GeoCallNumber implements Serializable {
  private static final long serialVersionUID = 1L;
  private String countryCode;
  private String onkz;
  private String tnum;

  public GeoCallNumber() {
    // Default Constructor
  }

  public GeoCallNumber(String countryCode, String onkz, String tnum) {
    this.countryCode = countryCode;
    this.onkz = onkz;
    this.tnum = tnum;
  }

  public String getCountryCode() {
    return countryCode;
  }

  public void setCountryCode(String countryCode) {
    this.countryCode = countryCode;
  }

  public String getOnkz() {
    return onkz;
  }

  public void setOnkz(String onkz) {
    this.onkz = onkz;
  }

  public String getTnum() {
    return tnum;
  }

  public void setTnum(String tnum) {
    this.tnum = tnum;
  }

  @Override
  public String toString() {
    return countryCode + " " + onkz + " " + tnum;
  }
}

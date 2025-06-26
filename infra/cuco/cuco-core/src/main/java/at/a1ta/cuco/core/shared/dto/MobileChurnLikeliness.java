package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class MobileChurnLikeliness implements Serializable {

  private String countryIdentification;
  private String cityIdentification;
  private String callNumber;
  private String churnLikeliness;

  public String getCountryIdentification() {
    return countryIdentification;
  }

  public void setCountryIdentification(String countryIdentification) {
    this.countryIdentification = countryIdentification;
  }

  public String getCityIdentification() {
    return cityIdentification;
  }

  public void setCityIdentification(String cityIdentification) {
    this.cityIdentification = cityIdentification;
  }

  public String getCallNumber() {
    return callNumber;
  }

  public void setCallNumber(String callNumber) {
    this.callNumber = callNumber;
  }

  public String getChurnLikeliness() {
    return churnLikeliness;
  }

  public void setChurnLikeliness(String churnLikeliness) {
    this.churnLikeliness = churnLikeliness;
  }

}

package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PhoneNumberStructure implements Serializable {
  public static final String AT_COUNTRY_CODE = "43";

  private String countryCode;
  private String onkz;
  private String number;
  private String extension;

  public PhoneNumberStructure() {}

  public PhoneNumberStructure(String countryCode, String onkz, String number) {
    this(countryCode, onkz, number, null);
  }

  public PhoneNumberStructure(String countryCode, String onkz, String number, String extension) {
    this.countryCode = countryCode;
    this.onkz = onkz;
    this.number = number;
    this.extension = extension;
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

  public String getNumber() {
    return number;
  }

  public void setNumber(String number) {
    this.number = number;
  }

  public String getExtension() {
    return extension;
  }

  public void setExtension(String extension) {
    this.extension = extension;
  }

  @Override
  public String toString() {
    StringBuffer sb = new StringBuffer(40);
    if (countryCode != null) {
      sb.append(countryCode);
    }
    if (onkz != null) {
      sb.append(" ");
      sb.append(onkz);
    }
    if (number != null) {
      sb.append(" ");
      sb.append(number);
    }
    if (extension != null) {
      sb.append(" ");
      sb.append(extension);
    }
    return sb.toString();
  }

}

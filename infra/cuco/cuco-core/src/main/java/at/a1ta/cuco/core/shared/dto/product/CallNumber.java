package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class CallNumber implements Serializable {
  private static final long serialVersionUID = 1L;
  private String countryCode;
  private String onkz;
  private String tnum;

  public CallNumber() {
    // default constructor to support GWT parsing
  }

  public CallNumber(String countryCode, String onkz, String tnum) {
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

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((countryCode == null) ? 0 : countryCode.hashCode());
    result = prime * result + ((onkz == null) ? 0 : onkz.hashCode());
    result = prime * result + ((tnum == null) ? 0 : tnum.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    CallNumber other = (CallNumber) obj;
    if (countryCode == null) {
      if (other.countryCode != null) {
        return false;
      }
    } else if (!countryCode.trim().equals(other.countryCode.trim())) {
      return false;
    }
    if (onkz == null) {
      if (other.onkz != null) {
        return false;
      }
    } else if (!onkz.trim().equals(other.onkz.trim())) {
      return false;
    }
    if (tnum == null) {
      if (other.tnum != null) {
        return false;
      }
    } else if (!tnum.trim().equals(other.tnum.trim())) {
      return false;
    }
    return true;
  }
}
